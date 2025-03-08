import requests

UNIPROTKB_SEARCH_API_URL = "https://rest.uniprot.org/uniprotkb/search"


def search_proteins(query: str) -> list[tuple[str, str]] | None:
    data = {
        "query": f"{query} AND organism_name:Homo sapiens",
        "fields": ["protein_name", "accession"],
    }

    response = requests.get(UNIPROTKB_SEARCH_API_URL, params=data)

    if response.status_code != 200:
        return None

    response_json = response.json()["results"]

    protein_list = []

    for protein_json in response_json:
        protein_name = protein_json["proteinDescription"]["recommendedName"][
            "fullName"
        ]["value"]
        uniprot_accession = protein_json["primaryAccession"]

        protein_list.append((protein_name, uniprot_accession))

    return protein_list
