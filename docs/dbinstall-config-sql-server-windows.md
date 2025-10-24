<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# SQL Server Installation and Configuration Guide
* One guide for Windows, Linux, and Docker—end to end. Install, configure, secure, and tune SQL Server—the right way.*

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Windows Installation](#windows-installation)
- [Linux Installation](#linux-installation)
- [Docker Installation](#docker-installation)
- [SQL Server Management Studio (SSMS)](#sql-server-management-studio-ssms)
- [Initial Configuration](#initial-configuration)
- [Security Configuration](#security-configuration)
- [Database Creation](#database-creation)
- [Connection Testing](#connection-testing)
- [Performance Optimization](#performance-optimization)
- [Backup and Recovery](#backup-and-recovery)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Overview

Microsoft SQL Server is a relational database management system developed by Microsoft. This guide covers the installation and configuration of SQL Server across different platforms, including Windows, Linux, and Docker environments.

**Supported Versions:**
- SQL Server 2019
- SQL Server 2022
- SQL Server Express (Free edition)
- SQL Server Developer (Free for development)

[Back to top](#table-of-contents)

## Prerequisites

### System Requirements

**Minimum Hardware Requirements:**
- **CPU**: x64 processor, 1.4 GHz minimum
- **RAM**: 512 MB minimum (1 GB+ recommended)
- **Storage**: 6 GB minimum for basic installation
- **Network**: TCP/IP protocol enabled

**Software Requirements:**
- Windows Server 2016+ or Windows 10+
- .NET Framework 4.6 or later
- PowerShell 5.1 or later

### Linux Requirements
- Red Hat Enterprise Linux 7/8
- SUSE Linux Enterprise Server v12 SP2+
- Ubuntu 16.04+ LTS
- Docker Engine 1.8+

[Back to top](#table-of-contents)

## Installation Methods

### 1. Windows Installation (GUI)
### 2. Windows Installation (Command Line)
### 3. Linux Installation
### 4. Docker Container
### 5. Azure SQL Database (Cloud)

## Windows Installation

### Download SQL Server

1. Visit the [Microsoft SQL Server Downloads](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) page
2. Choose your edition:
   - **Express**: Free, limited to 10 GB database size
   - **Developer**: Free, full-featured for development
   - **Standard/Enterprise**: Licensed versions

### GUI Installation Process

```batch
# Download SQL Server Installation Media
# Run the installer as Administrator
SqlServerSetup.exe
```

**Installation Steps:**

1. **Installation Type**
   - Basic: Quick installation with default settings
   - Custom: Advanced configuration options
   - Download Media: Download installation files

2. **Feature Selection**
   - Database Engine Services (required)
   - SQL Server Replication
   - Full-Text and Semantic Extractions for Search
   - Data Quality Services
   - PolyBase Query Service
   - Analysis Services
   - Reporting Services
   - Integration Services
   - Master Data Services
   - Machine Learning Services

3. **Instance Configuration**
   - Default instance: `MSSQLSERVER`
   - Named instance: Custom name (e.g., `SQLDEV`)

4. **Server Configuration**
   - Service accounts configuration
   - Collation settings
   - Authentication mode

5. **Database Engine Configuration**
   - Authentication Mode:
     - Windows Authentication (recommended)
     - Mixed Mode (SQL Server and Windows)
   - Administrator accounts
   - Data directories
   - TempDB configuration

### Command Line Installation

```batch
# Silent installation with custom parameters
Setup.exe /Q /IACCEPTSQLSERVERLICENSETERMS /ACTION=Install ^
/FEATURES=SQLENGINE /INSTANCENAME=MSSQLSERVER ^
/SQLSVCACCOUNT="NT Service\MSSQLSERVER" ^
/SQLSYSADMINACCOUNTS="DOMAIN\Administrator" ^
/SECURITYMODE=SQL /SAPWD="YourStrongPassword123!"
```

**Common Setup Parameters:**

```batch
# Basic installation parameters
/Q                              # Quiet mode
/IACCEPTSQLSERVERLICENSETERMS   # Accept license terms
/ACTION=Install                 # Installation action
/FEATURES=SQLENGINE            # Features to install
/INSTANCENAME=MSSQLSERVER      # Instance name
/SECURITYMODE=SQL              # Mixed authentication
/SAPWD="Password123!"          # SA password
/SQLSYSADMINACCOUNTS="Domain\User"  # Admin accounts
```

[Back to top](#table-of-contents)

## Linux Installation

### Red Hat/CentOS Installation

```bash
# Add Microsoft repository
sudo curl -o /etc/yum.repos.d/mssql-server.repo \
  https://packages.microsoft.com/config/rhel/8/mssql-server-2022.repo

# Install SQL Server
sudo yum install -y mssql-server

# Run setup
sudo /opt/mssql/bin/mssql-conf setup

# Start and enable service
sudo systemctl start mssql-server
sudo systemctl enable mssql-server

# Check status
sudo systemctl status mssql-server
```

### Ubuntu Installation

```bash
# Import GPG keys
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

# Add Microsoft repository
sudo add-apt-repository \
  "$(wget -qO- https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2022.list)"

# Update package list
sudo apt-get update

# Install SQL Server
sudo apt-get install -y mssql-server

# Run setup
sudo /opt/mssql/bin/mssql-conf setup

# Start service
sudo systemctl start mssql-server
sudo systemctl enable mssql-server
```

### Install SQL Server Command-Line Tools (Linux)

```bash
# Add tools repository (Ubuntu)
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | \
  sudo tee /etc/apt/sources.list.d/msprod.list

# Update and install
sudo apt-get update
sudo apt-get install mssql-tools unixodbc-dev

# Add to PATH
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
```

[Back to top](#table-of-contents)

## Docker Installation

### Pull and Run SQL Server Container

```bash
# Pull SQL Server 2022 image
docker pull mcr.microsoft.com/mssql/server:2022-latest

# Run SQL Server container
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" \
   -p 1433:1433 --name sqlserver2022 --hostname sqlserver2022 \
   -d mcr.microsoft.com/mssql/server:2022-latest

# Check container status
docker ps

# View container logs
docker logs sqlserver2022
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: sqlserver2022
    hostname: sqlserver2022
    ports:
      - "1433:1433"
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong@Passw0rd
      - MSSQL_PID=Developer
    volumes:
      - sqlserver_data:/var/opt/mssql
    restart: unless-stopped
    networks:
      - sqlserver_network

volumes:
  sqlserver_data:

networks:
  sqlserver_network:
    driver: bridge
```

```bash
# Start with docker-compose
docker-compose up -d

# Stop services
docker-compose down
```
[Back to top](#table-of-contents)

## SQL Server Management Studio (SSMS)

### Download and Install SSMS

```batch
# Download SSMS from Microsoft
# https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms

# Silent installation
SSMS-Setup-ENU.exe /install /quiet /norestart
```

### Alternative Tools

**Azure Data Studio** (Cross-platform)
```bash
# Download and install Azure Data Studio
# Available for Windows, macOS, and Linux
# https://docs.microsoft.com/en-us/sql/azure-data-studio/
```

**Command Line Tools**
```bash
# Connect using sqlcmd
sqlcmd -S localhost -U sa -P "YourPassword123!"

# Execute query
1> SELECT @@VERSION;
2> GO

# Exit
1> EXIT
```

[Back to top](#table-of-contents)

## Initial Configuration

### Basic Server Configuration

```sql
-- Check SQL Server version and edition
SELECT @@VERSION AS 'SQL Server Version',
       SERVERPROPERTY('Edition') AS 'Edition',
       SERVERPROPERTY('ProductLevel') AS 'Service Pack Level';

-- View server configuration
EXEC sp_configure;

-- Show advanced options
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure;
```

### Memory Configuration

```sql
-- Set maximum server memory (MB)
EXEC sp_configure 'max server memory (MB)', 4096;
RECONFIGURE;

-- Set minimum server memory (MB)
EXEC sp_configure 'min server memory (MB)', 1024;
RECONFIGURE;
```

### Database File Configuration

```sql
-- Configure default database file locations
EXEC xp_instance_regwrite 
    N'HKEY_LOCAL_MACHINE', 
    N'Software\Microsoft\MSSQLServer\MSSQLServer',
    N'DefaultData', 
    REG_SZ, 
    N'C:\Data\';

EXEC xp_instance_regwrite 
    N'HKEY_LOCAL_MACHINE', 
    N'Software\Microsoft\MSSQLServer\MSSQLServer',
    N'DefaultLog', 
    REG_SZ, 
    N'C:\Logs\';
```

[Back to top](#table-of-contents)

## Security Configuration

### Authentication Configuration

**Enable Mixed Mode Authentication:**

```sql
-- Check current authentication mode
SELECT CASE SERVERPROPERTY('IsIntegratedSecurityOnly')
    WHEN 1 THEN 'Windows Authentication'
    WHEN 0 THEN 'Mixed Mode'
END AS 'Authentication Mode';

-- Change to mixed mode (requires restart)
EXEC xp_instance_regwrite 
    N'HKEY_LOCAL_MACHINE',
    N'Software\Microsoft\MSSQLServer\MSSQLServer',
    N'LoginMode',
    REG_DWORD,
    2;
```

### Create SQL Server Login

```sql
-- Create new SQL login
CREATE LOGIN [developer_user] 
WITH PASSWORD = 'SecurePassword123!',
     DEFAULT_DATABASE = [master],
     CHECK_EXPIRATION = OFF,
     CHECK_POLICY = OFF;

-- Add to server roles
ALTER SERVER ROLE [sysadmin] ADD MEMBER [developer_user];
```

### Configure SA Account

```sql
-- Enable SA account (if disabled)
ALTER LOGIN [sa] ENABLE;

-- Change SA password
ALTER LOGIN [sa] WITH PASSWORD = 'NewSecurePassword123!';
```

### Network Configuration

**Enable TCP/IP Protocol:**

```sql
-- Check enabled protocols
EXEC xp_readerrorlog 0, 1, N'Server is listening on';

-- Enable TCP/IP through SQL Server Configuration Manager
-- Or use PowerShell:
```

```powershell
# Import SQL Server module
Import-Module SqlServer

# Enable TCP/IP protocol
$instance = "MSSQLSERVER"
$tcp = Get-WmiObject -Namespace "root\Microsoft\SqlServer\ComputerManagement15" `
       -Class ServerNetworkProtocol `
       -Filter "InstanceName='$instance' and ProtocolName='Tcp'"
$tcp.SetEnable()
```

[Back to top](#table-of-contents)

## Database Creation

### Create New Database

```sql
-- Create database with custom settings
CREATE DATABASE [CompanyDB]
ON 
( NAME = 'CompanyDB',
  FILENAME = 'C:\Data\CompanyDB.mdf',
  SIZE = 100MB,
  MAXSIZE = 1GB,
  FILEGROWTH = 10MB )
LOG ON 
( NAME = 'CompanyDB_Log',
  FILENAME = 'C:\Logs\CompanyDB.ldf',
  SIZE = 10MB,
  MAXSIZE = 100MB,
  FILEGROWTH = 10% );

-- Set database options
ALTER DATABASE [CompanyDB] 
SET RECOVERY FULL,
    AUTO_CLOSE OFF,
    AUTO_SHRINK OFF,
    ENABLE_BROKER;
```

### Create Database User

```sql
-- Switch to the database
USE [CompanyDB];

-- Create database user
CREATE USER [app_user] FOR LOGIN [developer_user];

-- Grant permissions
ALTER ROLE [db_datareader] ADD MEMBER [app_user];
ALTER ROLE [db_datawriter] ADD MEMBER [app_user];
ALTER ROLE [db_ddladmin] ADD MEMBER [app_user];
```

### Create Sample Tables

```sql
USE [CompanyDB];

-- Create Employees table
CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    HireDate DATE NOT NULL,
    Salary DECIMAL(10,2),
    DepartmentID INT,
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- Create Departments table
CREATE TABLE Departments (
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName NVARCHAR(100) NOT NULL,
    ManagerID INT,
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- Add foreign key constraint
ALTER TABLE Employees
ADD CONSTRAINT FK_Employees_Department 
FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID);

-- Insert sample data
INSERT INTO Departments (DepartmentName) VALUES 
('Human Resources'),
('Information Technology'),
('Finance'),
('Sales');

INSERT INTO Employees (FirstName, LastName, Email, HireDate, Salary, DepartmentID) VALUES
('John', 'Doe', 'john.doe@company.com', '2023-01-15', 75000.00, 2),
('Jane', 'Smith', 'jane.smith@company.com', '2023-02-20', 65000.00, 1),
('Mike', 'Johnson', 'mike.johnson@company.com', '2023-03-10', 80000.00, 2),
('Sarah', 'Wilson', 'sarah.wilson@company.com', '2023-04-05', 70000.00, 4);
```
[Back to top](#table-of-contents)

## Connection Testing

### Test Local Connection

```bash
# Using sqlcmd (Windows/Linux)
sqlcmd -S localhost -U sa -P "YourPassword123!"

# Test query
1> SELECT DB_NAME() AS CurrentDatabase;
2> GO

# Test with specific database
1> USE CompanyDB;
2> SELECT COUNT(*) FROM Employees;
3> GO
```

### Test Remote Connection

```bash
# Connect to remote SQL Server
sqlcmd -S "server_ip,1433" -U username -P "password"

# Connection string format
Server=server_name,1433;Database=database_name;User Id=username;Password=password;
```

### .NET Connection String Examples

```csharp
// Windows Authentication
"Server=localhost;Database=CompanyDB;Trusted_Connection=true;"

// SQL Server Authentication
"Server=localhost;Database=CompanyDB;User Id=sa;Password=YourPassword123!;"

// With encryption
"Server=localhost;Database=CompanyDB;User Id=sa;Password=YourPassword123!;Encrypt=true;TrustServerCertificate=true;"
```

[Back to top](#table-of-contents)

## Performance Optimization

### Index Management

```sql
-- Check for missing indexes
SELECT 
    dm_mid.database_id AS DatabaseID,
    dm_migs.avg_user_impact AS AvgUserImpact,
    dm_migs.avg_system_impact AS AvgSystemImpact,
    dm_mid.statement AS TableName,
    dm_mid.equality_columns AS EqualityColumns,
    dm_mid.inequality_columns AS InequalityColumns,
    dm_mid.included_columns AS IncludeColumns
FROM sys.dm_db_missing_index_groups dm_mig
INNER JOIN sys.dm_db_missing_index_group_stats dm_migs
    ON dm_migs.group_handle = dm_mig.index_group_handle
INNER JOIN sys.dm_db_missing_index_details dm_mid
    ON dm_mig.index_handle = dm_mid.index_handle
WHERE dm_mid.database_id = DB_ID('CompanyDB')
ORDER BY dm_migs.avg_user_impact DESC;

-- Create index based on recommendations
CREATE NONCLUSTERED INDEX IX_Employees_DepartmentID
ON Employees (DepartmentID)
INCLUDE (FirstName, LastName, Email);
```

### Query Performance

```sql
-- Enable Query Store
ALTER DATABASE [CompanyDB] 
SET QUERY_STORE = ON (
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 60
);

-- Update statistics
UPDATE STATISTICS Employees;
UPDATE STATISTICS Departments;

-- Recompile stored procedures if needed
EXEC sp_recompile 'Employees';
```

[Back to top](#table-of-contents)

## Backup and Recovery

### Full Database Backup

```sql
-- Create full backup
BACKUP DATABASE [CompanyDB] 
TO DISK = 'C:\Backups\CompanyDB_Full_20241201.bak'
WITH FORMAT, INIT, NAME = 'Full Backup of CompanyDB';

-- Create differential backup
BACKUP DATABASE [CompanyDB] 
TO DISK = 'C:\Backups\CompanyDB_Diff_20241201.bak'
WITH DIFFERENTIAL, FORMAT, INIT, 
NAME = 'Differential Backup of CompanyDB';

-- Create transaction log backup
BACKUP LOG [CompanyDB] 
TO DISK = 'C:\Backups\CompanyDB_Log_20241201.trn'
WITH FORMAT, INIT, NAME = 'Log Backup of CompanyDB';
```

### Automated Backup Script

```sql
-- Create maintenance plan or use SQL Agent Job
DECLARE @BackupPath NVARCHAR(500) = 'C:\Backups\';
DECLARE @DatabaseName NVARCHAR(128) = 'CompanyDB';
DECLARE @BackupFileName NVARCHAR(500);

SET @BackupFileName = @BackupPath + @DatabaseName + '_Full_' + 
    CONVERT(VARCHAR(8), GETDATE(), 112) + '.bak';

BACKUP DATABASE @DatabaseName 
TO DISK = @BackupFileName
WITH FORMAT, INIT, COMPRESSION,
NAME = 'Automated Full Backup';

PRINT 'Backup completed: ' + @BackupFileName;
```

### Restore Database

```sql
-- Restore from full backup
RESTORE DATABASE [CompanyDB_Restored] 
FROM DISK = 'C:\Backups\CompanyDB_Full_20241201.bak'
WITH MOVE 'CompanyDB' TO 'C:\Data\CompanyDB_Restored.mdf',
     MOVE 'CompanyDB_Log' TO 'C:\Logs\CompanyDB_Restored.ldf',
     REPLACE;
```

[Back to top](#table-of-contents)

## Monitoring and Maintenance

### System Monitoring Queries

```sql
-- Check database sizes
SELECT 
    DB_NAME(database_id) AS DatabaseName,
    SUM(CASE WHEN type = 0 THEN size END) * 8 / 1024 AS DataFileSizeMB,
    SUM(CASE WHEN type = 1 THEN size END) * 8 / 1024 AS LogFileSizeMB
FROM sys.master_files
WHERE database_id > 4 -- Exclude system databases
GROUP BY database_id;

-- Monitor active connections
SELECT 
    DB_NAME(database_id) AS DatabaseName,
    COUNT(*) AS ConnectionCount,
    loginame AS LoginName
FROM sys.sysprocesses
WHERE database_id > 0
GROUP BY database_id, loginame
ORDER BY ConnectionCount DESC;

-- Check for blocking processes
SELECT 
    blocking_session_id AS BlockingSessionID,
    session_id AS BlockedSessionID,
    wait_type AS WaitType,
    wait_time AS WaitTimeMS,
    wait_resource AS WaitResource
FROM sys.dm_exec_requests
WHERE blocking_session_id <> 0;
```

### Maintenance Tasks

```sql
-- Update statistics for all tables
EXEC sp_updatestats;

-- Rebuild indexes
ALTER INDEX ALL ON Employees REBUILD;

-- Check database integrity
DBCC CHECKDB('CompanyDB') WITH NO_INFOMSGS;

-- Shrink database files if needed (use carefully)
DBCC SHRINKDATABASE('CompanyDB', 10);
```

[Back to top](#table-of-contents)

## Troubleshooting

### Common Connection Issues

**Issue: Cannot connect to SQL Server**
```sql
-- Check if SQL Server service is running
SELECT servicename, status_desc FROM sys.dm_server_services;

-- Check listening ports
EXEC xp_readerrorlog 0, 1, N'Server is listening on';

-- Enable TCP/IP protocol in SQL Server Configuration Manager
```

**Issue: Login failed for user**
```sql
-- Check login exists
SELECT name, is_disabled FROM sys.server_principals WHERE name = 'username';

-- Reset password
ALTER LOGIN [username] WITH PASSWORD = 'NewPassword123!';

-- Check database access
SELECT 
    dp.name AS DatabaseUser,
    sp.name AS LoginName,
    dp.type_desc AS UserType
FROM sys.database_principals dp
LEFT JOIN sys.server_principals sp ON dp.sid = sp.sid
WHERE dp.name = 'username';
```

### Performance Troubleshooting

```sql
-- Find expensive queries
SELECT TOP 10
    qt.text AS QueryText,
    qs.execution_count AS ExecutionCount,
    qs.total_worker_time / 1000000.0 AS TotalCPUTimeSeconds,
    qs.total_elapsed_time / 1000000.0 AS TotalElapsedTimeSeconds,
    qs.total_logical_reads AS TotalLogicalReads
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY qs.total_worker_time DESC;

-- Check wait statistics
SELECT TOP 10
    wait_type,
    wait_time_ms,
    percentage = ROUND(wait_time_ms * 100.0 / SUM(wait_time_ms) OVER(), 2)
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE',
    'SLEEP_TASK', 'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH',
    'WAITFOR', 'LOGMGR_QUEUE', 'CHECKPOINT_QUEUE'
)
ORDER BY wait_time_ms DESC;
```

### Log Analysis

```sql
-- Read error log
EXEC sp_readerrorlog 0, 1;

-- Check database status
SELECT 
    name AS DatabaseName,
    state_desc AS Status,
    recovery_model_desc AS RecoveryModel
FROM sys.databases;
```
---
## Conclusion

This guide provides a comprehensive overview of SQL Server installation and configuration across multiple platforms. Regular maintenance, monitoring, and security updates are essential for optimal performance and security. Always test configurations in a development environment before applying them to production systems.

---
[Back to top](#table-of-contents)

---

**[🏠 Back to Main Portfolio](../README.md#top)**

---

## Author & Maintainer
<table>
  <tr>
    <td width="96" valign="top">
      <img src="https://github.com/vandersantanna.png?size=160" alt="Vanderley Sant Anna" width="96" height="96">
    </td>
    <td valign="top">
      <strong>Vanderley Sant Anna</strong><br>
      Senior Database Engineer (DBE) / Database Reliability Engineer (DBRE) / Senior DBA / DataOps Engineer
    </td>
  </tr>
</table>

**Preferred name:** Vander  

**Education:**  
- B.Sc. in Software Engineering — Centro Universitário de Maringá (UniCesumar) — *UniCesumar University Center*, Maringá, Brazil (2020)  
- Postgraduate Specialization (Lato Sensu) in Software Project Engineering — Universidade do Sul de Santa Catarina (UNISUL) — *Southern Santa Catarina University*, Florianópolis, Brazil (2008)  
- Technologist in Data Processing (*Tecnólogo em Processamento de Dados*) — Universidade do Estado de Santa Catarina (UDESC) — *Santa Catarina State University*, Joinville, Brazil (1995)  

**Certifications:**  
- Oracle OCP  
- MongoDB University — M102: MongoDB for DBAs  
- IBM Certified Database Associate — DB2 9 Fundamentals  

**Location & Timezone:** Blumenau, SC, Brazil (UTC−3) • **Availability:** Remote (Americas & Europe)

**Last Updated:** 2025-10-24 • **Status:** Actively maintained

## 📫 Contact
- **Email (primary):** [vandersantanna@gmail.com](mailto:vandersantanna@gmail.com)  
- **LinkedIn:** [linkedin.com/in/vandersantanna](https://www.linkedin.com/in/vandersantanna)  
- **GitHub:** [github.com/vandersantanna](https://github.com/vandersantanna)

<details>
  <summary><strong>Trademarks</strong></summary>

  <small>All product names, logos, and brands are property of their respective owners. 
  Use of these names is for identification purposes only and does not imply endorsement or affiliation.</small>
</details>


