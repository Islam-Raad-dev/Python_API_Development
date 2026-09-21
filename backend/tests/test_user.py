import os

import pytest
from app import schemas
from app.main import app
from app.oauth2 import ALGORITHM
from fastapi.testclient import TestClient
from jose import jwt

client = TestClient(app)

SECRET_KEY_FOR_JWT = os.getenv("SECRET_KEY_FOR_JWT")


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}


def test_create_user(client):
    res = client.post(
        "/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "hello123@gmail.com",
            "password": "password123",
        },
    )

    assert res.status_code == 201
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"


def test_login_user(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, SECRET_KEY_FOR_JWT, algorithms=[ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("islam@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("islam@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code