from http import HTTPStatus
import requests
from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5001"


def create_user_payload():
    return {
        "first_name": "Nik" + str(uuid4()),
        "last_name": "Wild" + str(uuid4()),
        "email": "test@test.ru",
    }


def test_user_create():
    payload = create_user_payload()
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

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["status"] == "deleted"


def test_user_create_wrong_email():
    payload = create_user_payload()
    payload["email"] = "testtest.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_posts():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]

    get_response = requests.get(
        f"{ENDPOINT}/users/{user_id}/posts", json={"sort": "asc"}
    )
    assert get_response.status_code == HTTPStatus.OK
    assert isinstance(get_response.json()["posts"], list)

    get_response = requests.get(
        f"{ENDPOINT}/users/{user_id}/posts", json={"sort": "desc"}
    )
    assert get_response.status_code == HTTPStatus.OK
    assert isinstance(get_response.json()["posts"], list)

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["status"] == "deleted"


def test_get_leaderboard():
    n = 3
    test_users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        test_users.append(create_response.json()["id"])
        assert create_response.status_code == HTTPStatus.OK

    payload = {"type": "list", "sort": "asc"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    leaderboard = get_response.json()["users"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == n

    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
