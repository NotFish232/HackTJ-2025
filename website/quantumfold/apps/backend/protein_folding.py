import json
from pathlib import Path
from urllib.request import urlretrieve
from website.quantumfold.apps.backend.alphafold_folding import alphafold_fetch
from website.quantumfold.apps.backend.quantum_folding import run_quantum_folding
from website.quantumfold.apps.web.models import ProteinResult

MEDIA_PATH = Path(__file__).parents[3] / "media"


def run_full_protein_folding(uniprot_accession: str) -> ProteinResult:
    # get results from alphafold api
    alphafold_result = alphafold_fetch(uniprot_accession)

    if alphafold_result is None:
        return False

    protein, protein_json, pdb_file_url = alphafold_result

    protein_dir = MEDIA_PATH / protein.uniprot_accession

    protein_dir.mkdir(exist_ok=True)

    # downloads the alphafold pdb
    urlretrieve(pdb_file_url, str(protein_dir / "alphafold.pdb"))

    # save protein json to file in case its needed
    json.dump(protein_json, open(str(protein_dir / "protein.json"), "w"), indent=4)

    quantum_folding_result = run_quantum_folding(str(protein_dir / "alphafold.pdb"))
    with open(protein_dir / "quantumfold.pdb")  as f:
        f.write(quantum_folding_result)

    p = ProteinResult(
        protein=protein
    )
    p.alphafold_result.name = str(protein_dir / "alphafold.pdb")
    p.quantum_result.name = str(protein_dir / "quantumfold.pdb")

    return p
