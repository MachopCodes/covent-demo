from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app from main.py

# Initialize the test client
client = TestClient(app)

# Test the root endpoint
def test_read_root():
    response = client.get("/")  # Send a GET request to the root endpoint
    assert response.status_code == 200  # Check the status code
    assert response.json() == {"hello": "world"}  # Check the response body