"""
Pydantic Schema Definitions

This module defines Pydantic models for request/response validation, including:
- Base schemas for common attributes
- Create schemas for new resource creation
- Response schemas for API outputs
- Update schemas for resource modifications
- Data validation and type checking

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

# Base Schemas - Define core attributes for each resource type
class UserBase(BaseModel):
    """Base user attributes for validation"""
    Username: str
    Email: EmailStr
    IsActive: bool = True

class DocumentTypeBase(BaseModel):
    """Base document type configuration"""
    TypeName: str
    Description: Optional[str] = None
    SchemaDefinition: Optional[str] = None
    IsActive: bool = True

class DocumentBase(BaseModel):
    """Core document attributes"""
    DocumentName: str
    FileType: str
    DocumentTypeId: Optional[int] = None

class DocumentVersionBase(BaseModel):
    VersionNumber: int
    DocumentId: int

class DocumentMetadataBase(BaseModel):
    DocumentId: int
    MetadataKey: str
    MetadataValue: Optional[str] = None
    DataType: str

class TagBase(BaseModel):
    TagName: str
    Description: Optional[str] = None
    IsActive: bool = True

class TopicBase(BaseModel):
    TopicName: str
    Description: Optional[str] = None
    ParentTopicId: Optional[int] = None
    IsActive: bool = True

# Create Schemas - Used for validating new resource creation requests
class UserCreate(UserBase):
    """Extends UserBase to include password for user creation"""
    Password: str

class DocumentTypeCreate(DocumentTypeBase):
    """Document type creation schema - uses base attributes"""
    pass

class DocumentCreate(DocumentBase):
    """Document creation with additional required fields"""
    FileSizeBytes: int
    ContentHash: str

class DocumentVersionCreate(DocumentVersionBase):
    FileLocation: str
    ContentHash: str

class DocumentMetadataCreate(DocumentMetadataBase):
    pass

class TagCreate(TagBase):
    pass

class TopicCreate(TopicBase):
    pass

# Response Schemas - Define API response structures
class User(UserBase):
    """Complete user representation including system-generated fields"""
    UserId: int
    CreatedDate: datetime
    LastLoginDate: Optional[datetime] = None

    class Config:
        from_attributes = True

class DocumentType(DocumentTypeBase):
    """Complete document type representation with timestamps"""
    DocumentTypeId: int
    CreatedDate: datetime
    LastModifiedDate: datetime

    class Config:
        from_attributes = True

class Document(DocumentBase):
    DocumentId: int
    FileLocation: str
    FileSizeBytes: int
    CreatedDate: datetime
    CreatedById: int
    LastModifiedDate: datetime
    LastModifiedById: int
    IsDeleted: bool
    ContentHash: str
    versions: List['DocumentVersion'] = []
    metadata: List['DocumentMetadata'] = []

    class Config:
        from_attributes = True

class DocumentVersion(DocumentVersionBase):
    VersionId: int
    FileLocation: str
    CreatedDate: datetime
    CreatedById: int
    ContentHash: str

    class Config:
        from_attributes = True

class DocumentMetadata(DocumentMetadataBase):
    DocumentMetadataId: int
    CreatedDate: datetime
    LastModifiedDate: datetime

    class Config:
        from_attributes = True

class Tag(TagBase):
    TagId: int

    class Config:
        from_attributes = True

class Topic(TopicBase):
    TopicId: int
    CreatedDate: datetime
    child_topics: List['Topic'] = []

    class Config:
        from_attributes = True

# Update Schemas - Define allowed fields for resource updates
class UserUpdate(BaseModel):
    """Optional fields that can be updated for a user"""
    Username: Optional[str] = None
    Email: Optional[EmailStr] = None
    Password: Optional[str] = None
    IsActive: Optional[bool] = None

class DocumentTypeUpdate(BaseModel):
    """Optional fields that can be updated for a document type"""
    TypeName: Optional[str] = None
    Description: Optional[str] = None
    SchemaDefinition: Optional[str] = None
    IsActive: Optional[bool] = None

class DocumentUpdate(BaseModel):
    DocumentName: Optional[str] = None
    DocumentTypeId: Optional[int] = None
    IsDeleted: Optional[bool] = None

class DocumentMetadataUpdate(BaseModel):
    MetadataValue: Optional[str] = None
    DataType: Optional[str] = None

class TagUpdate(BaseModel):
    TagName: Optional[str] = None
    Description: Optional[str] = None
    IsActive: Optional[bool] = None

class TopicUpdate(BaseModel):
    TopicName: Optional[str] = None
    Description: Optional[str] = None
    ParentTopicId: Optional[int] = None
    IsActive: Optional[bool] = None