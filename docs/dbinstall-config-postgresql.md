# 🐘PostgreSQL Installation and Configuration Guide

*Complete installation and configuration guide for PostgreSQL 16 across multiple platforms*

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows%20Server-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Linux Installations](#linux-installations)
- [Windows Server Installation](#windows-server-installation)
- [Cloud Deployments](#cloud-deployments)
- [Post-Installation Configuration](#post-installation-configuration)
- [Security Hardening](#security-hardening)
- [Performance Tuning](#performance-tuning)
- [High Availability Setup](#high-availability-setup)
- [Backup and Recovery](#backup-and-recovery)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

---

## Overview

This comprehensive guide covers PostgreSQL 16 installation and configuration across:

- **Operating Systems**: Red Hat Enterprise Linux 9/10, Ubuntu 22.04 LTS, Windows Server 2019/2022
- **Cloud Platforms**: AWS RDS, Azure Database for PostgreSQL, Google Cloud SQL
- **Deployment Types**: Standalone, Master-Slave, Streaming Replication, Hot Standby

### Prerequisites

- Administrative access to target system
- Network connectivity for package downloads
- Minimum 4GB RAM (8GB+ recommended for production)
- 50GB+ available disk space
- Basic understanding of SQL and database concepts

### PostgreSQL 16 Key Features

- **Logical Replication Enhancements**: Better performance and monitoring
- **SQL/JSON Improvements**: Advanced JSON query capabilities
- **Performance Optimizations**: Query planner improvements
- **Security Enhancements**: Enhanced authentication and authorization
- **Monitoring Improvements**: Better statistics and logging

[Back to top](#table-of-contents)

---

## Linux Installations

### Red Hat Enterprise Linux 9/10

#### Method 1: Using PostgreSQL Official Repository (Recommended)

```bash
# Install PostgreSQL official repository
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Update package index
sudo dnf update -y

# Install PostgreSQL 16 server and client
sudo dnf install -y postgresql16-server postgresql16 postgresql16-contrib

# Initialize database
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb

# Enable and start PostgreSQL service
sudo systemctl enable postgresql-16
sudo systemctl start postgresql-16

# Check service status
sudo systemctl status postgresql-16
```

#### Method 2: Using RHEL AppStream

```bash
# List available PostgreSQL streams
sudo dnf module list postgresql

# Install PostgreSQL from AppStream (older version)
sudo dnf module install postgresql:15 -y

# Initialize database
sudo postgresql-setup --initdb

# Enable and start service
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

#### PostgreSQL Installation Verification

```bash
# Switch to postgres user and connect
sudo -u postgres psql

# Check PostgreSQL version
postgres=# SELECT version();

# Create test database
postgres=# CREATE DATABASE testdb;

# List databases
postgres=# \l

# Exit PostgreSQL
postgres=# \q
```

#### Configuration File Locations (RHEL)
- **Main config**: `/var/lib/pgsql/16/data/postgresql.conf`
- **Authentication**: `/var/lib/pgsql/16/data/pg_hba.conf`
- **Data directory**: `/var/lib/pgsql/16/data/`
- **Log files**: `/var/lib/pgsql/16/data/log/`
- **Service name**: `postgresql-16`

### Ubuntu 22.04 LTS

#### Method 1: Using APT (Ubuntu Repository)

```bash
# Update package index
sudo apt update

# Install PostgreSQL and extensions
sudo apt install -y postgresql postgresql-contrib postgresql-client

# Check service status
sudo systemctl status postgresql

# PostgreSQL starts automatically, verify version
sudo -u postgres psql -c "SELECT version();"
```

#### Method 2: Using PostgreSQL Official Repository

```bash
# Install prerequisites
sudo apt install -y wget ca-certificates

# Add PostgreSQL official APT repository
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Update package index
sudo apt update

# Install PostgreSQL 16
sudo apt install -y postgresql-16 postgresql-client-16 postgresql-contrib-16

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Ubuntu-Specific Configuration

```bash
# Switch to postgres user
sudo -i -u postgres

# Create database user
createuser --interactive --pwprompt myuser

# Create database
createdb -O myuser mydatabase

# Connect to PostgreSQL
psql

# Set password for postgres user
postgres=# ALTER USER postgres PASSWORD 'SecurePassword123!';

# Exit PostgreSQL
postgres=# \q
```

#### Configuration File Locations (Ubuntu)
- **Main config**: `/etc/postgresql/16/main/postgresql.conf`
- **Authentication**: `/etc/postgresql/16/main/pg_hba.conf`
- **Data directory**: `/var/lib/postgresql/16/main/`
- **Log files**: `/var/log/postgresql/`
- **Service name**: `postgresql`

[Back to top](#table-of-contents)

---

## Windows Server Installation

### Prerequisites
- Windows Server 2019/2022
- Administrator privileges
- Microsoft Visual C++ Redistributable 2019+

### Installation Steps

#### Method 1: Using EnterpriseDB Installer (Recommended)

```powershell
# Download PostgreSQL installer from EnterpriseDB
# https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

# Run installer as Administrator
.\postgresql-16.1-1-windows-x64.exe

# Installation options:
# - Installation Directory: C:\Program Files\PostgreSQL\16
# - Data Directory: C:\Program Files\PostgreSQL\16\data
# - Password: Set secure password for postgres user
# - Port: 5432 (default)
# - Locale: Default locale
# - Components: PostgreSQL Server, pgAdmin 4, Stack Builder, Command Line Tools
```

#### Method 2: Using Chocolatey

```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install PostgreSQL using Chocolatey
choco install postgresql16 --params '/Password:SecurePassword123!'

# Start PostgreSQL service
Start-Service postgresql-x64-16
```

#### Windows Configuration

```powershell
# Add PostgreSQL to PATH
$env:PATH += ";C:\Program Files\PostgreSQL\16\bin"

# Create environment variable permanently
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, [EnvironmentVariableTarget]::Machine)

# Connect to PostgreSQL
psql -U postgres -d postgres

# Create database and user
CREATE DATABASE myapp;
CREATE USER appuser WITH PASSWORD 'AppPassword123!';
GRANT ALL PRIVILEGES ON DATABASE myapp TO appuser;
```

#### Windows Service Management

```powershell
# Service management
Get-Service postgresql-x64-16
Start-Service postgresql-x64-16
Stop-Service postgresql-x64-16
Restart-Service postgresql-x64-16

# Set service to start automatically
Set-Service -Name postgresql-x64-16 -StartupType Automatic

# Check service status
Get-Service postgresql-x64-16 | Format-List
```

### Windows Configuration Files

- **Main config**: `C:\Program Files\PostgreSQL\16\data\postgresql.conf`
- **Authentication**: `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`
- **Data directory**: `C:\Program Files\PostgreSQL\16\data\`
- **Log files**: `C:\Program Files\PostgreSQL\16\data\log\`

[Back to top](#table-of-contents)

---

## Cloud Deployments

### Amazon Web Services (AWS)

#### AWS RDS PostgreSQL Deployment

```bash
# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure

# Create DB subnet group
aws rds create-db-subnet-group \
    --db-subnet-group-name postgres-subnet-group \
    --db-subnet-group-description "PostgreSQL subnet group" \
    --subnet-ids subnet-12345678 subnet-87654321 subnet-11223344

# Create parameter group
aws rds create-db-parameter-group \
    --db-parameter-group-name postgres16-custom \
    --db-parameter-group-family postgres16 \
    --description "Custom PostgreSQL 16 parameters"

# Create RDS PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier postgres-prod-01 \
    --db-instance-class db.t3.medium \
    --engine postgres \
    --engine-version 16.1 \
    --master-username postgres \
    --master-user-password 'SecurePassword123!' \
    --allocated-storage 100 \
    --storage-type gp3 \
    --storage-encrypted \
    --vpc-security-group-ids sg-12345678 \
    --db-subnet-group-name postgres-subnet-group \
    --db-parameter-group-name postgres16-custom \
    --backup-retention-period 7 \
    --multi-az \
    --enable-performance-insights \
    --performance-insights-retention-period 7 \
    --monitoring-interval 60 \
    --monitoring-role-arn arn:aws:iam::123456789012:role/rds-monitoring-role
```

#### AWS RDS Configuration

```bash
# Modify PostgreSQL parameters
aws rds modify-db-parameter-group \
    --db-parameter-group-name postgres16-custom \
    --parameters "ParameterName=shared_preload_libraries,ParameterValue=pg_stat_statements,ApplyMethod=pending-reboot" \
               "ParameterName=max_connections,ParameterValue=500,ApplyMethod=pending-reboot" \
               "ParameterName=work_mem,ParameterValue=4096,ApplyMethod=immediate"

# Apply parameter group to instance
aws rds modify-db-instance \
    --db-instance-identifier postgres-prod-01 \
    --db-parameter-group-name postgres16-custom \
    --apply-immediately

# Create read replica
aws rds create-db-instance-read-replica \
    --db-instance-identifier postgres-prod-01-replica \
    --source-db-instance-identifier postgres-prod-01 \
    --db-instance-class db.t3.medium

# Create database snapshot
aws rds create-db-snapshot \
    --db-snapshot-identifier postgres-prod-01-snapshot-$(date +%Y%m%d) \
    --db-instance-identifier postgres-prod-01
```

#### Connection Example

```bash
# Connect to RDS PostgreSQL
psql -h postgres-prod-01.cluster-xyz.us-east-1.rds.amazonaws.com \
     -U postgres \
     -d postgres \
     --set=sslmode=require

# Connection string for applications
DATABASE_URL="postgresql://username:password@postgres-prod-01.cluster-xyz.us-east-1.rds.amazonaws.com:5432/database_name?sslmode=require"
```

### Microsoft Azure

#### Azure Database for PostgreSQL Deployment

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name postgres-rg --location eastus

# Create Azure Database for PostgreSQL Flexible Server
az postgres flexible-server create \
    --resource-group postgres-rg \
    --name postgres-server-01 \
    --location eastus \
    --admin-user postgres \
    --admin-password 'SecurePassword123!' \
    --sku-name Standard_B2s \
    --tier Burstable \
    --compute-generation Gen5 \
    --storage-size 128 \
    --backup-retention 7 \
    --geo-redundant-backup Enabled \
    --version 16 \
    --high-availability ZoneRedundant \
    --zone 1 \
    --standby-zone 2
```

#### Azure PostgreSQL Configuration

```bash
# Configure server parameters
az postgres flexible-server parameter set \
    --resource-group postgres-rg \
    --server-name postgres-server-01 \
    --name shared_preload_libraries \
    --value "pg_stat_statements,pg_cron"

az postgres flexible-server parameter set \
    --resource-group postgres-rg \
    --server-name postgres-server-01 \
    --name max_connections \
    --value 500

# Configure firewall rules
az postgres flexible-server firewall-rule create \
    --resource-group postgres-rg \
    --name postgres-server-01 \
    --rule-name AllowMyNetwork \
    --start-ip-address 203.0.113.0 \
    --end-ip-address 203.0.113.255

# Create database
az postgres flexible-server db create \
    --resource-group postgres-rg \
    --server-name postgres-server-01 \
    --database-name production_db
```

#### Azure Connection Example

```bash
# Connect to Azure PostgreSQL
psql "host=postgres-server-01.postgres.database.azure.com port=5432 dbname=postgres user=postgres password=SecurePassword123! sslmode=require"

# Connection string for applications
DATABASE_URL="postgresql://postgres:SecurePassword123!@postgres-server-01.postgres.database.azure.com:5432/production_db?sslmode=require"
```

### Google Cloud Platform (GCP)

#### Cloud SQL PostgreSQL Deployment

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize gcloud
gcloud init

# Create Cloud SQL PostgreSQL instance
gcloud sql instances create postgres-instance-01 \
    --database-version=POSTGRES_16 \
    --tier=db-custom-2-8192 \
    --region=us-central1 \
    --storage-type=SSD \
    --storage-size=100GB \
    --storage-auto-increase \
    --backup-start-time=03:00 \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=04 \
    --availability-type=REGIONAL \
    --enable-ip-alias \
    --authorized-networks=203.0.113.0/24
```

#### GCP Cloud SQL Configuration

```bash
# Set PostgreSQL flags
gcloud sql instances patch postgres-instance-01 \
    --database-flags shared_preload_libraries=pg_stat_statements,pg_cron \
    --database-flags max_connections=500 \
    --database-flags work_mem=4096

# Set root password
gcloud sql users set-password postgres \
    --host=% \
    --instance=postgres-instance-01 \
    --password='SecurePassword123!'

# Create database
gcloud sql databases create production_db \
    --instance=postgres-instance-01

# Create application user
gcloud sql users create appuser \
    --host=% \
    --instance=postgres-instance-01 \
    --password='AppPassword123!'
```

#### GCP Connection Example

```bash
# Install Cloud SQL Proxy
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
chmod +x cloud_sql_proxy

# Start proxy
./cloud_sql_proxy -instances=project-id:us-central1:postgres-instance-01=tcp:5432 &

# Connect to PostgreSQL
psql -h 127.0.0.1 -U postgres -d postgres
```

[Back to top](#table-of-contents)

---

## Post-Installation Configuration

### Essential Configuration Settings

#### Sample postgresql.conf for Production

```ini
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# Connection Settings
listen_addresses = '*'
port = 5432
max_connections = 500
superuser_reserved_connections = 3

# Authentication
authentication_timeout = 60s
password_encryption = scram-sha-256

#------------------------------------------------------------------------------
# RESOURCE USAGE (except WAL)
#------------------------------------------------------------------------------

# Memory
shared_buffers = 2GB
huge_pages = try
work_mem = 64MB
maintenance_work_mem = 512MB
effective_cache_size = 6GB

# Background Writer
bgwriter_delay = 200ms
bgwriter_lru_maxpages = 100
bgwriter_lru_multiplier = 2.0

# Asynchronous Behavior
effective_io_concurrency = 200
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_parallel_maintenance_workers = 4

#------------------------------------------------------------------------------
# WRITE-AHEAD LOGGING
#------------------------------------------------------------------------------

# Settings
wal_level = replica
fsync = on
synchronous_commit = on
full_page_writes = on

# Checkpoints
checkpoint_timeout = 15min
checkpoint_completion_target = 0.9
checkpoint_warning = 30s

# WAL Files
wal_buffers = 16MB
wal_writer_delay = 200ms
max_wal_size = 4GB
min_wal_size = 1GB

#------------------------------------------------------------------------------
# REPLICATION
#------------------------------------------------------------------------------

# Sending Servers
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1GB
hot_standby = on

# Standby Servers
hot_standby_feedback = on
max_standby_archive_delay = 30s
max_standby_streaming_delay = 30s

#------------------------------------------------------------------------------
# QUERY TUNING
#------------------------------------------------------------------------------

# Query Planning
random_page_cost = 1.1
seq_page_cost = 1.0
cpu_tuple_cost = 0.01
cpu_index_tuple_cost = 0.005
cpu_operator_cost = 0.0025

# Genetic Query Optimizer
geqo = on
geqo_threshold = 12

#------------------------------------------------------------------------------
# REPORTING AND LOGGING
#------------------------------------------------------------------------------

# Where to Log
log_destination = 'csvlog'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_file_mode = 0600
log_rotation_age = 1d
log_rotation_size = 100MB

# When to Log
log_min_messages = warning
log_min_error_statement = error
log_min_duration_statement = 1000

# What to Log
debug_print_parse = off
debug_print_rewritten = off
debug_print_plan = off
debug_pretty_print = on
log_checkpoints = on
log_connections = on
log_disconnections = on
log_duration = off
log_error_verbosity = default
log_hostname = off
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_lock_waits = on
log_statement = 'ddl'
log_replication_commands = on

#------------------------------------------------------------------------------
# STATISTICS
#------------------------------------------------------------------------------

# Query Statistics
track_activities = on
track_counts = on
track_io_timing = on
track_functions = pl
stats_temp_directory = 'pg_stat_tmp'

# Statement Statistics (requires pg_stat_statements extension)
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all

#------------------------------------------------------------------------------
# CLIENT CONNECTION DEFAULTS
#------------------------------------------------------------------------------

# Statement Behavior
search_path = '"$user", public'
default_tablespace = ''
temp_tablespaces = ''

# Locale and Formatting
datestyle = 'iso, mdy'
timezone = 'UTC'
lc_messages = 'en_US.UTF-8'
lc_monetary = 'en_US.UTF-8'
lc_numeric = 'en_US.UTF-8'
lc_time = 'en_US.UTF-8'
default_text_search_config = 'pg_catalog.english'

#------------------------------------------------------------------------------
# LOCK MANAGEMENT
#------------------------------------------------------------------------------

deadlock_timeout = 1s
max_locks_per_transaction = 64
max_pred_locks_per_transaction = 64

#------------------------------------------------------------------------------
# VERSION AND PLATFORM COMPATIBILITY
#------------------------------------------------------------------------------

# Array and JSON
array_nulls = on
standard_conforming_strings = on
```

#### Sample pg_hba.conf Configuration

```ini
# PostgreSQL Client Authentication Configuration File
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             postgres                                peer
local   all             all                                     scram-sha-256

# IPv4 local connections:
host    all             postgres        127.0.0.1/32            scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256

# IPv6 local connections:
host    all             postgres        ::1/128                 scram-sha-256
host    all             all             ::1/128                 scram-sha-256

# Application connections
host    production_db   appuser         10.0.0.0/8              scram-sha-256
host    production_db   appuser         192.168.0.0/16          scram-sha-256

# Replication connections
host    replication     replicator      10.0.0.0/8              scram-sha-256
host    replication     replicator      192.168.0.0/16          scram-sha-256

# SSL connections
hostssl all             all             0.0.0.0/0               scram-sha-256

# Reject all other connections
host    all             all             0.0.0.0/0               reject
```

### Database Initialization

```sql
-- Create administrative user
CREATE USER dbadmin WITH SUPERUSER CREATEDB CREATEROLE LOGIN;
ALTER USER dbadmin PASSWORD 'SecureAdminPass123!';

-- Create application database
CREATE DATABASE production_db 
    WITH OWNER = dbadmin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Create application user
CREATE USER appuser WITH LOGIN;
ALTER USER appuser PASSWORD 'SecureAppPass123!';

-- Grant privileges
GRANT CONNECT ON DATABASE production_db TO appuser;
GRANT USAGE ON SCHEMA public TO appuser;
GRANT CREATE ON SCHEMA public TO appuser;

-- Create read-only user for reporting
CREATE USER readonly WITH LOGIN;
ALTER USER readonly PASSWORD 'ReadOnlyPass123!';

GRANT CONNECT ON DATABASE production_db TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;

-- Create backup user
CREATE USER backup WITH LOGIN REPLICATION;
ALTER USER backup PASSWORD 'BackupPass123!';

-- Create replication user
CREATE USER replicator WITH REPLICATION LOGIN;
ALTER USER replicator PASSWORD 'ReplicatorPass123!';

-- Install useful extensions
\c production_db;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE EXTENSION IF NOT EXISTS btree_gist;
```

[Back to top](#table-of-contents)

---

## Security Hardening

### PostgreSQL Security Best Practices

#### 1. Authentication and Authorization

```sql
-- Enable password encryption
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
SELECT pg_reload_conf();

-- Create security policies
CREATE POLICY user_isolation ON sensitive_table
    USING (user_id = current_setting('app.current_user_id')::integer);

-- Enable row level security
ALTER TABLE sensitive_table ENABLE ROW LEVEL SECURITY;

-- Create security definer functions
CREATE OR REPLACE FUNCTION get_user_data(user_id INTEGER)
RETURNS TABLE(id INTEGER, name TEXT)
SECURITY DEFINER
LANGUAGE SQL AS $
    SELECT id, name FROM users WHERE id = user_id;
$;
```

#### 2. Network Security Configuration

```bash
# Configure SSL certificates
cd /var/lib/postgresql/16/data

# Generate private key
openssl genrsa -out server.key 2048
chmod 600 server.key
chown postgres:postgres server.key

# Generate certificate signing request
openssl req -new -key server.key -out server.csr \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=postgres-server.domain.com"

# Generate self-signed certificate
openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365
chmod 644 server.crt
chown postgres:postgres server.crt

# Update postgresql.conf for SSL
echo "ssl = on" >> /var/lib/postgresql/16/data/postgresql.conf
echo "ssl_cert_file = 'server.crt'" >> /var/lib/postgresql/16/data/postgresql.conf
echo "ssl_key_file = 'server.key'" >> /var/lib/postgresql/16/data/postgresql.conf

# Restart PostgreSQL
sudo systemctl restart postgresql-16
```

#### 3. Data Encryption

```sql
-- Use pgcrypto for data encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example: Encrypt sensitive data
CREATE TABLE encrypted_data (
    id SERIAL PRIMARY KEY,
    name TEXT,
    encrypted_ssn BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert encrypted data
INSERT INTO encrypted_data (name, encrypted_ssn) 
VALUES ('John Doe', pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Decrypt data
SELECT name, pgp_sym_decrypt(encrypted_ssn, 'encryption_key') as ssn 
FROM encrypted_data;
```

### Firewall Configuration

#### Linux (firewalld - RHEL/CentOS)

```bash
# Add PostgreSQL service
sudo firewall-cmd --permanent --add-service=postgresql
sudo firewall-cmd --permanent --add-port=5432/tcp

# Restrict to specific source
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="postgresql" accept'

# Reload firewall
sudo firewall-cmd --reload
```

[Back to top](#table-of-contents)

---

## Performance Tuning

### Memory Configuration

```sql
-- Check current memory settings
SELECT name, setting, unit, context 
FROM pg_settings 
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem', 'effective_cache_size');

-- Buffer cache hit ratio query
SELECT 
    'Buffer Cache Hit Ratio' as metric,
    ROUND(
        (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 2
    ) as percentage
FROM pg_statio_user_tables;

-- Monitor active connections
SELECT 
    datname,
    usename,
    client_addr,
    client_port,
    backend_start,
    state,
    state_change,
    query
FROM pg_stat_activity 
WHERE state != 'idle'
ORDER BY backend_start;
```

### Query Performance Optimization

```sql
-- Enable pg_stat_statements extension for query analysis
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_tup_read = 0 AND idx_tup_fetch = 0
ORDER BY schemaname, tablename;

-- Top 10 slowest queries
SELECT 
    query,
    calls,
    total_exec_time,
    total_exec_time/calls as avg_exec_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE calls > 5
ORDER BY total_exec_time DESC
LIMIT 10;
```

### Vacuum and Analyze Optimization

```sql
-- Configure autovacuum
ALTER SYSTEM SET autovacuum = on;
ALTER SYSTEM SET autovacuum_max_workers = 6;
ALTER SYSTEM SET autovacuum_naptime = '30s';
ALTER SYSTEM SET autovacuum_vacuum_threshold = 50;
ALTER SYSTEM SET autovacuum_vacuum_scale_factor = 0.1;
ALTER SYSTEM SET autovacuum_analyze_threshold = 50;
ALTER SYSTEM SET autovacuum_analyze_scale_factor = 0.05;
SELECT pg_reload_conf();

-- Monitor vacuum activity
SELECT 
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze,
    vacuum_count,
    autovacuum_count,
    analyze_count,
    autoanalyze_count
FROM pg_stat_user_tables
ORDER BY last_autovacuum DESC NULLS LAST;
```

[Back to top](#table-of-contents)

---

## High Availability Setup

### Streaming Replication Configuration

#### Master Server Setup

```bash
# Configure master server (postgresql.conf)
cat >> /var/lib/postgresql/16/data/postgresql.conf << EOF

# Replication Configuration
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
synchronous_commit = on
synchronous_standby_names = 'standby1'
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/archive/%f'
hot_standby = on
EOF

# Create replication slot
sudo -u postgres psql -c "SELECT pg_create_physical_replication_slot('standby1_slot');"

# Create archive directory
sudo mkdir -p /var/lib/postgresql/archive
sudo chown postgres:postgres /var/lib/postgresql/archive
sudo chmod 700 /var/lib/postgresql/archive

# Restart PostgreSQL
sudo systemctl restart postgresql-16
```

#### Standby Server Setup

```bash
# Stop PostgreSQL on standby
sudo systemctl stop postgresql-16

# Backup existing data directory
sudo mv /var/lib/postgresql/16/data /var/lib/postgresql/16/data.backup

# Create base backup from master
sudo -u postgres pg_basebackup -h master-server.domain.com -D /var/lib/postgresql/16/data -U replicator -v -P -W -R

# Create recovery configuration
cat > /var/lib/postgresql/16/data/postgresql.auto.conf << EOF
primary_conninfo = 'host=master-server.domain.com port=5432 user=replicator password=ReplicatorPass123! application_name=standby1'
primary_slot_name = 'standby1_slot'
EOF

# Set permissions
sudo chown -R postgres:postgres /var/lib/postgresql/16/data
sudo chmod 700 /var/lib/postgresql/16/data

# Start standby server
sudo systemctl start postgresql-16
```

#### Monitor Replication

```sql
-- On master: Check replication status
SELECT 
    client_addr,
    client_hostname,
    client_port,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag,
    sync_state
FROM pg_stat_replication;

-- On standby: Check recovery status
SELECT 
    pg_is_in_recovery() as in_recovery,
    pg_last_wal_receive_lsn() as receive_lsn,
    pg_last_wal_replay_lsn() as replay_lsn,
    CASE 
        WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0
        ELSE EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp())::int
    END as lag_seconds;
```

### Logical Replication Setup

```sql
-- On publisher (source database)
-- Create publication for all tables
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- Or create publication for specific tables
CREATE PUBLICATION specific_publication FOR TABLE users, orders, products;

-- Check publications
SELECT * FROM pg_publication;
SELECT * FROM pg_publication_tables;

-- On subscriber (target database)
-- Create subscription
CREATE SUBSCRIPTION my_subscription
    CONNECTION 'host=publisher.domain.com port=5432 user=replicator password=ReplicatorPass123! dbname=production_db'
    PUBLICATION my_publication;

-- Monitor subscription
SELECT * FROM pg_subscription;
SELECT * FROM pg_subscription_rel;
SELECT * FROM pg_stat_subscription;
```

### Failover and Switchover Procedures

#### Automated Failover Script

```bash
#!/bin/bash
# PostgreSQL failover script

MASTER_HOST="master-server.domain.com"
STANDBY_HOST="standby-server.domain.com"
VIP="192.168.1.100"
POSTGRES_USER="postgres"

# Function to check PostgreSQL status
check_postgres_status() {
    local host=$1
    pg_isready -h $host -p 5432 -U $POSTGRES_USER -t 5
    return $?
}

# Function to promote standby
promote_standby() {
    echo "Promoting standby server to master..."
    ssh root@$STANDBY_HOST "sudo -u postgres /usr/pgsql-16/bin/pg_ctl promote -D /var/lib/postgresql/16/data"
    
    if [ $? -eq 0 ]; then
        echo "Standby promoted successfully"
        # Move VIP to new master
        ssh root@$STANDBY_HOST "ip addr add $VIP/24 dev eth0"
        ssh root@$MASTER_HOST "ip addr del $VIP/24 dev eth0" 2>/dev/null
        return 0
    else
        echo "Failed to promote standby"
        return 1
    fi
}

# Main failover logic
echo "Checking master server status..."
if check_postgres_status $MASTER_HOST; then
    echo "Master server is healthy"
    exit 0
else
    echo "Master server is down, checking standby..."
    if check_postgres_status $STANDBY_HOST; then
        echo "Standby server is healthy, initiating failover..."
        promote_standby
        if [ $? -eq 0 ]; then
            echo "Failover completed successfully"
            # Send notification
            echo "PostgreSQL failover completed at $(date)" | mail -s "PostgreSQL Failover Alert" admin@company.com
        else
            echo "Failover failed"
            exit 1
        fi
    else
        echo "Both servers are down!"
        echo "CRITICAL: Both PostgreSQL servers are down!" | mail -s "PostgreSQL CRITICAL Alert" admin@company.com
        exit 2
    fi
fi
```

[Back to top](#table-of-contents)

---

## Backup and Recovery

### Physical Backup with pg_basebackup

#### Full Backup Script

```bash
#!/bin/bash
# PostgreSQL physical backup script

# Configuration
BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
POSTGRES_USER="backup"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
RETENTION_DAYS=7

# Create backup directory
mkdir -p $BACKUP_DIR

# Perform base backup
echo "Starting PostgreSQL base backup at $(date)"
pg_basebackup -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER \
    -D $BACKUP_DIR/base_backup_$DATE \
    -Ft -z -Xs -P -v

if [ $? -eq 0 ]; then
    echo "Base backup completed successfully: $BACKUP_DIR/base_backup_$DATE"
    
    # Create backup manifest
    echo "Backup Date: $(date)" > $BACKUP_DIR/base_backup_$DATE/backup_info.txt
    echo "PostgreSQL Version: $(psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -t -c "SELECT version();")" >> $BACKUP_DIR/base_backup_$DATE/backup_info.txt
    
    # Cleanup old backups
    find $BACKUP_DIR -name "base_backup_*" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} +
    
    echo "Backup cleanup completed"
else
    echo "Base backup failed!"
    exit 1
fi
```

### Logical Backup with pg_dump

#### Database Backup Script

```bash
#!/bin/bash
# PostgreSQL logical backup script

# Configuration
BACKUP_DIR="/backup/postgresql/logical"
DATE=$(date +%Y%m%d_%H%M%S)
POSTGRES_USER="backup"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
DATABASES=("production_db" "analytics_db" "reporting_db")

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup each database
for db in "${DATABASES[@]}"; do
    echo "Backing up database: $db"
    
    pg_dump -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER \
        -d $db -Fc -v --lock-wait-timeout=300000 \
        -f $BACKUP_DIR/${db}_backup_$DATE.dump
    
    if [ $? -eq 0 ]; then
        echo "Backup completed for $db"
        gzip $BACKUP_DIR/${db}_backup_$DATE.dump
    else
        echo "Backup failed for $db"
        exit 1
    fi
done

# Global objects backup (users, roles, tablespaces)
echo "Backing up global objects..."
pg_dumpall -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER \
    -g -v -f $BACKUP_DIR/globals_backup_$DATE.sql

gzip $BACKUP_DIR/globals_backup_$DATE.sql

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*_backup_*.dump.gz" -mtime +30 -delete
find $BACKUP_DIR -name "globals_backup_*.sql.gz" -mtime +30 -delete

echo "Logical backup completed at $(date)"
```

### Point-in-Time Recovery (PITR)

#### Archive Command Setup

```bash
# Configure archiving in postgresql.conf
cat >> /var/lib/postgresql/16/data/postgresql.conf << EOF

# Archive Configuration
archive_mode = on
archive_command = 'test ! -f /var/lib/postgresql/archive/%f && cp %p /var/lib/postgresql/archive/%f'
archive_timeout = 300
max_wal_senders = 3
wal_keep_size = 1GB
EOF

# Create archive directory
sudo mkdir -p /var/lib/postgresql/archive
sudo chown postgres:postgres /var/lib/postgresql/archive
sudo chmod 700 /var/lib/postgresql/archive

# Restart PostgreSQL
sudo systemctl restart postgresql-16
```

#### PITR Recovery Script

```bash
#!/bin/bash
# PostgreSQL Point-in-Time Recovery script

BACKUP_DIR="/backup/postgresql"
ARCHIVE_DIR="/var/lib/postgresql/archive"
DATA_DIR="/var/lib/postgresql/16/data"
RECOVERY_TIME="2024-10-01 14:30:00"
LATEST_BACKUP="base_backup_20241001_030000"

# Stop PostgreSQL
sudo systemctl stop postgresql-16

# Backup current data directory
sudo mv $DATA_DIR ${DATA_DIR}.$(date +%Y%m%d_%H%M%S)

# Restore base backup
sudo -u postgres tar -xzf $BACKUP_DIR/$LATEST_BACKUP/base.tar.gz -C /var/lib/postgresql/16/

# Create recovery configuration
cat > $DATA_DIR/postgresql.auto.conf << EOF
restore_command = 'cp $ARCHIVE_DIR/%f %p'
recovery_target_time = '$RECOVERY_TIME'
recovery_target_action = 'promote'
EOF

# Create recovery signal file
sudo -u postgres touch $DATA_DIR/recovery.signal

# Set permissions
sudo chown -R postgres:postgres $DATA_DIR
sudo chmod 700 $DATA_DIR

# Start PostgreSQL
sudo systemctl start postgresql-16

echo "Point-in-time recovery initiated to: $RECOVERY_TIME"
echo "Monitor PostgreSQL logs for recovery progress"
```

### Backup Validation and Testing

```bash
#!/bin/bash
# Backup validation script

BACKUP_DIR="/backup/postgresql"
TEST_RESTORE_DIR="/tmp/pg_restore_test"
LATEST_BACKUP=$(ls -t $BACKUP_DIR/base_backup_* | head -1)

echo "Validating backup: $LATEST_BACKUP"

# Create test restore directory
mkdir -p $TEST_RESTORE_DIR
rm -rf $TEST_RESTORE_DIR/*

# Extract and test backup
tar -xzf $LATEST_BACKUP/base.tar.gz -C $TEST_RESTORE_DIR

# Start test instance on different port
sudo -u postgres /usr/pgsql-16/bin/pg_ctl -D $TEST_RESTORE_DIR -o "-p 5433" -l $TEST_RESTORE_DIR/logfile start

# Wait for startup
sleep 10

# Test connection and basic functionality
if psql -h localhost -p 5433 -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
    echo "Backup validation successful"
    
    # Get database sizes from test instance
    psql -h localhost -p 5433 -U postgres -c "
    SELECT datname, pg_size_pretty(pg_database_size(datname)) as size 
    FROM pg_database 
    WHERE datname NOT IN ('template0', 'template1');"
    
else
    echo "Backup validation failed"
fi

# Stop test instance
sudo -u postgres /usr/pgsql-16/bin/pg_ctl -D $TEST_RESTORE_DIR stop

# Cleanup
rm -rf $TEST_RESTORE_DIR
```

[Back to top](#table-of-contents)

---

## Monitoring and Maintenance

### Performance Monitoring Queries

#### Database Health Check

```sql
-- Database overview
SELECT 
    datname as database,
    pg_size_pretty(pg_database_size(datname)) as size,
    numbackends as connections,
    xact_commit + xact_rollback as total_transactions,
    ROUND(100.0 * xact_commit / (xact_commit + xact_rollback), 2) as commit_ratio,
    blks_read + blks_hit as total_buffers,
    ROUND(100.0 * blks_hit / (blks_read + blks_hit), 2) as cache_hit_ratio,
    tup_returned,
    tup_fetched,
    tup_inserted + tup_updated + tup_deleted as total_dml,
    stats_reset
FROM pg_stat_database 
WHERE datname NOT IN ('template0', 'template1')
ORDER BY pg_database_size(datname) DESC;

-- Table statistics
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) as indexes_size,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_tuples,
    n_dead_tup as dead_tuples,
    ROUND(100.0 * n_dead_tup / GREATEST(n_live_tup + n_dead_tup, 1), 2) as dead_tuple_percent,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;
```

#### Connection and Session Monitoring

```sql
-- Active connections by state
SELECT 
    state,
    count(*) as connections,
    max(extract(epoch from (now() - state_change))::int) as max_duration_seconds
FROM pg_stat_activity 
WHERE state IS NOT NULL
GROUP BY state
ORDER BY connections DESC;

-- Long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    datname,
    usename,
    client_addr,
    state,
    left(query, 100) as query_snippet
FROM pg_stat_activity 
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
    AND state != 'idle'
ORDER BY duration DESC;

-- Blocking queries
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
        AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE
        AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
        AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
        AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
        AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
        AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
        AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
        AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
        AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
        AND blocking_locks.pid != blocked_locks.pid
    JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.GRANTED;
```

### Automated Maintenance Scripts

#### Daily Maintenance Script

```bash
#!/bin/bash
# PostgreSQL daily maintenance script

POSTGRES_USER="postgres"
POSTGRES_DB="postgres"
LOG_FILE="/var/log/postgresql_maintenance.log"
MAIL_TO="dba@company.com"

echo "=== PostgreSQL Maintenance - $(date) ===" >> $LOG_FILE

# Function to execute SQL and log results
execute_sql() {
    local sql="$1"
    local description="$2"
    
    echo "--- $description ---" >> $LOG_FILE
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c "$sql" >> $LOG_FILE 2>&1
    echo "" >> $LOG_FILE
}

# Check database sizes
execute_sql "
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database 
WHERE datname NOT IN ('template0', 'template1')
ORDER BY pg_database_size(datname) DESC;" "Database Sizes"

# Check for bloated tables
execute_sql "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    n_dead_tup,
    n_live_tup,
    ROUND(100.0 * n_dead_tup / GREATEST(n_live_tup + n_dead_tup, 1), 2) as dead_tuple_percent
FROM pg_stat_user_tables 
WHERE n_dead_tup > 1000 AND n_live_tup > 0
ORDER BY dead_tuple_percent DESC;" "Bloated Tables"

# Check replication lag (if applicable)
execute_sql "
SELECT 
    client_addr,
    state,
    extract(epoch from (now() - backend_start))::int as connection_duration,
    extract(epoch from write_lag)::numeric(10,3) as write_lag_seconds,
    extract(epoch from flush_lag)::numeric(10,3) as flush_lag_seconds,
    extract(epoch from replay_lag)::numeric(10,3) as replay_lag_seconds
FROM pg_stat_replication;" "Replication Status"

# Update table statistics (weekly on Sunday)
if [ $(date +%u) -eq 7 ]; then
    echo "--- Running Weekly Statistics Update ---" >> $LOG_FILE
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
    SELECT 'ANALYZE ' || schemaname || '.' || tablename || ';' 
    FROM pg_stat_user_tables;" -t | psql -U $POSTGRES_USER -d $POSTGRES_DB >> $LOG_FILE 2>&1
fi

# Check disk usage
echo "--- Disk Usage ---" >> $LOG_FILE
df -h /var/lib/postgresql >> $LOG_FILE

# Check for large log files
echo "--- Large Log Files ---" >> $LOG_FILE
find /var/log/postgresql -name "*.log" -size +100M -exec ls -lh {} \; >> $LOG_FILE

# Send email if maintenance log contains errors
if grep -i error $LOG_FILE >/dev/null; then
    mail -s "PostgreSQL Maintenance Errors - $(hostname)" $MAIL_TO < $LOG_FILE
fi

echo "=== Maintenance Complete - $(date) ===" >> $LOG_FILE
```

#### Performance Report Script

```bash
#!/bin/bash
# PostgreSQL performance report generator

POSTGRES_USER="postgres"
POSTGRES_DB="postgres"
REPORT_DIR="/var/reports/postgresql"
DATE=$(date +%Y%m%d)

mkdir -p $REPORT_DIR

# Generate comprehensive performance report
psql -U $POSTGRES_USER -d $POSTGRES_DB << EOF > $REPORT_DIR/performance_report_$DATE.txt

-- Server Information
\echo '=== Server Information ==='
SELECT 'PostgreSQL Version' as metric, version() as value;
SELECT 'Server Uptime' as metric, 
       date_trunc('second', now() - pg_postmaster_start_time()) as value;
SELECT 'Configuration File' as metric, 
       setting as value FROM pg_settings WHERE name = 'config_file';

-- Memory and Buffer Statistics
\echo '\n=== Memory and Buffer Statistics ==='
SELECT 
    'Shared Buffers' as metric,
    pg_size_pretty((SELECT setting::bigint * 8192 FROM pg_settings WHERE name = 'shared_buffers')) as value;
SELECT 
    'Work Memory' as metric,
    (SELECT setting FROM pg_settings WHERE name = 'work_mem') || ' kB' as value;
SELECT 
    'Effective Cache Size' as metric,
    pg_size_pretty((SELECT setting::bigint * 8192 FROM pg_settings WHERE name = 'effective_cache_size')) as value;

-- Connection Statistics
\echo '\n=== Connection Statistics ==='
SELECT 
    'Max Connections' as metric,
    setting as value 
FROM pg_settings WHERE name = 'max_connections';
SELECT 
    'Current Connections' as metric,
    count(*)::text as value 
FROM pg_stat_activity;
SELECT 
    'Active Queries' as metric,
    count(*)::text as value 
FROM pg_stat_activity WHERE state = 'active';

-- Database Statistics
\echo '\n=== Database Statistics ==='
SELECT 
    datname as database,
    numbackends as connections,
    xact_commit as commits,
    xact_rollback as rollbacks,
    blks_read as disk_reads,
    blks_hit as buffer_hits,
    ROUND(100.0 * blks_hit / GREATEST(blks_hit + blks_read, 1), 2) as cache_hit_ratio,
    tup_returned,
    tup_fetched,
    tup_inserted + tup_updated + tup_deleted as total_writes
FROM pg_stat_database 
WHERE datname NOT IN ('template0', 'template1')
ORDER BY datname;

-- Top 10 Largest Tables
\echo '\n=== Top 10 Largest Tables ==='
SELECT 
    schemaname || '.' || tablename as table_name,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) as indexes_size
FROM pg_stat_user_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC 
LIMIT 10;

-- Top 10 Most Active Tables
\echo '\n=== Top 10 Most Active Tables ==='
SELECT 
    schemaname || '.' || tablename as table_name,
    seq_scan as sequential_scans,
    seq_tup_read as seq_tuples_read,
    idx_scan as index_scans,
    idx_tup_fetch as idx_tuples_fetched,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables 
ORDER BY (seq_tup_read + idx_tup_fetch + n_tup_ins + n_tup_upd + n_tup_del) DESC 
LIMIT 10;

-- Slowest Queries (requires pg_stat_statements)
\echo '\n=== Top 10 Slowest Queries ==='
SELECT 
    ROUND(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    ROUND(mean_exec_time::numeric, 2) as avg_time_ms,
    ROUND(100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 1) AS hit_percent,
    left(query, 80) as query_sample
FROM pg_stat_statements 
WHERE calls > 5
ORDER BY total_exec_time DESC 
LIMIT 10;

EOF

echo "Performance report generated: $REPORT_DIR/performance_report_$DATE.txt"
```

### Monitoring with pg_stat_monitor

```bash
# Install pg_stat_monitor extension
# Download from: https://github.com/percona/pg_stat_monitor

# Add to postgresql.conf
echo "shared_preload_libraries = 'pg_stat_monitor'" >> /var/lib/postgresql/16/data/postgresql.conf

# Restart PostgreSQL
sudo systemctl restart postgresql-16

# Create extension in database
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS pg_stat_monitor;"

# Configure pg_stat_monitor
sudo -u postgres psql << EOF
-- Configure monitoring parameters
SELECT pg_stat_monitor_reset();
ALTER SYSTEM SET pg_stat_monitor.pgsm_max = 10000;
ALTER SYSTEM SET pg_stat_monitor.pgsm_query_max_len = 2048;
ALTER SYSTEM SET pg_stat_monitor.pgsm_track = 'all';
SELECT pg_reload_conf();
EOF
```

[Back to top](#table-of-contents)

---

## Troubleshooting

### Common Issues and Solutions

#### 1. PostgreSQL Won't Start

```bash
# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-16-main.log

# Common startup issues:

# Issue: Port already in use
sudo netstat -tlnp | grep :5432
sudo lsof -i :5432

# Issue: Permission problems
sudo chown -R postgres:postgres /var/lib/postgresql/16/data
sudo chmod 700 /var/lib/postgresql/16/data

# Issue: Insufficient shared memory
echo 'kernel.shmmax = 68719476736' >> /etc/sysctl.conf
echo 'kernel.shmall = 16777216' >> /etc/sysctl.conf
sysctl -p

# Issue: Lock file exists
sudo rm /var/lib/postgresql/16/data/postmaster.pid

# Issue: Disk space full
df -h /var/lib/postgresql
sudo du -sh /var/lib/postgresql/16/data/*
```

#### 2. Connection Issues

```sql
-- Check connection limits
SHOW max_connections;
SHOW superuser_reserved_connections;

-- Check current connections
SELECT 
    datname,
    usename,
    client_addr,
    state,
    count(*)
FROM pg_stat_activity 
GROUP BY datname, usename, client_addr, state
ORDER BY count(*) DESC;

-- Check pg_hba.conf configuration
SELECT * FROM pg_hba_file_rules WHERE error IS NOT NULL;

-- Test connection from different hosts
-- From local host
psql -h localhost -U username -d database

-- From remote host
psql -h server.domain.com -U username -d database

-- Check SSL configuration
SELECT name, setting FROM pg_settings WHERE name LIKE 'ssl%';
```

#### 3. Performance Issues

```sql
-- Identify slow queries
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE mean_exec_time > 1000  -- queries averaging more than 1 second
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check for table bloat
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    ROUND(100 * n_dead_tup / (n_dead_tup + n_live_tup + 1), 1) AS dead_pct
FROM pg_stat_user_tables 
WHERE n_dead_tup > 0
ORDER BY dead_pct DESC;

-- Manual vacuum for bloated tables
VACUUM VERBOSE ANALYZE table_name;

-- Check for lock contention
SELECT 
    locktype,
    database,
    relation::regclass,
    page,
    tuple,
    virtualxid,
    transactionid,
    mode,
    granted,
    count(*)
FROM pg_locks 
GROUP BY locktype, database, relation, page, tuple, virtualxid, transactionid, mode, granted
HAVING count(*) > 1
ORDER BY count(*) DESC;
```

#### 4. Replication Issues

```sql
-- Check replication lag on master
SELECT 
    client_addr,
    client_hostname,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag,
    sync_state,
    sync_priority
FROM pg_stat_replication;

-- Check standby status
SELECT 
    pg_is_in_recovery(),
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn(),
    pg_last_xact_replay_timestamp();

-- Calculate replication lag in seconds
SELECT 
    CASE 
        WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0
        ELSE EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))
    END AS lag_seconds;

-- Restart replication if stuck
-- On standby server:
SELECT pg_promote();

-- Recreate replication from scratch if needed
-- Stop standby, remove data directory, run pg_basebackup again
```

### Emergency Recovery Procedures

#### 1. Database Corruption Recovery

```bash
# Single-user mode for emergency repairs
sudo -u postgres /usr/pgsql-16/bin/postgres --single -D /var/lib/postgresql/16/data database_name

# In single-user mode, run:
REINDEX DATABASE database_name;
VACUUM FULL;

# If corruption is severe, try to extract data
pg_dump -Fc -v database_name > emergency_backup.dump

# Recreate database if necessary
dropdb database_name
createdb database_name
pg_restore -v -d database_name emergency_backup.dump
```

#### 2. Transaction Log Corruption

```bash
# Reset transaction logs (DANGEROUS - only in emergencies)
sudo systemctl stop postgresql-16
sudo -u postgres /usr/pgsql-16/bin/pg_resetwal -f /var/lib/postgresql/16/data

# Restart PostgreSQL
sudo systemctl start postgresql-16

# Immediately dump all data
pg_dumpall > emergency_full_dump.sql
```

#### 3. Disk Space Emergency

```bash
# Quick space recovery
# Move or compress old log files
cd /var/lib/postgresql/16/data/log
gzip postgresql-*.log

# Remove old WAL files if archiving is not critical
cd /var/lib/postgresql/16/data/pg_wal
rm -f 0000000100000000000000[0-5]*

# Vacuum to reclaim space
psql -d database_name -c "VACUUM FULL VERBOSE;"

# Drop unused databases/tables if safe
psql -c "DROP DATABASE old_database;"
```

---

## Maintenance Checklist

### Daily Tasks

- [ ] Check PostgreSQL service status
- [ ] Monitor database connections and sessions
- [ ] Review PostgreSQL error logs
- [ ] Verify backup completion
- [ ] Check disk space usage
- [ ] Monitor replication lag (if applicable)
- [ ] Review slow query log

### Weekly Tasks

- [ ] Run ANALYZE on frequently updated tables
- [ ] Check for bloated tables and indexes
- [ ] Review vacuum statistics
- [ ] Monitor index usage statistics
- [ ] Check for unused indexes
- [ ] Review pg_stat_statements data
- [ ] Validate backup restore procedures

### Monthly Tasks

- [ ] Run VACUUM FULL on heavily updated tables
- [ ] REINDEX tables with significant bloat
- [ ] Review and optimize postgresql.conf settings
- [ ] Analyze query performance trends
- [ ] Update table statistics manually if needed
- [ ] Check for PostgreSQL updates# PostgreSQL Installation and Configuration Guide
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
