import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.shared_setup import setup_module, teardown_module, get_test_headers, override_get_db
from app.database import get_db

# Override the app dependency
app.dependency_overrides[get_db] = override_get_db

# Setup and teardown for the module
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    setup_module()
    yield
    teardown_module()

# Initialize the TestClient
client = TestClient(app)
headers = get_test_headers()["test_auth_headers"]

def test_list_sponsors():
    response = client.get("/sponsors", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Sponsor 1"

def test_read_sponsor():
    response = client.get("/sponsors/1", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Sponsor 1"

def test_read_sponsor_not_found():
    response = client.get("/sponsors/999", headers=headers)
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
    response = client.put("/sponsors/1", json=updated_data, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == updated_data["name"]

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
    response = client.put("/sponsors/999", json=updated_data, headers=headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Sponsor not found"

def test_delete_sponsor():
    response = client.delete("/sponsors/1", headers=headers)
    assert response.status_code == 200, response.text

    response = client.get("/sponsors/1", headers=headers)
    assert response.status_code == 404

def test_delete_sponsor_not_found():
    response = client.delete("/sponsors/999", headers=headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Sponsor not found"
