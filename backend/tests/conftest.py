from fastapi.testclient import TestClient
import pytest
from unittest.mock import MagicMock
from app.main import app
from app.models import DBSponsor, DBEvent, DBProposal, DBUser
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.schemas.proposal import EventSnapshot, SponsorSnapshot

# Mock data
mock_proposals = [ DBProposal(
            id=1,
            event_id=1,
            sponsor_id=1,
            notes="Proposal Notes",
            owner_id=1,
            contact_info="contact@example.com",
            status="PENDING",
            event_snapshot=EventSnapshot(name="Tech Meetup", date="2024-12-31"),
            sponsor_snapshot=SponsorSnapshot(name="Sponsor 1", company_name="Tech Corp"),
        )]
mock_sponsors = [
    DBSponsor(
        id=1,
        name="Sponsor One",
        job_title="Manager",
        company_name="Tech Corp",
        budget=5000.0,
        industry="Technology",
        topics=["AI", "Cloud"],
        event_attendee_personas=["Developers", "Executives"],
        key_objectives_for_event_sponsorship=["Brand Awareness"],
        user_id=1,
    ),
    DBSponsor(
        id=2,
        name="Sponsor Two",
        job_title="CTO",
        company_name="Biz Inc",
        budget=10000.0,
        industry="Finance",
        topics=["FinTech"],
        event_attendee_personas=["Managers"],
        key_objectives_for_event_sponsorship=["Lead Generation"],
        user_id=2,
    ),
]
mock_events = [
    DBEvent(
        id=1,
        name="Tech Conference",
        event_overview="A premier event for tech professionals.",
        target_attendees=["Developers", "Entrepreneurs"],
        sponsorship_value="$5000",
        contact_info="info@techconf.com",
        user_id=1,
    )
]
mock_users = [
    DBUser(id=1, name="Alice", email="alice@example.com", hashed_password="hashed_pw", is_active=True, is_admin=False),
    DBUser(id=2, name="Bob", email="bob@example.com", hashed_password="hashed_pw", is_active=True, is_admin=False),
]

# Mock DB Query
class MockQuery:
    def __init__(self, items):
        self.items = items

    def filter(self, *conditions):
        filtered_items = [
            item for item in self.items if all(self._evaluate_condition(item, condition) for condition in conditions)
        ]
        return MockQuery(filtered_items)

    def _evaluate_condition(self, item, condition):
        if hasattr(condition.left, "key") and hasattr(condition.right, "value"):
            return getattr(item, condition.left.key) == condition.right.value
        return True

    def first(self):
        return self.items[0] if self.items else None

    def all(self):
        return self.items

# Mock DB Session
@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()

    def query_mock(model):
        if model == DBSponsor:
            return MockQuery(mock_sponsors)
        elif model == DBEvent:
            return MockQuery(mock_events)
        elif model == DBProposal:
            return MockQuery(mock_proposals)
        elif model == DBUser:
            return MockQuery(mock_users)
        return MockQuery([])

    def mock_add(instance):
        if isinstance(instance, DBProposal):
            instance.id = len(mock_proposals) + 1
            mock_proposals.append(instance)
        elif isinstance(instance, DBSponsor):
            instance.id = len(mock_sponsors) + 1
            mock_sponsors.append(instance)
        elif isinstance(instance, DBEvent):
            instance.id = len(mock_events) + 1
            mock_events.append(instance)

    mock_session.query.side_effect = query_mock
    mock_session.add.side_effect = mock_add
    mock_session.commit.side_effect = lambda: None
    mock_session.refresh.side_effect = lambda instance: instance

    return mock_session

# Override dependency
@pytest.fixture(autouse=True)
def override_dependency(mock_db_session):
    app.dependency_overrides[get_db] = lambda: mock_db_session

# Mock current user
@pytest.fixture
def mock_current_user():
    return DBUser(id=1, name="Test User", email="test@example.com", hashed_password="hashed", is_active=True)

@pytest.fixture(autouse=True)
def override_current_user(mock_current_user):
    app.dependency_overrides[get_current_user] = lambda: mock_current_user

# Client Fixture
@pytest.fixture
def client():
    return TestClient(app)
