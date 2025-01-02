import pytest

# Test Cases
def test_create_event(client):
    mock_event_data = {
        "name": "Test Event",
        "event_overview": "Overview of the event",
        "target_attendees": ["Developers", "Students"],
        "sponsorship_value": "$5000",
        "contact_info": "contact@example.com",
    }

    response = client.post("/events/", json=mock_event_data)
    assert response.status_code == 200
    assert response.json()["name"] == mock_event_data["name"]


def test_list_user_events(client):
    response = client.get("/events/mine")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_all_events(client):
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_event(client):
    event_id = 1
    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == event_id


def test_update_event(client):
    event_id = 1
    mock_updated_event_data = {
        "name": "Updated Event",
        "event_overview": "Updated Overview",
        "target_attendees": ["Professionals"],
        "sponsorship_value": "$10000",
        "contact_info": "updated@example.com",
    }

    response = client.put(f"/events/{event_id}", json=mock_updated_event_data)
    assert response.status_code == 200
    assert response.json()["name"] == mock_updated_event_data["name"]


def test_delete_event(client):
    event_id = 1
    response = client.delete(f"/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == event_id
