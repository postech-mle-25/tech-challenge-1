import requests
from requests import Response
import pytest

@pytest.fixture(scope="module")
def token():
    url: str = "http://127.0.0.1:8000/auth/token"
    headers: dict = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'username': 'login_that_exists',
        'password': 'test123',
    }

    response: Response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    return response.json()["access_token"]

def base_endpoint_create_test(token, endpoint: str, data: dict):
    url: str = f"http://127.0.0.1:8000/api/{endpoint}/criar/"
    headers: dict = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response: Response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert isinstance(response.json()["id"], int)

#def test_csv_ingestion_into_db():
#    response = requests.post("http://127.0.0.1:8000/api/ingest")
#    assert response.status_code == 200

def test_create_processamento(token):
    data: dict = {
        "control": "TINTAS",
        "arquivo": "ProcessaViniferas.csv",
        "pasta": "processamento",
        "ano": 1977,
        "quantidade": 1
    }

    base_endpoint_create_test(token, "processamento", data)

def test_create_comercio(token):
    data: dict = {
        "control": "VINHO DE MESA",
        "arquivo": "comercio.csv",
        "pasta": "comercio",
        "ano": 1977,
        "quantidade": 1
    }

    base_endpoint_create_test(token, "comercio", data)

def test_create_exportacao(token):
    data: dict = {
        "pais": "Alemanha",
        "arquivo": "ExpVinho.csv",
        "pasta": "exportacao",
        "ano": 1977,
        "quantidade": 1,
        "valor": 300
    }

    base_endpoint_create_test(token, "exportacao", data)

def test_create_importacao(token):

    data: dict = {
        "pais": "Alemanha",
        "arquivo": "ImpVinho.csv",
        "pasta": "importacao",
        "ano": 1977,
        "quantidade": 1,
        "valor": 300
    }

    base_endpoint_create_test(token, "importacao", data)

# def test_create_exportacao(token):
#     url: str = "http://127.0.0.1:8000/api/exportacao/criar/"
#     headers: dict = {
#         "accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#         }
#     data: dict = {
#         "control": "VINHO DE MESA",
#         "produto": "VINHO DE MESA",
#         "arquivo": "Producao.csv",
#         "pasta": "producao",
#         "ano": 1977,
#         "quantidade": 1,
#     }

#     response: Response = requests.post(url, headers=headers, json=data)
#     assert response.status_code == 200
#     assert 'id' in response.json().keys()
#     assert isinstance(response.json()["id"], int)