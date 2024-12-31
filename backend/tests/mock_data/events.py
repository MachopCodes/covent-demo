from app.models import DBEvent

def get_mock_events():
    return [
        DBEvent(
            name="Tech Meetup",
            event_overview="A tech-focused meetup",
            target_attendees=["Developers", "Managers"],
            sponsorship_value="$5000",
            contact_info="event1@domain.com",
            user_id=1,  # Associated with testuser
        )
    ]
