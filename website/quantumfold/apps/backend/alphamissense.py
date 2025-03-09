import requests

ALPHAMISSENSE_API_URL = "https://alphamissense.hegelab.org/hotspotapi"
def get_alphamissense_result(uniprot_id, residue_num):
    url = f"{ALPHAMISSENSE_API_URL}?uid={uniprot_id}&resi={residue_num}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None
    r_json = response.json()
    return {
        'benign': r_json['benign'],
        'pathogenic': r_json['pathogenic'],
        'ambiguous': r_json['ambiguous'],
    }

