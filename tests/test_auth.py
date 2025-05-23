import requests
from requests import Response

def test_root_unauthenticated():
    response = requests.get("http://127.0.0.1:8000/")
    assert response.status_code == 401

def test_create_new_generic_user():
    url: str = "http://127.0.0.1:8000/auth"
    headers: dict = {"accept": "application/json", "Content-Type": "application/json"}
    data: dict = {"username": "bruno","password": "test123"}

    response: Response = requests.post(url, headers=headers, json=data)

    response_json: dict = response.json()
    expected_result: list[str] = ['username', 'id', 'hashed_password']
    

    assert response.status_code == 201
    assert set(response_json.keys()) >= set(expected_result)

    assert isinstance(response_json["username"], str)
    assert isinstance(response_json["id"], int)
    assert isinstance(response_json["hashed_password"], str)

def test_root_authentication():
    url: str = "http://127.0.0.1:8000/auth/token"
    headers: dict = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'grant_type': 'password',
        'username': 'login_that_exists',
        'password': 'test123',
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string',
    }

    response: Response = requests.post(url, headers=headers, data=data)

    assert response.json()["token_type"] == 'bearer'
    assert response.status_code == 200