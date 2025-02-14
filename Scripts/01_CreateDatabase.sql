-- 01_CreateDatabase.sql
USE master;
GO

-- Check if database exists and drop if it does
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'DocumentManagement')
BEGIN
    ALTER DATABASE DocumentManagement SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DocumentManagement;
END
GO

-- Create the database
CREATE DATABASE DocumentManagement;
GO

-- Set database options
ALTER DATABASE DocumentManagement SET RECOVERY SIMPLE;
ALTER DATABASE DocumentManagement SET AUTO_SHRINK OFF;
ALTER DATABASE DocumentManagement SET AUTO_CREATE_STATISTICS ON;
ALTER DATABASE DocumentManagement SET AUTO_UPDATE_STATISTICS ON;
GO

USE DocumentManagement;
GO