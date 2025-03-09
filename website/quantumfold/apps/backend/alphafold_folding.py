import requests
from urllib.parse import quote
from typing_extensions import Any

from quantumfold.apps.web.models import Protein


UNIPROTKB_SEARCH_API_URL = "https://rest.uniprot.org/uniprotkb/search"

ALPHAFOLD_API_PRED_URL = "https://alphafold.ebi.ac.uk/api/prediction"


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

    uniprot_accession = response_json.get(UNIPROT_ACCESSION_KEY)
    entry_id = response_json.get(ENTRY_ID_KEY)
    uniprot_id = response_json.get(UNIPROT_ID_KEY)
    uniprot_description = response_json.get(UNIPROT_DESCRIPTION_KEY)
    uniprot_sequence = response_json.get(UNIPROT_SEQUENCE_KEY)

    pdb_file_url = response_json.get(PDBURL_KEY)

    if not pdb_file_url:
        return None

    protein = Protein(
        uniprot_accession=uniprot_accession,
        entry_id=entry_id,
        uniprot_id=uniprot_id,
        uniprot_description=uniprot_description,
        uniprot_sequence=uniprot_sequence,
    )

    return protein, response_json, pdb_file_url

