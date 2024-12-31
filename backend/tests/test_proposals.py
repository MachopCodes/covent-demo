from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, or_
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base, DBProposal, DBUser, DBEvent, DBSponsor
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
models_to_adapt = [DBProposal, DBUser, DBEvent, DBSponsor]
for model in models_to_adapt:
    adapt_model_to_sqlite(engine, model)

# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

# Test users and tokens
test_user_data = {"id": 1, "name": "testuser", "email": "test@example.com"}
sponsor_user_data = {"id": 2, "name": "sponsoruser", "email": "sponsor@example.com"}
test_token = create_access_token(test_user_data)
sponsor_token = create_access_token(sponsor_user_data)

# Headers for authenticated requests
auth_headers = {"Authorization": f"Bearer {test_token}"}
sponsor_auth_headers = {"Authorization": f"Bearer {sponsor_token}"}

def setup_module():
    """
    Create the test database and seed initial data before the tests run.
    """
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    user1 = DBUser(id=test_user_data["id"], name="testuser", email="test@example.com", hashed_password="hashed_pw")
    user2 = DBUser(id=sponsor_user_data["id"], name="sponsoruser", email="sponsor@example.com", hashed_password="hashed_pw")
    sponsor = DBSponsor(
        id=1,
        name="Sponsor 1",
        job_title="Manager",
        company_name="Tech Corp",
        budget=10000.0,  # Provide a valid budget
        industry="Technology",
        topics=["AI", "Cloud"],
        event_attendee_personas=["Developers", "Managers"],
        key_objectives_for_event_sponsorship=["Brand Awareness"],
        user_id=user2.id,
    )
    event = DBEvent(
        id=1,
        name="Tech Meetup",
        event_overview="A tech-focused meetup",
        target_attendees=["Developers", "Managers"],  # Provide target_attendees
        sponsorship_value="$5000",
        contact_info="event1@domain.com",
        user_id=user1.id,  # Associate with the test user
    )
    proposal = DBProposal(
        id=1,
        event_id=event.id,
        sponsor_id=sponsor.id,
        owner_id=user1.id,
        notes="Initial proposal notes",
        contact_info="test@example.com",
        status="PENDING",
        event_snapshot={"name": "Tech Meetup", "date": "2024-12-31"},
        sponsor_snapshot={"name": "Sponsor 1", "company_name": "Tech Corp"},
    )
    session.add_all([user1, user2, sponsor, event, proposal])
    session.commit()
    session.close()


def teardown_module():
    """
    Drop the test database after tests complete.
    """
    Base.metadata.drop_all(bind=engine)

# Tests

def test_list_proposals():
    response = client.get("/proposals", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["notes"] == "Initial proposal notes"

def test_read_proposal():
    response = client.get("/proposals/1", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "PENDING"

def test_read_proposal_not_found():
    response = client.get("/proposals/999", headers=auth_headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Proposal not found"

def test_create_proposal():
    new_proposal = {
        "event_id": 1,
        "sponsor_id": 1,
        "notes": "New proposal notes",
        "contact_info": "newproposal@example.com",
        "status": "PENDING",
        "event_snapshot": {"name": "Tech Meetup", "date": "2024-12-31"},
        "sponsor_snapshot": {"name": "Sponsor 1", "company_name": "Tech Corp"},
    }
    response = client.post("/proposals", json=new_proposal, headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["notes"] == new_proposal["notes"]
    assert data["status"] == new_proposal["status"]

def test_update_proposal():
    updated_proposal = {"notes": "Updated proposal notes", "status": "APPROVED"}
    response = client.put("/proposals/1", json=updated_proposal, headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["notes"] == updated_proposal["notes"]
    assert data["status"] == updated_proposal["status"]

def test_update_proposal_not_found():
    updated_proposal = {"notes": "Nonexistent update"}
    response = client.put("/proposals/999", json=updated_proposal, headers=auth_headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Proposal not found"

def test_delete_proposal():
    response = client.delete("/proposals/1", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1

    # Confirm deletion
    response = client.get("/proposals/1", headers=auth_headers)
    assert response.status_code == 404

def test_delete_proposal_not_found():
    response = client.delete("/proposals/999", headers=auth_headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Proposal not found"
