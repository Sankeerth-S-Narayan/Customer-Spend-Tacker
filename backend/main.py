import os
from datetime import datetime, timedelta
from typing import Any, List, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy import (create_engine, Column, Integer, String, Float,
                        DateTime, ForeignKey, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import case
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# ===============================================================================
# 1. SETTINGS AND CONFIGURATION
# ===============================================================================

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

# ===============================================================================
# 2. DATABASE SETUP
# ===============================================================================

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ===============================================================================
# 3. SQLALCHEMY ORM MODELS
# ===============================================================================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String)
    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    owner = relationship("User", back_populates="transactions")

# ===============================================================================
# 4. Pydantic Schemas (Data Validation)
# ===============================================================================

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionSchema(TransactionBase):
    id: int
    user_id: int
    transaction_date: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    transactions: List[TransactionSchema] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# ===============================================================================
# 5. SECURITY & AUTHENTICATION
# ===============================================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# ===============================================================================
# 6. CRUD (Create, Read, Update, Delete) Functions
# ===============================================================================

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_transactions_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100, 
                             start_date: str = None, end_date: str = None, categories: List[str] = None):
    query = db.query(Transaction).filter(Transaction.user_id == owner_id)
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    # Apply category filters if provided
    if categories and len(categories) > 0:
        query = query.filter(Transaction.category.in_(categories))
    
    return query.offset(skip).limit(limit).all()

def get_metrics_by_owner(db: Session, owner_id: int, start_date: str = None, end_date: str = None, categories: List[str] = None):
    query = db.query(Transaction).filter(Transaction.user_id == owner_id)
    
    # Apply same filters as transactions
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    if categories and len(categories) > 0:
        query = query.filter(Transaction.category.in_(categories))
    
    total_spent = query.with_entities(func.sum(Transaction.amount)).scalar() or 0.0
    average_transaction = query.with_entities(func.avg(Transaction.amount)).scalar() or 0.0
    
    spending_by_category = query.group_by(Transaction.category).with_entities(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).all()

    return {
        "total_spent": total_spent,
        "average_transaction": average_transaction,
        "spending_by_category": {cat: total for cat, total in spending_by_category}
    }

# ===============================================================================
# 7. FASTAPI APP AND DEPENDENCIES
# ===============================================================================

app = FastAPI(title="Analytics Dashboard API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# ===============================================================================
# 8. API ENDPOINTS
# ===============================================================================

@app.post("/api/v1/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    
    if not user or form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/users/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/v1/transactions", response_model=List[TransactionSchema])
def read_transactions(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 100,
    start_date: str = None,
    end_date: str = None,
    categories: str = None  # Comma-separated string of categories
):
    # Parse categories from comma-separated string
    category_list = None
    if categories:
        category_list = [cat.strip() for cat in categories.split(',') if cat.strip()]
    
    transactions = get_transactions_by_owner(
        db=db, 
        owner_id=current_user.id, 
        skip=skip, 
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        categories=category_list
    )
    return transactions

@app.get("/api/v1/transactions/metrics", response_model=dict)
def read_user_metrics(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    categories: str = None  # Comma-separated string of categories
):
    # Parse categories from comma-separated string
    category_list = None
    if categories:
        category_list = [cat.strip() for cat in categories.split(',') if cat.strip()]
    
    return get_metrics_by_owner(
        db=db, 
        owner_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        categories=category_list
    )

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}