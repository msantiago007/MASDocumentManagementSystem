-- 05_InitialData.sql
USE DocumentManagement;
GO

-- Insert initial admin user
INSERT INTO Users (Username, Email, PasswordHash, IsActive)
VALUES ('admin', 'admin@docmanagement.local', 'HASH_TO_BE_REPLACED', 1);

-- Insert basic document types
INSERT INTO DocumentTypes (TypeName, Description, IsActive)
VALUES 
    ('Generic', 'General purpose documents', 1),
    ('Contract', 'Legal contracts and agreements', 1),
    ('Report', 'Business and technical reports', 1),
    ('Policy', 'Internal policies and procedures', 1);

-- Insert initial topics
INSERT INTO Topics (TopicName, Description, IsActive)
VALUES 
    ('General', 'General purpose documents', 1),
    ('Legal', 'Legal documents and references', 1),
    ('Technical', 'Technical documentation', 1),
    ('Administrative', 'Administrative documents', 1);

GO