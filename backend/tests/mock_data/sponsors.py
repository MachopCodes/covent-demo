from app.models import DBSponsor

def get_mock_sponsors():
    return [
        DBSponsor(
            name="Sponsor 1",
            job_title="Manager",
            company_name="Tech Corp",
            budget=10000.0,
            industry="Technology",
            topics=["AI", "Cloud"],
            event_attendee_personas=["Developers", "Managers"],
            key_objectives_for_event_sponsorship=["Brand Awareness"],
            user_id=2,  # Associated with adminuser
        )
    ]
