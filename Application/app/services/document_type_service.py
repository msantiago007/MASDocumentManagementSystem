from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app import models
from app.schemas.schemas import DocumentTypeCreate, DocumentTypeUpdate

def create_document_type(db: Session, document_type: DocumentTypeCreate):
    """Create a new document type"""
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
    """Retrieve all active document types with pagination"""
    return db.query(models.DocumentType).filter(
        models.DocumentType.IsActive == True
    ).offset(skip).limit(limit).all()

def get_document_type(db: Session, type_id: int):
    """Retrieve a specific document type by ID"""
    return db.query(models.DocumentType).filter(
        models.DocumentType.DocumentTypeId == type_id,
        models.DocumentType.IsActive == True
    ).first()

def update_document_type(db: Session, type_id: int, document_type: DocumentTypeUpdate):
    """Update a document type"""
    db_type = get_document_type(db, type_id)
    if not db_type:
        return None
        
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
    """Deactivate a document type (soft delete)"""
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