def test_create_user(client):
    response = client.post(
        "/api/users/", json={"name": "testuser", "email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_read_users(client):
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_user(client):
    response = client.post(
        "/api/users/", json={"name": "testuser2", "email": "test2@example.com", "password": "testpass"})
    user_id = response.json()["id"]
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test2@example.com"


def test_delete_user(client):
    response = client.post(
        "/api/users/", json={"name": "testuser3", "email": "test3@example.com", "password": "testpass"})
    user_id = response.json()["id"]
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test3@example.com"
    # Ensure the user no longer exists
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404
