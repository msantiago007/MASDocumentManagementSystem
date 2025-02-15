"""
User Service Layer

This module handles user management business logic, including:
- User creation and password hashing
- User authentication and validation
- User information updates
- Account deactivation
- Error handling and database transactions

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext

from app import models
from app.schemas.schemas import UserCreate, UserUpdate

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password to hash
    
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    """
    Create a new user with hashed password
    
    Args:
        db: Database session
        user: User creation data including password
    
    Returns:
        models.User: Created user instance
    
    Raises:
        HTTPException: If creation fails due to validation or DB constraints
    """
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
    """
    Retrieve all active users with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List[models.User]: List of active user instances
    """
    return db.query(models.User).filter(
        models.User.IsActive == True
    ).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    """
    Retrieve a specific user by ID
    
    Args:
        db: Database session
        user_id: ID of user to retrieve
    
    Returns:
        models.User: User instance if found, None otherwise
    """
    return db.query(models.User).filter(
        models.User.UserId == user_id,
        models.User.IsActive == True
    ).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    """
    Update a user's information including password if provided
    
    Args:
        db: Database session
        user_id: ID of user to update
        user: Updated user information
    
    Returns:
        models.User: Updated user instance if found, None otherwise
    
    Raises:
        HTTPException: If update fails due to validation or DB constraints
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
        
    # Handle password hashing if included in update
    user_data = user.dict(exclude_unset=True)
    if "Password" in user_data:
        user_data["PasswordHash"] = get_password_hash(user_data.pop("Password"))
    
    # Update user attributes
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
    """
    Deactivate a user account (soft delete)
    
    Args:
        db: Database session
        user_id: ID of user to deactivate
    
    Returns:
        bool: True if user was deactivated, False if not found or operation failed
    """
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