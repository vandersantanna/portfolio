<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# SQL Server 2022 on Linux - Red Hat and Ubuntu Installation Guide
*From first package to production-ready SQL Server on RHEL & Ubuntu.*

---
## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Red Hat Enterprise Linux Installation](#red-hat-enterprise-linux-installation)
- [Ubuntu Installation](#ubuntu-installation)
- [Initial Configuration](#initial-configuration)
- [SQL Server Tools Installation](#sql-server-tools-installation)
- [Security Configuration](#security-configuration)
- [Network Configuration](#network-configuration)
- [Database Configuration](#database-configuration)
- [Performance Tuning](#performance-tuning)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [SSL/TLS Configuration](#ssltls-configuration)
- [High Availability Setup](#high-availability-setup)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

Microsoft SQL Server 2022 brings enterprise-grade database capabilities to Linux environments. This guide provides detailed instructions for installing and configuring SQL Server 2022 on Red Hat Enterprise Linux (RHEL) and Ubuntu distributions.

**Key Features of SQL Server 2022 on Linux:**
- Full T-SQL compatibility
- Advanced security features
- Built-in machine learning capabilities
- Container support
- High availability and disaster recovery
- Cross-platform development

[Back to top](#table-of-contents)

## Prerequisites

### Supported Linux Distributions

**Red Hat Enterprise Linux:**
- RHEL 8.0 - 8.7
- RHEL 9.0 - 9.1
- CentOS 8 (deprecated but supported)

**Ubuntu:**
- Ubuntu 18.04 LTS (Bionic Beaver)
- Ubuntu 20.04 LTS (Focal Fossa)
- Ubuntu 22.04 LTS (Jammy Jellyfish)

### Required Packages
```bash
# Common requirements for both distributions
- glibc >= 2.17
- kernel >= 4.x
- systemd
- python3
- openssl
```
[Back to top](#table-of-contents)

## System Requirements

### Minimum Hardware Requirements
```bash
# CPU: x86_64 architecture
CPU_CORES=2
CPU_SPEED="2.0 GHz"

# Memory
RAM_MINIMUM="2 GB"
RAM_RECOMMENDED="4 GB or more"

# Storage
DISK_SPACE_MINIMUM="6 GB"
DISK_SPACE_RECOMMENDED="20 GB or more"

# Network
NETWORK="TCP/IP enabled"
```

### Performance Recommendations
```bash
# For production environments
CPU_CORES_PROD=4
RAM_PROD="8 GB or more"
STORAGE_TYPE="SSD recommended"
NETWORK_SPEED="Gigabit Ethernet"
```

[Back to top](#table-of-contents)

## Red Hat Enterprise Linux Installation

### Step 1: System Preparation

```bash
# Update system packages
sudo yum update -y

# Install required dependencies
sudo yum install -y curl wget gnupg2

# Check system version
cat /etc/redhat-release
uname -r
```

### Step 2: Add Microsoft Repository

```bash
# Download and install Microsoft signing key
sudo curl -o /etc/yum.repos.d/mssql-server.repo \
  https://packages.microsoft.com/config/rhel/8/mssql-server-2022.repo

# Verify repository was added
ls -la /etc/yum.repos.d/ | grep mssql

# Update package cache
sudo yum makecache
```

### Alternative Repository Setup for RHEL 9

```bash
# For RHEL 9.x systems
sudo curl -o /etc/yum.repos.d/mssql-server.repo \
  https://packages.microsoft.com/config/rhel/9/mssql-server-2022.repo

# Import Microsoft GPG key
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
```

### Step 3: Install SQL Server 2022

```bash
# Install SQL Server package
sudo yum install -y mssql-server

# Verify installation
rpm -qa | grep mssql-server

# Check installed version
sudo /opt/mssql/bin/mssql-conf --version
```

### Step 4: Configure SQL Server

```bash
# Run SQL Server setup
sudo /opt/mssql/bin/mssql-conf setup

# Configuration prompts:
# 1. Choose edition:
#    1) Evaluation (free, no production use rights, 180-day limit)
#    2) Developer (free, no production use rights)
#    3) Express (free)
#    4) Web (PAID)
#    5) Standard (PAID)
#    6) Enterprise (PAID)
#    7) I bought a license through a retail sales channel and have a product key to enter.

# 2. Accept license terms: Yes

# 3. Enter SA password (must meet complexity requirements):
#    - At least 8 characters
#    - Contains characters from 3 of these 4 sets:
#      * Uppercase letters
#      * Lowercase letters  
#      * Digits
#      * Symbols
```

### Step 5: Start and Enable Services

```bash
# Start SQL Server service
sudo systemctl start mssql-server

# Enable service to start on boot
sudo systemctl enable mssql-server

# Check service status
sudo systemctl status mssql-server

# Verify SQL Server is listening
sudo netstat -tulnp | grep 1433
```

[Back to top](#table-of-contents)

## Ubuntu Installation

### Step 1: System Preparation

```bash
# Update package lists
sudo apt update

# Upgrade existing packages
sudo apt upgrade -y

# Install required dependencies
sudo apt install -y curl wget gnupg lsb-release

# Check Ubuntu version
lsb_release -a
uname -r
```

### Step 2: Add Microsoft Repository

```bash
# Import Microsoft GPG key
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

# Add Microsoft repository for Ubuntu 20.04
sudo add-apt-repository \
  "$(wget -qO- https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2022.list)"

# For Ubuntu 22.04
sudo add-apt-repository \
  "$(wget -qO- https://packages.microsoft.com/config/ubuntu/22.04/mssql-server-2022.list)"

# Alternative method using sources.list
echo "deb [arch=amd64,armhf,arm64] https://packages.microsoft.com/ubuntu/20.04/mssql-server-2022 focal main" | \
  sudo tee /etc/apt/sources.list.d/mssql-server-2022.list
```

### Step 3: Install SQL Server 2022

```bash
# Update package cache
sudo apt update

# Install SQL Server
sudo apt install -y mssql-server

# Verify installation
dpkg -l | grep mssql-server

# Check installed files
dpkg -L mssql-server | head -20
```

### Step 4: Configure SQL Server

```bash
# Run SQL Server configuration
sudo /opt/mssql/bin/mssql-conf setup

# Follow the same configuration prompts as RHEL installation
# Choose edition, accept license, set SA password
```

### Step 5: Start and Enable Services

```bash
# Start SQL Server
sudo systemctl start mssql-server

# Enable auto-start
sudo systemctl enable mssql-server

# Check service status
sudo systemctl status mssql-server

# Verify listening ports
sudo ss -tulnp | grep 1433
```
[Back to top](#table-of-contents)

## Initial Configuration

### Verify Installation

```bash
# Check SQL Server version
sudo /opt/mssql/bin/mssql-conf --version

# View current configuration
sudo /opt/mssql/bin/mssql-conf list

# Check SQL Server processes
ps aux | grep sqlservr

# View SQL Server logs
sudo tail -f /var/opt/mssql/log/errorlog
```

### Basic Configuration Options

```bash
# Set custom TCP port (default 1433)
sudo /opt/mssql/bin/mssql-conf set network.tcpport 1433

# Enable SQL Server Agent
sudo /opt/mssql/bin/mssql-conf set sqlagent.enabled true

# Set default data directory
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultdatadir /var/opt/mssql/data

# Set default log directory
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultlogdir /var/opt/mssql/data

# Set default backup directory
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultbackupdir /var/opt/mssql/backup

# Restart to apply changes
sudo systemctl restart mssql-server
```

### Memory Configuration

```bash
# Set maximum memory (in MB)
sudo /opt/mssql/bin/mssql-conf set memory.memorylimitmb 4096

# Set minimum memory (in MB)
sudo /opt/mssql/bin/mssql-conf set memory.minservermemory 1024

# Restart service
sudo systemctl restart mssql-server
```

[Back to top](#table-of-contents)

## SQL Server Tools Installation

### Red Hat/CentOS Tools Installation

```bash
# Add tools repository
sudo curl -o /etc/yum.repos.d/msprod.repo \
  https://packages.microsoft.com/config/rhel/8/prod.repo

# Install SQL Server command-line tools
sudo yum install -y mssql-tools unixODBC-devel

# Accept EULA during installation
# Add tools to PATH
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
which sqlcmd
sqlcmd -?
```

### Ubuntu Tools Installation

```bash
# Add Microsoft repository for tools
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | \
  sudo tee /etc/apt/sources.list.d/msprod.list

# Update package cache
sudo apt update

# Install SQL Server tools
sudo apt install -y mssql-tools unixodbc-dev

# Add to PATH
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

# Test installation
sqlcmd -S localhost -U SA -P 'YourPassword123!'
```

### PowerShell Core Installation

**Red Hat/CentOS:**
```bash
# Install PowerShell Core
sudo yum install -y powershell

# Or using snap
sudo yum install -y snapd
sudo systemctl enable --now snapd.socket
sudo snap install powershell --classic
```

**Ubuntu:**
```bash
# Install PowerShell Core
sudo apt install -y powershell

# Or download and install manually
wget https://github.com/PowerShell/PowerShell/releases/download/v7.3.0/powershell_7.3.0-1.deb_amd64.deb
sudo dpkg -i powershell_7.3.0-1.deb_amd64.deb
```

### SQL Server PowerShell Module

```powershell
# Start PowerShell
pwsh

# Install SqlServer module
Install-Module -Name SqlServer -Force

# Import module
Import-Module SqlServer

# Test connection
Invoke-Sqlcmd -ServerInstance "localhost" -Database "master" -Query "SELECT @@VERSION"
```
[Back to top](#table-of-contents)

## Security Configuration

### Firewall Configuration

**Red Hat/CentOS (firewalld):**
```bash
# Check firewall status
sudo firewall-cmd --state

# Allow SQL Server port
sudo firewall-cmd --zone=public --add-port=1433/tcp --permanent

# Reload firewall rules
sudo firewall-cmd --reload

# Verify rule was added
sudo firewall-cmd --zone=public --list-ports
```

**Ubuntu (ufw):**
```bash
# Enable UFW if not already enabled
sudo ufw enable

# Allow SQL Server port
sudo ufw allow 1433/tcp

# Check UFW status
sudo ufw status

# Allow specific IP range (optional)
sudo ufw allow from 192.168.1.0/24 to any port 1433
```

### SQL Server Authentication

```bash
# Connect to SQL Server
sqlcmd -S localhost -U SA -P 'YourPassword123!'

# Create new login
1> CREATE LOGIN [linux_admin] WITH PASSWORD='SecureLinuxPassword123!';
2> GO

# Add to sysadmin role
1> ALTER SERVER ROLE sysadmin ADD MEMBER [linux_admin];
2> GO

# Create database user
1> USE master;
2> CREATE USER [linux_admin] FOR LOGIN [linux_admin];
3> GO

# Exit
1> EXIT
```

### SSL/TLS Certificate Configuration

```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -newkey rsa:2048 -subj '/CN=sqlserver' \
  -keyout /var/opt/mssql/private.key -out /var/opt/mssql/certificate.crt -days 365

# Set proper permissions
sudo chown mssql:mssql /var/opt/mssql/private.key /var/opt/mssql/certificate.crt
sudo chmod 600 /var/opt/mssql/private.key /var/opt/mssql/certificate.crt

# Configure SQL Server to use certificate
sudo /opt/mssql/bin/mssql-conf set network.tlscert /var/opt/mssql/certificate.crt
sudo /opt/mssql/bin/mssql-conf set network.tlskey /var/opt/mssql/private.key
sudo /opt/mssql/bin/mssql-conf set network.tlsprotocols 1.2
sudo /opt/mssql/bin/mssql-conf set network.forceencryption 1

# Restart SQL Server
sudo systemctl restart mssql-server
```
[Back to top](#table-of-contents)

## Network Configuration

### Configure Network Settings

```bash
# Set custom TCP port
sudo /opt/mssql/bin/mssql-conf set network.tcpport 1433

# Enable/disable TCP protocol
sudo /opt/mssql/bin/mssql-conf set network.tcpenabled true

# Set IP address binding (listen on all interfaces)
sudo /opt/mssql/bin/mssql-conf set network.ipaddress 0.0.0.0

# Set specific IP address
# sudo /opt/mssql/bin/mssql-conf set network.ipaddress 192.168.1.100

# Restart to apply changes
sudo systemctl restart mssql-server

# Verify listening addresses
sudo netstat -tlnp | grep 1433
```

### Test Network Connectivity

```bash
# Test local connection
sqlcmd -S localhost -U SA -P 'YourPassword123!'

# Test TCP connection
sqlcmd -S localhost,1433 -U SA -P 'YourPassword123!'

# Test from remote machine
sqlcmd -S server_ip,1433 -U SA -P 'YourPassword123!'

# Use telnet to test port connectivity
telnet localhost 1433
```

[Back to top](#table-of-contents)

## Database Configuration

### Create Sample Database

```sql
-- Connect to SQL Server
sqlcmd -S localhost -U SA -P 'YourPassword123!'

-- Create database
CREATE DATABASE LinuxCompanyDB
ON 
( NAME = 'LinuxCompanyDB_Data',
  FILENAME = '/var/opt/mssql/data/LinuxCompanyDB.mdf',
  SIZE = 100MB,
  MAXSIZE = 1GB,
  FILEGROWTH = 10MB )
LOG ON 
( NAME = 'LinuxCompanyDB_Log',
  FILENAME = '/var/opt/mssql/data/LinuxCompanyDB.ldf',
  SIZE = 10MB,
  MAXSIZE = 100MB,
  FILEGROWTH = 10% );
GO

-- Set database options
ALTER DATABASE LinuxCompanyDB 
SET RECOVERY FULL,
    AUTO_CLOSE OFF,
    AUTO_SHRINK OFF;
GO

-- Use database
USE LinuxCompanyDB;
GO
```

### Create Application User

```sql
-- Create login
CREATE LOGIN app_user WITH PASSWORD='AppUserPassword123!';
GO

-- Create database user
USE LinuxCompanyDB;
CREATE USER app_user FOR LOGIN app_user;
GO

-- Grant permissions
ALTER ROLE db_datareader ADD MEMBER app_user;
ALTER ROLE db_datawriter ADD MEMBER app_user;
ALTER ROLE db_ddladmin ADD MEMBER app_user;
GO
```

### Sample Tables and Data

```sql
USE LinuxCompanyDB;
GO

-- Create tables
CREATE TABLE Departments (
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName NVARCHAR(100) NOT NULL,
    Location NVARCHAR(100),
    CreatedDate DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Phone NVARCHAR(20),
    HireDate DATE NOT NULL,
    Salary DECIMAL(10,2),
    DepartmentID INT FOREIGN KEY REFERENCES Departments(DepartmentID),
    CreatedDate DATETIME2 DEFAULT GETDATE()
);

-- Insert sample data
INSERT INTO Departments (DepartmentName, Location) VALUES 
('Information Technology', 'Building A'),
('Human Resources', 'Building B'),
('Finance', 'Building C'),
('Sales', 'Building D');

INSERT INTO Employees (FirstName, LastName, Email, Phone, HireDate, Salary, DepartmentID) VALUES
('John', 'Doe', 'john.doe@company.com', '+1-555-0001', '2023-01-15', 75000.00, 1),
('Jane', 'Smith', 'jane.smith@company.com', '+1-555-0002', '2023-02-20', 65000.00, 2),
('Mike', 'Johnson', 'mike.johnson@company.com', '+1-555-0003', '2023-03-10', 80000.00, 1),
('Sarah', 'Wilson', 'sarah.wilson@company.com', '+1-555-0004', '2023-04-05', 70000.00, 4),
('David', 'Brown', 'david.brown@company.com', '+1-555-0005', '2023-05-12', 72000.00, 3);
GO

-- Create indexes
CREATE NONCLUSTERED INDEX IX_Employees_DepartmentID 
ON Employees (DepartmentID);

CREATE NONCLUSTERED INDEX IX_Employees_Email 
ON Employees (Email);
GO
```

[Back to top](#table-of-contents)

## Performance Tuning

### System-Level Optimizations

```bash
# Increase file descriptor limits
echo "mssql soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "mssql hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Set kernel parameters for performance
echo "vm.swappiness = 1" | sudo tee -a /etc/sysctl.conf
echo "vm.dirty_ratio = 15" | sudo tee -a /etc/sysctl.conf
echo "vm.dirty_background_ratio = 5" | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p

# Configure huge pages (optional for large memory systems)
echo "vm.nr_hugepages = 1024" | sudo tee -a /etc/sysctl.conf
```

### SQL Server Performance Configuration

```bash
# Set maximum memory (leave 2-4GB for OS)
TOTAL_RAM_MB=$(free -m | awk 'NR==2{printf "%.0f", $2}')
SQL_MAX_MEMORY=$((TOTAL_RAM_MB - 2048))

sudo /opt/mssql/bin/mssql-conf set memory.memorylimitmb $SQL_MAX_MEMORY

# Enable Query Store for all new databases
sudo /opt/mssql/bin/mssql-conf set querystore.defaultquerystore 1

# Set optimal worker threads
sudo /opt/mssql/bin/mssql-conf set sqlos.maxworkerthreads 0

# Restart to apply settings
sudo systemctl restart mssql-server
```

### Database-Level Performance

```sql
-- Connect and optimize database settings
sqlcmd -S localhost -U SA -P 'YourPassword123!'

USE LinuxCompanyDB;
GO

-- Enable Query Store
ALTER DATABASE LinuxCompanyDB SET QUERY_STORE = ON 
(
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 60,
    MAX_STORAGE_SIZE_MB = 1000,
    QUERY_CAPTURE_MODE = AUTO,
    SIZE_BASED_CLEANUP_MODE = AUTO
);
GO

-- Update statistics
UPDATE STATISTICS Employees;
UPDATE STATISTICS Departments;
GO

-- Check fragmentation and rebuild indexes if needed
SELECT 
    object_name(ips.object_id) as TableName,
    i.name as IndexName,
    ips.avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 10
ORDER BY ips.avg_fragmentation_in_percent DESC;
GO
```

[Back to top](#table-of-contents)

## Monitoring and Maintenance

### System Monitoring Scripts

```bash
# Create monitoring script
cat << 'EOF' > /opt/mssql/scripts/monitor_sqlserver.sh
#!/bin/bash

# SQL Server monitoring script for Linux

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/var/opt/mssql/log/monitoring.log"

echo "[$TIMESTAMP] SQL Server Monitoring Report" >> $LOG_FILE

# Check service status
if systemctl is-active --quiet mssql-server; then
    echo "[$TIMESTAMP] SQL Server service: RUNNING" >> $LOG_FILE
else
    echo "[$TIMESTAMP] SQL Server service: STOPPED" >> $LOG_FILE
fi

# Check memory usage
MEM_USAGE=$(ps aux | grep sqlservr | grep -v grep | awk '{sum+=$6} END {print sum/1024}')
echo "[$TIMESTAMP] SQL Server Memory Usage: ${MEM_USAGE}MB" >> $LOG_FILE

# Check disk space
DISK_USAGE=$(df -h /var/opt/mssql | tail -1 | awk '{print $5}')
echo "[$TIMESTAMP] Data directory disk usage: $DISK_USAGE" >> $LOG_FILE

# Check connections
CONNECTION_COUNT=$(netstat -an | grep :1433 | grep ESTABLISHED | wc -l)
echo "[$TIMESTAMP] Active connections: $CONNECTION_COUNT" >> $LOG_FILE

echo "[$TIMESTAMP] Monitoring complete" >> $LOG_FILE
echo "" >> $LOG_FILE
EOF

# Make script executable
sudo chmod +x /opt/mssql/scripts/monitor_sqlserver.sh

# Create directory for scripts
sudo mkdir -p /opt/mssql/scripts
sudo chown -R mssql:mssql /opt/mssql/scripts
```

### Automated Backup Script

```bash
# Create backup script
cat << 'EOF' > /opt/mssql/scripts/backup_databases.sh
#!/bin/bash

# Automated backup script for SQL Server on Linux

BACKUP_DIR="/var/opt/mssql/backup"
DATE_SUFFIX=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/opt/mssql/log/backup.log"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

# Database backup function
backup_database() {
    local db_name=$1
    local backup_file="${BACKUP_DIR}/${db_name}_Full_${DATE_SUFFIX}.bak"
    
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q \
    "BACKUP DATABASE [$db_name] TO DISK = N'$backup_file' WITH FORMAT, INIT, COMPRESSION, NAME = 'Full Backup of $db_name';"
    
    if [ $? -eq 0 ]; then
        echo "$(date): SUCCESS - Backup of $db_name completed: $backup_file" >> $LOG_FILE
        
        # Compress backup file
        gzip "$backup_file"
        echo "$(date): Backup file compressed: ${backup_file}.gz" >> $LOG_FILE
    else
        echo "$(date): ERROR - Backup of $db_name failed" >> $LOG_FILE
    fi
}

# Backup user databases
backup_database "LinuxCompanyDB"

# Clean up old backups (older than 7 days)
find $BACKUP_DIR -name "*.bak.gz" -mtime +7 -delete
echo "$(date): Old backup files cleaned up" >> $LOG_FILE
EOF

sudo chmod +x /opt/mssql/scripts/backup_databases.sh
```

### Create Cron Jobs

```bash
# Add cron jobs for monitoring and backup
(crontab -l 2>/dev/null; echo "*/15 * * * * /opt/mssql/scripts/monitor_sqlserver.sh") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/mssql/scripts/backup_databases.sh") | crontab -

# Verify cron jobs
crontab -l
```

### Log Rotation Configuration

```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/mssql-server << EOF
/var/opt/mssql/log/errorlog {
    copytruncate
    rotate 5
    weekly
    missingok
    notifempty
    compress
    delaycompress
}

/var/opt/mssql/log/monitoring.log {
    rotate 10
    weekly
    missingok
    notifempty
    compress
    delaycompress
}

/var/opt/mssql/log/backup.log {
    rotate 5
    monthly
    missingok
    notifempty
    compress
    delaycompress
}
EOF
```

[Back to top](#table-of-contents)

## SSL/TLS Configuration

### Production SSL Certificate Setup

```bash
# Obtain SSL certificate from Let's Encrypt (example)
# Install certbot first
sudo yum install -y certbot  # RHEL/CentOS
# sudo apt install -y certbot  # Ubuntu

# Generate certificate (replace with your domain)
sudo certbot certonly --standalone -d your-sqlserver.domain.com

# Copy certificates to SQL Server directory
sudo cp /etc/letsencrypt/live/your-sqlserver.domain.com/fullchain.pem /var/opt/mssql/
sudo cp /etc/letsencrypt/live/your-sqlserver.domain.com/privkey.pem /var/opt/mssql/

# Set proper ownership and permissions
sudo chown mssql:mssql /var/opt/mssql/fullchain.pem /var/opt/mssql/privkey.pem
sudo chmod 600 /var/opt/mssql/fullchain.pem /var/opt/mssql/privkey.pem
```

### Configure SQL Server for SSL

```bash
# Configure SSL certificate
sudo /opt/mssql/bin/mssql-conf set network.tlscert /var/opt/mssql/fullchain.pem
sudo /opt/mssql/bin/mssql-conf set network.tlskey /var/opt/mssql/privkey.pem
sudo /opt/mssql/bin/mssql-conf set network.tlsprotocols 1.2
sudo /opt/mssql/bin/mssql-conf set network.forceencryption 1

# Restart SQL Server
sudo systemctl restart mssql-server

# Test SSL connection
sqlcmd -S localhost -U SA -P 'YourPassword123!' -N -C
```
[Back to top](#table-of-contents)

## High Availability Setup

### Always On Availability Groups Preparation

```bash
# Enable Always On Availability Groups
sudo /opt/mssql/bin/mssql-conf set hadr.hadrenabled 1

# Restart SQL Server
sudo systemctl restart mssql-server

# Create certificate for endpoint authentication
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'MasterKeyPassword123!';
CREATE CERTIFICATE AG_Certificate WITH SUBJECT = 'AG Certificate';
BACKUP CERTIFICATE AG_Certificate TO FILE = '/var/opt/mssql/data/AG_Certificate.cer';
"
```

### Pacemaker Cluster Setup (Basic Example)

```bash
# Install Pacemaker packages
# RHEL/CentOS
sudo yum install -y pacemaker pcs fence-agents-all resource-agents

# Ubuntu
# sudo apt install -y pacemaker pcs fence-agents resource-agents

# Configure Pacemaker authentication
sudo passwd hacluster

# Start and enable services
sudo systemctl start pcsd
sudo systemctl enable pcsd
sudo systemctl start pacemaker
sudo systemctl enable pacemaker

# Create cluster (run on one node)
sudo pcs cluster auth node1 node2 node3
sudo pcs cluster setup --name sqlcluster node1 node2 node3
sudo pcs cluster start --all
sudo pcs cluster enable --all
```

[Back to top](#table-of-contents)

## Troubleshooting

### Common Installation Issues

**Issue: Repository not found**
```bash
# Check if repository file exists
ls -la /etc/yum.repos.d/ | grep mssql

# Re-add repository
sudo curl -o /etc/yum.repos.d/mssql-server.repo \
  https://packages.microsoft.com/config/rhel/8/mssql-server-2022.repo

# Clear cache and try again
sudo yum clean all
sudo yum makecache
```

**Issue: Package dependency conflicts**
```bash
# Check for conflicting packages
rpm -qa | grep mssql

# Remove old versions
sudo yum remove mssql-server-*

# Clean up and reinstall
sudo yum autoremove
sudo yum install -y mssql-server
```

### Service Issues

```bash
# Check SQL Server service status
sudo systemctl status mssql-server -l

# View detailed logs
sudo journalctl -u mssql-server -f

# Check SQL Server error log
sudo tail -f /var/opt/mssql/log/errorlog

# Check system log
sudo tail -f /var/log/messages  # RHEL/CentOS
sudo tail -f /var/log/syslog    # Ubuntu
```

### Memory and Performance Issues

```bash
# Check memory usage
free -h
ps aux | grep sqlservr | grep -v grep

# Check disk I/O
iostat -x 1 5

# Monitor SQL Server processes
top -p $(pgrep -d ',' sqlservr)

# Check for OOM killer activity
dmesg | grep -i "killed process"
grep -i "killed process" /var/log/messages
```

### Network Connectivity Issues

```bash
# Check if SQL Server is listening
sudo netstat -tlnp | grep :1433
sudo ss -tlnp | grep :1433

# Test local connectivity
telnet localhost 1433

# Check firewall rules
sudo firewall-cmd --list-all  # RHEL/CentOS
sudo ufw status verbose       # Ubuntu

# Check SELinux status (RHEL/CentOS)
getenforce
sudo ausearch -m avc -ts recent | grep sql

# Temporarily disable SELinux for testing
sudo setenforce 0

# Check iptables rules
sudo iptables -L -n | grep 1433
```

### Authentication Issues

```sql
-- Reset SA password
sudo /opt/mssql/bin/mssql-conf set-sa-password

-- Check login status
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
SELECT name, is_disabled, create_date, modify_date 
FROM sys.server_principals 
WHERE type = 'S';
"

-- Enable SA login if disabled
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
ALTER LOGIN [sa] ENABLE;
"
```

### Database Corruption Issues

```bash
# Check database integrity
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
USE LinuxCompanyDB;
DBCC CHECKDB('LinuxCompanyDB') WITH NO_INFOMSGS;
"

# Repair database (if needed)
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
USE master;
ALTER DATABASE LinuxCompanyDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DBCC CHECKDB('LinuxCompanyDB', REPAIR_ALLOW_DATA_LOSS);
ALTER DATABASE LinuxCompanyDB SET MULTI_USER;
"
```
[Back to top](#table-of-contents)

## Best Practices

### Security Best Practices

```bash
# 1. Change default SA password regularly
sudo /opt/mssql/bin/mssql-conf set-sa-password

# 2. Create dedicated service account
sudo useradd -r -s /bin/false -U mssqlsvc
sudo /opt/mssql/bin/mssql-conf set sqlagent.databasemailprofile mssqlsvc

# 3. Configure minimal required permissions
# 4. Enable TLS/SSL encryption
# 5. Use firewall to restrict access
# 6. Regular security updates
```

### Performance Best Practices

```bash
# 1. Allocate appropriate memory
TOTAL_RAM_GB=$(free -g | awk 'NR==2{print $2}')
SQL_MAX_MEMORY_MB=$(( (TOTAL_RAM_GB - 2) * 1024 ))
sudo /opt/mssql/bin/mssql-conf set memory.memorylimitmb $SQL_MAX_MEMORY_MB

# 2. Place data and log files on separate drives
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultdatadir /data/mssql/data
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultlogdir /logs/mssql/logs

# 3. Configure TempDB properly
sudo /opt/mssql/bin/mssql-conf set tempdb.defaultdatadir /tempdb/data
sudo /opt/mssql/bin/mssql-conf set tempdb.defaultlogdir /tempdb/logs

# 4. Enable Query Store for performance monitoring
# 5. Regular index maintenance
# 6. Monitor and optimize queries
```

### Maintenance Best Practices

```bash
# 1. Automated backups
cat << 'EOF' > /opt/mssql/scripts/maintenance.sh
#!/bin/bash

# Weekly maintenance script

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/var/opt/mssql/log/maintenance.log"

echo "[$TIMESTAMP] Starting weekly maintenance" >> $LOG_FILE

# Update statistics
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
EXEC sp_updatestats;
" >> $LOG_FILE 2>&1

# Rebuild fragmented indexes
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
USE LinuxCompanyDB;
DECLARE @sql NVARCHAR(MAX) = '';
SELECT @sql = @sql + 'ALTER INDEX ' + i.name + ' ON ' + OBJECT_NAME(i.object_id) + ' REBUILD;' + CHAR(13)
FROM sys.indexes i
INNER JOIN sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ps
    ON i.object_id = ps.object_id AND i.index_id = ps.index_id
WHERE ps.avg_fragmentation_in_percent > 30 AND i.index_id > 0;
EXEC sp_executesql @sql;
" >> $LOG_FILE 2>&1

# Clean up old backup files
find /var/opt/mssql/backup -name "*.bak.gz" -mtime +30 -delete

echo "[$TIMESTAMP] Weekly maintenance completed" >> $LOG_FILE
EOF

chmod +x /opt/mssql/scripts/maintenance.sh

# Add to crontab (run weekly on Sunday at 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * 0 /opt/mssql/scripts/maintenance.sh") | crontab -
```

### Disaster Recovery Setup

```bash
# 1. Configure log shipping
mkdir -p /var/opt/mssql/backup/logship

# 2. Setup Always On Availability Groups for critical databases
# 3. Regular disaster recovery testing
# 4. Document recovery procedures

cat << 'EOF' > /opt/mssql/scripts/dr_test.sh
#!/bin/bash

# Disaster Recovery Test Script

DR_LOG="/var/opt/mssql/log/dr_test.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting DR test" >> $DR_LOG

# Test restore from latest backup
LATEST_BACKUP=$(ls -t /var/opt/mssql/backup/*.bak.gz | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    echo "[$TIMESTAMP] Testing restore from: $LATEST_BACKUP" >> $DR_LOG
    
    # Uncompress backup
    gunzip -c "$LATEST_BACKUP" > /tmp/test_restore.bak
    
    # Perform test restore
    sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
    RESTORE DATABASE [TestRestore] FROM DISK = '/tmp/test_restore.bak'
    WITH MOVE 'LinuxCompanyDB_Data' TO '/tmp/TestRestore.mdf',
         MOVE 'LinuxCompanyDB_Log' TO '/tmp/TestRestore.ldf',
         REPLACE;
    " >> $DR_LOG 2>&1
    
    # Clean up test database
    sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
    DROP DATABASE [TestRestore];
    " >> $DR_LOG 2>&1
    
    # Clean up files
    rm -f /tmp/test_restore.bak /tmp/TestRestore.*
    
    echo "[$TIMESTAMP] DR test completed successfully" >> $DR_LOG
else
    echo "[$TIMESTAMP] No backup files found for DR test" >> $DR_LOG
fi
EOF

chmod +x /opt/mssql/scripts/dr_test.sh
```
[Back to top](#table-of-contents)

## Advanced Configuration

### Container Integration

```bash
# Run SQL Server alongside application containers
cat << 'EOF' > docker-compose.prod.yml
version: '3.8'

services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: sqlserver-prod
    restart: unless-stopped
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=ProductionPassword123!
      - MSSQL_PID=Standard
    ports:
      - "1433:1433"
    volumes:
      - sqlserver_data:/var/opt/mssql
      - sqlserver_logs:/var/opt/mssql/log
      - sqlserver_backups:/var/opt/mssql/backup
    networks:
      - app_network
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'ProductionPassword123!' -Q 'SELECT 1'"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  app:
    build: ./app
    depends_on:
      sqlserver:
        condition: service_healthy
    environment:
      - CONNECTION_STRING=Server=sqlserver,1433;Database=LinuxCompanyDB;User Id=app_user;Password=AppPassword123!;
    networks:
      - app_network

volumes:
  sqlserver_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/sqlserver/data
  sqlserver_logs:
    driver: local  
    driver_opts:
      type: none
      o: bind
      device: /opt/sqlserver/logs
  sqlserver_backups:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/sqlserver/backups

networks:
  app_network:
    driver: bridge
EOF
```

### Monitoring Integration

```bash
# Configure monitoring with Prometheus and Grafana
# Install SQL Server exporter
wget https://github.com/awaragi/prometheus-mssql-exporter/releases/download/v0.1.5/prometheus-mssql-exporter-0.1.5.linux-amd64.tar.gz
tar xzf prometheus-mssql-exporter-0.1.5.linux-amd64.tar.gz
sudo mv prometheus-mssql-exporter /usr/local/bin/

# Create configuration
cat << 'EOF' > /etc/prometheus-mssql-exporter.yml
connection_string: "server=localhost;user id=monitoring_user;password=MonitoringPassword123!;port=1433;database=master"
query_timeout: 5
max_idle_connections: 3
max_open_connections: 3

queries:
  - name: "database_size"
    help: "Database size in bytes"
    query: |
      SELECT 
        db.name as database_name,
        SUM(mf.size * 8192) as size_bytes
      FROM sys.databases db
      JOIN sys.master_files mf ON db.database_id = mf.database_id
      WHERE db.database_id > 4
      GROUP BY db.name
    metrics:
      - database_name:
          usage: "LABEL"
          description: "Database name"
      - size_bytes:
          usage: "GAUGE"
          description: "Size in bytes"

  - name: "active_connections"  
    help: "Number of active connections per database"
    query: |
      SELECT 
        DB_NAME(database_id) as database_name,
        COUNT(*) as connection_count
      FROM sys.dm_exec_sessions
      WHERE database_id > 0
      GROUP BY database_id
    metrics:
      - database_name:
          usage: "LABEL"
          description: "Database name"
      - connection_count:
          usage: "GAUGE"
          description: "Active connections"
EOF

# Create systemd service
cat << 'EOF' > /etc/systemd/system/prometheus-mssql-exporter.service
[Unit]
Description=Prometheus SQL Server Exporter
After=network.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecStart=/usr/local/bin/prometheus-mssql-exporter -config-file /etc/prometheus-mssql-exporter.yml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable prometheus-mssql-exporter
sudo systemctl start prometheus-mssql-exporter
```

### Automation Scripts

```bash
# Health check script
cat << 'EOF' > /opt/mssql/scripts/health_check.sh
#!/bin/bash

# Comprehensive health check for SQL Server on Linux

HEALTH_LOG="/var/opt/mssql/log/health_check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
ALERT_EMAIL="admin@company.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to log and print
log_message() {
    local level=$1
    local message=$2
    echo -e "${level}[$TIMESTAMP] $message${NC}"
    echo "[$TIMESTAMP] $message" >> $HEALTH_LOG
}

# Check SQL Server service
check_service() {
    if systemctl is-active --quiet mssql-server; then
        log_message $GREEN "✓ SQL Server service is running"
        return 0
    else
        log_message $RED "✗ SQL Server service is not running"
        return 1
    fi
}

# Check database connectivity
check_connectivity() {
    if sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "SELECT 1" >/dev/null 2>&1; then
        log_message $GREEN "✓ Database connectivity OK"
        return 0
    else
        log_message $RED "✗ Cannot connect to database"
        return 1
    fi
}

# Check disk space
check_disk_space() {
    local threshold=85
    local usage=$(df -h /var/opt/mssql | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ $usage -lt $threshold ]; then
        log_message $GREEN "✓ Disk space OK ($usage% used)"
        return 0
    else
        log_message $YELLOW "⚠ Disk space warning ($usage% used, threshold: $threshold%)"
        return 1
    fi
}

# Check memory usage
check_memory() {
    local sql_memory=$(ps aux | grep sqlservr | grep -v grep | awk '{sum+=$6} END {print sum/1024}')
    local total_memory=$(free -m | awk 'NR==2{print $2}')
    local usage_percent=$(echo "scale=2; $sql_memory * 100 / $total_memory" | bc)
    
    log_message $GREEN "✓ SQL Server memory usage: ${sql_memory}MB (${usage_percent}% of total)"
}

# Check error log for issues
check_error_log() {
    local error_count=$(tail -100 /var/opt/mssql/log/errorlog | grep -i error | wc -l)
    
    if [ $error_count -eq 0 ]; then
        log_message $GREEN "✓ No recent errors in SQL Server log"
        return 0
    else
        log_message $YELLOW "⚠ Found $error_count errors in recent log entries"
        return 1
    fi
}

# Main health check
main() {
    log_message $NC "Starting SQL Server health check..."
    
    local failed_checks=0
    
    check_service || ((failed_checks++))
    check_connectivity || ((failed_checks++))
    check_disk_space || ((failed_checks++))
    check_memory
    check_error_log || ((failed_checks++))
    
    if [ $failed_checks -eq 0 ]; then
        log_message $GREEN "✓ All health checks passed"
        exit 0
    else
        log_message $RED "✗ $failed_checks health check(s) failed"
        # Send alert email (optional)
        # echo "SQL Server health check failed on $(hostname)" | mail -s "SQL Server Alert" $ALERT_EMAIL
        exit 1
    fi
}

main
EOF

chmod +x /opt/mssql/scripts/health_check.sh

# Add to cron for regular health checks
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/mssql/scripts/health_check.sh") | crontab -
```
[Back to top](#table-of-contents)

## Migration and Upgrade

### Migration from Windows to Linux

```bash
# 1. Backup databases from Windows SQL Server
# 2. Transfer backup files to Linux server
# 3. Restore on Linux SQL Server

# Example restore script
cat << 'EOF' > /opt/mssql/scripts/migrate_from_windows.sh
#!/bin/bash

# Migration script from Windows SQL Server to Linux

BACKUP_DIR="/var/opt/mssql/backup/migration"
LOG_FILE="/var/opt/mssql/log/migration.log"

# Create migration directory
mkdir -p $BACKUP_DIR

# Function to restore database
restore_database() {
    local backup_file=$1
    local database_name=$2
    
    echo "Restoring $database_name from $backup_file" >> $LOG_FILE
    
    sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
    RESTORE DATABASE [$database_name] FROM DISK = '$backup_file'
    WITH MOVE '$database_name' TO '/var/opt/mssql/data/${database_name}.mdf',
         MOVE '${database_name}_Log' TO '/var/opt/mssql/data/${database_name}.ldf',
         REPLACE, STATS = 10;
    " >> $LOG_FILE 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Successfully restored $database_name" >> $LOG_FILE
    else
        echo "Failed to restore $database_name" >> $LOG_FILE
    fi
}

# Restore databases
# restore_database "$BACKUP_DIR/Database1.bak" "Database1"
# restore_database "$BACKUP_DIR/Database2.bak" "Database2"

echo "Migration completed. Check log file: $LOG_FILE"
EOF

chmod +x /opt/mssql/scripts/migrate_from_windows.sh
```

### Upgrade SQL Server

```bash
# Check current version
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "SELECT @@VERSION"

# Backup all databases before upgrade
/opt/mssql/scripts/backup_databases.sh

# Update repository (if needed)
sudo yum update mssql-server  # RHEL/CentOS
# sudo apt update && sudo apt upgrade mssql-server  # Ubuntu

# Restart service after upgrade
sudo systemctl restart mssql-server

# Verify upgrade
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "SELECT @@VERSION"

# Update database compatibility levels
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
ALTER DATABASE [LinuxCompanyDB] SET COMPATIBILITY_LEVEL = 160;  -- SQL Server 2022
"
```
[Back to top](#table-of-contents)

## Final Notes and Resources

### Documentation and Support

- **Official Documentation**: [SQL Server on Linux Documentation](https://docs.microsoft.com/en-us/sql/linux/)
- **Community Support**: [SQL Server Community](https://techcommunity.microsoft.com/t5/sql-server/ct-p/SQLServer)
- **GitHub Issues**: [SQL Server Docker](https://github.com/microsoft/mssql-docker)
- **Red Hat Support**: [SQL Server on RHEL](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/deploying_different_types_of_servers/using-sql-server-on-red-hat-enterprise-linux_deploying-different-types-of-servers)

### License Considerations

```bash
# Check current license/edition
sqlcmd -S localhost -U SA -P 'YourPassword123!' -Q "
SELECT 
    SERVERPROPERTY('Edition') AS Edition,
    SERVERPROPERTY('ProductLevel') AS ServicePack,
    SERVERPROPERTY('ProductVersion') AS Version,
    SERVERPROPERTY('LicenseType') AS LicenseType;
"

# Change edition (requires restart)
sudo /opt/mssql/bin/mssql-conf set-edition
```

### Performance Baseline

```sql
-- Create baseline performance queries
-- Save as /opt/mssql/scripts/performance_baseline.sql

-- CPU utilization
SELECT 
    record.value('(./Record/@id)[1]', 'int') AS record_id,
    record.value('(./Record/SchedulerMonitorEvent/SystemHealth/SystemIdle)[1]', 'int') AS system_idle,
    record.value('(./Record/SchedulerMonitorEvent/SystemHealth/ProcessUtilization)[1]', 'int') AS sql_cpu_utilization,
    DATEADD(ms, -1 * (ts_now - [timestamp]), GETDATE()) AS event_time
FROM (
    SELECT timestamp, CONVERT(xml, record) AS record, ts_now
    FROM sys.dm_os_ring_buffers
    CROSS JOIN (SELECT cpu_ticks / (cpu_ticks/ms_ticks) AS ts_now FROM sys.dm_os_sys_info) AS t
    WHERE ring_buffer_type = N'RING_BUFFER_SCHEDULER_MONITOR'
        AND record LIKE '%<SystemHealth>%'
) AS x
ORDER BY record_id DESC;

-- Memory usage
SELECT 
    (total_physical_memory_kb/1024) AS total_physical_memory_mb,
    (available_physical_memory_kb/1024) AS available_physical_memory_mb,
    (total_page_file_kb/1024) AS total_page_file_mb,
    (available_page_file_kb/1024) AS available_page_file_mb,
    (system_memory_state_desc) AS system_memory_state
FROM sys.dm_os_sys_memory;

-- Wait statistics
SELECT TOP 10
    wait_type,
    wait_time_ms,
    percentage = ROUND(wait_time_ms * 100.0 / SUM(wait_time_ms) OVER(), 2),
    avg_wait_time_ms = ROUND(wait_time_ms * 1.0 / waiting_tasks_count, 2)
FROM sys.dm_os_wait_stats
WHERE waiting_tasks_count > 0
    AND wait_type NOT IN (
        'CLR_SEMAPHORE','LAZYWRITER_SLEEP','RESOURCE_QUEUE','SLEEP_TASK',
        'SLEEP_SYSTEMTASK','SQLTRACE_BUFFER_FLUSH','WAITFOR', 'LOGMGR_QUEUE',
        'CHECKPOINT_QUEUE','REQUEST_FOR_DEADLOCK_SEARCH','XE_TIMER_EVENT',
        'BROKER_TO_FLUSH','BROKER_TASK_STOP','CLR_MANUAL_EVENT','CLR_AUTO_EVENT',
        'DISPATCHER_QUEUE_SEMAPHORE','FT_IFTS_SCHEDULER_IDLE_WAIT','XE_DISPATCHER_WAIT',
        'XE_DISPATCHER_JOIN','SQLTRACE_INCREMENTAL_FLUSH_SLEEP'
    )
ORDER BY wait_time_ms DESC;
```
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
      Senior Database Engineer (DBE) / Senior Database Reliability Engineer (DBRE) / Senior DBA / DataOps Engineer
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

---


