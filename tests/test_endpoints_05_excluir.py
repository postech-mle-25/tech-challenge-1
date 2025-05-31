import requests
from typing import Any

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

    response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    return response.json()["access_token"]

def base_test_endpoints_excluir(token: Any, endpoint: str, item_id: int):
    url = f"{constants.Authentication.url}/api/{endpoint}/excluir/?item_id={item_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.delete(url, headers=headers)
    assert response.status_code == 200
    assert 'ok' in response.json().keys()
    assert isinstance(response.json()["ok"], bool)

def test_endpoind_comercio_excluir_item_not_found(token):
    url = f"{constants.Authentication.url}/api/comercio/excluir/?item_id=0"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.delete(url, headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

@pytest.mark.parametrize(
        "endpoint, item_id",
        [
            ("processamento", 999999),
            ("comercio", 999999),
            ("exportacao", 999999),
            ("importacao", 999999),
            ("producao", 999999)
        ],
        ids=["processamento", "comercio", "exportacao", "importacao", "producao"]
    )

def test_endpoints_excluir(token: Any, endpoint: str, item_id: int):
    base_test_endpoints_excluir(token, endpoint, item_id)