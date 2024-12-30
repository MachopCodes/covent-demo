from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal, Optional


class EventSnapshot(BaseModel):
    name: str
    date: str


class SponsorSnapshot(BaseModel):
    name: str
    company_name: str


class Proposal(BaseModel):
    id: int
    event_id: int
    sponsor_id: int
    owner_id: int
    notes: Optional[str] = Field(None, description="Additional details about the proposal")
    contact_info: Optional[str] = Field(None, description="Sponsor's contact information")
    status: Literal['Approved', 'Pending', 'Rejected']
    event_snapshot: EventSnapshot
    sponsor_snapshot: SponsorSnapshot

    model_config = ConfigDict(from_attributes=True)


class ProposalCreate(BaseModel):
    event_id: int
    sponsor_id: int
    notes: Optional[str] = Field(None, description="Additional details about the proposal")
    contact_info: Optional[str] = Field(None, description="Sponsor's contact information")
    status: Literal['Approved', 'Pending', 'Rejected'] = 'Pending'
    event_snapshot: EventSnapshot
    sponsor_snapshot: SponsorSnapshot


class ProposalUpdate(BaseModel):
    notes: Optional[str] = Field(None, description="Additional details about the proposal")
    contact_info: Optional[str] = Field(None, description="Sponsor's contact information")
    status: Optional[Literal['Approved', 'Pending', 'Rejected']] = None
