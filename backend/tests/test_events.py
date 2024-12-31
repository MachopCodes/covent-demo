import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.shared_setup import setup_module, teardown_module, get_test_headers

# Setup and teardown for the module
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """
    Automatically set up and tear down the database for all tests in this module.
    """
    setup_module()
    yield
    teardown_module()

# Initialize the TestClient
client = TestClient(app)

# Headers for authenticated requests
headers = get_test_headers()

def test_list_events():
    response = client.get("/events", headers=headers["test_auth_headers"])
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure at least one event is returned
    assert data[0]["name"] == "Event 1"

# def test_read_event():
#     response = client.get("/events/1", headers=headers["test_auth_headers"])
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["name"] == "Event 1"
#     assert data["event_overview"] == "Overview of Event 1"

# def test_read_event_not_found():
#     response = client.get("/events/999", headers=headers["test_auth_headers"])
#     assert response.status_code == 404, response.text
#     assert response.json()["detail"] == "Event not found"

# def test_create_event():
#     new_event = {
#         "name": "New Event",
#         "event_overview": "Overview of New Event",
#         "target_attendees": ["managers", "executives"],
#         "sponsorship_value": "$7000",
#         "contact_info": "newevent@domain.com",
#     }
#     response = client.post("/events", json=new_event, headers=headers["test_auth_headers"])
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["name"] == new_event["name"]
#     assert data["event_overview"] == new_event["event_overview"]

# def test_update_event():
#     updated_event = {
#         "name": "Updated Event",
#         "event_overview": "Updated Overview",
#         "target_attendees": ["developers"],
#         "sponsorship_value": "$4000",
#         "contact_info": "updatedevent@domain.com",
#     }
#     response = client.put("/events/1", json=updated_event, headers=headers["test_auth_headers"])
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["name"] == updated_event["name"]
#     assert data["event_overview"] == updated_event["event_overview"]

# def test_update_event_not_found():
#     updated_event = {
#         "name": "Nonexistent Event",
#         "event_overview": "N/A",
#         "target_attendees": [],
#         "sponsorship_value": "$0",
#         "contact_info": "notfound@domain.com",
#     }
#     response = client.put("/events/999", json=updated_event, headers=headers["test_auth_headers"])
#     assert response.status_code == 404, response.text
#     assert response.json()["detail"] == "Event not found"

# def test_delete_event():
#     response = client.delete("/events/1", headers=headers["test_auth_headers"])
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["id"] == 1

#     # Confirm deletion
#     response = client.get("/events/1", headers=headers["test_auth_headers"])
#     assert response.status_code == 404

# def test_delete_event_not_found():
#     response = client.delete("/events/999", headers=headers["test_auth_headers"])
#     assert response.status_code == 404, response.text
#     assert response.json()["detail"] == "Event not found"
