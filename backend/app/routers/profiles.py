from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import DBProfile  # SQLAlchemy model
from app.schemas import  Profile, ProfileUpdate, ProfileCreate  # Pydantic schemas
from app.database import get_db

router = APIRouter()

@router.post("/profiles")
def create_item(profile: ProfileCreate, db: Session = Depends(get_db)) -> Profile:
    db_item = DBProfile(**profile.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return Profile(**db_item.__dict__)

@router.get("/profiles")
def list_items(db: Session = Depends(get_db)) -> list[Profile]:
    db_items = db.query(DBProfile).all()
    return [Profile(**db_item.__dict__) for db_item in db_items]


@router.get("/profiles/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> Profile:
    db_item = db.query(DBProfile).filter(DBProfile.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Profile(**db_item.__dict__)


@router.put("/profiles/{item_id}")
def update_item(item_id: int, item: ProfileUpdate, db: Session = Depends(get_db)) -> Profile:
    db_item = db.query(DBProfile).filter(DBProfile.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return Profile(**db_item.__dict__)


@router.delete("/profiles/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Profile:
    db_item = db.query(DBProfile).filter(DBProfile.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return Profile(**db_item.__dict__)