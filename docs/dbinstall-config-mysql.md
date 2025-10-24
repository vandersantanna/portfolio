# 🐬 MySQL Installation and Configuration Guide <img src="https://www.mysql.com/favicon.ico" alt="MySQL" height="24" style="vertical-align:middle;margin-right:8px;">

*Complete installation and configuration guide for MySQL 8.0 across multiple platforms*

![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows%20Server-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Linux Installations](#-linux-installations)
  - [Red Hat Enterprise Linux 9/10](#red-hat-enterprise-linux-910)
  - [Ubuntu 22.04 LTS](#ubuntu-2204-lts)
- [Windows Server Installation](#-windows-server-installation)
- [Cloud Deployments](#-cloud-deployments)
  - [Amazon Web Services (AWS)](#amazon-web-services-aws)
  - [Microsoft Azure](#microsoft-azure)
  - [Google Cloud Platform (GCP)](#google-cloud-platform-gcp)
- [Post-Installation Configuration](#-post-installation-configuration)
- [Security Hardening](#-security-hardening)
- [Performance Tuning](#-performance-tuning)
- [Backup and Recovery](#-backup-and-recovery)
- [Monitoring and Maintenance](#-monitoring-and-maintenance)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

This comprehensive guide covers MySQL 8.0 installation and configuration across:

- **Operating Systems**: Red Hat Enterprise Linux 9/10, Ubuntu 22.04 LTS, Windows Server 2019/2022
- **Cloud Platforms**: AWS RDS, Azure Database for MySQL, Google Cloud SQL
- **Deployment Types**: Standalone, Master-Slave, Master-Master, Cluster

### Prerequisites

- Administrative access to target system
- Network connectivity for package downloads
- Minimum 4GB RAM (8GB+ recommended for production)
- 20GB+ available disk space

---

## 🐧 Linux Installations

### Red Hat Enterprise Linux 9/10

#### Method 1: Using MySQL Official Repository

```bash
# Download and install MySQL repository
wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
sudo dnf install mysql80-community-release-el9-1.noarch.rpm -y

# Update package index
sudo dnf update -y

# Install MySQL Server
sudo dnf install mysql-community-server -y

# Start and enable MySQL service
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Get temporary root password
sudo grep 'temporary password' /var/log/mysqld.log

# Secure MySQL installation
sudo mysql_secure_installation
```

#### Method 2: Using DNF Module (RHEL 9/10)

```bash
# List available MySQL modules
sudo dnf module list mysql

# Install MySQL 8.0 module
sudo dnf module install mysql:8.0 -y

# Start and enable service
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Secure installation
sudo mysql_secure_installation
```

#### Configuration File Location
- **Main config**: `/etc/my.cnf`
- **Additional configs**: `/etc/my.cnf.d/`
- **Data directory**: `/var/lib/mysql`
- **Log files**: `/var/log/mysqld.log`

### Ubuntu 22.04 LTS

#### Method 1: Using APT Package Manager

```bash
# Update package index
sudo apt update

# Install MySQL Server
sudo apt install mysql-server -y

# Start and enable MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure MySQL installation
sudo mysql_secure_installation

# Check service status
sudo systemctl status mysql
```

#### Method 2: Using MySQL Official Repository

```bash
# Download MySQL APT repository
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb

# Install repository package
sudo dpkg -i mysql-apt-config_0.8.29-1_all.deb

# Update package index
sudo apt update

# Install MySQL Server
sudo apt install mysql-server -y

# Configure MySQL
sudo mysql_secure_installation
```

#### Configuration File Locations
- **Main config**: `/etc/mysql/mysql.conf.d/mysqld.cnf`
- **Additional configs**: `/etc/mysql/conf.d/`
- **Data directory**: `/var/lib/mysql`
- **Log files**: `/var/log/mysql/error.log`

#### Ubuntu-Specific Commands

```bash
# Connect to MySQL as root (Ubuntu uses auth_socket)
sudo mysql

# Create administrative user
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

---

## 🖥️ Windows Server Installation

### Prerequisites
- Windows Server 2019/2022
- Administrator privileges
- .NET Framework 4.8+

### Installation Steps

#### Method 1: MySQL Installer (Recommended)

```powershell
# Download MySQL Installer from official website
# https://dev.mysql.com/downloads/installer/

# Run as Administrator
.\mysql-installer-community-8.0.35.0.msi

# Select "Server only" or "Custom" installation
# Configure MySQL Server:
# - Config Type: Server Computer
# - Connectivity: TCP/IP, Port 3306
# - Authentication Method: Strong Password Encryption
# - Root Password: Set secure password
```

#### Method 2: ZIP Archive Installation

```powershell
# Create MySQL directory
New-Item -ItemType Directory -Path "C:\mysql"

# Extract ZIP archive to C:\mysql
# Add MySQL bin directory to PATH
$env:PATH += ";C:\mysql\bin"

# Initialize MySQL data directory
mysqld --initialize-insecure --basedir=C:\mysql --datadir=C:\mysql\data

# Install MySQL as Windows Service
mysqld --install MySQL --defaults-file=C:\mysql\my.ini

# Start MySQL service
net start MySQL

# Connect and set root password
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'secure_password';
```

### Windows Configuration

#### Sample my.ini Configuration

```ini
[mysqld]
# General settings
basedir = C:/mysql
datadir = C:/mysql/data
port = 3306
bind-address = 127.0.0.1

# Performance settings
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
max_connections = 200

# Security settings
local_infile = 0
skip_show_database

# Log settings
log-error = C:/mysql/data/mysql_error.log
slow_query_log = 1
slow_query_log_file = C:/mysql/data/mysql_slow.log
long_query_time = 2

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4
```

#### Windows Service Management

```powershell
# Service management commands
net start MySQL
net stop MySQL
net restart MySQL

# Check service status
Get-Service -Name MySQL

# Configure service startup
Set-Service -Name MySQL -StartupType Automatic
```

---

## ☁️ Cloud Deployments

### Amazon Web Services (AWS)

#### AWS RDS MySQL Deployment

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure

# Create RDS MySQL instance
aws rds create-db-instance \
    --db-instance-identifier mysql-prod-01 \
    --db-instance-class db.t3.medium \
    --engine mysql \
    --engine-version 8.0.35 \
    --master-username admin \
    --master-user-password 'SecurePassword123!' \
    --allocated-storage 100 \
    --storage-type gp2 \
    --vpc-security-group-ids sg-12345678 \
    --db-subnet-group-name default \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted \
    --enable-performance-insights
```

#### AWS RDS Configuration

```bash
# Describe RDS instance
aws rds describe-db-instances --db-instance-identifier mysql-prod-01

# Create parameter group for custom configuration
aws rds create-db-parameter-group \
    --db-parameter-group-name mysql80-custom \
    --db-parameter-group-family mysql8.0 \
    --description "Custom MySQL 8.0 parameters"

# Modify parameters
aws rds modify-db-parameter-group \
    --db-parameter-group-name mysql80-custom \
    --parameters "ParameterName=innodb_buffer_pool_size,ParameterValue={DBInstanceClassMemory*3/4},ApplyMethod=pending-reboot"

# Apply parameter group to instance
aws rds modify-db-instance \
    --db-instance-identifier mysql-prod-01 \
    --db-parameter-group-name mysql80-custom \
    --apply-immediately
```

#### Connection Example

```bash
# Connect to RDS MySQL
mysql -h mysql-prod-01.cluster-xyz.us-east-1.rds.amazonaws.com \
      -u admin -p \
      --ssl-mode=REQUIRED
```

### Microsoft Azure

#### Azure Database for MySQL Deployment

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name mysql-rg --location eastus

# Create Azure Database for MySQL
az mysql flexible-server create \
    --resource-group mysql-rg \
    --name mysql-server-01 \
    --location eastus \
    --admin-user mysqladmin \
    --admin-password 'SecurePassword123!' \
    --sku-name Standard_B2s \
    --tier Burstable \
    --compute-generation Gen5 \
    --storage-size 100 \
    --backup-retention 7 \
    --geo-redundant-backup Enabled \
    --version 8.0.21
```

#### Azure MySQL Configuration

```bash
# List server configurations
az mysql flexible-server parameter list \
    --resource-group mysql-rg \
    --server-name mysql-server-01

# Update server parameter
az mysql flexible-server parameter set \
    --resource-group mysql-rg \
    --server-name mysql-server-01 \
    --name innodb_buffer_pool_size \
    --value 2147483648

# Configure firewall rule
az mysql flexible-server firewall-rule create \
    --resource-group mysql-rg \
    --name mysql-server-01 \
    --rule-name AllowMyIP \
    --start-ip-address 203.0.113.0 \
    --end-ip-address 203.0.113.255
```

#### Connection Example

```bash
# Connect to Azure MySQL
mysql -h mysql-server-01.mysql.database.azure.com \
      -u mysqladmin \
      -p \
      --ssl-mode=REQUIRED \
      --ssl-ca=/path/to/DigiCertGlobalRootG2.crt.pem
```

### Google Cloud Platform (GCP)

#### Cloud SQL MySQL Deployment

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize gcloud
gcloud init

# Create Cloud SQL MySQL instance
gcloud sql instances create mysql-instance-01 \
    --database-version=MYSQL_8_0 \
    --tier=db-n1-standard-2 \
    --region=us-central1 \
    --storage-type=SSD \
    --storage-size=100GB \
    --backup-start-time=03:00 \
    --enable-bin-log \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=04 \
    --authorized-networks=203.0.113.0/24
```

#### GCP Cloud SQL Configuration

```bash
# Set root password
gcloud sql users set-password root \
    --host=% \
    --instance=mysql-instance-01 \
    --password='SecurePassword123!'

# Create database
gcloud sql databases create production_db \
    --instance=mysql-instance-01

# Create user
gcloud sql users create appuser \
    --host=% \
    --instance=mysql-instance-01 \
    --password='AppPassword123!'

# Update instance configuration
gcloud sql instances patch mysql-instance-01 \
    --database-flags innodb_buffer_pool_size=2147483648,max_connections=500
```

#### Connection Example

```bash
# Connect using Cloud SQL Proxy
./cloud_sql_proxy -instances=project-id:us-central1:mysql-instance-01=tcp:3306 &

# Connect to MySQL
mysql -h 127.0.0.1 -u root -p
```

---

## ⚙️ Post-Installation Configuration

### Essential Configuration Settings

#### Sample my.cnf for Production

```ini
[mysqld]
# Server identification
server-id = 1
bind-address = 0.0.0.0
port = 3306

# Character set and collation
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Storage engine
default-storage-engine = InnoDB

# Memory settings
innodb_buffer_pool_size = 4G
innodb_buffer_pool_instances = 4
innodb_log_buffer_size = 64M
innodb_log_file_size = 1G
innodb_log_files_in_group = 2

# Connection settings
max_connections = 500
max_user_connections = 450
max_connect_errors = 1000000
connect_timeout = 60
wait_timeout = 28800
interactive_timeout = 28800

# Query cache (disabled in MySQL 8.0)
# query_cache_type = 0
# query_cache_size = 0

# Logging
log-error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
log_queries_not_using_indexes = 1
log_throttle_queries_not_using_indexes = 60

# Binary logging
log-bin = /var/log/mysql/mysql-bin
binlog_format = ROW
binlog_row_image = FULL
expire_logs_days = 7
max_binlog_size = 500M
sync_binlog = 1

# Replication settings
gtid_mode = ON
enforce_gtid_consistency = ON
log_slave_updates = ON
relay_log_recovery = ON

# Security settings
local_infile = 0
secure_file_priv = /var/lib/mysql-files/

# Performance settings
innodb_flush_log_at_trx_commit = 1
innodb_flush_method = O_DIRECT
innodb_io_capacity = 200
innodb_io_capacity_max = 400
innodb_read_io_threads = 8
innodb_write_io_threads = 8

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4
```

### Database Initialization

```sql
-- Create administrative user
CREATE USER 'dbadmin'@'localhost' IDENTIFIED BY 'SecureAdminPass123!';
GRANT ALL PRIVILEGES ON *.* TO 'dbadmin'@'localhost' WITH GRANT OPTION;

-- Create application user
CREATE USER 'appuser'@'%' IDENTIFIED BY 'SecureAppPass123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_database.* TO 'appuser'@'%';

-- Create read-only user for reporting
CREATE USER 'readonly'@'%' IDENTIFIED BY 'ReadOnlyPass123!';
GRANT SELECT ON app_database.* TO 'readonly'@'%';

-- Create backup user
CREATE USER 'backup'@'localhost' IDENTIFIED BY 'BackupPass123!';
GRANT SELECT, SHOW DATABASES, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER ON *.* TO 'backup'@'localhost';
GRANT REPLICATION CLIENT ON *.* TO 'backup'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;
```

---

## 🔒 Security Hardening

### MySQL Security Best Practices

#### 1. Secure Installation Checklist

```bash
# Run MySQL secure installation
mysql_secure_installation

# Verify security settings
mysql -u root -p -e "
SELECT User, Host FROM mysql.user WHERE User = '';
SELECT User, Host FROM mysql.user WHERE User = 'root' AND Host != 'localhost';
SHOW DATABASES LIKE 'test';
SELECT * FROM mysql.user WHERE authentication_string = '' OR authentication_string IS NULL;
"
```

#### 2. User Account Management

```sql
-- Password validation component
INSTALL COMPONENT 'file://component_validate_password';

-- Check password validation settings
SHOW VARIABLES LIKE 'validate_password%';

-- Set password validation policy
SET GLOBAL validate_password.policy = 'STRONG';
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_char_count = 1;

-- Create users with strong passwords
CREATE USER 'secure_user'@'192.168.1.%' IDENTIFIED BY 'StrongP@ssw0rd123!';

-- Set password expiration
ALTER USER 'appuser'@'%' PASSWORD EXPIRE INTERVAL 90 DAY;

-- Lock unused accounts
ALTER USER 'unused_user'@'%' ACCOUNT LOCK;
```

#### 3. Network Security

```sql
-- Restrict root login
UPDATE mysql.user SET Host = 'localhost' WHERE User = 'root' AND Host = '%';
FLUSH PRIVILEGES;

-- Remove anonymous users
DELETE FROM mysql.user WHERE User = '';

-- Remove test database
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db = 'test' OR Db = 'test\_%';

FLUSH PRIVILEGES;
```

#### 4. SSL/TLS Configuration

```bash
# Generate SSL certificates (self-signed)
mysql_ssl_rsa_setup --datadir=/var/lib/mysql

# Verify SSL is enabled
mysql -u root -p -e "SHOW VARIABLES LIKE '%ssl%';"
```

```sql
-- Require SSL for specific users
ALTER USER 'appuser'@'%' REQUIRE SSL;

-- Create SSL-required user
CREATE USER 'ssl_user'@'%' IDENTIFIED BY 'SecureSSLPass123!' REQUIRE SSL;
GRANT SELECT, INSERT ON app_database.* TO 'ssl_user'@'%';
```

### Firewall Configuration

#### Linux (iptables)

```bash
# Allow MySQL port
sudo iptables -A INPUT -p tcp --dport 3306 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 3306 -j DROP

# Save rules (RHEL/CentOS)
sudo service iptables save

# Save rules (Ubuntu)
sudo iptables-save > /etc/iptables/rules.v4
```

#### Linux (firewalld - RHEL/CentOS)

```bash
# Add MySQL service
sudo firewall-cmd --permanent --add-service=mysql
sudo firewall-cmd --permanent --add-port=3306/tcp

# Restrict to specific source
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="mysql" accept'

# Reload firewall
sudo firewall-cmd --reload
```

---

## 🚀 Performance Tuning

### Memory Configuration

#### InnoDB Buffer Pool Sizing

```sql
-- Check current memory usage
SELECT 
    FORMAT(@@innodb_buffer_pool_size/1024/1024/1024, 2) AS 'Buffer Pool Size (GB)',
    FORMAT((SELECT SUM(data_length + index_length) FROM information_schema.tables WHERE engine = 'InnoDB')/1024/1024/1024, 2) AS 'InnoDB Data Size (GB)';

-- Monitor buffer pool efficiency
SELECT 
    ROUND((Innodb_buffer_pool_read_requests - Innodb_buffer_pool_reads) / Innodb_buffer_pool_read_requests * 100, 2) AS 'Buffer Pool Hit Ratio %'
FROM 
    (SELECT VARIABLE_VALUE AS Innodb_buffer_pool_read_requests FROM performance_schema.global_status WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests') AS t1,
    (SELECT VARIABLE_VALUE AS Innodb_buffer_pool_reads FROM performance_schema.global_status WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads') AS t2;
```

### Query Optimization

#### Performance Schema Configuration

```sql
-- Enable Performance Schema
UPDATE performance_schema.setup_instruments 
SET ENABLED = 'YES' 
WHERE NAME LIKE 'statement/%';

-- Enable statement tracking
UPDATE performance_schema.setup_consumers 
SET ENABLED = 'YES' 
WHERE NAME LIKE '%statements%';

-- Top 10 slowest queries
SELECT 
    SCHEMA_NAME,
    FORMAT(TIMER_WAIT/1000000000000,6) AS 'Duration (sec)',
    SQL_TEXT,
    FORMAT(ROWS_EXAMINED,0) AS 'Rows Examined',
    FORMAT(ROWS_SENT,0) AS 'Rows Sent'
FROM performance_schema.events_statements_history_long 
WHERE SCHEMA_NAME IS NOT NULL 
ORDER BY TIMER_WAIT DESC 
LIMIT 10;
```

#### Index Optimization

```sql
-- Find tables without primary key
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME
FROM information_schema.TABLES t
WHERE TABLE_TYPE = 'BASE TABLE'
    AND NOT EXISTS (
        SELECT * FROM information_schema.STATISTICS s 
        WHERE s.TABLE_SCHEMA = t.TABLE_SCHEMA 
            AND s.TABLE_NAME = t.TABLE_NAME 
            AND s.INDEX_NAME = 'PRIMARY'
    );

-- Find unused indexes
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME,
    COUNT_FETCH,
    COUNT_INSERT,
    COUNT_UPDATE,
    COUNT_DELETE
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
    AND COUNT_FETCH = 0
    AND OBJECT_SCHEMA != 'mysql'
ORDER BY OBJECT_SCHEMA, OBJECT_NAME;
```

### Connection Pool Optimization

```sql
-- Monitor connection usage
SELECT 
    PROCESSLIST_USER as 'User',
    PROCESSLIST_HOST as 'Host',
    COUNT(*) as 'Connections',
    PROCESSLIST_STATE as 'State'
FROM performance_schema.threads 
WHERE TYPE = 'FOREGROUND'
GROUP BY PROCESSLIST_USER, PROCESSLIST_HOST, PROCESSLIST_STATE
ORDER BY Connections DESC;

-- Connection history
SELECT 
    CONNECTION_TYPE,
    COUNT(*) as 'Total Connections'
FROM performance_schema.accounts
WHERE USER IS NOT NULL
GROUP BY CONNECTION_TYPE;
```

---

## 💾 Backup and Recovery

### Logical Backups with mysqldump

#### Full Database Backup

```bash
#!/bin/bash
# Full database backup script

DB_USER="backup_user"
DB_PASS="BackupPass123!"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Full backup
mysqldump \
    --user=$DB_USER \
    --password=$DB_PASS \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --all-databases \
    --master-data=2 \
    --flush-logs \
    --compress | gzip > $BACKUP_DIR/full_backup_$DATE.sql.gz

# Verify backup
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_DIR/full_backup_$DATE.sql.gz"
    
    # Remove backups older than 7 days
    find $BACKUP_DIR -name "full_backup_*.sql.gz" -mtime +7 -delete
else
    echo "Backup failed!"
    exit 1
fi
```

#### Incremental Backup with Binary Logs

```bash
#!/bin/bash
# Binary log backup script

MYSQL_USER="backup_user"
MYSQL_PASS="BackupPass123!"
BACKUP_DIR="/backup/mysql/binlogs"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Flush logs to create new binary log file
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "FLUSH LOGS;"

# Get binary log files
BINLOGS=$(mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SHOW BINARY LOGS;" | awk '{print $1}' | grep -v Log_name)

# Copy binary log files
for log in $BINLOGS; do
    if [ -f "/var/lib/mysql/$log" ]; then
        cp "/var/lib/mysql/$log" "$BACKUP_DIR/${log}_$DATE"
        gzip "$BACKUP_DIR/${log}_$DATE"
    fi
done

echo "Binary log backup completed: $BACKUP_DIR"
```

### Physical Backup with MySQL Enterprise Backup

```bash
# Install MySQL Enterprise Backup (requires license)
# Download from Oracle support

# Full backup
mysqlbackup \
    --user=backup_user \
    --password=BackupPass123! \
    --backup-dir=/backup/mysql/physical \
    backup-and-apply-log

# Incremental backup
mysqlbackup \
    --user=backup_user \
    --password=BackupPass123! \
    --backup-dir=/backup/mysql/incremental \
    --incremental \
    --incremental-base=dir:/backup/mysql/physical \
    backup
```

### Point-in-Time Recovery

```bash
#!/bin/bash
# Point-in-time recovery script

BACKUP_FILE="/backup/mysql/full_backup_20241001_030000.sql.gz"
BINLOG_DIR="/backup/mysql/binlogs"
RECOVERY_TIME="2024-10-01 14:30:00"

# Stop MySQL service
sudo systemctl stop mysql

# Restore from full backup
zcat $BACKUP_FILE | mysql -u root -p

# Apply binary logs up to recovery time
for binlog in $(ls $BINLOG_DIR/*.gz | sort); do
    zcat $binlog | mysqlbinlog \
        --stop-datetime="$RECOVERY_TIME" \
        --database=production_db - | mysql -u root -p
done

# Start MySQL service
sudo systemctl start mysql

echo "Point-in-time recovery completed to: $RECOVERY_TIME"
```

---

## 📊 Monitoring and Maintenance

### Performance Monitoring Queries

#### Server Status Monitoring

```sql
-- Database size monitoring
SELECT 
    TABLE_SCHEMA AS 'Database',
    FORMAT(SUM(data_length + index_length)/1024/1024/1024, 2) AS 'Size (GB)',
    FORMAT(SUM(data_length)/1024/1024/1024, 2) AS 'Data (GB)',
    FORMAT(SUM(index_length)/1024/1024/1024, 2) AS 'Index (GB)',
    COUNT(TABLE_NAME) AS 'Tables'
FROM information_schema.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
GROUP BY TABLE_SCHEMA
ORDER BY SUM(data_length + index_length) DESC;

-- Connection monitoring
SHOW PROCESSLIST;

-- InnoDB status
SHOW ENGINE INNODB STATUS\G

-- Global status variables
SHOW GLOBAL STATUS LIKE 'Threads_%';
SHOW GLOBAL STATUS LIKE 'Connections';
SHOW GLOBAL STATUS LIKE 'Max_used_connections';
SHOW GLOBAL STATUS LIKE 'Aborted_%';
```

#### Replication Monitoring

```sql
-- Master status
SHOW MASTER STATUS;

-- Slave status (on slave server)
SHOW SLAVE STATUS\G

-- Check replication lag
SELECT 
    SECONDS_BEHIND_MASTER,
    MASTER_LOG_FILE,
    READ_MASTER_LOG_POS,
    RELAY_MASTER_LOG_FILE,
    EXEC_MASTER_LOG_POS
FROM performance_schema.replication_connection_status rcs
JOIN performance_schema.replication_applier_status_by_coordinator rasc
    ON rcs.CHANNEL_NAME = rasc.CHANNEL_NAME;
```

### Automated Maintenance Scripts

#### Daily Maintenance Script

```bash
#!/bin/bash
# MySQL daily maintenance script

MYSQL_USER="admin"
MYSQL_PASS="AdminPass123!"
LOG_FILE="/var/log/mysql_maintenance.log"

echo "=== MySQL Maintenance - $(date) ===" >> $LOG_FILE

# Check for crashed tables
echo "Checking for crashed tables..." >> $LOG_FILE
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "
    SELECT TABLE_SCHEMA, TABLE_NAME 
    FROM information_schema.TABLES 
    WHERE TABLE_COMMENT LIKE '%crashed%';" >> $LOG_FILE

# Optimize tables (weekly on Sunday)
if [ $(date +%u) -eq 7 ]; then
    echo "Running weekly table optimization..." >> $LOG_FILE
    mysql -u$MYSQL_USER -p$MYSQL_PASS -e "
        SELECT CONCAT('OPTIMIZE TABLE ', TABLE_SCHEMA, '.', TABLE_NAME, ';') AS stmt
        FROM information_schema.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
            AND TABLE_SCHEMA NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
            AND DATA_FREE > 0;" | grep -v stmt | mysql -u$MYSQL_USER -p$MYSQL_PASS
fi

# Update table statistics
echo "Updating table statistics..." >> $LOG_FILE
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "
    SELECT CONCAT('ANALYZE TABLE ', TABLE_SCHEMA, '.', TABLE_NAME, ';') AS stmt
    FROM information_schema.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' 
        AND TABLE_SCHEMA NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');" | grep -v stmt | mysql -u$MYSQL_USER -p$MYSQL_PASS

# Purge binary logs older than 7 days
echo "Purging old binary logs..." >> $LOG_FILE
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);"

# Check disk usage
echo "Disk usage check:" >> $LOG_FILE
df -h /var/lib/mysql >> $LOG_FILE

echo "=== Maintenance complete - $(date) ===" >> $LOG_FILE
```

#### Performance Report Script

```bash
#!/bin/bash
# MySQL performance report generator

MYSQL_USER="monitoring"
MYSQL_PASS="MonitorPass123!"
REPORT_DIR="/var/reports/mysql"
DATE=$(date +%Y%m%d)

mkdir -p $REPORT_DIR

# Generate performance report
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "
-- Server Information
SELECT 'Server Information' as Section, '' as Metric, '' as Value;
SELECT 'Version' as Section, @@version as Metric, '' as Value;
SELECT 'Uptime' as Section, 'Uptime (hours)' as Metric, ROUND(@@global.uptime/3600,2) as Value;
SELECT 'Buffer Pool' as Section, 'Size (GB)' as Metric, ROUND(@@innodb_buffer_pool_size/1024/1024/1024,2) as Value;

-- Connection Statistics
SELECT 'Connections' as Section, '' as Metric, '' as Value;
SELECT 'Connections' as Section, 'Max Connections' as Metric, @@max_connections as Value;
SELECT 'Connections' as Section, 'Current Connections' as Metric, (SELECT COUNT(*) FROM information_schema.processlist) as Value;
SELECT 'Connections' as Section, 'Max Used Connections' as Metric, (SELECT VARIABLE_VALUE FROM performance_schema.global_status WHERE VARIABLE_NAME = 'Max_used_connections') as Value;

-- Database Sizes
SELECT 'Database Sizes' as Section, '' as Metric, '' as Value;
SELECT 'Database Sizes' as Section, TABLE_SCHEMA as Metric, CONCAT(ROUND(SUM(data_length + index_length)/1024/1024/1024,2), ' GB') as Value
FROM information_schema.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
GROUP BY TABLE_SCHEMA
ORDER BY SUM(data_length + index_length) DESC;

-- Top 10 Largest Tables
SELECT 'Largest Tables' as Section, '' as Metric, '' as Value;
SELECT 'Largest Tables' as Section, CONCAT(TABLE_SCHEMA, '.', TABLE_NAME) as Metric, CONCAT(ROUND((data_length + index_length)/1024/1024/1024,2), ' GB') as Value
FROM information_schema.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY (data_length + index_length) DESC 
LIMIT 10;

-- InnoDB Metrics
SELECT 'InnoDB Metrics' as Section, '' as Metric, '' as Value;
SELECT 'InnoDB Metrics' as Section, 'Buffer Pool Hit Ratio' as Metric, 
    CONCAT(ROUND((1 - (SELECT VARIABLE_VALUE FROM performance_schema.global_status WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads') / 
    (SELECT VARIABLE_VALUE FROM performance_schema.global_status WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests')) * 100, 2), '%') as Value;
" > $REPORT_DIR/mysql_report_$DATE.txt

echo "Performance report generated: $REPORT_DIR/mysql_report_$DATE.txt"
```

### Monitoring with MySQL Enterprise Monitor (MEM)

```bash
# Install MySQL Enterprise Monitor Agent (requires license)
# Download from Oracle support

# Configure agent
./mysqlmonitoragent.sh --install \
    --host=mysql-server.domain.com \
    --port=3306 \
    --user=monitor_user \
    --password=MonitorPass123!

# Start agent
service mysql-monitor-agent start
```

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. MySQL Won't Start

```bash
# Check error log
sudo tail -f /var/log/mysql/error.log

# Common issues and fixes:

# Issue: InnoDB log file size mismatch
# Solution: Remove log files and restart
sudo systemctl stop mysql
sudo rm /var/lib/mysql/ib_logfile*
sudo systemctl start mysql

# Issue: Disk space full
# Solution: Check disk usage and free space
df -h /var/lib/mysql
sudo du -sh /var/lib/mysql/*

# Issue: Permission problems
# Solution: Fix ownership
sudo chown -R mysql:mysql /var/lib/mysql
sudo chmod 750 /var/lib/mysql

# Issue: Port already in use
# Solution: Check what's using port 3306
sudo netstat -tlnp | grep :3306
sudo lsof -i :3306
```

#### 2. Connection Issues

```sql
-- Check user accounts and privileges
SELECT User, Host, authentication_string, password_expired, account_locked 
FROM mysql.user 
WHERE User = 'problematic_user';

-- Check connection limits
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'max_user_connections';

-- Check current connections
SELECT User, Host, COUNT(*) as Connections 
FROM information_schema.processlist 
GROUP BY User, Host;

-- Reset user password
ALTER USER 'username'@'hostname' IDENTIFIED BY 'NewPassword123!';
FLUSH PRIVILEGES;
```

#### 3. Performance Issues

```sql
-- Identify slow queries
SELECT 
    SQL_TEXT,
    EXEC_COUNT,
    AVG_TIMER_WAIT/1000000000 as AVG_EXEC_TIME_SEC,
    FORMAT(ROWS_EXAMINED_MAX,0) as MAX_ROWS_EXAMINED
FROM performance_schema.events_statements_summary_by_digest 
ORDER BY AVG_TIMER_WAIT DESC 
LIMIT 10;

-- Check for lock waits
SELECT 
    r.trx_id waiting_trx_id,
    r.trx_mysql_thread_id waiting_thread,
    r.trx_query waiting_query,
    b.trx_id blocking_trx_id,
    b.trx_mysql_thread_id blocking_thread,
    b.trx_query blocking_query
FROM information_schema.innodb_lock_waits w
INNER JOIN information_schema.innodb_trx b
    ON b.trx_id = w.blocking_trx_id
INNER JOIN information_schema.innodb_trx r
    ON r.trx_id = w.requesting_trx_id;

-- Check table locks
SHOW OPEN TABLES WHERE In_use > 0;
```

#### 4. Replication Issues

```sql
-- Check replication status on slave
SHOW SLAVE STATUS\G

-- Common replication fixes:

-- Skip one problematic statement
STOP SLAVE SQL_THREAD;
SET GLOBAL sql_slave_skip_counter = 1;
START SLAVE SQL_THREAD;

-- Reset replication completely
STOP SLAVE;
RESET SLAVE ALL;
CHANGE MASTER TO 
    MASTER_HOST='master-server.domain.com',
    MASTER_USER='repl_user',
    MASTER_PASSWORD='ReplPass123!',
    MASTER_AUTO_POSITION=1;
START SLAVE;

-- Check master binary log position
SHOW MASTER STATUS;
```

### Emergency Recovery Procedures

#### 1. InnoDB Crash Recovery

```bash
# Add to my.cnf for crash recovery
[mysqld]
innodb_force_recovery = 1

# Recovery levels (1-6, increasing severity):
# 1 - Ignore corruption of a page
# 2 - Prevent master thread operations
# 3 - Do not run transaction rollbacks
# 4 - Do not run insert buffer operations
# 5 - Do not look at undo logs
# 6 - Do not do transaction rollbacks (extreme)

# Start MySQL with recovery mode
sudo systemctl start mysql

# Export data immediately
mysqldump --single-transaction --all-databases > emergency_backup.sql

# Remove recovery mode and restart normally
sudo systemctl stop mysql
# Remove innodb_force_recovery line from my.cnf
sudo systemctl start mysql
```

#### 2. Binary Log Corruption

```bash
# Check binary log integrity
mysqlbinlog /var/lib/mysql/mysql-bin.000001

# If corrupted, purge and start fresh
mysql -u root -p -e "RESET MASTER;"

# Or purge specific logs
mysql -u root -p -e "PURGE BINARY LOGS TO 'mysql-bin.000010';"
```

---

## 📋 Maintenance Checklist

### Daily Tasks

- [ ] Check MySQL service status
- [ ] Monitor error log for issues
- [ ] Verify backup completion
- [ ] Check disk space usage
- [ ] Monitor active connections
- [ ] Review slow query log

### Weekly Tasks

- [ ] Run table optimization
- [ ] Update table statistics (ANALYZE TABLE)
- [ ] Purge old binary logs
- [ ] Review performance metrics
- [ ] Check for unused indexes
- [ ] Validate backup restore procedures

### Monthly Tasks

- [ ] Review and rotate log files
- [ ] Update MySQL statistics
- [ ] Performance tuning review
- [ ] Security audit (user accounts, privileges)
- [ ] Check for MySQL updates
- [ ] Review and update documentation

### Quarterly Tasks

- [ ] Full security audit
- [ ] Disaster recovery testing
- [ ] Performance benchmarking
- [ ] MySQL version upgrade planning
- [ ] Infrastructure capacity planning
- [ ] Update backup and recovery procedures

---

## 📚 Additional Resources

### Official Documentation

- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [MySQL Installation Guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
- [MySQL Security Guide](https://dev.mysql.com/doc/refman/8.0/en/security.html)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

### Cloud Provider Documentation

- [AWS RDS for MySQL](https://docs.aws.amazon.com/rds/latest/userguide/CHAP_MySQL.html)
- [Azure Database for MySQL](https://docs.microsoft.com/en-us/azure/mysql/)
- [Google Cloud SQL for MySQL](https://cloud.google.com/sql/docs/mysql)

### Tools and Utilities

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) - GUI administration tool
- [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit) - MySQL utilities
- [mysqldumper](https://github.com/mysqldumper/mysqldumper) - Web-based MySQL backup
- [phpMyAdmin](https://www.phpmyadmin.net/) - Web-based MySQL administration

### Monitoring Solutions

- [Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management)
- [MySQL Enterprise Monitor](https://www.mysql.com/products/enterprise/monitor.html)
- [Zabbix MySQL Templates](https://www.zabbix.com/integrations/mysql)
- [Nagios MySQL Plugins](https://exchange.nagios.org/directory/Plugins/Databases/MySQL)

---

## 🤝 Contributing

Contributions to improve this guide are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

---

## 📄 License

This guide is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
---

[Back to top](#table-of-contents)

---

**[🏠 Back to Main Portfolio](https://github.com/vandersantanna/portfolio/blob/main/README.md)**

---
## 📫 Contact
- **Email (primary):** [vandersantanna@gmail.com](mailto:vandersantanna@gmail.com)  
- **LinkedIn:** [linkedin.com/in/vandersantanna](https://www.linkedin.com/in/vandersantanna)  
- **GitHub:** [github.com/vandersantanna](https://github.com/vandersantanna)  
- **Location & Timezone:** Blumenau, SC, Brazil — GMT-3
- **Availability:** Remote — Americas & Europe • Contract (B2B / Independent Contractor) — also open to full-time remote  
---
