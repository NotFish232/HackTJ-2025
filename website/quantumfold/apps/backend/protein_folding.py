import requests
from urllib.parse import quote
from urllib.request import urlretrieve
from pathlib import Path
import json
from typing_extensions import Any

from quantumfold.apps.web.models import Protein


UNIPROTKB_SEARCH_API_URL = "https://rest.uniprot.org/uniprotkb/search"

ALPHAFOLD_API_PRED_URL = "https://alphafold.ebi.ac.uk/api/prediction"

MEDIA_PATH = Path(__file__).parents[3] / "media"


SCIENTIFIC_NAME_KEY = "organismScientificName"
HUMAN_SPECIES_VALUE = "Homo sapiens"

UNIPROT_ACCESSION_KEY = "uniprotAccession"
ENTRY_ID_KEY = "entryId"
UNIPROT_ID_KEY = "uniprotId"
UNIPROT_DESCRIPTION_KEY = "uniprotDescription"
UNIPROT_SEQUENCE_KEY = "uniprotSequence"
PDBURL_KEY = "pdbUrl"


def alphafold_fetch(
    uniprot_accession: str,
) -> tuple[Protein, dict[str, Any], str] | None:
    response = requests.get(f"{ALPHAFOLD_API_PRED_URL}/{quote(uniprot_accession)}")
    if response.status_code != 200:
        return None

    response_json = response.json()[0]

    uniprot_accession = response_json[UNIPROT_ACCESSION_KEY]
    entry_id = response_json[ENTRY_ID_KEY]
    uniprot_id = response_json[UNIPROT_ID_KEY]
    uniprot_description = response_json[UNIPROT_DESCRIPTION_KEY]
    uniprot_sequence = response_json[UNIPROT_SEQUENCE_KEY]

    pdb_file_url = response_json[PDBURL_KEY]

    protein = Protein(
        uniprot_accession=uniprot_accession,
        entry_id=entry_id,
        uniprot_id=uniprot_id,
        uniprot_description=uniprot_description,
        uniprot_sequence=uniprot_sequence,
    )

    return protein, response_json, pdb_file_url


def run_quantum_protein_folding() -> None:
    pass


def run_full_protein_folding(uniprot_accession: str) -> bool:
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

    return True
