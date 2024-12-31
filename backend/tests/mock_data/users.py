from app.models import DBUser

def get_mock_users():
    return [
        DBUser(
            name="testuser",
            email="test@example.com",  # Unique email
            hashed_password="hashed_pw",
            is_active=True,
            is_admin=False
        ),
        DBUser(
            name="adminuser",
            email="admin@example.com",  # Unique email
            hashed_password="hashed_pw",
            is_active=True,
            is_admin=True
        ),
    ]