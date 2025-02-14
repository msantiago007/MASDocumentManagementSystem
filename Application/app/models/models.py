from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    UserId = Column(Integer, primary_key=True)
    Username = Column(String(100), unique=True, nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    IsActive = Column(Boolean, default=True)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    LastLoginDate = Column(DateTime, nullable=True)

class DocumentType(Base):
    __tablename__ = "DocumentTypes"
    __table_args__ = {"schema": "dbo"}

    DocumentTypeId = Column(Integer, primary_key=True)
    TypeName = Column(String(100), nullable=False)
    Description = Column(String(500))
    SchemaDefinition = Column(Text)
    IsActive = Column(Boolean, default=True)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    LastModifiedDate = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = "Documents"
    __table_args__ = {"schema": "dbo"}

    DocumentId = Column(Integer, primary_key=True)
    DocumentName = Column(String(255), nullable=False)
    FileLocation = Column(String(1000), nullable=False)
    FileType = Column(String(50), nullable=False)
    FileSizeBytes = Column(Integer, nullable=False)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    CreatedById = Column(Integer, ForeignKey("dbo.Users.UserId"))
    LastModifiedDate = Column(DateTime, default=datetime.utcnow)
    LastModifiedById = Column(Integer, ForeignKey("dbo.Users.UserId"))
    IsDeleted = Column(Boolean, default=False)
    ContentHash = Column(String(255), nullable=False)
    DocumentTypeId = Column(Integer, ForeignKey("dbo.DocumentTypes.DocumentTypeId"))

    created_by = relationship("User", foreign_keys=[CreatedById])
    modified_by = relationship("User", foreign_keys=[LastModifiedById])
    document_type = relationship("DocumentType")
    versions = relationship("DocumentVersion", back_populates="document")
    metadata = relationship("DocumentMetadata", back_populates="document")

class DocumentVersion(Base):
    __tablename__ = "DocumentVersions"
    __table_args__ = {"schema": "dbo"}

    VersionId = Column(Integer, primary_key=True)
    DocumentId = Column(Integer, ForeignKey("dbo.Documents.DocumentId"))
    VersionNumber = Column(Integer, nullable=False)
    FileLocation = Column(String(1000), nullable=False)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    CreatedById = Column(Integer, ForeignKey("dbo.Users.UserId"))
    ContentHash = Column(String(255), nullable=False)

    document = relationship("Document", back_populates="versions")
    created_by = relationship("User")

class DocumentMetadata(Base):
    __tablename__ = "DocumentMetadata"
    __table_args__ = {"schema": "dbo"}

    DocumentMetadataId = Column(Integer, primary_key=True)
    DocumentId = Column(Integer, ForeignKey("dbo.Documents.DocumentId"))
    MetadataKey = Column(String(100), nullable=False)
    MetadataValue = Column(Text)
    DataType = Column(String(50), nullable=False)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    LastModifiedDate = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="metadata")

class Tag(Base):
    __tablename__ = "Tags"
    __table_args__ = {"schema": "dbo"}

    TagId = Column(Integer, primary_key=True)
    TagName = Column(String(100), unique=True, nullable=False)
    Description = Column(String(500))
    IsActive = Column(Boolean, default=True)

class Topic(Base):
    __tablename__ = "Topics"
    __table_args__ = {"schema": "dbo"}

    TopicId = Column(Integer, primary_key=True)
    TopicName = Column(String(100), unique=True, nullable=False)
    Description = Column(String(500))
    IsActive = Column(Boolean, default=True)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    ParentTopicId = Column(Integer, ForeignKey("dbo.Topics.TopicId"))

    parent_topic = relationship("Topic", remote_side=[TopicId])