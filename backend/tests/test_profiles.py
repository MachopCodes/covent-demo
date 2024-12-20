from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_profiles():
    response = client.get("/profiles")
    assert response.status_code == 200
    assert response.json() == {"message": "Profiles endpoint is working!"}
