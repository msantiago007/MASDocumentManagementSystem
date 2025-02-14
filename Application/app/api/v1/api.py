"""
Main API Router Configuration

This module configures the main API router and includes all sub-routers
for different resource endpoints (documents, users, document types).

Author: Marco Alejandro Santiago
Created: February 14, 2025
"""

from fastapi import APIRouter
from app.api.v1 import documents, users, document_types

# Initialize main API router
api_router = APIRouter()

# Include sub-routers with their respective prefixes and tags
api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["documents"]
)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)
api_router.include_router(
    document_types.router,
    prefix="/document-types",
    tags=["document-types"]
)