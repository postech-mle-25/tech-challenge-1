import requests
from requests import Response
import pytest
from tests import constants

@pytest.fixture(scope="module")
def token():
    url: str = f"{constants.Authentication.url}/auth/token"
    headers: dict = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'username': constants.Authentication.username,
        'password': constants.Authentication.password,
    }

    response: Response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    return response.json()["access_token"]

def base_endpoint_criar_test(token, endpoint: str, data: dict):
    url: str = f"{constants.Authentication.url}/api/{endpoint}/criar/"
    headers: dict = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response: Response = requests.post(url, headers=headers, json=data)
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
                "control": "TINTAS",
                "arquivo": "ProcessaViniferas.csv",
                "pasta": "processamento",
                "ano": 1977,
                "quantidade": 1
            }),
            ("comercio", {
                "control": "VINHO DE MESA",
                "arquivo": "comercio.csv",
                "pasta": "comercio",
                "ano": 1977,
                "quantidade": 1
            }),
            ("exportacao", {
                "pais": "Alemanha",
                "arquivo": "ExpVinho.csv",
                "pasta": "exportacao",
                "ano": 1977,
                "quantidade": 1,
                "valor": 300
            }),
            ("importacao", {
                "pais": "Alemanha",
                "arquivo": "ImpVinho.csv",
                "pasta": "importacao",
                "ano": 1977,
                "quantidade": 1,
                "valor": 300
            }),
        ],
        ids=["processamento", "comercio", "exportacao", "importacao"]
    )

def test_criacao_endpoint(token, endpoint, data):
    base_endpoint_criar_test(token, endpoint, data)