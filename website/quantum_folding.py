import protein_folding
from protein_folding.penalty_parameters import PenaltyParameters
from protein_folding.interactions.miyazawa_jernigan_interaction import (
    MiyazawaJerniganInteraction,
)
from protein_folding.peptide.peptide import Peptide
from protein_folding.protein_folding_problem import ProteinFoldingProblem
from protein_folding.penalty_parameters import PenaltyParameters

from qiskit.circuit.library import RealAmplitudes  # type: ignore
from qiskit.algorithms.optimizers import COBYLA  # type: ignore
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE  # type: ignore
from qiskit.primitives import Sampler  # type: ignore

AMINO_ACID_3_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}

MIN_NUM_AMINO_ACIDS = 5
MAX_NUM_AMINO_ACIDS = 7
MIN_CONFIDENCE_THRESHOLD = 60


def extract_amino_groups(
    pdb_file: str,
) -> list[tuple[str, float, list[tuple[str, tuple[float, float, float]]]]]:
    pdb_content = open(pdb_file).read().splitlines()
    atom_data = [l.split() for l in pdb_content if l.startswith("ATOM")]

    amino_groups = []

    i = 0
    while i < len(atom_data):
        amino_acid = atom_data[i][3]
        confidence = float(atom_data[i][10])
        id = atom_data[i][5]

        elements = []

        while i < len(atom_data) and atom_data[i][5] == id:
            x, y, z = map(float, atom_data[i][6:9])
            element_name = atom_data[i][11]

            elements.append((element_name, (x, y, z)))

            i += 1

        amino_groups.append((amino_acid, confidence, elements))

    return amino_groups


def extract_low_confidence_chains(
    amino_groups: list[tuple[str, float, list[tuple[str, tuple[float, float, float]]]]],
) -> list[list[int]]:
    low_confidence_chains = []

    i = 0
    while i < len(amino_groups):
        chain = [i]

        j = 1
        while i + j < len(amino_groups):
            chain.append(i + j)

            if (
                sum(amino_groups[k][1] for k in chain) / len(chain)
                > MIN_CONFIDENCE_THRESHOLD
            ):
                chain.pop()
                break

            if len(chain) == MAX_NUM_AMINO_ACIDS:
                break

            j += 1

        if len(chain) >= MIN_NUM_AMINO_ACIDS:
            low_confidence_chains.append(chain)
            i += len(chain)
        else:
            i += 1

    return low_confidence_chains


def run_vqe(main_chain: str) -> list[tuple[float, float, float]]:
    side_chains = [""] * len(main_chain)

    peptide = Peptide(main_chain, side_chains)

    interactions = MiyazawaJerniganInteraction()

    penalty_back = 10
    penalty_chiral = 10
    penalty_locality = 10
    penalty_terms = PenaltyParameters(penalty_chiral, penalty_back, penalty_locality)

    protein_folding_problem = ProteinFoldingProblem(
        peptide, interactions, penalty_terms
    )

    qubit_op = protein_folding_problem.qubit_op()

    sampler = Sampler()
    ansatz = RealAmplitudes(reps=1)
    optimizer = COBYLA(maxiter=50)

    vqe = SamplingVQE(
        sampler,
        ansatz,
        optimizer,
        aggregation=0.1,
    )

    raw_result = vqe.compute_minimum_eigenvalue(qubit_op)
    result = protein_folding_problem.interpret(raw_result)

    coordinates_np = result.protein_shape_file_gen.get_xyz_data()
    coordinates = [(float(c[1]), float(c[2]), float(c[3])) for c in coordinates_np]

    return coordinates


def mean(points: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    mean_x, mean_y, mean_z = 0.0, 0.0, 0.0

    for x, y, z in points:
        mean_x += x
        mean_y += y
        mean_z += z

    mean_x /= len(points)
    mean_y /= len(points)
    mean_z /= len(points)

    return mean_x, mean_y, mean_z


def translate_to_mean(
    points_a: list[tuple[float, float, float]], mean_b: tuple[float, float, float]
) -> list[tuple[float, float, float]]:
    mean_a = mean(points_a)
    new_points = []

    for point in points_a:
        new_x = point[0] + mean_b[0] - mean_a[0]
        new_y = point[1] + mean_b[1] - mean_a[1]
        new_z = point[2] + mean_b[2] - mean_a[2]

        new_points.append((new_x, new_y, new_z))

    return new_points


def apply_updated_amino_acid_coordinates(
    pdb_content: list[str],
    amino_groups: list[tuple[str, float, list[tuple[str, tuple[float, float, float]]]]],
    idxs_list: list[list[int]],
    new_coordinates_list: list[list[tuple[float, float, float]]],
) -> list[str]:
    first_amino_idx = next(i for i, l in enumerate(pdb_content) if l.startswith("ATOM"))

    # for i in range(first_amino_idx, first_amino_idx + sum(len(a[2]) for a in amino_groups)):
    #     pdb_content[i] = pdb_content[i][:-19] + " 0.01" + pdb_content[i][-14:]
 
    for idxs, new_coordinates in zip(idxs_list, new_coordinates_list):
        current_amino_chain_coordinates = [
            mean([a[1] for a in amino_groups[i][2]]) for i in idxs
        ]
        new_amino_chain_coordinates = translate_to_mean(
            new_coordinates, mean(current_amino_chain_coordinates)
        )

        for amino_idx, new_amino_acid_coordinate in zip(
            idxs, new_amino_chain_coordinates
        ):
            current_element_coordinates = [a[1] for a in amino_groups[amino_idx][2]]
            new_element_coordinates = translate_to_mean(
                current_element_coordinates, new_amino_acid_coordinate
            )

            amino_idx_offset = first_amino_idx + sum(
                len(amino_groups[i][2]) for i in range(amino_idx)
            )

            for i, coord in zip(
                range(
                    amino_idx_offset,
                    amino_idx_offset + len(new_element_coordinates),
                ),
                new_element_coordinates,
            ):
                l = pdb_content[i].split()
     
                l[6] = f"{coord[0]:.3f}"
                l[7] = f"{coord[1]:.3f}"
                l[8] = f"{coord[2]:.3f}"

                l[1] = l[1].rjust(7)
                l[2] = "  " + l[2].ljust(4)
                l[4] = l[4].rjust(2)
                l[5] = l[5].rjust(4)
                l[6] = l[6].rjust(12)
                l[7] = l[7].rjust(8)
                l[8] = l[8].rjust(8)
                l[9] = l[9].rjust(6)
                l[10] = "99.99".rjust(6)
                l[11] = l[11].ljust(3).rjust(14)

                pdb_content[i] = "".join(l)

    return pdb_content


def run_quantum_folding(pdb_file: str) -> str:
    amino_groups = extract_amino_groups(pdb_file)
    low_confidence_chains = extract_low_confidence_chains(amino_groups)

    amino_acid_coordinates_list = []

    for chain in low_confidence_chains:
        s_chain = "".join(AMINO_ACID_3_TO_1[amino_groups[c][0]] for c in chain)
        amino_acid_coordinates = run_vqe(s_chain)

        amino_acid_coordinates_list.append(amino_acid_coordinates)

    pdb_content = open(pdb_file).read().splitlines()
    pdb_content = apply_updated_amino_acid_coordinates(
        pdb_content, amino_groups, low_confidence_chains, amino_acid_coordinates_list
    )

    open("media/changed.pdb", "w").write("\n".join(pdb_content))

    return ""


print(run_quantum_folding("media/angiotensin_alphafold.pdb"))
