import requests
from typing import Any

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

def base_test_endpoints_criar(token: Any, endpoint: str, data: dict):
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

@pytest.mark.parametrize(
        "endpoint, data", 
        [
            ("processamento", {
                "id": 999999,
                "control": "TINTAS",
                "cultivar": "TINTAS",
                "tipo": "pro_americanas_hibridas",
                "ano": 1977,
                "quantidade": 1
            }),
            ("comercio", {
                "id": 999999,
                "control": "vm_Branco",
                "produto": "Branco",
                "ano": 1977,
                "quantidade": 1
            }),
            ("exportacao", {
                "id": 999999,
                "pais": "Alemanha",
                "tipo": "exp_espumantes",
                "ano": 1977,
                "quantidade": 1,
                "valor": 300
            }),
            ("importacao", {
                "id": 999999,
                "pais": "Alemanha",
                "tipo": "imp_espumantes",
                "ano": 1977,
                "quantidade": 1,
                "valor": 300
            }),
            ("producao", {
                "id": 999999,
                "control": "vm_Tinto",
                "produto": "Tinto",
                "ano": 1977,
                "quantidade": 1,
            })
        ],
        ids=["processamento", "comercio", "exportacao", "importacao", "producao"]
    )

def test_endpoints_criar(token: Any, endpoint: str, data: dict):
    base_test_endpoints_criar(token, endpoint, data)