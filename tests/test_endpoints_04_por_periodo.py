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

def base_test_endpoints_por_ano(token: Any, endpoint: str, apos: int, ate: int):
    url = f"{constants.Authentication.url}/api/{endpoint}/{endpoint}_por_periodo?apos={apos}&ate={ate}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    for item in response.json():
        assert 'id' in item.keys()
        assert isinstance(item['id'], int)


def test_endpoint_get_comercio_por_periodo_empty_response(token: Any):
    url = f"{constants.Authentication.url}/api/comercio/comercio_por_periodo?apos=-1&ate=0"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.get(url, headers=headers)

    assert not response.json()


@pytest.mark.parametrize(
        "endpoint, apos, ate", 
        [
            ("processamento", 1977, 1979),
            ("comercio", 1977, 1979),
            ("producao", 1977, 1979)
        ],
        ids=["processamento", "comercio", "producao"]
    )

def test_endpoints_por_ano(token: Any, endpoint: str, apos: int, ate: int):
    base_test_endpoints_por_ano(token, endpoint, apos, ate)