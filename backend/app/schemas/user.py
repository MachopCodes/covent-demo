from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr