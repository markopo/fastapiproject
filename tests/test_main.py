from starlette.testclient import TestClient

from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping() -> None:
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_crud_user() -> None:
    email, name, response = create_test_user()
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == email
    assert user["name"] == name

    user_id = user["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == email
    assert user["name"] == name

    new_name = "olle ollonson"
    response = client.put(f"/api/users/{user_id}", json={"id": user_id,"email": email, "name": new_name})
    assert response.status_code == 200
    user = response.json()
    assert user["name"] == new_name

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200


def create_test_user():
    email = "jay.testilainen@mail.com"
    name = "jay testilainen"
    response = client.post("/api/users/", json={"email": email, "name": name})
    return email, name, response
