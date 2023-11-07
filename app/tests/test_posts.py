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


def test_create_post():
    user_payload = create_user_payload()
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=user_payload)
    user_data = create_user_response.json()
    post_payload = {
        "author_id": f"{user_data['id']}",
        "text": "wow",
    }
    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    post_data = create_post_response.json()

    assert create_post_response.status_code == HTTPStatus.OK
    assert post_data["author_id"] == int(post_payload["author_id"])
    assert post_data["text"] == post_payload["text"]
    assert isinstance(post_data["reactions"], list)

    get_post_response = requests.get(f"{ENDPOINT}/posts/{post_data['id']}")

    assert get_post_response.status_code == HTTPStatus.OK
    assert get_post_response.json()["author_id"] == int(post_payload["author_id"])
    assert get_post_response.json()["text"] == post_payload["text"]
    assert isinstance(get_post_response.json()["reactions"], list)

    delete_user_response = requests.delete(f"{ENDPOINT}/users/{user_data['id']}")

    assert delete_user_response.status_code == HTTPStatus.OK
    assert delete_user_response.json()["first_name"] == user_payload["first_name"]
    assert delete_user_response.json()["last_name"] == user_payload["last_name"]
    assert delete_user_response.json()["email"] == user_payload["email"]
    assert delete_user_response.json()["status"] == "deleted"

    delete_post_response = requests.delete(f"{ENDPOINT}/posts/{post_data['id']}")

    assert delete_post_response.status_code == HTTPStatus.OK
    assert delete_post_response.json()["author_id"] == int(post_payload["author_id"])
    assert delete_post_response.json()["text"] == post_payload["text"]
    assert delete_post_response.json()["status"] == "deleted"
    assert isinstance(delete_post_response.json()["reactions"], list)


def test_post_reaction():
    user_payload = create_user_payload()
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=user_payload)
    user_data = create_user_response.json()
    post_payload = {
        "author_id": f"{user_data['id']}",
        "text": "wow",
    }
    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    post_data = create_post_response.json()

    assert create_post_response.status_code == HTTPStatus.OK

    reaction_payload = {
        "user_id": f"{user_data['id']}",
        "reaction": "heart",
    }

    create_reaction_response = requests.post(
        f"{ENDPOINT}/posts/{post_data['id']}/reaction", json=reaction_payload
    )

    get_post_response = requests.get(f"{ENDPOINT}/posts/{post_data['id']}")

    assert get_post_response.status_code == HTTPStatus.OK
    assert create_reaction_response.status_code == HTTPStatus.OK
    assert reaction_payload["reaction"] in get_post_response.json()["reactions"]

    delete_user_response = requests.delete(f"{ENDPOINT}/users/{user_data['id']}")

    assert delete_user_response.status_code == HTTPStatus.OK

    delete_post_response = requests.delete(f"{ENDPOINT}/posts/{post_data['id']}")

    assert delete_post_response.status_code == HTTPStatus.OK
