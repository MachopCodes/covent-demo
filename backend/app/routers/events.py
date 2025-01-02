from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import DBEvent
from app.schemas.event import Event, EventCreate, EventUpdate
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import DBUser  # Assuming DBUser is the user model

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("/", response_model=Event)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Event:
    """
    Create a new event and associate it with the current user.
    """
    db_event = DBEvent(**event.model_dump(), user_id=current_user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return Event.model_validate(db_event)

@router.get("/mine", response_model=List[Event])
def list_events(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> List[Event]:
    """
    Retrieve a list of all events. Requires authentication.
    """
    events = db.query(DBEvent).filter(DBEvent.user_id == current_user.id).all()
    return [Event.model_validate(event) for event in events]

@router.get("/", response_model=List[Event])
def list_events(
    db: Session = Depends(get_db),
) -> List[Event]:
    """
    Retrieve a list of all events.
    """
    events = db.query(DBEvent).all()
    return [Event.model_validate(event) for event in events]



@router.get("/{event_id}", response_model=Event)
def read_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Event:
    """
    Retrieve details of a specific event by ID. Requires authentication.
    """
    db_event = db.query(DBEvent).filter(
        DBEvent.id == event_id,
    ).first()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    return Event.model_validate(db_event)


@router.put("/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Event:
    """
    Update an existing event. Only the event owner can update it. Requires authentication.
    """
    db_event = db.query(DBEvent).filter(
        DBEvent.id == event_id,
        DBEvent.user_id == current_user.id
    ).first()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return Event.model_validate(db_event)


@router.delete("/{event_id}", response_model=Event)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Event:
    """
    Delete an existing event. Only the event owner can delete it. Requires authentication.
    """
    db_event = db.query(DBEvent).filter(
        DBEvent.id == event_id,
        DBEvent.user_id == current_user.id
    ).first()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(db_event)
    db.commit()
    return Event.model_validate(db_event)
