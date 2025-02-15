"""
Document Type Service Layer

This module handles document type management business logic, including:
- Document type creation and validation
- Type retrieval and listing
- Type updates and modifications
- Soft deletion functionality
- Error handling and database transactions

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app import models
from app.schemas.schemas import DocumentTypeCreate, DocumentTypeUpdate

def create_document_type(db: Session, document_type: DocumentTypeCreate):
    """
    Create a new document type
    
    Args:
        db: Database session
        document_type: Document type creation data
    
    Returns:
        models.DocumentType: Created document type instance
    
    Raises:
        HTTPException: If creation fails due to validation or DB constraints
    """
    db_type = models.DocumentType(
        TypeName=document_type.TypeName,
        Description=document_type.Description,
        SchemaDefinition=document_type.SchemaDefinition,
        IsActive=True,
        CreatedDate=datetime.utcnow(),
        LastModifiedDate=datetime.utcnow()
    )
    try:
        db.add(db_type)
        db.commit()
        db.refresh(db_type)
        return db_type
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_document_types(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all active document types with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List[models.DocumentType]: List of active document type instances
    """
    return db.query(models.DocumentType).filter(
        models.DocumentType.IsActive == True
    ).offset(skip).limit(limit).all()

def get_document_type(db: Session, type_id: int):
    """
    Retrieve a specific document type by ID
    
    Args:
        db: Database session
        type_id: ID of document type to retrieve
    
    Returns:
        models.DocumentType: Document type instance if found, None otherwise
    """
    return db.query(models.DocumentType).filter(
        models.DocumentType.DocumentTypeId == type_id,
        models.DocumentType.IsActive == True
    ).first()

def update_document_type(db: Session, type_id: int, document_type: DocumentTypeUpdate):
    """
    Update a document type's attributes
    
    Args:
        db: Database session
        type_id: ID of document type to update
        document_type: Updated document type information
    
    Returns:
        models.DocumentType: Updated document type instance if found, None otherwise
    
    Raises:
        HTTPException: If update fails due to validation or DB constraints
    """
    db_type = get_document_type(db, type_id)
    if not db_type:
        return None
        
    # Update only provided fields
    for field, value in document_type.dict(exclude_unset=True).items():
        setattr(db_type, field, value)
    
    db_type.LastModifiedDate = datetime.utcnow()
    
    try:
        db.commit()
        db.refresh(db_type)
        return db_type
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_document_type(db: Session, type_id: int) -> bool:
    """
    Deactivate a document type (soft delete)
    
    Args:
        db: Database session
        type_id: ID of document type to deactivate
    
    Returns:
        bool: True if document type was deactivated, False if not found or operation failed
    """
    db_type = get_document_type(db, type_id)
    if not db_type:
        return False
        
    db_type.IsActive = False
    db_type.LastModifiedDate = datetime.utcnow()
    
    try:
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False