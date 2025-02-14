-- 03_CreateConstraints.sql
USE DocumentManagement;
GO

-- Add unique constraints
ALTER TABLE Users ADD CONSTRAINT UQ_Users_Username UNIQUE (Username);
ALTER TABLE Users ADD CONSTRAINT UQ_Users_Email UNIQUE (Email);
ALTER TABLE DocumentTypes ADD CONSTRAINT UQ_DocumentTypes_TypeName UNIQUE (TypeName);
ALTER TABLE Topics ADD CONSTRAINT UQ_Topics_TopicName UNIQUE (TopicName);
ALTER TABLE Tags ADD CONSTRAINT UQ_Tags_TagName UNIQUE (TagName);
ALTER TABLE DocumentMetadata ADD CONSTRAINT UQ_DocumentMetadata UNIQUE (DocumentId, MetadataKey);
ALTER TABLE DocumentVersions ADD CONSTRAINT UQ_DocumentVersion UNIQUE (DocumentId, VersionNumber);

-- Add foreign key constraints
ALTER TABLE Documents ADD CONSTRAINT FK_Documents_Users_CreatedBy 
    FOREIGN KEY (CreatedById) REFERENCES Users(UserId);
    
ALTER TABLE Documents ADD CONSTRAINT FK_Documents_Users_ModifiedBy 
    FOREIGN KEY (LastModifiedById) REFERENCES Users(UserId);
    
ALTER TABLE Documents ADD CONSTRAINT FK_Documents_DocumentTypes 
    FOREIGN KEY (DocumentTypeId) REFERENCES DocumentTypes(DocumentTypeId);

ALTER TABLE DocumentVersions ADD CONSTRAINT FK_DocumentVersions_Documents 
    FOREIGN KEY (DocumentId) REFERENCES Documents(DocumentId);
    
ALTER TABLE DocumentVersions ADD CONSTRAINT FK_DocumentVersions_Users 
    FOREIGN KEY (CreatedById) REFERENCES Users(UserId);

ALTER TABLE Topics ADD CONSTRAINT FK_Topics_ParentTopic 
    FOREIGN KEY (ParentTopicId) REFERENCES Topics(TopicId);

ALTER TABLE DocumentMetadata ADD CONSTRAINT FK_DocumentMetadata_Documents 
    FOREIGN KEY (DocumentId) REFERENCES Documents(DocumentId);

ALTER TABLE DocumentRelationships ADD CONSTRAINT FK_DocumentRelationships_SourceDoc 
    FOREIGN KEY (SourceDocumentId) REFERENCES Documents(DocumentId);
    
ALTER TABLE DocumentRelationships ADD CONSTRAINT FK_DocumentRelationships_TargetDoc 
    FOREIGN KEY (TargetDocumentId) REFERENCES Documents(DocumentId);
    
ALTER TABLE DocumentRelationships ADD CONSTRAINT FK_DocumentRelationships_Users 
    FOREIGN KEY (CreatedById) REFERENCES Users(UserId);

-- Add check constraints
ALTER TABLE DocumentMetadata ADD CONSTRAINT CHK_DataType 
    CHECK (DataType IN ('string', 'number', 'date', 'boolean', 'json'));

GO