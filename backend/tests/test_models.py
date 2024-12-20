import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Profile

# Test setup: use an in-memory SQLite database for tests
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_profile_model(test_db):
    session = test_db

    # Create a new Profile instance
    profile = Profile(
        name="Test User",
        email="testuser@example.com",
        description="A test user profile",
        budget_max=1000,
        target_audiences=["audience1", "audience2"],
        objectives=["objective1", "objective2"]
    )

    # Add and commit the profile
    session.add(profile)
    session.commit()

    # Retrieve the profile and assert its attributes
    saved_profile = session.query(Profile).first()
    assert saved_profile.name == "Test User"
    assert saved_profile.email == "testuser@example.com"
    assert saved_profile.description == "A test user profile"
    assert saved_profile.budget_max == 1000
    assert saved_profile.target_audiences == ["audience1", "audience2"]
    assert saved_profile.objectives == ["objective1", "objective2"]
