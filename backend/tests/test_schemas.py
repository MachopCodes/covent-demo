from app.schemas import Sponsor
import pytest
from pydantic import ValidationError

def test_sponsor_schema_valid():
    # Valid data
    data = {
        "id": 1,
        "name": "John Doe",
        "job_title": "Marketing Director",
        "company_name": "Tech Innovations",
        "budget": 50000,
        "industry": "Technology",
        "topics": ["Artificial Intelligence", "Cloud Computing"],
        "event_attendee_personas": ["C-suite executives", "Tech professionals"],
        "key_objectives_for_event_sponsorship": ["Brand awareness", "Networking with industry leaders"]
    }
    sponsor = Sponsor(**data)

    # Assert attributes
    assert sponsor.id == 1
    assert sponsor.name == "John Doe"
    assert sponsor.job_title == "Marketing Director"
    assert sponsor.company_name == "Tech Innovations"
    assert sponsor.budget == 50000
    assert sponsor.industry == "Technology"
    assert sponsor.topics == ["Artificial Intelligence", "Cloud Computing"]
    assert sponsor.event_attendee_personas == ["C-suite executives", "Tech professionals"]
    assert sponsor.key_objectives_for_event_sponsorship == ["Brand awareness", "Networking with industry leaders"]

def test_sponsor_schema_invalid():
    # Invalid data (missing required fields)
    invalid_data = {
        "id": 1,
        "name": "John Doe",
        "job_title": "Marketing Director",
        "budget": 50000,
    }
    with pytest.raises(ValidationError):
        Sponsor(**invalid_data)
