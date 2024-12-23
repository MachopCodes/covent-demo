import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models import Base, DBSponsor
from tests.test_utils import adapt_model_to_sqlite

# Test setup: use an in-memory SQLite database for tests
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Apply model adaptation for SQLite
adapt_model_to_sqlite(engine, DBSponsor)

@pytest.fixture(scope="module")
def test_db():
    """Create the test database and return a session."""
    Base.metadata.create_all(bind=engine)
    Session = TestingSessionLocal()
    yield Session
    Session.close()
    Base.metadata.drop_all(bind=engine)

def test_insert_record(test_db):
    """Test inserting a record into the sponsors table."""
    session = test_db
    sponsor = DBSponsor(
        name="Test Sponsor",
        job_title="Marketing Manager",
        company_name="Innovative Tech Inc.",
        budget=5000.0,
        industry="Technology",
        topics=["AI", "Blockchain"],
        event_attendee_personas=["Developers", "Executives"],
        key_objectives_for_event_sponsorship=["Brand Awareness", "Networking"]
    )
    session.add(sponsor)
    session.commit()

    # Verify the record was inserted
    db_sponsor = session.query(DBSponsor).filter(DBSponsor.name == "Test Sponsor").first()
    assert db_sponsor is not None, "Sponsor was not inserted"
    assert db_sponsor.name == "Test Sponsor"

def test_update_record(test_db):
    """Test updating a record in the sponsors table."""
    session = test_db
    sponsor = session.query(DBSponsor).filter(DBSponsor.name == "Test Sponsor").first()
    assert sponsor is not None, "Sponsor to update was not found"

    # Update the sponsor's budget
    sponsor.budget = 7000.0
    session.commit()

    updated_sponsor = session.query(DBSponsor).filter(DBSponsor.name == "Test Sponsor").first()
    assert updated_sponsor.budget == 7000.0, "Sponsor budget was not updated"

def test_delete_record(test_db):
    """Test deleting a record from the sponsors table."""
    session = test_db
    sponsor = session.query(DBSponsor).filter(DBSponsor.name == "Test Sponsor").first()
    assert sponsor is not None, "Sponsor to delete was not found"

    # Delete the sponsor
    session.delete(sponsor)
    session.commit()

    deleted_sponsor = session.query(DBSponsor).filter(DBSponsor.name == "Test Sponsor").first()
    assert deleted_sponsor is None, "Sponsor was not deleted"
