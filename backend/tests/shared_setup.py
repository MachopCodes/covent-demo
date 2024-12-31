from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.models import Base, DBEvent, DBUser, DBProposal, DBSponsor
from tests.test_utils import adapt_model_to_sqlite
from app.utils.jwt import create_access_token
from tests.mock_data.users import get_mock_users
from tests.mock_data.sponsors import get_mock_sponsors
from tests.mock_data.events import get_mock_events
from tests.mock_data.proposals import get_mock_proposals

# Common in-memory SQLite database setup
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Adapt PostgreSQL models for SQLite compatibility
def adapt_models():
    models_to_adapt = [DBEvent, DBUser, DBSponsor, DBProposal]
    for model in models_to_adapt:
        adapt_model_to_sqlite(engine, model)

# Dependency override for database access in tests
def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.rollback()
        database.close()

# Seed mock data into the database
def seed_data(session):
    users = get_mock_users()
    sponsors = get_mock_sponsors()
    events = get_mock_events()
    proposals = get_mock_proposals()

    session.add_all(users + sponsors + events + proposals)
    session.commit()

# General setup function
def setup_module():
    adapt_models()  # Ensure models are adapted for SQLite
    Base.metadata.create_all(bind=engine)  # Create tables
    session = TestingSessionLocal()
    seed_data(session)  # Seed mock data
    session.close()

# General teardown function
def teardown_module():
    Base.metadata.drop_all(bind=engine)

# Shared headers for authenticated requests
def get_test_headers():
    test_user_data = {"id": 1, "name": "testuser", "email": "test@example.com", "is_active": True, "is_admin": False}
    admin_user_data = {"id": 2, "name": "adminuser", "email": "admin@example.com", "is_active": True, "is_admin": True}
    test_token = create_access_token(test_user_data)
    admin_token = create_access_token(admin_user_data)
    return {
        "test_auth_headers": {"Authorization": f"Bearer {test_token}"},
        "admin_auth_headers": {"Authorization": f"Bearer {admin_token}"},
    }
