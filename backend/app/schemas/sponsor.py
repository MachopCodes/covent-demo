from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class Sponsor(BaseModel):
    id: int
    name: str
    job_title: str
    company_name: str
    budget: int
    industry: str
    topics: List[str]
    event_attendee_personas: List[str]
    key_objectives_for_event_sponsorship: List[str]

    model_config = ConfigDict(from_attributes=True)

class SponsorCreate(BaseModel):
    name: str
    job_title: str
    company_name: str
    budget: int
    industry: str
    topics: List[str]
    event_attendee_personas: List[str]
    key_objectives_for_event_sponsorship: List[str]

class SponsorUpdate(BaseModel):
    name: Optional[str]
    job_title: Optional[str]
    company_name: Optional[str]
    budget: Optional[int]
    industry: Optional[str]
    topics: Optional[List[str]]
    event_attendee_personas: Optional[List[str]]
    key_objectives_for_event_sponsorship: Optional[List[str]]
