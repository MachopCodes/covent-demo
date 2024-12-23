from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from .base import Base


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
