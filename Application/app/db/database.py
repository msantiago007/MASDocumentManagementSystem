"""
Database Configuration and Session Management

This module configures the SQLAlchemy database connection and session handling, including:
- Database engine creation
- Session factory setup
- Base model class definition
- Database dependency injection

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create database engine with debugging enabled
engine = create_engine(settings.DATABASE_URL, echo=True)

# Configure session factory for database operations
# - autocommit=False: Transactions must be explicitly committed
# - autoflush=False: Changes won't be automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to handle database session lifecycle.
    
    Yields:
        Session: Database session that will be automatically closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()