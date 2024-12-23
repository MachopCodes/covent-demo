from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from app.models.base import Base


class DBSponsor(Base):
    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    industry = Column(String, nullable=False)
    topics = Column(PG_ARRAY(String), nullable=False)  # PostgreSQL ARRAY
    event_attendee_personas = Column(PG_ARRAY(String), nullable=False)  # PostgreSQL ARRAY
    key_objectives_for_event_sponsorship = Column(PG_ARRAY(String), nullable=False)  # PostgreSQL ARRAY

    # Foreign Key to link to the User table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Relationship to link to the User model
    user = relationship("DBUser", back_populates="sponsors")
