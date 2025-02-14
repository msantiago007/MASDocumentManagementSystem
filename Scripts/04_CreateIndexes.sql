-- 04_CreateIndexes.sql
USE DocumentManagement;
GO

-- Create indexes for better query performance
CREATE INDEX IX_Documents_DocumentType 
ON Documents(DocumentTypeId);

CREATE INDEX IX_Documents_CreatedDate 
ON Documents(CreatedDate);

CREATE INDEX IX_Documents_IsDeleted 
ON Documents(IsDeleted);

CREATE INDEX IX_DocumentMetadata_Key 
ON DocumentMetadata(MetadataKey);

CREATE INDEX IX_DocumentRelationships_Source 
ON DocumentRelationships(SourceDocumentId);

CREATE INDEX IX_DocumentRelationships_Target 
ON DocumentRelationships(TargetDocumentId);

CREATE INDEX IX_DocumentVersions_Document 
ON DocumentVersions(DocumentId, VersionNumber);

CREATE INDEX IX_Users_Email 
ON Users(Email);

GO