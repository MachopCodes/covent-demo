import pytest

# Test Cases
def test_create_sponsor(client):
    mock_sponsor_data = {
        "name": "New Sponsor",
        "job_title": "Marketing Manager",
        "company_name": "Ad Ventures",
        "budget": 7500.0,
        "industry": "Advertising",
        "topics": ["Digital Marketing", "SEO"],
        "event_attendee_personas": ["Marketers"],
        "key_objectives_for_event_sponsorship": ["Brand Awareness", "Customer Acquisition"],
    }

    response = client.post("/sponsors/", json=mock_sponsor_data)
    assert response.status_code == 200
    assert response.json()["name"] == mock_sponsor_data["name"]
    assert response.json()["budget"] == mock_sponsor_data["budget"]


def test_list_sponsors(client):
    response = client.get("/sponsors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Ensure there are sponsors in the list


def test_read_sponsor(client):
    sponsor_id = 1
    response = client.get(f"/sponsors/{sponsor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sponsor_id


def test_delete_sponsor(client):
    sponsor_id = 1
    response = client.delete(f"/sponsors/{sponsor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sponsor_id
