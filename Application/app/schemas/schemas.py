from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

# Base Schemas - Used for common attributes
class UserBase(BaseModel):
    Username: str
    Email: EmailStr
    IsActive: bool = True

class DocumentTypeBase(BaseModel):
    TypeName: str
    Description: Optional[str] = None
    SchemaDefinition: Optional[str] = None
    IsActive: bool = True

class DocumentBase(BaseModel):
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

# Create Schemas - Used when creating new items
class UserCreate(UserBase):
    Password: str

class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentCreate(DocumentBase):
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

# Response Schemas - Used for API responses
class User(UserBase):
    UserId: int
    CreatedDate: datetime
    LastLoginDate: Optional[datetime] = None

    class Config:
        from_attributes = True

class DocumentType(DocumentTypeBase):
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

# Update Schemas - Used when updating existing items
class UserUpdate(BaseModel):
    Username: Optional[str] = None
    Email: Optional[EmailStr] = None
    Password: Optional[str] = None
    IsActive: Optional[bool] = None

class DocumentTypeUpdate(BaseModel):
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