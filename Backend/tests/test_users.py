def test_create_user(client):
    response = client.post("/users/", json={
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "phone": "1234567890",
        "gender": "male",
        "password": "Password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_duplicate_user(client):
    user_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "phone": "1234567890",
        "gender": "male",
        "password": "Password123"
    }
    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_get_user(client):
    res = client.post("/users/", json={
        "name": "Test2",
        "surname": "User2",
        "email": "test2@example.com",
        "phone": "1234567890",
        "gender": "female",
        "password": "Password123"
    })
    user_id = res.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test2@example.com"

def test_get_nonexistent_user(client):
    response = client.get("/users/9999")
    assert response.status_code == 404
