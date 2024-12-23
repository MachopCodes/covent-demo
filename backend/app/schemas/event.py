from pydantic import BaseModel
from typing import List


class Event(BaseModel):
    id: int
    name: str
    event_overview: str
    target_attendees: List[str]
    sponsorship_value: str
    contact_info: str
    user_id: int

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    name: str
    event_overview: str
    target_attendees: List[str]
    sponsorship_value: str
    contact_info: str
    # user_id: int TODO we will auto add the user id based on whos logged in


class EventUpdate(BaseModel):
    name: str
    event_overview: str
    target_attendees: List[str]
    sponsorship_value: str
    contact_info: str
    # user_id: int int TODO we will auto add the user id based on whos logged in
