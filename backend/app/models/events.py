from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from app.models.base import Base


class DBEvent(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    event_overview = Column(String, nullable=False)
    target_attendees = Column(PG_ARRAY(String), nullable=False)  # PostgreSQL ARRAY
    sponsorship_value = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    
    # Foreign Key to link to the User table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to link to the User model
    user = relationship("DBUser", back_populates="events")
