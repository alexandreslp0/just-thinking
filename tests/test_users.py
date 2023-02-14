import pytest
from jose import jwt
from app.config import settings
from app.schemas import UserFullResponse, Token


def test_create_user(client):
    res = client.post("/users", json={"email": "test@gmail.com", "password": "senha"})

    new_user = UserFullResponse(**res.json())
    assert res.json().get("email") == "test@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    login_res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert login_res.status_code == 200

    new_token = Token(**login_res.json())
    payload = jwt.decode(new_token.access_token, settings.secret_key, algorithms=[settings.algorithm])

    assert payload.get("user_id") == test_user["id"]


@pytest.mark.parametrize("email, password, status_code", [
    ("test@user.com", "wrong-password", 403),
    ("wrong@email.com", "wrong-password", 403),
    ("wrong@email.com", "senhateste", 403),
    (None, "senhateste", 422),
    ("test@user.com", None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    login_res = client.post("/login", data={"username": email, "password": password})

    assert login_res.status_code == status_code

