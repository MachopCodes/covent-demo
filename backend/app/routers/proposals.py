from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import or_
from app.models import DBProposal
from app.schemas.proposal import Proposal, ProposalCreate, ProposalUpdate
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import DBUser  # Assuming DBUser is the user model

router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"]
)

@router.post("/", response_model=Proposal)
def create_proposal(
    proposal: ProposalCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Proposal:
    """
    Create a new proposal. Requires authentication.
    """
    db_proposal = DBProposal(**proposal.model_dump(), owner_id=current_user.id)
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return Proposal.model_validate(db_proposal)


@router.get("/", response_model=List[Proposal])
def list_proposals(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> List[Proposal]:
    """
    Retrieve a list of all proposals where the current user is either the owner or the sponsor.
    """
    proposals = db.query(DBProposal).filter(
        or_(
            DBProposal.owner_id == current_user.id,
            DBProposal.sponsor_id == current_user.id
        )
    ).all()

    return [Proposal.model_validate(proposal) for proposal in proposals]


@router.get("/{proposal_id}", response_model=Proposal)
def read_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Proposal:
    """
    Retrieve details of a specific proposal by ID where the current user is either the owner or the sponsor.
    """
    db_proposal = db.query(DBProposal).filter(
        DBProposal.id == proposal_id,
        or_(
            DBProposal.owner_id == current_user.id,
            DBProposal.sponsor_id == current_user.id
        )
    ).first()

    if not db_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    return Proposal.model_validate(db_proposal)



@router.put("/{proposal_id}", response_model=Proposal)
def update_proposal(
    proposal_id: int,
    proposal: ProposalUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Proposal:
    """
    Update an existing proposal. Requires authentication.
    """
    db_proposal = db.query(DBProposal).filter(
        DBProposal.id == proposal_id,
    ).first()

    if not db_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    for key, value in proposal.model_dump(exclude_unset=True).items():
        setattr(db_proposal, key, value)
    db.commit()
    db.refresh(db_proposal)
    return Proposal.model_validate(db_proposal)


@router.delete("/{proposal_id}", response_model=Proposal)
def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)  # Token required
) -> Proposal:
    """
    Delete an existing proposal. Requires authentication.
    """
    db_proposal = db.query(DBProposal).filter(
        DBProposal.id == proposal_id,
        DBProposal.owner_id == current_user.id
    ).first()

    if not db_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    db.delete(db_proposal)
    db.commit()
    return Proposal.model_validate(db_proposal)
