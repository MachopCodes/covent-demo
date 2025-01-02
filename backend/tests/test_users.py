import pytest

# Test Cases
def test_list_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0  # Ensure users are present
    assert users[0]["id"] == 1  # Validate the first user


def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["name"] == "Alice"


# def test_create_user(client):
#     new_user_data = {
#         "name": "Charlie",
#         "email": "charlie@example.com",
#         "password": "securepassword",
#     }
#     response = client.post("/users/", json=new_user_data)
#     assert response.status_code == 200
#     created_user = response.json()
#     assert created_user["name"] == "Charlie"
#     assert created_user["email"] == "charlie@example.com"


def test_update_user(client):
    updated_user_data = {"name": "Updated Alice"}
    response = client.put("/users/1", json=updated_user_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Updated Alice"


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == 200
    deleted_user = response.json()
    assert deleted_user["id"] == 1
