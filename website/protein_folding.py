import requests
from urllib.parse import quote
import json

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quantumfold.settings")
import django

django.setup()
from quantumfold import Protein

ALPHAFOLD_API_PRED_URL = "https://alphafold.ebi.ac.uk/api/prediction"


SCIENTIFIC_NAME_KEY = "organismScientificName"
HUMAN_SPECIES_VALUE = "Homo sapiens"

ENTRY_ID_KEY = "entryId"


def alphafold_fetch(protein_name: str) -> tuple[str, str, str] | None:
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

    return Protein.objects.create()

    print(json.dumps(human_protein_json, indent=4))
