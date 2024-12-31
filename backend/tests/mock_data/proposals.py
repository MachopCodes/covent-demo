from app.models import DBProposal
from app.models.proposals import ProposalStatus

def get_mock_proposals():
    return [
        DBProposal(
            event_id=1,
            sponsor_id=1,
            owner_id=1,
            notes="Initial proposal notes",
            contact_info="test@example.com",
            status='PENDING',
            event_snapshot={"name": "Tech Meetup", "date": "2024-12-31"},
            sponsor_snapshot={"name": "Sponsor 1", "company_name": "Tech Corp"},
        ),
        DBProposal(
            event_id=2,
            sponsor_id=1,
            owner_id=1,
            notes="Second proposal notes",
            contact_info="second@example.com",
            status='APPROVED',
            event_snapshot={"name": "Tech Conference", "date": "2024-12-31"},
            sponsor_snapshot={"name": "Sponsor 1", "company_name": "Tech Corp"},
        ),
    ]