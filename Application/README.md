# Document Management System

## Overview
A sophisticated document management system built with FastAPI that provides automated document classification, processing, and storage capabilities. The system supports various document formats, implements user authentication, and offers a RESTful API interface for document operations.

## System Requirements

### Minimum Hardware Requirements
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB available space

### Software Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Tesseract OCR engine
- Required OS: Windows 10/11, Ubuntu 20.04+, or macOS 10.15+

### Required Python Packages
Key dependencies include:
- FastAPI
- SQLAlchemy
- PyTesseract
- python-docx
- PyPDF2
- Pillow
- scikit-learn
(Full list available in requirements.txt)

## Installation Guide

### 1. Python Setup
# Check Python version
python --version  # Should be 3.8 or higher

# If Python needs to be installed:
# For Ubuntu
sudo apt update
sudo apt install python3.8 python3.8-venv python3-pip

# For Windows
# Download Python installer from python.org and run with admin privileges

### 2. PostgreSQL Installation
# For Ubuntu
sudo apt install postgresql postgresql-contrib

# For Windows
# Download and run PostgreSQL installer from postgresql.org

### 3. Tesseract OCR Installation
# For Ubuntu
sudo apt install tesseract-ocr

# For Windows
# Download and install from github.com/UB-Mannheim/tesseract/wiki

### 4. Project Setup

1. Clone the repository:
git clone [repository-url]
cd DocumentManagement

2. Create and activate virtual environment:
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows
venv\Scripts\activate

# For Unix/MacOS
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Create environment file:
# Create .env file in project root
touch .env

# Add the following configurations:
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TESSERACT_PATH=/path/to/tesseract  # Windows example: C:\Program Files\Tesseract-OCR\tesseract.exe

5. Initialize database:
# Create database
psql -U postgres
CREATE DATABASE db_name;
\q

# Run migrations (if using Alembic)
alembic upgrade head

6. Verify installation:
# Run driver verification
python check_drivers.py

## Project Structure
DocumentManagement/
+-- app/
¦   +-- api/
¦   ¦   +-- v1/
¦   ¦       +-- api.py          # API router configuration
¦   ¦       +-- documents.py    # Document endpoints
¦   ¦       +-- document_types.py # Document type endpoints
¦   ¦       +-- users.py        # User management endpoints
¦   +-- core/
¦   ¦   +-- config.py          # Application settings
¦   +-- db/
¦   ¦   +-- database.py        # Database configuration
¦   +-- models/
¦   ¦   +-- models.py          # Database models
¦   +-- schemas/
¦   ¦   +-- schemas.py         # Data validation schemas
¦   +-- services/
¦   ¦   +-- document_service.py      # Document processing
¦   ¦   +-- document_type_service.py # Type management
¦   ¦   +-- user_service.py          # User operations
¦   +-- main.py                # Application entry point
+-- check_drivers.py           # Installation verification
+-- requirements.txt           # Dependencies
+-- Starting the application.txt # Startup guide

## Running the Application

1. Ensure virtual environment is activated:
# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate

2. Start the application:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

3. Verify the application is running:
- Access API documentation: http://localhost:8000/docs
- Access alternative API documentation: http://localhost:8000/redoc

## API Documentation

### Authentication
- POST `/api/v1/users/login`: User authentication
- POST `/api/v1/users/register`: User registration

### Documents
- POST `/api/v1/documents/`: Upload new document
- GET `/api/v1/documents/`: List documents
- GET `/api/v1/documents/{id}`: Get document details
- PUT `/api/v1/documents/{id}`: Update document
- DELETE `/api/v1/documents/{id}`: Delete document

### Document Types
- POST `/api/v1/document-types/`: Create document type
- GET `/api/v1/document-types/`: List document types
- GET `/api/v1/document-types/{id}`: Get type details
- PUT `/api/v1/document-types/{id}`: Update type
- DELETE `/api/v1/document-types/{id}`: Delete type

## Troubleshooting

### Common Installation Issues

1. Database Connection Errors
# Check PostgreSQL service status
# Windows
services.msc  # Look for PostgreSQL service

# Linux
sudo systemctl status postgresql

2. Tesseract OCR Issues
# Verify Tesseract installation
tesseract --version

# Check Tesseract path in .env file
TESSERACT_PATH=/path/to/tesseract

3. Python Package Conflicts
# Clean installation
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

### Error Logging
- Application logs are stored in `logs/app.log`
- Database logs are in PostgreSQL's default logging location

## License

N/A

## Contact Info
Marco Alejandro Santiago
msantiago@excelendeavormedia.com