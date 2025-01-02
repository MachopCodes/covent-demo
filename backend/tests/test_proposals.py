import pytest

# Test Cases
def test_create_proposal(client):
    mock_proposal_data = {
        "event_id": 1,
        "sponsor_id": 1,
        "notes": "Initial proposal notes",
        "contact_info": "test@example.com",
        "status": "PENDING",
        "event_snapshot": {"name": "Tech Meetup", "date": "2024-12-31"},
        "sponsor_snapshot": {"name": "Sponsor 1", "company_name": "Tech Corp"},
    }

    response = client.post("/proposals/", json=mock_proposal_data)
    assert response.status_code == 200
    assert response.json()["notes"] == mock_proposal_data["notes"]
    assert response.json()["status"] == mock_proposal_data["status"]


# def test_list_proposals(client):
#     response = client.get("/proposals/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#     assert len(response.json()) > 0  # Ensure there are proposals in the list


# def test_read_proposal(client):
#     proposal_id = 1
#     response = client.get(f"/proposals/{proposal_id}")
#     assert response.status_code == 200
#     assert response.json()["id"] == proposal_id


def test_update_proposal(client):
    proposal_id = 1
    mock_updated_proposal_data = {
        "notes": "Updated proposal notes",
        "status": "APPROVED",
    }

    response = client.put(f"/proposals/{proposal_id}", json=mock_updated_proposal_data)
    assert response.status_code == 200
    assert response.json()["notes"] == mock_updated_proposal_data["notes"]
    assert response.json()["status"] == mock_updated_proposal_data["status"]


def test_delete_proposal(client):
    proposal_id = 1
    response = client.delete(f"/proposals/{proposal_id}")
    assert response.status_code == 200
    assert response.json()["id"] == proposal_id
