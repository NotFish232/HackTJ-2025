import requests
from urllib.parse import quote
from urllib.request import urlretrieve
from pathlib import Path

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quantumfold.settings")
import django

django.setup()

from quantumfold.apps.web.models import Protein


ALPHAFOLD_API_PRED_URL = "https://alphafold.ebi.ac.uk/api/prediction"

MEDIA_PATH = Path(__file__).parent / "media"


SCIENTIFIC_NAME_KEY = "organismScientificName"
HUMAN_SPECIES_VALUE = "Homo sapiens"

ENTRY_ID_KEY = "entryId"
UNIPROT_ID_KEY = "uniprotId"
UNIPROT_DESCRIPTION_KEY = "uniprotDescription"
UNIPROT_SEQUENCE_KEY = "uniprotSequence"
PDBURL_KEY = "pdbUrl"


def alphafold_fetch(protein_name: str) -> tuple[Protein, str] | None:
    response = requests.get(f"{ALPHAFOLD_API_PRED_URL}/{quote(protein_name)}")
    if response.status_code != 200:
        return None

    response_json = response.json()

    human_protein_json = next(
        (x for x in response_json if x[SCIENTIFIC_NAME_KEY] == HUMAN_SPECIES_VALUE),
        None,
    )
    if human_protein_json is None:
        return None

    entry_id = human_protein_json[ENTRY_ID_KEY]
    uniprot_id = human_protein_json[UNIPROT_ID_KEY]
    uniprot_description = human_protein_json[UNIPROT_DESCRIPTION_KEY]
    uniprot_sequence = human_protein_json[UNIPROT_SEQUENCE_KEY]

    pdb_file_url = human_protein_json[PDBURL_KEY]

    protein = Protein(
        entry_id=entry_id,
        uniprot_id=uniprot_id,
        uniprot_description=uniprot_description,
        uniprot_sequence=uniprot_sequence,
    )

    return protein, pdb_file_url


def run_quantum_protein_folding() -> None:
    pass

def run_full_protein_folding(protein_name: str) -> bool:
    # get results from alphafold api
    alphafold_result = alphafold_fetch(protein_name)

    if alphafold_result is None:
        return False

    protein, pdb_file_url = alphafold_result

    protein_dir = MEDIA_PATH / protein.uniprot_id

    protein_dir.mkdir(exist_ok=True)

    # downloads the alphafold pdb
    urlretrieve(pdb_file_url, str(protein_dir / "alphafold.pdb"))

    return True


print(run_full_protein_folding("Angiotensin 1-10"))
