"""
Documents API Router

This module handles all document-related API endpoints, including document creation,
retrieval, updating, and deletion operations. It also handles file uploads and
document metadata management.

Author: Marco Alejandro Santiago
Created: February 14, 2025
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app import schemas, models
from app.services import document_service

# Initialize router
router = APIRouter()

@router.get("/", response_model=List[schemas.Document])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all documents with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session dependency
    
    Returns:
        List of document objects
    """
    return document_service.get_documents(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Document)
async def create_document(
    document: schemas.DocumentCreate,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Create a new document with file upload
    
    Args:
        document: DocumentCreate schema containing metadata
        file: Uploaded file object
        db: Database session dependency
    
    Returns:
        Created document object
    """
    return await document_service.create_document(db, document, file)

@router.get("/{document_id}", response_model=schemas.Document)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific document by ID
    
    Args:
        document_id: Document's unique identifier
        db: Database session dependency
    
    Returns:
        Document object if found
    
    Raises:
        HTTPException: If document is not found
    """
    document = document_service.get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=schemas.Document)
async def update_document(
    document_id: int,
    document: schemas.DocumentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a document's metadata
    
    Args:
        document_id: Document's unique identifier
        document: DocumentUpdate schema containing update data
        db: Database session dependency
    
    Returns:
        Updated document object
    
    Raises:
        HTTPException: If document is not found
    """
    updated_document = document_service.update_document(db, document_id, document)
    if updated_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return updated_document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a document (soft delete)
    
    Args:
        document_id: Document's unique identifier
        db: Database session dependency
    
    Returns:
        Success message
    
    Raises:
        HTTPException: If document is not found
    """
    success = document_service.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "message": "Document deleted successfully"}