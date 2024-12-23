from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import DBEvent
from app.schemas.event import Event, EventCreate, EventUpdate
from app.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db)) -> Event:
    """
    Create a new event. Placeholder for user_id verification.
    """
    # TODO: Replace user_id with actual logged-in user verification.
    user_id = 1  # Placeholder user ID
    db_event = DBEvent(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return Event.model_validate(db_event)


@router.get("/", response_model=List[Event])
def list_events(db: Session = Depends(get_db)) -> List[Event]:
    """
    List all events.
    """
    events = db.query(DBEvent).all()
    return [Event.model_validate(event) for event in events]


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    """
    Get a specific event by ID.
    """
    db_event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event.model_validate(db_event)


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)) -> Event:
    """
    Update an existing event. Placeholder for user_id verification.
    """
    db_event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # TODO: Replace user_id with actual logged-in user verification.
    user_id = 1  # Placeholder user ID
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this event")

    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return Event.model_validate(db_event)


@router.delete("/{event_id}", response_model=Event)
def delete_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    """
    Delete an existing event. Placeholder for user_id verification.
    """
    db_event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # TODO: Replace user_id with actual logged-in user verification.
    user_id = 1  # Placeholder user ID
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this event")

    db.delete(db_event)
    db.commit()
    return Event.model_validate(db_event)
