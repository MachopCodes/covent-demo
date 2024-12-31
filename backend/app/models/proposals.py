from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.models.base import Base

# Enum for status
class ProposalStatus(enum.Enum):
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"

class DBProposal(Base):
    __tablename__ = "proposals"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    sponsor_id = Column(Integer, ForeignKey("sponsors.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Text fields
    notes = Column(Text, nullable=True)
    contact_info = Column(String(255), nullable=True)

    # Status field using Enum
    status = Column(String, nullable=False)

    # Snapshot fields (stored as JSON)
    event_snapshot = Column(JSONB, nullable=False)  # JSON field for event details
    sponsor_snapshot = Column(JSONB, nullable=False)  # JSON field for sponsor details


    def __repr__(self):
        return (
            f"<DBProposal(id={self.id}, event_id={self.event_id}, sponsor_id={self.sponsor_id}, "
            f"owner_id={self.owner_id}, status={self.status}, contact_info={self.contact_info})>"
        )
