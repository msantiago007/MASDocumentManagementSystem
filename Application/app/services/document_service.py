from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import hashlib
import os
from datetime import datetime

from app.schemas.schemas import DocumentCreate, DocumentUpdate
from app import models
from app.core.config import settings

async def create_document(db: Session, document: DocumentCreate, file: UploadFile):
    """Create a new document with file upload"""
    # Create storage directory if it doesn't exist
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    storage_filename = f"{timestamp}{file_extension}"
    file_path = settings.STORAGE_DIR / storage_filename
    
    # Save file
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Calculate content hash
    content_hash = hashlib.sha256(content).hexdigest()
    
    # Create document record
    db_document = models.Document(
        DocumentName=document.DocumentName,
        FileLocation=str(file_path),
        FileType=document.FileType,
        FileSizeBytes=len(content),
        ContentHash=content_hash,
        DocumentTypeId=document.DocumentTypeId,
        CreatedById=1,  # TODO: Replace with actual user ID
        LastModifiedById=1  # TODO: Replace with actual user ID
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all documents with pagination"""
    return db.query(models.Document).filter(
        models.Document.IsDeleted == False
    ).offset(skip).limit(limit).all()

def get_document(db: Session, document_id: int):
    """Retrieve a specific document by ID"""
    return db.query(models.Document).filter(
        models.Document.DocumentId == document_id,
        models.Document.IsDeleted == False
    ).first()

def update_document(db: Session, document_id: int, document: DocumentUpdate):
    """Update a document's metadata"""
    db_document = get_document(db, document_id)
    if not db_document:
        return None
        
    # Update fields if provided
    for field, value in document.dict(exclude_unset=True).items():
        setattr(db_document, field, value)
    
    db_document.LastModifiedDate = datetime.utcnow()
    db_document.LastModifiedById = 1  # TODO: Replace with actual user ID
    
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int) -> bool:
    """Soft delete a document"""
    db_document = get_document(db, document_id)
    if not db_document:
        return False
        
    db_document.IsDeleted = True
    db_document.LastModifiedDate = datetime.utcnow()
    db_document.LastModifiedById = 1  # TODO: Replace with actual user ID
    
    db.commit()
    return True