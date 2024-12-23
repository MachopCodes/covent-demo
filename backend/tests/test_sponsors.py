from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base, DBSponsor
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
adapt_model_to_sqlite(engine, DBSponsor)

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
    sponsors = [
        DBSponsor(
            name="Sponsor 1",
            job_title="CEO",
            company_name="Tech Innovators",
            budget=1000.0,
            industry="Education",
            topics=["AI", "Cloud"],
            event_attendee_personas=["students"],
            key_objectives_for_event_sponsorship=["brand awareness"],
        ),
        DBSponsor(
            name="Sponsor 2",
            job_title="CTO",
            company_name="NextGen Solutions",
            budget=2000.0,
            industry="Technology",
            topics=["Networking"],
            event_attendee_personas=["professionals"],
            key_objectives_for_event_sponsorship=["networking"],
        ),
    ]
    session.add_all(sponsors)
    session.commit()
    session.close()

def teardown_module():
    """
    Drop the test database after tests complete.
    """
    Base.metadata.drop_all(bind=engine)

# Tests

def test_list_sponsors():
    response = client.get("/sponsors")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Sponsor 1"
    assert data[1]["name"] == "Sponsor 2"

def test_read_sponsor():
    response = client.get("/sponsors/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Sponsor 1"
    assert data["job_title"] == "CEO"
    assert data["company_name"] == "Tech Innovators"
    assert data["description"] == "First test sponsor"

def test_read_sponsor_not_found():
    response = client.get("/sponsors/999")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Sponsor not found"

def test_update_sponsor():
    updated_data = {
        "name": "Updated Sponsor",
        "job_title": "CMO",
        "company_name": "Updated Inc.",
        "budget": 3000.0,
        "industry": "Healthcare",
        "topics": ["Innovation"],
        "event_attendee_personas": ["graduates"],
        "key_objectives_for_event_sponsorship": ["career advancement"],
    }
    response = client.put("/sponsors/1", json=updated_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["job_title"] == updated_data["job_title"]
    assert data["company_name"] == updated_data["company_name"]

def test_update_sponsor_not_found():
    updated_data = {
        "name": "Nonexistent Sponsor",
        "job_title": "COO",
        "company_name": "Ghost Corp.",
        "budget": 0.0,
        "industry": "Unknown",
        "topics": [],
        "event_attendee_personas": [],
        "key_objectives_for_event_sponsorship": [],
    }
    response = client.put("/sponsors/999", json=updated_data)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Sponsor not found"

def test_delete_sponsor():
    response = client.delete("/sponsors/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1

    # Confirm deletion
    response = client.get("/sponsors/1")
    assert response.status_code == 404

def test_delete_sponsor_not_found():
    response = client.delete("/sponsors/999")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Sponsor not found"
