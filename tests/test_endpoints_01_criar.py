import requests
from requests import Response
import pytest
from tests import constants

@pytest.fixture(scope="module")
def token():
    url = f"{constants.Authentication.url}/auth/token"
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'username': constants.Authentication.username,
        'password': constants.Authentication.password,
    }

    response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    return response.json()["access_token"]

def base_test_endpoints_criar(token, endpoint: str, data: dict):
    url = f"{constants.Authentication.url}/api/{endpoint}/criar/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert isinstance(response.json()["id"], int)

# def test_csv_ingestion_into_db():
#    response = requests.post(f"{constants.Authentication.url}/api/ingest")
#    assert response.status_code == 200

@pytest.mark.parametrize(
        "endpoint, data", 
        [
            ("processamento", {
                "id": 1,
                "control": "TINTAS",
                "arquivo": "ProcessaViniferas.csv",
                "pasta": "processamento",
                "ano": 1977,
                "quantidade": 1
            }),
            ("comercio", {
                "id": 1,
                "control": "VINHO DE MESA",
                "arquivo": "comercio.csv",
                "pasta": "comercio",
                "ano": 1977,
                "quantidade": 1
            }),
            ("exportacao", {
                "id": 1,
                "pais": "Alemanha",
                "arquivo": "ExpVinho.csv",
                "pasta": "exportacao",
                "ano": 1977,
                "quantidade": 1,
                "valor": 300
            }),
            ("importacao", {
                "id": 1,
                "pais": "Alemanha",
                "arquivo": "ImpVinho.csv",
                "pasta": "importacao",
                "ano": 1977,
                "quantidade": 1,
                "valor": 300
            }),
            ("producao", {
                "id": 1,
                "control": "VINHO DE MESA",
                "arquivo": "Producao.csv",
                "pasta": "producao",
                "ano": 1977,
                "quantidade": 1,
            })
        ],
        ids=["processamento", "comercio", "exportacao", "importacao", "producao"]
    )

def test_endpoints_criar(token, endpoint, data):
    base_test_endpoints_criar(token, endpoint, data)