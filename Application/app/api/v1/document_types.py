"""
Document Types API Router

This module handles all document type-related API endpoints, including creation,
retrieval, updating, and deletion of document type definitions.

Author: Marco Alejandro Santiago
Created: February 14, 2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.schemas import DocumentTypeCreate, DocumentType, DocumentTypeUpdate
from app.services import document_type_service

# Initialize router
router = APIRouter()

@router.post("/", response_model=DocumentType)
def create_document_type(
    document_type: DocumentTypeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new document type
    
    Args:
        document_type: DocumentTypeCreate schema with type details
        db: Database session dependency
    
    Returns:
        Created document type object
    """
    return document_type_service.create_document_type(
        db=db,
        document_type=document_type
    )

@router.get("/", response_model=List[DocumentType])
def get_document_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all document types with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session dependency
    
    Returns:
        List of document type objects
    """
    return document_type_service.get_document_types(db, skip=skip, limit=limit)

@router.get("/{type_id}", response_model=DocumentType)
def get_document_type(type_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific document type by ID
    
    Args:
        type_id: Document type's unique identifier
        db: Database session dependency
    
    Returns:
        Document type object if found
    
    Raises:
        HTTPException: If document type is not found
    """
    db_type = document_type_service.get_document_type(db, type_id=type_id)
    if db_type is None:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )
    return db_type

@router.put("/{type_id}", response_model=DocumentType)
def update_document_type(
    type_id: int,
    document_type: DocumentTypeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a document type
    
    Args:
        type_id: Document type's unique identifier
        document_type: DocumentTypeUpdate schema with update data
        db: Database session dependency
    
    Returns:
        Updated document type object
    
    Raises:
        HTTPException: If document type is not found
    """
    db_type = document_type_service.update_document_type(
        db,
        type_id=type_id,
        document_type=document_type
    )
    if db_type is None:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )
    return db_type

@router.delete("/{type_id}")
def delete_document_type(type_id: int, db: Session = Depends(get_db)):
    """
    Deactivate a document type
    
    Args:
        type_id: Document type's unique identifier
        db: Database session dependency
    
    Returns:
        Success message
    
    Raises:
        HTTPException: If document type is not found
    """
    success = document_type_service.delete_document_type(db, type_id=type_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )
    return {
        "status": "success",
        "message": "Document type deactivated successfully"
    }