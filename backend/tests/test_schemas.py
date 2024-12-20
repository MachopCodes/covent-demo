from app.schemas import Profile
import pytest
from pydantic import ValidationError

def test_profile_schema_valid():
    # Valid data
    data = {
        "id": 1,
        "name": "Test User",
        "email": "testuser@example.com",
        "description": "A test user profile",
        "budget_max": 1000,
        "target_audiences": ["audience1", "audience2"],
        "objectives": ["objective1", "objective2"]
    }
    profile = Profile(**data)

    # Assert attributes
    assert profile.id == 1
    assert profile.name == "Test User"
    assert profile.email == "testuser@example.com"
    assert profile.description == "A test user profile"
    assert profile.budget_max == 1000
    assert profile.target_audiences == ["audience1", "audience2"]
    assert profile.objectives == ["objective1", "objective2"]

def test_profile_schema_invalid():
    # Invalid data (missing required fields)
    invalid_data = {
        "id": 1,
        "email": "testuser@example.com"
    }
    with pytest.raises(ValidationError):
        Profile(**invalid_data)
