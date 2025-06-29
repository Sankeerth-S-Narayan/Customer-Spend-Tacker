from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve transactions for the current user.
    """
    transactions = crud.transaction.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return transactions

@router.get("/metrics", response_model=dict)
def read_metrics(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve analytics metrics for the current user.
    """
    metrics = crud.transaction.get_metrics_by_owner(db=db, owner_id=current_user.id)
    return metrics 