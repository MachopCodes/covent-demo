from typing import List
from pydantic import BaseModel
from typing import Optional

class Profile(BaseModel):
    id: int
    name: str
    description: Optional[str]
    email: str
    budget_max: int
    target_audiences: Optional[List[str]]
    objectives: Optional[List[str]]


class ProfileCreate(BaseModel):
    name: str
    description: Optional[str]
    email: str
    budget_max: int
    target_audiences: Optional[List[str]]
    objectives: Optional[List[str]]


class ProfileUpdate(BaseModel):
      name: str
      description: Optional[str]
      email: str
      budget_max: int
      target_audiences: Optional[List[str]]
      objectives: Optional[List[str]]