"""
Users API Router

This module handles all user-related API endpoints, including user creation,
retrieval, updating, and deletion operations.

Author: Marco Alejandro Santiago
Created: February 14, 2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.schemas import UserCreate, User, UserUpdate
from app.services import user_service

# Initialize router
router = APIRouter()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user endpoint
    
    Args:
        user: UserCreate schema containing user creation data
        db: Database session dependency
    
    Returns:
        Created user object
    """
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all users with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session dependency
    
    Returns:
        List of user objects
    """
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID
    
    Args:
        user_id: User's unique identifier
        db: Database session dependency
    
    Returns:
        User object if found
    
    Raises:
        HTTPException: If user is not found
    """
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a user's information
    
    Args:
        user_id: User's unique identifier
        user: UserUpdate schema containing update data
        db: Database session dependency
    
    Returns:
        Updated user object
    
    Raises:
        HTTPException: If user is not found
    """
    db_user = user_service.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deactivate a user (soft delete)
    
    Args:
        user_id: User's unique identifier
        db: Database session dependency
    
    Returns:
        Success message
    
    Raises:
        HTTPException: If user is not found
    """
    success = user_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": "success",
        "message": "User deactivated successfully"
    }