import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from app.main import app  # Assuming this is where your FastAPI app instance is defined
from app.models import DBEvent, DBUser
from app.schemas.event import EventCreate, EventUpdate
from app.database import get_db
from app.utils.dependencies import get_current_user

# Mock dependencies
def get_mock_db():
    mock_session = MagicMock()
    
    mock_event = DBEvent(
        id=1,
        name="Test Event",
        event_overview="Overview of the event",
        target_attendees=["Developers", "Students"],
        sponsorship_value="$5000",
        contact_info="contact@example.com",
        user_id=1
    )
    
    def mock_add(instance):
        instance.id = 1  # Simulate the database assigning an ID
        return instance

    mock_session.add.side_effect = mock_add
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_event
    mock_session.query.return_value = mock_query

    return mock_session

def get_mock_current_user():
    return DBUser(id=1, name="Test User", email="test@example.com", hashed_password="hashed", is_active=True)

app.dependency_overrides[get_db] = get_mock_db
app.dependency_overrides[get_current_user] = get_mock_current_user

client = TestClient(app)

# Mock data
mock_event_data = {
    "name": "Test Event",
    "event_overview": "Overview of the event",
    "target_attendees": ["Developers", "Students"],
    "sponsorship_value": "$5000",
    "contact_info": "contact@example.com",
}

mock_updated_event_data = {
    "name": "Updated Event",
    "event_overview": "Updated Overview",
    "target_attendees": ["Professionals"],
    "sponsorship_value": "$10000",
    "contact_info": "updated@example.com",
}


# Test cases
def test_create_event():
    mock_event_data = {
        "name": "Test Event",
        "event_overview": "Overview of the event",
        "target_attendees": ["Developers", "Students"],
        "sponsorship_value": "$5000",
        "contact_info": "contact@example.com",
    }

    response = client.post("/events/", json=mock_event_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"
    assert response.json()["id"] == 1  # Validate the mocked ID

def test_list_user_events():
    response = client.get("/events/mine")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_all_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_event():
    # Mock event ID
    event_id = 1
    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == event_id

def test_update_event():
    # Mock event ID
    event_id = 1
    response = client.put(f"/events/{event_id}", json=mock_updated_event_data)
    assert response.status_code == 200
    assert response.json()["name"] == mock_updated_event_data["name"]

def test_delete_event():
    # Mock event ID
    event_id = 1
    response = client.delete(f"/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == event_id

