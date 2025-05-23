import requests
import json

def test_root_unauthenticated():
    response = requests.get("http://127.0.0.1:8000/")
    assert response.status_code == 401

def test_create_new_generic_user():
    url = "http://127.0.0.1:8000/auth"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"username": "bruno","password": "test123"}

    response = requests.post(url, headers=headers, json=data)

    response_text_dict = json.loads(response.text)
    expected_result = ['username', 'id', 'hashed_password']
    

    assert response.status_code == 201
    assert list(response_text_dict.keys()) == expected_result