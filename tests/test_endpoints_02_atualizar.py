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

    response: Response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    return response.json()["access_token"]

def base_test_endpoints_atualizar(token, endpoint: str, data: dict):
    url = f"{constants.Authentication.url}/api/{endpoint}/atualizar/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response: Response = requests.patch(url, headers=headers, json=data)
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert isinstance(response.json()["id"], int)

def test_endpoind_comercio_atualizar_item_not_found(token):
    url = f"{constants.Authentication.url}/api/comercio/atualizar/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }

    data = {
        "id": 0,
        "control": "TINTAS",
        "arquivo": "Comercio.csv",
        "pasta": "comercio",
        "ano": 1978,
        "quantidade": 1
    }

    response = requests.patch(url, headers=headers, json=data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

@pytest.mark.parametrize(
        "endpoint, data", 
        [
            ("comercio", {
                "id": 999999,
                "pasta": "comercio",
                "ano": 1977,
                "quantidade": 2
            }),
            ("exportacao", {
                "id": 999999,
                "pais": "Alemanha",
                "ano": 1977,
                "quantidade": 2,
                "valor": 300
            }),
            ("importacao", {
                "id": 999999,
                "pais": "Alemanha",
                "ano": 1977,
                "quantidade": 2,
                "valor": 300
            }),
            ("producao", {
                "id": 999999,
                "pasta": "producao",
                "ano": 1977,
                "quantidade": 2,
            })
        ],
        ids=["comercio", "exportacao", "importacao", "producao"]
    )

def test_endpoints_atualizar(token, endpoint, data):
    base_test_endpoints_atualizar(token, endpoint, data)