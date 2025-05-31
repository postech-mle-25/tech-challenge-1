import requests
from requests import Response

from tests import constants

def test_root_unauthenticated():
    response = requests.get(constants.Authentication.url + "/")
    assert response.status_code == 401

def test_create_new_generic_user():
    url = f"{constants.Authentication.url}/auth"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"username": constants.Authentication.username,
                  "password": constants.Authentication.password}

    response: Response = requests.post(url, headers=headers, json=data)

    response_json: dict = response.json()
    expected_result: list[str] = ['username', 'id', 'hashed_password']
    

    assert response.status_code == 201
    assert set(response_json.keys()) >= set(expected_result)

    assert isinstance(response_json["username"], str)
    assert isinstance(response_json["id"], int)
    assert isinstance(response_json["hashed_password"], str)

def test_root_authentication():
    url = f"{constants.Authentication.url}/auth/token"
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": constants.Authentication.username,
                  "password": constants.Authentication.password}

    response: Response = requests.post(url, headers=headers, data=data)

    assert response.json()["token_type"] == 'bearer'
    assert response.status_code == 200