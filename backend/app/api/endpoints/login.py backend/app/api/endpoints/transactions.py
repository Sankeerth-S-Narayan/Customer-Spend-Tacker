from fastapi import APIRouter
from typing import List
from backend.schemas import Token, Transaction

router = APIRouter()

@router.post("/", response_model=Token)
def login(username: str, password: str):
    # Implementation of login logic
    pass

@router.get("/", response_model=List[Transaction])
def get_transactions():
    # Implementation of getting transactions
    pass 