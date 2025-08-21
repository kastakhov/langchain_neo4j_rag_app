import requests


def get_current_configuration(base_url: str):
    response = requests.get(f"{base_url}/config/show")
    return response.json()

def update_configuration(base_url: str, configuration: dict):
    response = requests.post(f"{base_url}/config/update", json=configuration)
    return response.json()
