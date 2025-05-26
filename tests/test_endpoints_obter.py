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

def base_test_endpoints_obter(token, endpoint: str, id: int):
    url = f"{constants.Authentication.url}/api/{endpoint}/obter/{id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert isinstance(response.json()["id"], int)

def test_endpoind_comercio_obter_item_not_found(token):
    url = f"{constants.Authentication.url}/api/comercio/obter/{0}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
        }

    response: Response = requests.get(url, headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

@pytest.mark.parametrize(
        "endpoint, id", 
        [
            ("comercio", 1),
            ("exportacao", 1),
            ("importacao", 1),
            ("producao", 1)
        ],
        ids=["comercio", "exportacao", "importacao", "producao"]
    )

def test_endpoints_obter(token, endpoint, id):
    base_test_endpoints_obter(token, endpoint, id)