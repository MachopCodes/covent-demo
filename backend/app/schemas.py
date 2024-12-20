from typing import List
from pydantic import BaseModel

class Profile(BaseModel):
    id: int
    name: str
    email: str
    description: str
    budget_max: int
    target_audiences: List[str]
    objectives: List[str]

    class Config:
        orm_mode = True

