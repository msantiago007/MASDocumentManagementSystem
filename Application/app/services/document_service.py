"""
Document Service Layer

This module handles document management business logic, including:
- File upload and storage
- Document creation and metadata management
- Document retrieval and updates
- Soft deletion functionality
- Content hash verification

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import hashlib
import os
from datetime import datetime

from app.schemas.schemas import DocumentCreate, DocumentUpdate
from app import models
from app.core.config import settings

async def create_document(db: Session, document: DocumentCreate, file: UploadFile):
    """
    Create a new document with file upload
    
    Args:
        db: Database session
        document: Document metadata and type information
        file: Uploaded file object
    
    Returns:
        models.Document: Created document instance
    
    Raises:
        HTTPException: If file saving fails
    """
    # Create storage directory if it doesn't exist
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)
    
    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    storage_filename = f"{timestamp}{file_extension}"
    file_path = settings.STORAGE_DIR / storage_filename
    
    # Save file to storage directory
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Calculate SHA-256 hash for file integrity
    content_hash = hashlib.sha256(content).hexdigest()
    
    # Create document record in database
    db_document = models.Document(
        DocumentName=document.DocumentName,
        FileLocation=str(file_path),
        FileType=document.FileType,
        FileSizeBytes=len(content),
        ContentHash=content_hash,
        DocumentTypeId=document.DocumentTypeId,
        CreatedById=1,  # TODO: Replace with actual user ID from auth
        LastModifiedById=1  # TODO: Replace with actual user ID from auth
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all non-deleted documents with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List[models.Document]: List of document instances
    """
    return db.query(models.Document).filter(
        models.Document.IsDeleted == False
    ).offset(skip).limit(limit).all()

def get_document(db: Session, document_id: int):
    """
    Retrieve a specific non-deleted document by ID
    
    Args:
        db: Database session
        document_id: ID of document to retrieve
    
    Returns:
        models.Document: Document instance if found, None otherwise
    """
    return db.query(models.Document).filter(
        models.Document.DocumentId == document_id,
        models.Document.IsDeleted == False
    ).first()

def update_document(db: Session, document_id: int, document: DocumentUpdate):
    """
    Update a document's metadata
    
    Args:
        db: Database session
        document_id: ID of document to update
        document: Updated document information
    
    Returns:
        models.Document: Updated document instance if found, None otherwise
    """
    db_document = get_document(db, document_id)
    if not db_document:
        return None
        
    # Update only provided fields
    for field, value in document.dict(exclude_unset=True).items():
        setattr(db_document, field, value)
    
    db_document.LastModifiedDate = datetime.utcnow()
    db_document.LastModifiedById = 1  # TODO: Replace with actual user ID from auth
    
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int) -> bool:
    """
    Soft delete a document
    
    Args:
        db: Database session
        document_id: ID of document to delete
    
    Returns:
        bool: True if document was deleted, False if not found
    """
    db_document = get_document(db, document_id)
    if not db_document:
        return False
        
    db_document.IsDeleted = True
    db_document.LastModifiedDate = datetime.utcnow()
    db_document.LastModifiedById = 1  # TODO: Replace with actual user ID from auth
    
    db.commit()
    return True