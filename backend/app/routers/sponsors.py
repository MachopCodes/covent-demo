from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import DBSponsor  # SQLAlchemy model
from app.schemas import Sponsor, SponsorCreate, SponsorUpdate  # Pydantic schemas
from app.database import get_db

router = APIRouter(
    prefix="/sponsors",
    tags=["Sponsors"]
)


@router.post("/", response_model=Sponsor)
def create_sponsor(sponsor: SponsorCreate, db: Session = Depends(get_db)) -> Sponsor:
    """
    Create a new sponsor and save it to the database.
    """
    db_item = DBSponsor(**sponsor.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return Sponsor.model_validate(db_item)


@router.get("/", response_model=list[Sponsor])
def list_sponsors(db: Session = Depends(get_db)) -> list[Sponsor]:
    """
    Retrieve a list of all sponsors.
    """
    db_items = db.query(DBSponsor).all()
    return [Sponsor.model_validate(db_item) for db_item in db_items]


@router.get("/{sponsor_id}", response_model=Sponsor)
def read_sponsor(sponsor_id: int, db: Session = Depends(get_db)) -> Sponsor:
    """
    Retrieve details of a specific sponsor by ID.
    """
    db_item = db.query(DBSponsor).filter(DBSponsor.id == sponsor_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    return Sponsor.model_validate(db_item)


@router.put("/{sponsor_id}", response_model=Sponsor)
def update_sponsor(sponsor_id: int, sponsor: SponsorUpdate, db: Session = Depends(get_db)) -> Sponsor:
    """
    Update an existing sponsor's details.
    """
    db_item = db.query(DBSponsor).filter(DBSponsor.id == sponsor_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    for key, value in sponsor.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return Sponsor.model_validate(db_item)


@router.delete("/{sponsor_id}", response_model=Sponsor)
def delete_sponsor(sponsor_id: int, db: Session = Depends(get_db)) -> Sponsor:
    """
    Delete a sponsor from the database.
    """
    db_item = db.query(DBSponsor).filter(DBSponsor.id == sponsor_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    db.delete(db_item)
    db.commit()
    return Sponsor.model_validate(db_item)
