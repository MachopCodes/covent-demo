from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class DBProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    description = Column(String)
    budget_max = Column(Integer)
    target_audiences = Column(JSON)  # Store list of strings as JSON
    objectives = Column(JSON)  # Store list of strings as JSON
