import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from app.main import app
from app.models.users import DBUser
from app.utils.jwt import get_password_hash

# Use the FastAPI test client
client = TestClient(app)

# Mocked database session and user data
def get_mock_db():
    mock_session = MagicMock()

    # Mocking a database query for users
    users = [
        DBUser(id=1, name="Alice", email="alice@example.com", hashed_password=get_password_hash("password")),
        DBUser(id=2, name="Bob", email="bob@example.com", hashed_password=get_password_hash("securepassword")),
    ]

    def mock_query(model):
        mock_query = MagicMock()
        mock_query.filter.return_value.first.side_effect = lambda: next(
            (user for user in users if user.email == model or user.name == model), None
        )
        return mock_query

    mock_session.query.side_effect = mock_query
    return mock_session

app.dependency_overrides[get_mock_db] = get_mock_db

# Test data
mock_user_create = {"name": "Charlie", "email": "charlie@example.com", "password": "securepassword"}
mock_user_login = {"name": "Alice", "password": "password"}
mock_invalid_login = {"name": "Unknown", "password": "wrongpassword"}



# def test_register(client):
#     response = client.post(
#         "/auth/register",
#         json={"name": "Charlie", "email": "charlie@example.com", "password": "securepassword"}
#     )
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# def test_login(client):
#     response = client.post(
#         "/auth/login",
#         json={"name": "Alice", "password": "password"}
#     )
#     assert response.status_code == 200
#     assert "access_token" in response.json()


