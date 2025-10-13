
# Linux for DBRE - Portfolio Guide
---
Linux Configuration Guide for DBA and DBRE

![RHEL 9](https://img.shields.io/badge/RHEL-9-EE0000?style=for-the-badge&logo=redhat&logoColor=white)
![Ubuntu 24.04 LTS](https://img.shields.io/badge/Ubuntu-24.04%20LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Debian 12](https://img.shields.io/badge/Debian-12-A81D33?style=for-the-badge&logo=debian&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white)
![openSUSE](https://img.shields.io/badge/openSUSE-73BA25?style=for-the-badge&logo=opensuse&logoColor=white)
![Oracle Linux 9](https://img.shields.io/badge/Oracle%20Linux-9-F80000?style=for-the-badge&logo=oracle&logoColor=white)
![Rocky Linux 9](https://img.shields.io/badge/Rocky%20Linux-9-10B981?style=for-the-badge&logo=rockylinux&logoColor=white)
![AlmaLinux 9](https://img.shields.io/badge/AlmaLinux-9-2E95EA?style=for-the-badge&logo=almalinux&logoColor=white)

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose & Scope](#11-purpose--scope)
   - 1.2 [Target Audience](#12-target-audience)
2. [Essential Linux Commands for DBRE](#2-essential-linux-commands-for-dbre)
   - 2.1 [File System Operations](#21-file-system-operations)
   - 2.2 [Process Management](#22-process-management)
   - 2.3 [Network Diagnostics](#23-network-diagnostics)
   - 2.4 [Disk & Storage Management](#24-disk--storage-management)
   - 2.5 [Text Processing & Log Analysis](#25-text-processing--log-analysis)
3. [Performance Monitoring & Diagnostics](#3-performance-monitoring--diagnostics)
   - 3.1 [System Resources](#31-system-resources-cpu-memory-io)
   - 3.2 [Real-time Monitoring Tools](#32-real-time-monitoring-tools)
   - 3.3 [Historical Performance Analysis](#33-historical-performance-analysis)
4. [Database-Specific Linux Operations](#4-database-specific-linux-operations)
   - 4.1 [Oracle Database on Red Hat Linux](#41-oracle-database-on-red-hat-linux)
   - 4.2 [SQL Server on Linux](#42-sql-server-on-linux)
   - 4.3 [MySQL/MariaDB](#43-mysqlmariadb)
   - 4.4 [MongoDB](#44-mongodb)
   - 4.5 [Redis](#45-redis)
   - 4.6 [DB2](#46-db2)
5. [Automation & Scripting](#5-automation--scripting)
   - 5.1 [Shell Scripting for Database Tasks](#51-shell-scripting-for-database-tasks)
   - 5.2 [Cron Jobs & Scheduling](#52-cron-jobs--scheduling)
   - 5.3 [Systemd Services](#53-systemd-services)
6. [Security & Access Control](#6-security--access-control)
   - 6.1 [User & Permission Management](#61-user--permission-management)
   - 6.2 [Firewall Configuration](#62-firewall-configuration-firewalld)
   - 6.3 [SELinux Essentials](#63-selinux-essentials)
   - 6.4 [SSH Hardening](#64-ssh-hardening)
7. [Backup & Recovery Operations](#7-backup--recovery-operations)
   - 7.1 [File System Backups](#71-file-system-backups)
   - 7.2 [Database Backup Commands](#72-database-backup-commands)
   - 7.3 [Recovery Procedures](#73-recovery-procedures)
8. [Troubleshooting Guide](#8-troubleshooting-guide)
   - 8.1 [System Performance Issues](#81-system-performance-issues)
   - 8.2 [Database Connectivity Problems](#82-database-connectivity-problems)
   - 8.3 [Storage & I/O Issues](#83-storage--io-issues)
   - 8.4 [Log Analysis Techniques](#84-log-analysis-techniques)
9. [High Availability & Clustering](#9-high-availability--clustering)
   - 9.1 [Pacemaker/Corosync Basics](#91-pacemakercorosync-basics)
   - 9.2 [Network Configuration for HA](#92-network-configuration-for-ha)
   - 9.3 [Shared Storage Management](#93-shared-storage-management)
10. [DBRE/SRE Best Practices](#10-dbresre-best-practices)
    - 10.1 [Monitoring Strategies](#101-monitoring-strategies)
    - 10.2 [Incident Response Workflows](#102-incident-response-workflows)
    - 10.3 [Change Management](#103-change-management)
    - 10.4 [Documentation & Runbooks](#104-documentation--runbooks)
    - 10.5 [On-Call Best Practices](#105-on-call-best-practices)

---

## 1. Introduction

### 1.1 Purpose & Scope

This guide provides essential Linux commands and practices for Database Reliability Engineers (DBRE) working with Red Hat Enterprise Linux. It focuses on practical, day-to-day operations for managing Oracle, SQL Server, MySQL, MongoDB, Redis, and DB2 databases. The content emphasizes command-line efficiency, troubleshooting techniques, and operational reliability.

### 1.2 Target Audience

This documentation is designed for DBREs, SREs, and database administrators who need quick reference for Linux operations in production database environments. It assumes basic Linux knowledge and focuses on intermediate to advanced commands that directly impact database reliability and performance.

---

## 2. Essential Linux Commands for DBRE

### 2.1 File System Operations

Efficient file system navigation and manipulation are critical for database file management. Understanding file permissions, ownership, and storage locations enables quick diagnosis of database issues related to file access and space management.

```bash
# Find large database files
find /u01/app/oracle -type f -size +1G -exec ls -lh {} \;

# Check directory size for database locations
du -sh /var/lib/mysql /var/opt/mssql /data/mongodb

# Locate Oracle trace files modified in last 24 hours
find /u01/app/oracle/diag -name "*.trc" -mtime -1

# Change ownership recursively for database directories
chown -R oracle:oinstall /u01/app/oracle/product/19c

# Set proper permissions for database files
chmod 640 /etc/my.cnf /var/opt/mssql/mssql.conf
```

### 2.2 Process Management

Managing database processes requires identifying resource-intensive operations, controlling service states, and investigating hung processes. Proper process management prevents system overload and enables graceful shutdowns during maintenance.

```bash
# Find Oracle processes and their memory usage
ps aux | grep pmon | grep -v grep
ps -eo pid,user,%cpu,%mem,vsz,rss,comm | grep oracle

# Kill specific database session (use with caution)
kill -9 $(ps aux | grep 'LOCAL=NO' | awk '{print $2}')

# Check SQL Server processes
ps aux | grep sqlservr

# Monitor MongoDB connections
ps aux | grep mongod | wc -l

# View process tree for database hierarchy
pstree -p $(pgrep -o pmon)
```

### 2.3 Network Diagnostics

Network connectivity is fundamental for database client connections, replication, and cluster communication. Quick network diagnostics help identify connectivity issues before they escalate to service outages.

```bash
# Test Oracle listener connectivity
telnet hostname 1521
nc -zv hostname 1521

# Check all listening database ports
netstat -tuln | grep -E '1521|3306|1433|27017|6379|50000'
ss -tuln | grep LISTEN

# Verify firewall rules for database ports
firewall-cmd --list-all | grep -E '1521|3306|1433'

# Test network latency to replica
ping -c 5 replica-hostname
traceroute replica-hostname

# Check established database connections
netstat -an | grep ESTABLISHED | grep 1521 | wc -l
```

### 2.4 Disk & Storage Management

Database performance heavily depends on disk I/O capabilities and available storage. Monitoring disk usage, throughput, and latency helps prevent storage-related outages and identifies performance bottlenecks.

```bash
# Check disk usage for database filesystems
df -h | grep -E 'oracle|mysql|mssql|mongodb'

# Monitor I/O statistics in real-time
iostat -x 2 5

# Identify which process is using disk I/O
iotop -o

# Check LVM volumes for database storage
lvdisplay | grep -A 5 "LV Name"
vgdisplay

# Verify mount options for database filesystems
mount | grep -E 'oracle|data'

# Test disk write performance
dd if=/dev/zero of=/u01/testfile bs=1G count=1 oflag=direct
```

### 2.5 Text Processing & Log Analysis

Database logs contain critical diagnostic information. Efficient log analysis using grep, awk, and sed enables rapid identification of errors, performance issues, and security events across multiple database platforms.

```bash
# Search Oracle alert log for errors
grep -i "ora-\|error" /u01/app/oracle/diag/rdbms/*/alert_*.log | tail -50

# Count specific errors in logs
grep -c "ORA-00600" /u01/app/oracle/diag/rdbms/*/trace/*.trc

# Extract slow queries from MySQL slow log
awk '/Query_time: [5-9]|Query_time: [0-9]{2,}/ {print; getline; print}' /var/lib/mysql/slow.log

# Parse SQL Server error log for deadlocks
grep -A 10 "deadlock" /var/opt/mssql/log/errorlog

# MongoDB log analysis for slow operations
grep "SLOW" /var/log/mongodb/mongod.log | tail -20

# Real-time log monitoring with filtering
tail -f /var/log/messages | grep --line-buffered -i "database\|error\|fail"
```

---

## 3. Performance Monitoring & Diagnostics

### 3.1 System Resources (CPU, Memory, I/O)

Understanding system resource utilization is essential for database performance tuning. DBREs must quickly identify CPU bottlenecks, memory pressure, and I/O contention that impact database operations. Red Hat provides comprehensive tools for real-time and historical analysis.

```bash
# CPU usage per core
mpstat -P ALL 2 5

# Memory breakdown including cache and buffers
free -h
cat /proc/meminfo | grep -E 'MemTotal|MemFree|Cached|Buffers'

# Identify memory-hungry database processes
ps aux --sort=-%mem | head -10

# Check swap usage (critical for databases)
swapon -s
vmstat 2 5

# I/O wait time (high values indicate disk bottleneck)
iostat -x 2 5 | grep -E 'Device|sd|vd'

# Identify top I/O consuming processes
pidstat -d 2 5
```

### 3.2 Real-time Monitoring Tools

Real-time monitoring enables immediate response to performance degradation. Tools like top, htop, and glances provide interactive dashboards for system health, while specialized utilities offer database-specific insights into resource consumption patterns.

```bash
# Interactive process viewer with color coding
htop -u oracle

# Real-time system overview
glances --disable-quicklook

# Monitor specific Oracle processes
top -p $(pgrep -d',' pmon)

# Track network connections in real-time
watch -n 2 'netstat -an | grep ESTABLISHED | wc -l'

# Live disk I/O monitoring
iotop -oPa

# Real-time memory usage by process
watch -n 1 'ps aux --sort=-%mem | head -15'
```

### 3.3 Historical Performance Analysis

Historical data analysis identifies trends, capacity planning needs, and recurring performance patterns. Using sar (System Activity Reporter), DBREs can investigate issues that occurred during off-hours and correlate system metrics with database performance problems.

```bash
# CPU usage history for past 24 hours
sar -u -f /var/log/sa/sa$(date +%d -d yesterday)

# Memory usage history
sar -r 2 10

# Disk I/O history
sar -d -p 2 10

# Network traffic history
sar -n DEV 2 10

# Review system performance from specific date
sar -A -f /var/log/sa/sa15

# Generate performance report for yesterday
sar -f /var/log/sa/sa$(date +%d -d yesterday) > perf_report_$(date +%Y%m%d).txt
```

---

## 4. Database-Specific Linux Operations

### 4.1 Oracle Database on Red Hat Linux

Oracle Database requires specific environment variables, kernel parameters, and user configurations on Red Hat Linux. DBREs must manage Oracle services, listener configurations, and ASM storage while ensuring proper resource limits and system settings for optimal performance.

```bash
# Set Oracle environment
export ORACLE_HOME=/u01/app/oracle/product/19c/dbhome_1
export ORACLE_SID=PRODDB
export PATH=$ORACLE_HOME/bin:$PATH

# Check Oracle processes and memory
ps -ef | grep pmon
ipcs -m | grep oracle

# Start/stop Oracle database
su - oracle -c "sqlplus / as sysdba" <<EOF
startup;
exit;
EOF

# Check listener status
lsnrctl status
lsnrctl services

# Verify kernel parameters for Oracle
sysctl -a | grep -E 'shmmax|shmmni|shmall|sem'

# Monitor Oracle ASM disks
oracleasm listdisks
ls -l /dev/oracleasm/disks/

# Check Oracle user limits
su - oracle -c 'ulimit -a'
```

### 4.2 SQL Server on Linux

Microsoft SQL Server on Linux uses systemd for service management and requires specific configurations for TLS, memory management, and high availability. Understanding mssql-conf tool and log locations is crucial for troubleshooting SQL Server on Red Hat environments.

```bash
# Manage SQL Server service
systemctl status mssql-server
systemctl restart mssql-server
journalctl -u mssql-server -n 50

# Check SQL Server configuration
cat /var/opt/mssql/mssql.conf

# Verify SQL Server memory settings
grep -i memory /var/opt/mssql/mssql.conf

# Test SQL Server connectivity
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourPassword' -Q "SELECT @@VERSION"

# Monitor SQL Server resource usage
pidstat -p $(pgrep sqlservr) 2 5

# Check SQL Server error log
tail -f /var/opt/mssql/log/errorlog

# Verify TLS certificates
ls -l /var/opt/mssql/security/
```

### 4.3 MySQL/MariaDB

MySQL and MariaDB management on Red Hat Linux involves configuration file handling, storage engine tuning, and replication monitoring. DBREs must understand socket connections, user privileges, and binary log management for reliable operation.

```bash
# Manage MySQL service
systemctl status mysqld
systemctl restart mariadb

# Check MySQL configuration
cat /etc/my.cnf /etc/my.cnf.d/*.cnf

# Verify MySQL socket and port
netstat -ln | grep 3306
ls -l /var/lib/mysql/mysql.sock

# Test MySQL connectivity
mysql -u root -p -e "SELECT VERSION();"

# Check MySQL data directory size
du -sh /var/lib/mysql/

# Monitor MySQL error log
tail -f /var/log/mysqld.log

# Verify binary log settings
ls -lh /var/lib/mysql/binlog.*
```

### 4.4 MongoDB

MongoDB on Red Hat Linux requires proper configuration for WiredTiger cache, replica sets, and sharding. Understanding MongoDB's storage engine, NUMA settings, and transparent huge pages is essential for production deployments.

```bash
# Manage MongoDB service
systemctl status mongod
systemctl restart mongod

# Check MongoDB configuration
cat /etc/mongod.conf

# Verify MongoDB data directory
du -sh /var/lib/mongo/
ls -lh /var/lib/mongo/

# Test MongoDB connectivity
mongosh --eval "db.adminCommand('serverStatus')"

# Monitor MongoDB logs
tail -f /var/log/mongodb/mongod.log

# Check replica set status
mongosh --eval "rs.status()"

# Disable transparent huge pages (recommended)
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
```

### 4.5 Redis

Redis requires careful memory management, persistence configuration, and replication setup on Red Hat Linux. DBREs must monitor Redis memory usage, understand RDB and AOF persistence modes, and configure proper limits for production environments.

```bash
# Manage Redis service
systemctl status redis
systemctl restart redis

# Check Redis configuration
cat /etc/redis.conf | grep -v "^#" | grep -v "^$"

# Test Redis connectivity
redis-cli ping
redis-cli INFO

# Monitor Redis memory usage
redis-cli INFO memory

# Check Redis persistence files
ls -lh /var/lib/redis/dump.rdb
ls -lh /var/lib/redis/appendonly.aof

# Monitor slow queries
redis-cli SLOWLOG GET 10

# Check Redis replication status
redis-cli INFO replication
```

### 4.6 DB2

IBM DB2 on Red Hat Linux requires instance management, tablespace monitoring, and proper kernel parameter configuration. Understanding DB2 registry variables, diagnostic logs, and the db2 command-line processor is critical for DB2 administration.

```bash
# Set DB2 environment
su - db2inst1
. /home/db2inst1/sqllib/db2profile

# Check DB2 instance status
db2pd -inst

# List databases
db2 list database directory

# Connect to database
db2 connect to PRODDB

# Check tablespace usage
db2 list tablespaces show detail

# Monitor DB2 processes
ps aux | grep db2sys

# Check DB2 diagnostic logs
db2diag -h /home/db2inst1/sqllib/db2dump

# Verify kernel parameters for DB2
sysctl -a | grep kernel.sem
```

---

## 5. Automation & Scripting

### 5.1 Shell Scripting for Database Tasks

Shell scripting automates repetitive database operations, reducing human error and enabling consistent execution of complex tasks. DBREs use bash scripts for health checks, backup validation, log rotation, and automated recovery procedures across multiple database platforms.

```bash
#!/bin/bash
# Database health check script example

check_oracle_status() {
    export ORACLE_HOME=/u01/app/oracle/product/19c/dbhome_1
    export ORACLE_SID=PRODDB
    STATUS=$($ORACLE_HOME/bin/sqlplus -s / as sysdba <<EOF
    SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
    SELECT status FROM v\$instance;
    EXIT;
EOF
    )
    echo "Oracle Status: $STATUS"
}

check_mysql_status() {
    systemctl is-active mysqld >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "MySQL Status: Running"
    else
        echo "MySQL Status: Stopped"
    fi
}

# Execute checks
check_oracle_status
check_mysql_status
```

### 5.2 Cron Jobs & Scheduling

Cron scheduling enables automated execution of database maintenance tasks, backups, and monitoring scripts. Proper cron configuration ensures reliable execution timing, logging, and error handling for critical database operations.

```bash
# Edit crontab for oracle user
crontab -e -u oracle

# Example cron entries for database operations

# Daily RMAN backup at 2 AM
0 2 * * * /home/oracle/scripts/rman_backup.sh >> /var/log/oracle/backup.log 2>&1

# Hourly log rotation check
0 * * * * find /u01/app/oracle/diag -name "*.trc" -mtime +7 -delete

# MySQL binlog purge daily at 3 AM
0 3 * * * mysql -u root -p'password' -e "PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);" >> /var/log/mysql_purge.log 2>&1

# MongoDB backup every 6 hours
0 */6 * * * /usr/bin/mongodump --out /backup/mongo/$(date +\%Y\%m\%d_\%H\%M) >> /var/log/mongo_backup.log 2>&1

# Redis snapshot every 4 hours
0 */4 * * * redis-cli BGSAVE >> /var/log/redis_backup.log 2>&1

# List current cron jobs
crontab -l -u oracle
```

### 5.3 Systemd Services

Systemd provides robust service management for database processes, including automatic restart, resource limits, and dependency management. Creating custom systemd units enables standardized database service control across Red Hat environments.

```bash
# Check database service status
systemctl status oracle-db.service
systemctl status mssql-server.service

# View systemd unit file
systemctl cat mysqld.service

# Example custom Oracle systemd unit
cat /etc/systemd/system/oracle-db.service
[Unit]
Description=Oracle Database Service
After=network.target

[Service]
Type=forking
User=oracle
ExecStart=/home/oracle/scripts/start_db.sh
ExecStop=/home/oracle/scripts/stop_db.sh
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target

# Enable service to start at boot
systemctl enable oracle-db.service

# View service logs
journalctl -u mssql-server -n 100 -f

# Restart service with timeout
systemctl restart mysqld.service --timeout=300
```

---

## 6. Security & Access Control

### 6.1 User & Permission Management

Proper user and permission management prevents unauthorized database access and maintains security compliance. DBREs must configure appropriate user accounts, group memberships, and file permissions for database software, data directories, and configuration files.

```bash
# Create database user with specific UID
useradd -u 54321 -g oinstall -G dba,oper oracle

# Verify user groups
id oracle
groups oracle

# Set proper ownership for database directories
chown -R oracle:oinstall /u01/app/oracle
chown -R mysql:mysql /var/lib/mysql

# Configure secure file permissions
chmod 750 /u01/app/oracle/product/19c
chmod 640 /etc/my.cnf
chmod 600 /var/opt/mssql/secrets/*

# Manage sudo access for database users
visudo
# Add: oracle ALL=(ALL) NOPASSWD: /bin/systemctl restart oracle-db

# Review user login history
last -a | grep oracle
```

### 6.2 Firewall Configuration (firewalld)

Firewalld configuration controls network access to database ports, ensuring only authorized systems can connect. DBREs must configure appropriate zones, services, and rich rules while maintaining security without blocking legitimate database traffic.

```bash
# Check firewalld status
systemctl status firewalld
firewall-cmd --state

# List active zones and rules
firewall-cmd --get-active-zones
firewall-cmd --list-all

# Open Oracle listener port
firewall-cmd --permanent --add-port=1521/tcp
firewall-cmd --reload

# Open multiple database ports
firewall-cmd --permanent --add-port={3306/tcp,1433/tcp,27017/tcp,6379/tcp}
firewall-cmd --reload

# Add rich rule for specific source
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="1521" accept'

# Remove port from firewall
firewall-cmd --permanent --remove-port=1521/tcp
firewall-cmd --reload

# View all open ports
firewall-cmd --list-ports
```

### 6.3 SELinux Essentials

SELinux provides mandatory access control that can block database operations if not properly configured. Understanding SELinux contexts, booleans, and audit logs is essential for resolving permission denied errors in secured Red Hat environments.

```bash
# Check SELinux status
getenforce
sestatus

# View SELinux context for database directories
ls -Z /var/lib/mysql
ls -Z /u01/app/oracle

# Set correct SELinux context
semanage fcontext -a -t mysqld_db_t "/data/mysql(/.*)?"
restorecon -Rv /data/mysql

# Check SELinux booleans for databases
getsebool -a | grep -E 'mysql|oracle|mssql|mongodb'

# Enable SELinux boolean
setsebool -P mysql_connect_any 1
setsebool -P postgresql_can_rsync 1

# Review SELinux denials
ausearch -m avc -ts recent | grep denied
sealert -a /var/log/audit/audit.log

# Temporarily disable SELinux (troubleshooting only)
setenforce 0
```

### 6.4 SSH Hardening

SSH hardening protects database servers from unauthorized remote access while maintaining operational efficiency. DBREs must configure key-based authentication, disable root login, and implement connection restrictions for secure remote database administration.

```bash
# Generate SSH key pair for database server access
ssh-keygen -t ed25519 -C "dbre@company.com"

# Copy public key to remote server
ssh-copy-id -i ~/.ssh/id_ed25519.pub oracle@dbserver01

# Harden SSH configuration
vi /etc/ssh/sshd_config
# Recommended settings:
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes
# Port 2222 (non-standard port)
# AllowUsers oracle dba

# Restart SSH service
systemctl restart sshd

# Test SSH connection
ssh -i ~/.ssh/id_ed25519 oracle@dbserver01 -p 2222

# View SSH login attempts
grep "Failed password" /var/log/secure
grep "Accepted publickey" /var/log/secure
```

---

## 7. Backup & Recovery Operations

### 7.1 File System Backups

File system backups protect database configuration files, scripts, and documentation. Using tar, rsync, and LVM snapshots, DBREs can create consistent point-in-time copies of critical database infrastructure components independent of database-native backup tools.

```bash
# Backup Oracle configuration files
tar -czf /backup/oracle_config_$(date +%Y%m%d).tar.gz /u01/app/oracle/product/19c/network/admin /etc/oratab

# Backup MySQL configuration
tar -czf /backup/mysql_config_$(date +%Y%m%d).tar.gz /etc/my.cnf /etc/my.cnf.d/

# Rsync database scripts to backup server
rsync -avz --progress /home/oracle/scripts/ backup-server:/backup/scripts/

# Create LVM snapshot for database filesystem
lvcreate -L 10G -s -n orasnap /dev/vg_data/lv_oracle

# Mount snapshot and backup
mkdir /mnt/orasnap
mount /dev/vg_data/orasnap /mnt/orasnap
tar -czf /backup/ora_snapshot_$(date +%Y%m%d).tar.gz -C /mnt/orasnap .

# Remove snapshot after backup
umount /mnt/orasnap
lvremove -f /dev/vg_data/orasnap
```

### 7.2 Database Backup Commands

Database-native backup commands ensure transactional consistency and enable point-in-time recovery. DBREs must understand backup modes, compression options, and verification procedures for each database platform to guarantee reliable recovery capabilities.

```bash
# Oracle RMAN backup
rman target / <<EOF
BACKUP DATABASE PLUS ARCHIVELOG;
BACKUP CURRENT CONTROLFILE;
DELETE NOPROMPT OBSOLETE;
EXIT;
EOF

# MySQL full backup with mysqldump
mysqldump -u root -p --all-databases --single-transaction --routines --triggers > /backup/mysql_full_$(date +%Y%m%d).sql

# MySQL binary backup with XtraBackup
xtrabackup --backup --target-dir=/backup/mysql/full_$(date +%Y%m%d)

# MongoDB backup
mongodump --host localhost --port 27017 --out /backup/mongo/$(date +%Y%m%d)

# Redis backup (RDB)
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb /backup/redis/dump_$(date +%Y%m%d).rdb

# SQL Server backup via sqlcmd
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Password' -Q "BACKUP DATABASE [ProductionDB] TO DISK='/backup/proddb_$(date +%Y%m%d).bak'"

# DB2 offline backup
db2 backup database PRODDB to /backup/db2
```

### 7.3 Recovery Procedures

Recovery procedures restore databases to operational state after failures, data corruption, or disasters. Understanding recovery modes, validation steps, and verification techniques ensures successful restoration with minimal data loss and downtime.

```bash
# Oracle RMAN restore and recover
rman target / <<EOF
STARTUP MOUNT;
RESTORE DATABASE;
RECOVER DATABASE;
ALTER DATABASE OPEN;
EXIT;
EOF

# MySQL point-in-time recovery
mysql -u root -p < /backup/mysql_full_20251008.sql
mysqlbinlog /var/lib/mysql/binlog.000015 | mysql -u root -p

# MongoDB restore
mongorestore --host localhost --port 27017 /backup/mongo/20251008/

# Redis restore
systemctl stop redis
cp /backup/redis/dump_20251008.rdb /var/lib/redis/dump.rdb
chown redis:redis /var/lib/redis/dump.rdb
systemctl start redis

# Verify Oracle database after recovery
sqlplus / as sysdba <<EOF
SELECT name, open_mode FROM v\$database;
SELECT tablespace_name, status FROM dba_tablespaces;
EXIT;
EOF

# Verify MySQL recovery
mysql -u root -p -e "SHOW DATABASES; SELECT COUNT(*) FROM mysql.user;"
```

---

## 8. Troubleshooting Guide

### 8.1 System Performance Issues

System performance degradation manifests as slow queries, high CPU usage, or excessive wait times. DBREs must quickly identify whether issues originate from hardware limitations, kernel configuration, or resource contention using systematic diagnostic approaches.

```bash
# Identify CPU-bound processes
top -b -n 1 | head -20
ps aux --sort=-%cpu | head -10

# Check system load and uptime
uptime
cat /proc/loadavg

# Identify I/O bottlenecks
iostat -x 2 5
iotop -oPa -n 5

# Memory pressure indicators
free -h
cat /proc/meminfo | grep -E 'MemAvailable|SwapFree'
vmstat 2 5

# Check for Out of Memory killer events
dmesg | grep -i "out of memory"
grep -i "killed process" /var/log/messages

# Network latency testing
ping -c 100 remote-host | tail -5
mtr --report remote-host

# System call analysis for slow process
strace -p <pid> -c -f -e trace=all
```

### 8.2 Database Connectivity Problems

Connectivity issues prevent applications from accessing databases, causing service disruptions. Systematic troubleshooting involves verifying network paths, listener status, firewall rules, and authentication mechanisms across all database platforms.

```bash
# Test basic TCP connectivity
telnet dbserver 1521
nc -zv dbserver 3306

# Check listening ports
netstat -tuln | grep -E '1521|3306|1433|27017|6379'
ss -tuln | grep LISTEN

# Verify Oracle listener
lsnrctl status
lsnrctl services
tnsping PRODDB

# Test MySQL socket connection
mysql -u root -p --socket=/var/lib/mysql/mysql.sock

# Check SQL Server connectivity
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Password' -Q "SELECT @@VERSION"

# Verify firewall rules
firewall-cmd --list-ports
iptables -L -n | grep -E '1521|3306|1433'

# DNS resolution check
nslookup dbserver
dig dbserver

# Monitor active database connections
netstat -an | grep ESTABLISHED | grep 1521 | wc -l
```

### 8.3 Storage & I/O Issues

Storage problems cause database corruption, performance degradation, and service interruptions. DBREs must monitor disk space, identify I/O bottlenecks, and detect failing hardware using comprehensive storage diagnostics.

```bash
# Check filesystem usage and inodes
df -h
df -i

# Identify large files quickly
find /u01 -type f -size +1G -exec ls -lh {} \; 2>/dev/null

# Monitor disk I/O in real-time
iostat -x 2 5
iotop -oPa

# Check for disk errors
dmesg | grep -i error
smartctl -a /dev/sda | grep -E 'Error|SMART'

# Verify mount options
mount | grep -E 'oracle|mysql|data'

# Test write performance
dd if=/dev/zero of=/u01/testfile bs=1M count=1024 oflag=direct conv=fdatasync
rm /u01/testfile

# Check multipath configuration
multipath -ll
dmsetup ls

# Monitor storage queue depth
cat /sys/block/sda/device/queue_depth
```

### 8.4 Log Analysis Techniques

Log analysis reveals root causes of database failures, security incidents, and performance problems. Efficient log parsing using grep, awk, and specialized tools enables rapid diagnosis across multiple log sources and formats.

```bash
# Search Oracle alert log for errors
grep -i "ora-\|error" /u01/app/oracle/diag/rdbms/*/alert_*.log | tail -100

# Analyze Oracle trace files
tkprof trace_file.trc output.txt explain=user/pass

# Parse MySQL error log
grep -E "ERROR|WARN" /var/log/mysqld.log | tail -50

# Identify slow queries in MySQL
mysqldumpslow -s t -t 10 /var/lib/mysql/slow.log

# SQL Server error log analysis
grep -i "error\|fail" /var/opt/mssql/log/errorlog

# MongoDB slow query analysis
grep "SLOW" /var/log/mongodb/mongod.log | awk '{print $0}' | tail -20

# Redis log monitoring
tail -f /var/log/redis/redis.log | grep -E "WARNING|ERROR"

# Centralized log search across multiple files
grep -r "ORA-00600" /u01/app/oracle/diag/rdbms/*/trace/

# Extract timestamps and count errors
awk '/ERROR/ {print $1,$2}' /var/log/mysqld.log | sort | uniq -c
```

---

## 9. High Availability & Clustering

### 9.1 Pacemaker/Corosync Basics

Pacemaker and Corosync provide clustering infrastructure for database high availability on Red Hat Linux. DBREs must configure cluster resources, manage node membership, and monitor cluster health to ensure automatic failover during database failures.

```bash
# Check cluster status
pcs status
crm_mon -1

# View cluster configuration
pcs config
pcs cluster cib

# Manage cluster nodes
pcs cluster start --all
pcs cluster stop --all
pcs cluster standby node01

# Check node communication
corosync-cfgtool -s
corosync-quorumtool -l

# Create database resource
pcs resource create oracledb ocf:heartbeat:oracle sid=PRODDB home=/u01/app/oracle/product/19c/dbhome_1

# Verify resource status
pcs resource show oracledb
pcs resource status

# Manage resource constraints
pcs constraint location oracledb prefers node01=100

# View cluster logs
journalctl -u pacemaker -n 100
journalctl -u corosync -n 100
```

### 9.2 Network Configuration for HA

High availability networking requires redundant network paths, virtual IP addresses, and proper network bonding configuration. Proper network setup ensures seamless client connectivity during database failover events.

```bash
# Configure network bonding for redundancy
cat /proc/net/bonding/bond0

# Create virtual IP for database access
pcs resource create db-vip ocf:heartbeat:IPaddr2 ip=192.168.1.100 cidr_netmask=24 nic=eth0

# Verify network interface configuration
ip addr show
ip link show

# Test virtual IP failover
pcs resource move db-vip node02
ping -c 5 192.168.1.100

# Configure bonding mode
cat /etc/sysconfig/network-scripts/ifcfg-bond0
# BONDING_OPTS="mode=active-backup miimon=100"

# Verify routing for cluster network
ip route show
route -n

# Monitor network interface statistics
ethtool eth0
ethtool -S eth0
```

### 9.3 Shared Storage Management

Shared storage enables multiple cluster nodes to access database files during failover scenarios. DBREs must configure multipath I/O, verify storage connectivity, and ensure proper LUN masking for clustered database environments.

```bash
# Check multipath configuration
multipath -ll
multipathd show config

# Verify shared storage visibility
lsblk
ls -l /dev/disk/by-id/

# Configure multipath for database LUNs
cat /etc/multipath.conf

# Scan for new LUNs
echo "- - -" > /sys/class/scsi_host/host0/scan
rescan-scsi-bus.sh

# Check filesystem cluster awareness
mount | grep -E 'gfs2|ocfs2'

# Configure Oracle ASM for shared storage
oracleasm listdisks
oracleasm createdisk DATA1 /dev/mapper/mpatha

# Verify LUN ownership and permissions
ls -l /dev/mapper/mpath*
chown oracle:asmadmin /dev/mapper/mpatha

# Monitor I/O path status
multipath -ll | grep -E 'active|enabled'
```

---

## 10. DBRE/SRE Best Practices

### 10.1 Monitoring Strategies

Effective monitoring provides early warning of database issues before they impact production services. DBREs implement comprehensive monitoring covering system resources, database metrics, application performance, and business KPIs using both agent-based and agentless approaches.

Monitoring should include multiple layers: infrastructure metrics (CPU, memory, disk, network), database-specific metrics (connections, transactions, locks, cache hit ratios), and application-level metrics (query performance, response times). Using tools like Prometheus, Grafana, and database-native monitoring, DBREs create dashboards that provide actionable insights and trigger alerts based on dynamic thresholds.

```bash
# System resource monitoring script
#!/bin/bash
THRESHOLD_CPU=80
THRESHOLD_MEM=90

CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEM=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')

if (( $(echo "$CPU > $THRESHOLD_CPU" | bc -l) )); then
    echo "ALERT: CPU usage is ${CPU}%"
fi

# Database connection monitoring
CHECK_ORACLE_CONN="SELECT COUNT(*) FROM v\$session WHERE status='ACTIVE';"
CHECK_MYSQL_CONN="SHOW STATUS LIKE 'Threads_connected';"

# Set up Prometheus node exporter for system metrics
systemctl status node_exporter

# Monitor database-specific metrics
mysqld_exporter --config.my-cnf=/etc/my.cnf
oracle_exporter --default.metrics
```

### 10.2 Incident Response Workflows

Incident response requires structured approaches to minimize downtime and data loss during database emergencies. DBREs follow runbooks that define triage procedures, escalation paths, communication protocols, and post-incident review processes.

Effective incident response includes immediate assessment, containment of the issue, stakeholder communication, root cause analysis, and documentation. Using on-call tools and establishing clear severity definitions ensures consistent handling of database incidents across teams. Post-mortems identify preventive measures and improve future response.

```bash
# Incident response checklist script
#!/bin/bash
echo "=== Database Incident Response ==="
echo "1. Check database availability"
systemctl status mysqld oracle-db mongod

echo "2. Check system resources"
uptime
free -h
df -h

echo "3. Review recent logs"
tail -100 /var/log/mysqld.log | grep ERROR
tail -100 /u01/app/oracle/diag/rdbms/*/alert*.log

echo "4. Check active connections"
netstat -an | grep ESTABLISHED | wc -l

echo "5. Identify long-running queries"
# Platform-specific query identification commands

echo "6. Document findings in incident ticket"
echo "Incident timestamp: $(date)"
```

### 10.3 Change Management

Change management prevents outages caused by unauthorized or untested database modifications. DBREs implement approval workflows, testing procedures, rollback plans, and maintenance windows to ensure safe deployment of database changes.

All database changes should follow documented procedures including peer review, testing in non-production environments, and automated validation. Using infrastructure-as-code tools like Ansible and version control systems like Git, DBREs track configuration changes and enable rapid rollback when issues arise.

```bash
# Pre-change validation script
#!/bin/bash
echo "=== Pre-Change Validation ==="

# Backup before change
echo "Creating pre-change backup..."
mysqldump --all-databases > /backup/pre_change_$(date +%Y%m%d_%H%M).sql

# Document current configuration
cp /etc/my.cnf /backup/config/my.cnf.$(date +%Y%m%d_%H%M)

# Verify rollback procedures
echo "Rollback script: /home/dba/scripts/rollback_change.sh"

# Test connectivity
mysql -u root -p -e "SELECT VERSION();" || echo "FAILED: Pre-change connectivity test"

# Create change log entry
echo "$(date): Change initiated by $(whoami)" >> /var/log/database_changes.log
```

### 10.4 Documentation & Runbooks

Documentation and runbooks provide standardized procedures for database operations, troubleshooting, and disaster recovery. DBREs maintain living documents that include architecture diagrams, configuration details, operational procedures, and troubleshooting guides.

Effective runbooks are action-oriented, tested regularly, and updated after incidents. They should include step-by-step instructions, expected outputs, and decision trees for common scenarios. Version control and peer review ensure documentation accuracy and accessibility during incidents.

```markdown
# Example Runbook Structure

## Database Restart Procedure - Oracle Production

**Purpose:** Safely restart Oracle database with minimal downtime
**Estimated Time:** 15 minutes
**Prerequisites:** 
- Root/Oracle user access
- Verification of backup completion
- Stakeholder notification

**Procedure:**
1. Check database status:
   ```bash
   lsnrctl status
   sqlplus / as sysdba -e "SELECT STATUS FROM V$INSTANCE;"
   ```

2. Notify stakeholders of planned restart

3. Execute graceful shutdown:
   ```bash
   sqlplus / as sysdba <<EOF
   SHUTDOWN IMMEDIATE;
   EXIT;
   EOF
   ```

4. Verify process termination:
   ```bash
   ps aux | grep pmon
   ```

5. Start database:
   ```bash
   sqlplus / as sysdba <<EOF
   STARTUP;
   EXIT;
   EOF
   ```

6. Validate connectivity and services

**Rollback:** If startup fails, review alert log and execute recovery procedures

**Last Updated:** 2025-10-08
**Tested By:** DBRE Team
```

### 10.5 On-Call Best Practices

On-call responsibilities require DBREs to respond effectively to production incidents while maintaining work-life balance. Best practices include proper handoff procedures, escalation paths, tool accessibility, and fair rotation schedules.

Successful on-call programs provide comprehensive playbooks, access to necessary systems, clear severity definitions, and support from secondary responders. DBREs should have mobile access to monitoring dashboards, runbooks, and communication channels. Post-incident reviews identify opportunities to reduce alert fatigue and improve automated recovery.

```bash
# On-call readiness checklist
#!/bin/bash

echo "=== On-Call Readiness Check ==="

# Verify VPN connectivity
ping -c 3 internal-jumphost.company.com || echo "WARNING: VPN connectivity issue"

# Test database access from remote
ssh -i ~/.ssh/id_rsa dba@dbserver01 "hostname" || echo "WARNING: SSH access issue"

# Verify monitoring dashboard access
curl -s -o /dev/null -w "%{http_code}" https://monitoring.company.com || echo "WARNING: Monitoring access issue"

# Check on-call tooling
command -v pagerduty-cli >/dev/null || echo "WARNING: PagerDuty CLI not installed"

# Verify runbook access
ls ~/runbooks/*.md || echo "WARNING: Runbooks not available locally"

echo "=== On-Call Schedule ==="
echo "Primary: $(whoami)"
echo "Secondary: Check PagerDuty schedule"
echo "Escalation: DBA Manager"

echo "=== Emergency Contacts ==="
cat ~/on-call/contacts.txt
```

---

## Conclusion

This guide provides essential Linux knowledge for Database Reliability Engineers managing production database environments on Red Hat Enterprise Linux. The commands and practices outlined here form the foundation for reliable database operations, efficient troubleshooting, and effective incident response.

DBREs should regularly practice these commands, maintain up-to-date runbooks, and continuously improve automation to reduce manual intervention. Combining strong Linux fundamentals with database-specific expertise ensures high availability, optimal performance, and rapid recovery during incidents.

**For questions or contributions, please refer to the repository issues section.**

---

**Repository:** [Your GitHub Profile]  
**License:** MIT  
**Last Updated:** October 2025
