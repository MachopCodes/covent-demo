from pydantic import BaseModel, ConfigDict
from typing import List


class Sponsor(BaseModel):
    id: int
    name: str
    job_title: str
    company_name: str
    budget: float
    industry: str
    topics: List[str]
    event_attendee_personas: List[str]
    key_objectives_for_event_sponsorship: List[str]
    user_id: int  # New field


    model_config = ConfigDict(from_attributes=True)

class SponsorCreate(BaseModel):
    name: str
    job_title: str
    company_name: str
    budget: float
    industry: str
    topics: List[str]
    event_attendee_personas: List[str]
    key_objectives_for_event_sponsorship: List[str]
     # user_id: int TODO we will auto add the user id based on whos logged in


class SponsorUpdate(BaseModel):
    name: str
    job_title: str
    company_name: str
    budget: float
    industry: str
    topics: List[str]
    event_attendee_personas: List[str]
    key_objectives_for_event_sponsorship: List[str]
     # user_id: int TODO we will auto add the user id based on whos logged in
