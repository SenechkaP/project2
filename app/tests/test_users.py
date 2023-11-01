from http import HTTPStatus
import requests

ENDPOINT = "http://127.0.0.1:5001"


def test_user_create():
    payload = {
        "first_name": "Nik",
        "last_name": "Wild",
        "email": "test@test.ru",
    }
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]

    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")

    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]


def test_user_create_wrong_email():
    payload = {
        "first_name": "Nik",
        "last_name": "Wild",
        "email": "testtest.ru",
    }
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
