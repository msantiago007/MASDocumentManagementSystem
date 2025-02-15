"""
FastAPI Application Entry Point

This module initializes and configures the FastAPI application, including:
- CORS middleware setup
- API router integration
- Global exception handling
- Logging configuration
- Root endpoint definition

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.api import api_router

# Initialize logger
logger = setup_logging()

# Create FastAPI application instance with configuration
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router with version prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

# Global exception handler to catch and log all unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

# Root endpoint for basic API information
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Document Management System API",
        "version": settings.VERSION
    }