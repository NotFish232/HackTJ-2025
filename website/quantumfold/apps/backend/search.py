import requests
import json

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
    # with open("/home/alan/0Code/HackTJ-2025/test.json", "w") as f:
    #     json.dump(response_json, f)

    protein_list = []

    for protein_json in response_json:
        protein_name = protein_json.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value")
        uniprot_accession = protein_json.get("primaryAccession")

        if protein_name is None or uniprot_accession is None:
            continue

        protein_list.append((protein_name, uniprot_accession))

    return protein_list
