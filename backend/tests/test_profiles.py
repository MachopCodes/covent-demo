from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base, DBProfile

# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

def setup_module():
    """
    Create the test database and seed initial data before the tests run.
    """
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    profiles = [
        DBProfile(
            name="Profile 1",
            email="profile1@example.com",
            description="First test profile",
            budget_max=1000,
            target_audiences=["students"],
            objectives=["education"],
        ),
        DBProfile(
            name="Profile 2",
            email="profile2@example.com",
            description="Second test profile",
            budget_max=2000,
            target_audiences=["professionals"],
            objectives=["training"],
        ),
    ]
    session.add_all(profiles)
    session.commit()
    session.close()

def teardown_module():
    """
    Drop the test database after tests complete.
    """
    Base.metadata.drop_all(bind=engine)

# Tests

def test_list_profiles():
    response = client.get("/profiles")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Profile 1"
    assert data[1]["name"] == "Profile 2"

def test_read_profile():
    response = client.get("/profiles/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Profile 1"
    assert data["email"] == "profile1@example.com"
    assert data["description"] == "First test profile"

def test_read_profile_not_found():
    response = client.get("/profiles/999")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Item not found"

def test_update_profile():
    updated_data = {
        "name": "Updated Profile",
        "email": "updated@example.com",
        "description": "Updated profile description",
        "budget_max": 3000,
        "target_audiences": ["graduates"],
        "objectives": ["career advancement"],
    }
    response = client.put("/profiles/1", json=updated_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]
    assert data["description"] == updated_data["description"]

def test_update_profile_not_found():
    updated_data = {
        "name": "Nonexistent Profile",
        "email": "nonexistent@example.com",
        "description": "This profile does not exist",
        "budget_max": 0,
        "target_audiences": [],
        "objectives": [],
    }
    response = client.put("/profiles/999", json=updated_data)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Item not found"

def test_delete_profile():
    response = client.delete("/profiles/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1

    # Confirm deletion
    response = client.get("/profiles/1")
    assert response.status_code == 404

def test_delete_profile_not_found():
    response = client.delete("/profiles/999")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Item not found"
