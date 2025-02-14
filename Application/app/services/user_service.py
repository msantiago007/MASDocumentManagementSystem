from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext

from app import models
from app.schemas.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    """Create a new user"""
    hashed_password = get_password_hash(user.Password)
    db_user = models.User(
        Username=user.Username,
        Email=user.Email,
        PasswordHash=hashed_password,
        IsActive=True
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all active users with pagination"""
    return db.query(models.User).filter(
        models.User.IsActive == True
    ).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    """Retrieve a specific user by ID"""
    return db.query(models.User).filter(
        models.User.UserId == user_id,
        models.User.IsActive == True
    ).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    """Update a user's information"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
        
    user_data = user.dict(exclude_unset=True)
    if "Password" in user_data:
        user_data["PasswordHash"] = get_password_hash(user_data.pop("Password"))
    
    for field, value in user_data.items():
        setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_user(db: Session, user_id: int) -> bool:
    """Deactivate a user (soft delete)"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
        
    db_user.IsActive = False
    
    try:
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False