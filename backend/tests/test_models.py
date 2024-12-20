import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, DBProfile

# Test setup: use an in-memory SQLite database for tests
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models import Base, DBProfile

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module(module):
    """Create tables in the test database."""
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    """Drop tables in the test database."""
    Base.metadata.drop_all(bind=engine)

def test_insert_record():
    """Test inserting a record into the profiles table."""
    session = TestingSessionLocal()
    profile = DBProfile(
        name="Test User",
        email="test@example.com",
        description="Test description",
        budget_max=1000,
        target_audiences=["students", "professionals"],
        objectives=["education", "training"]
    )
    session.add(profile)
    session.commit()

    # Verify the record was inserted
    db_profile = session.query(DBProfile).filter(DBProfile.email == "test@example.com").first()
    assert db_profile is not None, "Profile was not inserted"
    assert db_profile.name == "Test User"
    session.close()

def test_unique_email_constraint():
    """Test unique constraint on the email field."""
    session = TestingSessionLocal()
    profile1 = DBProfile(
        name="User One",
        email="unique@example.com",
        description="First user",
        budget_max=500,
        target_audiences=["students"],
        objectives=["education"]
    )
    profile2 = DBProfile(
        name="User Two",
        email="unique@example.com",
        description="Second user",
        budget_max=700,
        target_audiences=["professionals"],
        objectives=["training"]
    )
    session.add(profile1)
    session.commit()

    try:
        session.add(profile2)
        session.commit()
    except IntegrityError:
        session.rollback()
    else:
        assert False, "Unique constraint on email did not raise an error"
    session.close()

def test_update_record():
    """Test updating a record in the profiles table."""
    session = TestingSessionLocal()
    profile = session.query(DBProfile).filter(DBProfile.email == "test@example.com").first()
    assert profile is not None, "Profile to update was not found"
    
    # Update the profile's budget
    profile.budget_max = 1500
    session.commit()

    updated_profile = session.query(DBProfile).filter(DBProfile.email == "test@example.com").first()
    assert updated_profile.budget_max == 1500, "Profile budget was not updated"
    session.close()

def test_delete_record():
    """Test deleting a record from the profiles table."""
    session = TestingSessionLocal()
    profile = session.query(DBProfile).filter(DBProfile.email == "test@example.com").first()
    assert profile is not None, "Profile to delete was not found"
    
    # Delete the profile
    session.delete(profile)
    session.commit()

    deleted_profile = session.query(DBProfile).filter(DBProfile.email == "test@example.com").first()
    assert deleted_profile is None, "Profile was not deleted"
    session.close()
