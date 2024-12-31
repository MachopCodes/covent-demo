from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base, DBUser
from app.utils.jwt import create_access_token
from tests.test_utils import adapt_model_to_sqlite

# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Apply the model adaptation for SQLite
adapt_model_to_sqlite(engine, DBUser)

# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

# Test data
test_user_data = {"id": 1, "name": "testuser", "email": "test@example.com", "is_active": True, "is_admin": False}
admin_user_data = {"id": 2, "name": "adminuser", "email": "admin@example.com", "is_active": True, "is_admin": True}
test_token = create_access_token(test_user_data)
admin_token = create_access_token(admin_user_data)

# Headers for authenticated requests
auth_headers = {"Authorization": f"Bearer {test_token}"}
admin_auth_headers = {"Authorization": f"Bearer {admin_token}"}

def setup_module():
    """
    Create the test database and seed initial data before the tests run.
    """
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    user1 = DBUser(
        id=test_user_data["id"],
        name="testuser",
        email="test@example.com",
        hashed_password="hashed_pw",
        is_active=True,
        is_admin=False
    )
    user2 = DBUser(
        id=admin_user_data["id"],
        name="adminuser",
        email="admin@example.com",
        hashed_password="hashed_pw",
        is_active=True,
        is_admin=True
    )
    session.add_all([user1, user2])
    session.commit()
    session.close()

def teardown_module():
    """
    Drop the test database after tests complete.
    """
    Base.metadata.drop_all(bind=engine)

# Tests

def test_list_users():
    response = client.get("/users", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "testuser"
    assert data[1]["name"] == "adminuser"

def test_get_user():
    response = client.get("/users/1", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_user_not_found():
    response = client.get("/users/999", headers=auth_headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "User not found"

def test_update_user():
    updated_data = {"name": "Updated User", "email": "updated@example.com"}
    response = client.put("/users/1", json=updated_data, headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]

def test_update_user_not_found():
    updated_data = {"name": "Nonexistent User"}
    response = client.put("/users/999", json=updated_data, headers=auth_headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "User not found"

def test_delete_user():
    response = client.delete("/users/1", headers=admin_auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1

    # Confirm deletion
    response = client.get("/users/1", headers=auth_headers)
    assert response.status_code == 404

def test_delete_user_not_found():
    response = client.delete("/users/999", headers=admin_auth_headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "User not found"
