-- 02_CreateTables.sql
USE DocumentManagement;
GO

-- Create base tables without foreign key constraints
CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    Username VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    LastLoginDate DATETIME NULL
);

CREATE TABLE DocumentTypes (
    DocumentTypeId INT IDENTITY(1,1) PRIMARY KEY,
    TypeName VARCHAR(100) NOT NULL,
    Description VARCHAR(500) NULL,
    SchemaDefinition NVARCHAR(MAX) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    LastModifiedDate DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE Documents (
    DocumentId INT IDENTITY(1,1) PRIMARY KEY,
    DocumentName VARCHAR(255) NOT NULL,
    FileLocation VARCHAR(1000) NOT NULL,
    FileType VARCHAR(50) NOT NULL,
    FileSizeBytes BIGINT NOT NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedById INT NOT NULL,
    LastModifiedDate DATETIME NOT NULL DEFAULT GETDATE(),
    LastModifiedById INT NOT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    ContentHash VARCHAR(255) NOT NULL,
    DocumentTypeId INT NULL
);

CREATE TABLE DocumentVersions (
    VersionId INT IDENTITY(1,1) PRIMARY KEY,
    DocumentId INT NOT NULL,
    VersionNumber INT NOT NULL,
    FileLocation VARCHAR(1000) NOT NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedById INT NOT NULL,
    ContentHash VARCHAR(255) NOT NULL
);

CREATE TABLE Topics (
    TopicId INT IDENTITY(1,1) PRIMARY KEY,
    TopicName VARCHAR(100) NOT NULL,
    Description VARCHAR(500) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    ParentTopicId INT NULL
);

CREATE TABLE Tags (
    TagId INT IDENTITY(1,1) PRIMARY KEY,
    TagName VARCHAR(100) NOT NULL,
    Description VARCHAR(500) NULL,
    IsActive BIT NOT NULL DEFAULT 1
);

CREATE TABLE DocumentMetadata (
    DocumentMetadataId INT IDENTITY(1,1) PRIMARY KEY,
    DocumentId INT NOT NULL,
    MetadataKey VARCHAR(100) NOT NULL,
    MetadataValue NVARCHAR(MAX) NULL,
    DataType VARCHAR(50) NOT NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    LastModifiedDate DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE DocumentRelationships (
    RelationshipId INT IDENTITY(1,1) PRIMARY KEY,
    SourceDocumentId INT NOT NULL,
    TargetDocumentId INT NOT NULL,
    RelationshipType VARCHAR(50) NOT NULL,
    RelationshipMetadata NVARCHAR(MAX) NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedById INT NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1
);

GO