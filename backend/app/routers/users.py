from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import DBUser  # SQLAlchemy model
from app.schemas import User, UserCreate, UserUpdate  # Pydantic schemas
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[User])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    users = db.query(DBUser).all()
    return [User.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User.model_validate(user)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> User:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return User.model_validate(user)


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return User.model_validate(user)
