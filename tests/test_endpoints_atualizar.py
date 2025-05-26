import requests
from requests import Response
import pytest
from tests import constants

@pytest.fixture(scope="module")
def token():
    url: str = f"{constants.Authentication.url}/auth/token"
    headers: dict = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'username': 'login_that_exists',
        'password': 'test123',
    }

    response: Response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    return response.json()["access_token"]

def base_endpoint_atualizar_test(token, endpoint: str, data: dict):
    url: str = f"{constants.Authentication.url}/api/{endpoint}/criar/"
    headers: dict = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response: Response = requests.patch(url, headers=headers, json=data)
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert isinstance(response.json()["id"], int)

def test_endpoind_atualizar_processamento_item_not_found(token):
    url: str = f"{constants.Authentication.url}/api/{endpoint}/criar/"
    headers: dict = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    data: dict = {
        "id": 0,
        "control": "TINTAS",
        "arquivo": "ProcessaViniferas.csv",
        "pasta": "processamento",
        "ano": 1978,
        "quantidade": 1
    }

    response: Response = requests.patch(url, headers=headers, json=data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


# def test_atualizar_processamento(token):
#     data: dict = {
#         "id": 0,
#         "control": "TINTAS",
#         "arquivo": "ProcessaViniferas.csv",
#         "pasta": "processamento",
#         "ano": 1978,
#         "quantidade": 1
#     }

#     base_endpoint_atualizar_test(token, "processamento", data)

# def test_atualizar_comercio(token):
#     data: dict = {
#         "control": "VINHO DE MESA",
#         "arquivo": "comercio.csv",
#         "pasta": "comercio",
#         "ano": 1977,
#         "quantidade": 1
#     }

#     base_endpoint_atualizar_test(token, "comercio", data)

# def test_atualizar_exportacao(token):
#     data: dict = {
#         "pais": "Alemanha",
#         "arquivo": "ExpVinho.csv",
#         "pasta": "exportacao",
#         "ano": 1977,
#         "quantidade": 1,
#         "valor": 300
#     }

#     base_endpoint_atualizar_test(token, "exportacao", data)

# def test_atualizar_importacao(token):

#     data: dict = {
#         "pais": "Alemanha",
#         "arquivo": "ImpVinho.csv",
#         "pasta": "importacao",
#         "ano": 1977,
#         "quantidade": 1,
#         "valor": 300
#     }

#     base_endpoint_atualizar_test(token, "importacao", data)

# def test_atualizar_exportacao(token):
#     data: dict = {
#         "pais": "Alemanha",
#         "arquivo": "ExpVinho.csv",
#         "pasta": "exportacao",
#         "ano": 1977,
#         "quantidade": 1,
#         "valor": 300
#     }

#     base_endpoint_atualizar_test(token, "exportacao", data)