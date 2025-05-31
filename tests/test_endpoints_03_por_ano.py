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

def base_test_endpoints_por_ano(token: Any, endpoint: str, ano: int):
    url = f"{constants.Authentication.url}/api/{endpoint}/{endpoint}_por_ano?ano={ano}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    for item in response.json():
        assert 'id' in item.keys()
        assert isinstance(item['id'], int)

def test_endpoint_get_comercio_por_ano_empty_response(token: Any):
    url = f"{constants.Authentication.url}/api/comercio/comercio_por_ano?ano=0"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.get(url, headers=headers)

    assert not response.json()


@pytest.mark.parametrize(
        "endpoint, ano", 
        [
            ("processamento", 1977),
            ("comercio", 1977),
            ("exportacao", 1977),
            ("importacao", 1977),
            ("producao", 1977)
        ],
        ids=["processamento", "comercio", "exportacao", "importacao", "producao"]
    )

def test_endpoints_por_ano(token: Any, endpoint: str, ano: int):
    base_test_endpoints_por_ano(token, endpoint, ano)