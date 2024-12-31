# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy.dialects.sqlite import JSON
# from app.models import Base, DBEvent, DBProposal, DBSponsor, DBUser
# from app.models.proposals import ProposalStatus
# from sqlalchemy.types import Enum, String
# from sqlalchemy.dialects.postgresql import JSONB, ARRAY
# from sqlalchemy.dialects.sqlite import JSON
# from tests.test_utils import adapt_model_to_sqlite


# # Setup in-memory SQLite database for testing
# DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Adapt ARRAY fields to JSON for SQLite
# for model in [DBEvent, DBSponsor]:
#      for column in model.__table__.columns:
#             if isinstance(column.type, ARRAY):
#                 column.type = JSON()  # Replace ARRAY with JSON
#             elif isinstance(column.type, JSONB):
#                 column.type = JSON()  # Replace JSONB with JSON
#             elif isinstance(column.type, Enum):
#                 column.type = String()  # Replace Enum with String
   


# # Initialize the database schema
# Base.metadata.create_all(bind=engine)


# @pytest.fixture
# def db_session():
#     """
#     Provides a database session for each test.
#     Rolls back transactions after each test.
#     """
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = TestingSessionLocal(bind=connection)

#     yield session

#     session.close()
#     transaction.rollback()
#     connection.close()


# # Tests for DBUser
# def test_create_user(db_session):
#     user = DBUser(
#         name="John Doe",
#         email="john.doe@example.com",
#         hashed_password="hashedpassword123",
#         is_active=True,
#         is_admin=False,
#     )
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     assert user.id is not None
#     assert user.name == "John Doe"
#     assert user.email == "john.doe@example.com"


# def test_user_email_unique_constraint(db_session):
#     user1 = DBUser(
#         name="Jane Doe",
#         email="jane.doe@example.com",
#         hashed_password="password123",
#     )
#     user2 = DBUser(
#         name="Another Jane",
#         email="jane.doe@example.com",  # Duplicate email
#         hashed_password="password123",
#     )
#     db_session.add(user1)
#     db_session.commit()

#     with pytest.raises(IntegrityError):
#         db_session.add(user2)
#         db_session.commit()


# # Tests for DBSponsor
# def test_create_sponsor(db_session):
#     user = DBUser(name="Sponsor Owner", email="owner@example.com", hashed_password="password")
#     db_session.add(user)
#     db_session.commit()

#     sponsor = DBSponsor(
#         name="Tech Sponsor",
#         job_title="Marketing Lead",
#         company_name="Tech Innovations",
#         budget=100000.0,
#         industry="Technology",
#         topics=["AI", "Cloud"],  # JSON format for SQLite
#         event_attendee_personas=["Developers", "C-Suite"],
#         key_objectives_for_event_sponsorship=["Brand Awareness", "Networking"],
#         user_id=user.id,
#     )
#     db_session.add(sponsor)
#     db_session.commit()
#     db_session.refresh(sponsor)

#     assert sponsor.id is not None
#     assert sponsor.name == "Tech Sponsor"


# # Tests for DBEvent
# def test_create_event(db_session):
#     user = DBUser(name="Event Owner", email="owner@example.com", hashed_password="password")
#     db_session.add(user)
#     db_session.commit()

#     event = DBEvent(
#         name="Tech Meetup",
#         event_overview="Networking event for tech enthusiasts",
#         target_attendees=["Developers", "Entrepreneurs"],  # JSON format for SQLite
#         sponsorship_value="5000 USD",
#         contact_info="contact@techmeetup.com",
#         user_id=user.id,
#     )
#     db_session.add(event)
#     db_session.commit()
#     db_session.refresh(event)

#     assert event.id is not None
#     assert event.name == "Tech Meetup"


# # Tests for DBProposal
# def test_create_proposal(db_session):
#     user = DBUser(name="Proposal Owner", email="owner@example.com", hashed_password="password")
#     sponsor = DBSponsor(
#         name="Sponsor A",
#         job_title="CEO",
#         company_name="Sponsor Co.",
#         budget=5000.0,
#         industry="Tech",
#         topics=["AI", "ML"],
#         event_attendee_personas=["Developers"],
#         key_objectives_for_event_sponsorship=["Visibility"],
#         user_id=user.id,
#     )
#     event = DBEvent(
#         name="Tech Conference",
#         event_overview="Conference for tech enthusiasts",
#         target_attendees=["Developers", "Startups"],
#         sponsorship_value="10,000 USD",
#         contact_info="info@techconference.com",
#         user_id=user.id,
#     )
#     db_session.add_all([user, sponsor, event])
#     db_session.commit()

#     proposal = DBProposal(
#         event_id=event.id,
#         sponsor_id=sponsor.id,
#         owner_id=user.id,
#         notes="This is a test proposal",
#         contact_info="contact@example.com",
#         status=ProposalStatus.PENDING,
#         event_snapshot={"name": "Tech Conference", "date": "2024-12-31"},
#         sponsor_snapshot={"name": "Sponsor A", "company_name": "Sponsor Co."},
#     )
#     db_session.add(proposal)
#     db_session.commit()
#     db_session.refresh(proposal)

#     assert proposal.id is not None
#     assert proposal.status == ProposalStatus.PENDING
