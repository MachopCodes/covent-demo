import pytest
from pydantic import ValidationError
from app.schemas.sponsor import Sponsor, SponsorCreate, SponsorUpdate
from app.schemas.event import Event, EventCreate, EventUpdate
from app.schemas.proposal import Proposal, ProposalCreate, ProposalUpdate, EventSnapshot, SponsorSnapshot
from app.schemas.user import User, UserCreate, UserUpdate, UserLogin
from app.models.proposals import ProposalStatus


# Sponsor Tests
def test_sponsor_schema_valid():
    data = {
        "id": 1,
        "name": "John Doe",
        "job_title": "Marketing Director",
        "company_name": "Tech Innovations",
        "budget": 50000,
        "industry": "Technology",
        "topics": ["Artificial Intelligence", "Cloud Computing"],
        "event_attendee_personas": ["C-suite executives", "Tech professionals"],
        "key_objectives_for_event_sponsorship": ["Brand awareness", "Networking with industry leaders"],
        "user_id": 10,
    }
    sponsor = Sponsor(**data)
    assert sponsor.id == 1
    assert sponsor.name == "John Doe"


def test_sponsor_schema_invalid():
    data = {"id": 1, "name": "John Doe"}
    with pytest.raises(ValidationError):
        Sponsor(**data)


# Event Tests
def test_event_schema_valid():
    data = {
        "id": 1,
        "name": "Tech Meetup",
        "event_overview": "A gathering of tech professionals.",
        "target_attendees": ["Developers", "Startups"],
        "sponsorship_value": "5000 USD",
        "contact_info": "contact@meetup.com",
        "user_id": 5,
    }
    event = Event(**data)
    assert event.name == "Tech Meetup"


def test_event_schema_invalid():
    data = {"id": 1, "name": "Tech Meetup"}
    with pytest.raises(ValidationError):
        Event(**data)


# Proposal Tests
def test_proposal_schema_valid():
    data = {
        "id": 1,
        "event_id": 2,
        "sponsor_id": 3,
        "owner_id": 4,
        "notes": "Important proposal details.",
        "contact_info": "contact@sponsor.com",
        "status": ProposalStatus.PENDING,
        "event_snapshot": {"name": "Tech Meetup", "date": "2024-12-31"},
        "sponsor_snapshot": {"name": "Sponsor A", "company_name": "Tech Innovations"},
    }
    proposal = Proposal(**data)
    assert proposal.status == ProposalStatus.PENDING


def test_proposal_schema_invalid():
    data = {
        "id": 1,
        "event_id": 2,
        "sponsor_id": 3,
        "owner_id": 4,
        "status": "InvalidStatus",
    }
    with pytest.raises(ValidationError):
        Proposal(**data)


# User Tests
def test_user_schema_valid():
    data = {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "is_active": True,
        "is_admin": False,
    }
    user = User(**data)
    assert user.email == "jane.doe@example.com"


def test_user_schema_invalid():
    data = {"id": 1, "name": "Jane Doe"}
    with pytest.raises(ValidationError):
        User(**data)


def test_user_create_schema_valid():
    data = {"name": "Jane Doe", "email": "jane.doe@example.com", "password": "securepassword"}
    user_create = UserCreate(**data)
    assert user_create.password == "securepassword"


def test_user_create_schema_invalid():
    data = {"name": "Jane Doe", "email": "jane.doe@example.com"}
    with pytest.raises(ValidationError):
        UserCreate(**data)


# Schema-Specific Validation
def test_event_snapshot_schema_valid():
    data = {"name": "Tech Event", "date": "2024-12-31"}
    snapshot = EventSnapshot(**data)
    assert snapshot.name == "Tech Event"


def test_event_snapshot_schema_invalid():
    data = {"name": "Tech Event", "date": 12345}  # Invalid date format
    with pytest.raises(ValidationError):
        EventSnapshot(**data)


def test_sponsor_snapshot_schema_valid():
    data = {"name": "Sponsor A", "company_name": "Tech Innovations"}
    snapshot = SponsorSnapshot(**data)
    assert snapshot.company_name == "Tech Innovations"


def test_sponsor_snapshot_schema_invalid():
    data = {"name": "Sponsor A"}  # Missing company_name
    with pytest.raises(ValidationError):
        SponsorSnapshot(**data)
