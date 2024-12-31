from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class EventSnapshot(BaseModel):
    name: str
    date: Optional[str] = None

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
    status: str
    event_snapshot: EventSnapshot
    sponsor_snapshot: SponsorSnapshot

    model_config = ConfigDict(from_attributes=True)


class ProposalCreate(BaseModel):
    event_id: int
    sponsor_id: int
    notes: Optional[str] = Field(None, description="Additional details about the proposal")
    contact_info: Optional[str] = Field(None, description="Sponsor's contact information")
    status: str = 'PENDING'
    event_snapshot: EventSnapshot
    sponsor_snapshot: SponsorSnapshot


class ProposalUpdate(BaseModel):
    notes: Optional[str] = Field(None, description="Additional details about the proposal")
    contact_info: Optional[str] = Field(None, description="Sponsor's contact information")
    status: Optional[str] = None
