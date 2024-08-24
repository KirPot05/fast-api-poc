def test_create_post(client):
    user_response = client.post(
        "/api/users/", json={"name": "testuser", "email": "testuser@example.com", "password": "testpass"})
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/posts/", json={"title": "Test Post", "description": "Test Description", "user_id": user_id})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["description"] == "Test Description"
    assert response.json()["user_id"] == user_id
    assert "id" in response.json()
    assert response.json()["is_blocked"] is False


def test_read_posts(client):
    response = client.get("/api/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_post(client):
    response = client.post(
        "/api/posts/", json={"title": "Another Post", "description": "Another Description", "user_id": 1})
    post_id = response.json()["id"]
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Another Post"


def test_update_post(client):
    user_response = client.post(
        "/api/users/", json={"name": "testuser22", "email": "testuser78@example.com", "password": "testpass"})
    print(user_response)

    user_id = user_response.json()["id"]

    post_response = client.post(
        "/api/posts/", json={"title": "Initial Title", "description": "Initial Description", "user_id": user_id})
    post_id = post_response.json()["id"]

    update_response = client.put(f"/api/posts/{post_id}", json={
                                 "title": "Updated Title", "description": "Updated Description", "user_id": user_id})

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"
    assert update_response.json()["description"] == "Updated Description"


def test_block_post(client):
    response = client.post(
        "/api/posts/", json={"title": "Blockable Post", "description": "To be blocked", "user_id": 1})
    post_id = response.json()["id"]

    response = client.put(f"/api/posts/{post_id}/block")
    assert response.status_code == 200
    assert response.json()["is_blocked"] is True


def test_delete_post(client):
    response = client.post(
        "/api/posts/", json={"title": "Deletable Post", "description": "To be deleted", "user_id": 1})
    post_id = response.json()["id"]

    response = client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Deletable Post"

    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 404
