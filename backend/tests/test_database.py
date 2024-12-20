from app.database import engine, SessionLocal

def test_engine_creation():
    """Test if the engine is created with the correct URL."""
    assert engine.url is not None, "Engine URL is not set"
    assert "sqlite" in str(engine.url) or "postgresql" in str(engine.url), "Unexpected engine URL"

def test_session_local_creation():
    """Test if the sessionmaker creates a valid session."""
    session = SessionLocal()
    assert session is not None, "SessionLocal did not create a session"
    session.close()