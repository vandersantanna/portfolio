# MongoDB Installation and Configuration Guide

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Replica Set Configuration](#replica-set-configuration)
- [Sharded Cluster Setup](#sharded-cluster-setup)
- [Security Configuration](#security-configuration)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Backup and Recovery](#backup-and-recovery)
- [High Availability Best Practices](#high-availability-best-practices)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)
- [Author](#author)

## Overview

MongoDB is a document-oriented NoSQL database designed for scalability, performance, and high availability. This guide covers enterprise-grade deployment scenarios including replica sets and sharded clusters.

**Key Features:**
- Document-based flexible schema
- Horizontal scaling through sharding
- High availability via replica sets
- Rich aggregation framework
- Built-in replication and failover
- Real-time change streams

## Prerequisites

### Supported Operating Systems

**Red Hat Enterprise Linux:**
- RHEL 8.x, 9.x, 10.x

**Ubuntu:**
- Ubuntu 20.04 LTS (Focal Fossa)
- Ubuntu 22.04 LTS (Jammy Jellyfish)
- Ubuntu 24.04 LTS (Noble Numbat)

**Windows Server:**
- Windows Server 2022

### Hardware Requirements

**Minimum Production Requirements:**
- **CPU**: 4 cores x86_64
- **RAM**: 16GB (32GB+ recommended)
- **Storage**: SSD with high IOPS
- **Network**: Gigabit Ethernet

## System Requirements

### Linux System Configuration

```bash
# Disable Transparent Huge Pages
echo 'never' | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo 'never' | sudo tee /sys/kernel/mm/transparent_hugepage/defrag

# Create systemd service to disable THP permanently
sudo tee /etc/systemd/system/disable-thp.service << 'EOF'
[Unit]
Description=Disable Transparent Huge Pages (THP)
DefaultDependencies=no
After=sysinit.target local-fs.target
Before=mongod.service

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo never | tee /sys/kernel/mm/transparent_hugepage/enabled > /dev/null'
ExecStart=/bin/sh -c 'echo never | tee /sys/kernel/mm/transparent_hugepage/defrag > /dev/null'

[Install]
WantedBy=basic.target
EOF

sudo systemctl enable disable-thp
sudo systemctl start disable-thp
```

### System Limits Configuration

```bash
# Configure limits for MongoDB
sudo tee -a /etc/security/limits.conf << 'EOF'
mongod soft nofile 64000
mongod hard nofile 64000
mongod soft nproc 64000
mongod hard nproc 64000
EOF

# Configure systemd limits
sudo mkdir -p /etc/systemd/system/mongod.service.d
sudo tee /etc/systemd/system/mongod.service.d/limits.conf << 'EOF'
[Service]
LimitFSIZE=infinity
LimitCPU=infinity
LimitAS=infinity
LimitNOFILE=64000
LimitNPROC=64000
EOF
```

### Kernel Parameters

```bash
# Optimize kernel parameters
sudo tee -a /etc/sysctl.conf << 'EOF'
# MongoDB optimizations
vm.swappiness = 1
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
net.core.somaxconn = 4096
net.ipv4.tcp_keepalive_time = 300
fs.file-max = 98000
EOF

sudo sysctl -p
```

## Installation

### Ubuntu Installation (20.04, 22.04, 24.04 LTS)

```bash
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install
sudo apt update
sudo apt install -y mongodb-org

# Hold packages to prevent unintended upgrades
sudo apt-mark hold mongodb-org mongodb-org-database mongodb-org-server mongodb-org-mongos mongodb-org-tools

# Verify installation
mongod --version
```

### RHEL Installation (8.x, 9.x, 10.x)

```bash
# Create MongoDB repository
sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo << 'EOF'
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOF

# Install MongoDB
sudo dnf install -y mongodb-org

# Prevent automatic updates
sudo sed -i '/\[mongodb-org-7.0\]/a exclude=mongodb-org,mongodb-org-database,mongodb-org-server,mongodb-org-mongos,mongodb-org-tools' /etc/yum.repos.d/mongodb-org-7.0.repo

# Verify installation
mongod --version
```

### Windows Server 2022 Installation

```powershell
# Download MongoDB MSI installer
Invoke-WebRequest -Uri "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4-signed.msi" -OutFile "$env:TEMP\mongodb-installer.msi"

# Install MongoDB as service
Start-Process msiexec.exe -Wait -ArgumentList '/i', "$env:TEMP\mongodb-installer.msi", '/quiet', 'INSTALLLOCATION="C:\Program Files\MongoDB\Server\7.0"', 'ADDLOCAL="ServerService,Client"'

# Create data directory
New-Item -ItemType Directory -Force -Path "C:\data\db"

# Start MongoDB service
Start-Service -Name "MongoDB"
Set-Service -Name "MongoDB" -StartupType Automatic

# Verify installation
& "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --version
```

### Basic Configuration

```bash
# Create MongoDB configuration file
sudo tee /etc/mongod.conf << 'EOF'
# MongoDB Configuration File

storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 8
      journalCompressor: snappy
      directoryForIndexes: true
    collectionConfig:
      blockCompressor: snappy
    indexConfig:
      prefixCompression: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
  logRotate: rename

net:
  port: 27017
  bindIp: 127.0.0.1
  maxIncomingConnections: 65536

processManagement:
  fork: true
  pidFilePath: /var/run/mongod.pid

operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100

setParameter:
  enableLocalhostAuthBypass: false
EOF

# Start MongoDB
sudo systemctl enable mongod
sudo systemctl start mongod
sudo systemctl status mongod
```

### Initial Setup

```javascript
// Connect to MongoDB
mongosh

// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "AdminPassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})

// Create application database and user
use myapp
db.createUser({
  user: "appuser",
  pwd: "AppPassword123!",
  roles: [{ role: "readWrite", db: "myapp" }]
})

// Insert sample data
db.users.insertMany([
  { 
    name: "John Doe", 
    email: "john@example.com", 
    department: "Engineering",
    created_at: new Date()
  },
  { 
    name: "Jane Smith", 
    email: "jane@example.com", 
    department: "Marketing",
    created_at: new Date()
  }
])

// Create indexes
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "department": 1 })
db.users.createIndex({ "created_at": 1 })

exit
```
## Replica Set Configuration

### Three-Node Replica Set Setup

**Network Configuration:**
```bash
# Configure hosts file on all nodes
sudo tee -a /etc/hosts << 'EOF'
10.0.1.10    mongo1
10.0.1.11    mongo2
10.0.1.12    mongo3
EOF
```

**Create Keyfile for Authentication:**
```bash
# Generate keyfile on primary node
sudo openssl rand -base64 756 | sudo tee /var/lib/mongodb/keyfile
sudo chmod 400 /var/lib/mongodb/keyfile
sudo chown mongodb:mongodb /var/lib/mongodb/keyfile

# Copy to other nodes
scp /var/lib/mongodb/keyfile user@mongo2:/tmp/
scp /var/lib/mongodb/keyfile user@mongo3:/tmp/

# On mongo2 and mongo3
ssh mongo2 "sudo mv /tmp/keyfile /var/lib/mongodb/ && sudo chmod 400 /var/lib/mongodb/keyfile && sudo chown mongodb:mongodb /var/lib/mongodb/keyfile"
ssh mongo3 "sudo mv /tmp/keyfile /var/lib/mongodb/ && sudo chmod 400 /var/lib/mongodb/keyfile && sudo chown mongodb:mongodb /var/lib/mongodb/keyfile"
```

**Replica Set Configuration (All Nodes):**
```yaml
# Update /etc/mongod.conf on all nodes
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 8

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 0.0.0.0

replication:
  replSetName: "rs0"
  oplogSizeMB: 2048

security:
  authorization: enabled
  keyFile: /var/lib/mongodb/keyfile
```

**Initialize Replica Set:**
```javascript
// Connect to mongo1
mongosh --host mongo1:27017

// Initialize replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 1 }
  ]
})

// Wait and check status
sleep(10000)
rs.status()

// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "AdminPassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})
```

## Sharded Cluster Setup

### Architecture Overview
```
Config Servers (3): config1:27019, config2:27019, config3:27019
Shard 1 (3): shard1a:27018, shard1b:27018, shard1c:27018
Shard 2 (3): shard2a:27018, shard2b:27018, shard2c:27018
Mongos Routers (2): router1:27017, router2:27017
```

### Config Server Setup

**Configuration:**
```yaml
# /etc/mongod-config.conf
storage:
  dbPath: /var/lib/mongodb-config
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod-config.log

net:
  port: 27019
  bindIp: 0.0.0.0

replication:
  replSetName: "configReplSet"

sharding:
  clusterRole: configsvr

security:
  authorization: enabled
  keyFile: /var/lib/mongodb/keyfile
```

**Initialize Config Servers:**
```javascript
// Connect to config1:27019
mongosh --host config1:27019

rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [
    { _id: 0, host: "config1:27019" },
    { _id: 1, host: "config2:27019" },
    { _id: 2, host: "config3:27019" }
  ]
})

// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "AdminPassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})
```

### Shard Server Setup

**Shard Configuration:**
```yaml
# /etc/mongod-shard1.conf
storage:
  dbPath: /var/lib/mongodb-shard1
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod-shard1.log

net:
  port: 27018
  bindIp: 0.0.0.0

replication:
  replSetName: "shard1"

sharding:
  clusterRole: shardsvr

security:
  authorization: enabled
  keyFile: /var/lib/mongodb/keyfile
```

**Initialize Shard Replica Sets:**
```javascript
// Initialize shard1
mongosh --host shard1a:27018

rs.initiate({
  _id: "shard1",
  members: [
    { _id: 0, host: "shard1a:27018" },
    { _id: 1, host: "shard1b:27018" },
    { _id: 2, host: "shard1c:27018" }
  ]
})

// Create admin user (repeat for shard2)
use admin
db.createUser({
  user: "admin",
  pwd: "AdminPassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})
```

### Mongos Router Setup

**Mongos Configuration:**
```yaml
# /etc/mongos.conf
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongos.log

net:
  port: 27017
  bindIp: 0.0.0.0

sharding:
  configDB: configReplSet/config1:27019,config2:27019,config3:27019

security:
  keyFile: /var/lib/mongodb/keyfile
```

**Add Shards to Cluster:**
```javascript
// Connect to mongos
mongosh --host router1:27017 -u admin -p AdminPassword123! --authenticationDatabase admin

// Add shards
sh.addShard("shard1/shard1a:27018,shard1b:27018,shard1c:27018")
sh.addShard("shard2/shard2a:27018,shard2b:27018,shard2c:27018")

// Enable sharding for database
sh.enableSharding("myapp")

// Shard collections
sh.shardCollection("myapp.users", { "user_id": "hashed" })
sh.shardCollection("myapp.orders", { "customer_id": 1, "order_date": 1 })

// Check status
sh.status()
```

## Security Configuration

### Authentication and Authorization

```javascript
// Advanced user management
mongosh --host localhost:27017 -u admin -p AdminPassword123! --authenticationDatabase admin

use admin

// Create custom roles
db.createRole({
  role: "appDeveloper",
  privileges: [
    {
      resource: { db: "myapp", collection: "" },
      actions: [
        "find", "insert", "update", "remove", 
        "createIndex", "dropIndex", "createCollection"
      ]
    }
  ],
  roles: []
})

// Create specialized users
db.createUser({
  user: "developer",
  pwd: "DevPassword123!",
  roles: [
    { role: "appDeveloper", db: "admin" },
    { role: "readWrite", db: "myapp" }
  ]
})

db.createUser({
  user: "readonly",
  pwd: "ReadOnlyPass123!",
  roles: [{ role: "read", db: "myapp" }]
})

db.createUser({
  user: "backup",
  pwd: "BackupPass123!",
  roles: [
    { role: "backup", db: "admin" },
    { role: "clusterMonitor", db: "admin" }
  ]
})
```

### SSL/TLS Configuration

```bash
# Generate SSL certificates
sudo mkdir -p /etc/mongodb/ssl
cd /etc/mongodb/ssl

# Create CA certificate
sudo openssl genrsa -out ca-key.pem 4096
sudo openssl req -new -x509 -days 3650 -key ca-key.pem -out ca-cert.pem \
    -subj "/C=US/ST=NY/L=NYC/O=Company/OU=IT/CN=MongoDB-CA"

# Create server certificate
sudo openssl genrsa -out server-key.pem 4096
sudo openssl req -new -key server-key.pem -out server.csr \
    -subj "/C=US/ST=NY/L=NYC/O=Company/OU=IT/CN=mongodb-server"
sudo openssl x509 -req -days 365 -in server.csr -CA ca-cert.pem \
    -CAkey ca-key.pem -CAcreateserial -out server-cert.pem

# Combine key and certificate
sudo cat server-key.pem server-cert.pem > server.pem

# Set permissions
sudo chown -R mongodb:mongodb /etc/mongodb/ssl
sudo chmod 600 /etc/mongodb/ssl/*.pem
sudo chmod 644 /etc/mongodb/ssl/ca-cert.pem
```

**Update Configuration for SSL:**
```yaml
# Add to /etc/mongod.conf
net:
  port: 27017
  bindIp: 0.0.0.0
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/mongodb/ssl/server.pem
    CAFile: /etc/mongodb/ssl/ca-cert.pem
```

### Auditing Configuration

```yaml
# Add to /etc/mongod.conf
auditLog:
  destination: file
  format: JSON
  path: /var/log/mongodb/audit.log
  filter: |
    {
      "atype": {
        "$in": [
          "authenticate", "authCheck", "createUser", "dropUser",
          "createRole", "dropRole", "createCollection", "dropCollection"
        ]
      }
    }
```
## Performance Optimization

### Configuration Tuning

```yaml
# Optimized /etc/mongod.conf for production
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
    commitIntervalMs: 100
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 16  # 50% of available RAM
      journalCompressor: snappy
      directoryForIndexes: true
    collectionConfig:
      blockCompressor: snappy
    indexConfig:
      prefixCompression: true

net:
  port: 27017
  bindIp: 0.0.0.0
  maxIncomingConnections: 65536
  compression:
    compressors: snappy,zstd,zlib

operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100

setParameter:
  wiredTigerConcurrentReadTransactions: 128
  wiredTigerConcurrentWriteTransactions: 128
  maxTimeMS: 30000
```

### Index Optimization

```javascript
// Effective indexing strategies
use myapp

// Compound indexes for common queries
db.users.createIndex({ "department": 1, "status": 1, "created_at": -1 })

// Partial index for active users only
db.users.createIndex(
  { "email": 1 },
  { 
    partialFilterExpression: { "status": "active" },
    unique: true
  }
)

// Text search index
db.articles.createIndex({
  "title": "text",
  "content": "text"
}, {
  weights: { title: 3, content: 1 }
})

// TTL index for session cleanup
db.sessions.createIndex(
  { "created_at": 1 },
  { expireAfterSeconds: 3600 }
)

// Geospatial index
db.locations.createIndex({ "coordinates": "2dsphere" })

// Check index usage
db.users.aggregate([{ $indexStats: {} }])
```

### Query Optimization

```javascript
// Efficient aggregation pipeline
db.orders.aggregate([
  // Match first to reduce dataset
  { $match: { 
      "order_date": { $gte: ISODate("2024-01-01") },
      "status": "completed"
    }
  },
  // Group and calculate metrics
  { $group: {
      _id: "$customer_id",
      total_orders: { $sum: 1 },
      total_amount: { $sum: "$total" },
      avg_order_value: { $avg: "$total" }
    }
  },
  { $sort: { "total_amount": -1 } },
  { $limit: 100 }
], { allowDiskUse: true })

// Use projection to limit fields
db.users.find(
  { "department": "Engineering" },
  { "name": 1, "email": 1, "_id": 0 }
)

// Force index usage
db.users.find({ "department": "Engineering" })
  .hint({ "department": 1, "status": 1 })

// Bulk operations for better performance
const bulk = db.users.initializeUnorderedBulkOp();
for (let i = 0; i < 1000; i++) {
  bulk.insert({ name: `User${i}`, email: `user${i}@example.com` });
}
bulk.execute({ writeConcern: { w: "majority" } });
```

## Monitoring and Maintenance

### Health Monitoring Script

```bash
# Create monitoring script
sudo mkdir -p /opt/mongodb/scripts
sudo tee /opt/mongodb/scripts/mongodb_monitor.sh << 'EOF'
#!/bin/bash

# MongoDB Health Monitoring
export PATH=/usr/bin:$PATH
LOG_FILE="/var/log/mongodb/monitor.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log_message() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Check MongoDB service
if systemctl is-active --quiet mongod; then
    log_message "✓ MongoDB service is running"
else
    log_message "✗ MongoDB service is down"
    exit 1
fi

# Check connectivity
if mongosh --quiet --eval "db.runCommand('ping')" >/dev/null 2>&1; then
    log_message "✓ MongoDB is responding"
else
    log_message "✗ MongoDB not responding"
    exit 1
fi

# Check replica set status
REPLICA_STATUS=$(mongosh --quiet --eval "
try {
    var status = rs.status();
    if (status.ok === 1) {
        var primary = status.members.find(m => m.stateStr === 'PRIMARY');
        var secondaries = status.members.filter(m => m.stateStr === 'SECONDARY');
        print('RS:' + status.set + ',PRIMARY:' + (primary ? 1 : 0) + ',SECONDARIES:' + secondaries.length);
    } else {
        print('STANDALONE');
    }
} catch (e) {
    print('STANDALONE');
}
" 2>/dev/null)

if [[ "$REPLICA_STATUS" == *"PRIMARY:1"* ]]; then
    log_message "✓ Replica set healthy: $REPLICA_STATUS"
elif [[ "$REPLICA_STATUS" == "STANDALONE" ]]; then
    log_message "✓ Standalone instance"
else
    log_message "⚠ Replica set issues: $REPLICA_STATUS"
fi

# Check disk space
DISK_USAGE=$(df /var/lib/mongodb | tail -1 | awk '{print $5}' | sed 's/%//')
if [[ $DISK_USAGE -gt 85 ]]; then
    log_message "⚠ High disk usage: ${DISK_USAGE}%"
else
    log_message "✓ Disk usage: ${DISK_USAGE}%"
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3/$2*100}')
log_message "✓ Memory usage: ${MEM_USAGE}%"

log_message "Health check completed"
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_monitor.sh
```

### Performance Monitoring

```bash
# Performance monitoring script
sudo tee /opt/mongodb/scripts/mongodb_performance.sh << 'EOF'
#!/bin/bash

export PATH=/usr/bin:$PATH
LOG_FILE="/var/log/mongodb/performance.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] MongoDB Performance Report" >> "$LOG_FILE"

mongosh --quiet --eval "
var status = db.serverStatus();

print('--- Server Info ---');
print('MongoDB Version: ' + status.version);
print('Uptime: ' + Math.round(status.uptime / 3600) + ' hours');

print('--- Memory Usage ---');
print('Resident: ' + Math.round(status.mem.resident) + ' MB');
print('Virtual: ' + Math.round(status.mem.virtual) + ' MB');

print('--- Connections ---');
print('Current: ' + status.connections.current);
print('Available: ' + status.connections.available);

if (status.wiredTiger) {
    var cache = status.wiredTiger.cache;
    var hitRatio = Math.round(
        ((cache['pages requested from the cache'] - cache['pages read into cache']) / 
         cache['pages requested from the cache']) * 100
    );
    print('Cache Hit Ratio: ' + hitRatio + '%');
}

print('--- Operations ---');
var ops = status.opcounters;
print('Insert: ' + ops.insert);
print('Query: ' + ops.query);  
print('Update: ' + ops.update);
print('Delete: ' + ops.delete);

print('--- Network ---');
if (status.network) {
    print('Bytes In: ' + Math.round(status.network.bytesIn / 1024 / 1024) + ' MB');
    print('Bytes Out: ' + Math.round(status.network.bytesOut / 1024 / 1024) + ' MB');
}
" >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_performance.sh
```

## Backup and Recovery

### Automated Backup Strategy

```bash
# Create backup script
sudo mkdir -p /backup/mongodb/{daily,weekly,monthly}
sudo chown -R mongodb:mongodb /backup/mongodb

sudo tee /opt/mongodb/scripts/mongodb_backup.sh << 'EOF'
#!/bin/bash

# MongoDB Backup Script
export PATH=/usr/bin:$PATH
BACKUP_TYPE=${1:-"daily"}
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BASE_DIR="/backup/mongodb"
LOG_FILE="/var/log/mongodb/backup.log"

# Retention periods (days)
DAILY_RETENTION=7
WEEKLY_RETENTION=28
MONTHLY_RETENTION=365

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create backup
create_backup() {
    local backup_dir="${BASE_DIR}/${BACKUP_TYPE}"
    local backup_name="mongodb_${BACKUP_TYPE}_${TIMESTAMP}"
    local backup_path="${backup_dir}/${backup_name}"
    
    log_message "Starting $BACKUP_TYPE backup"
    
    mkdir -p "$backup_path"
    
    # Check if replica set for oplog backup
    IS_REPLICA=$(mongosh --quiet --eval "
        try {
            rs.status();
            print('true');
        } catch(e) {
            print('false');
        }
    " 2>/dev/null)
    
    if [[ "$IS_REPLICA" == "true" ]]; then
        # Replica set backup with oplog
        mongodump --oplog --gzip --out "$backup_path" 2>>"$LOG_FILE"
    else
        # Standard backup
        mongodump --gzip --out "$backup_path" 2>>"$LOG_FILE"
    fi
    
    if [[ $? -eq 0 ]]; then
        # Compress backup
        tar -czf "${backup_path}.tar.gz" -C "$backup_dir" "$backup_name"
        rm -rf "$backup_path"
        
        local size=$(du -h "${backup_path}.tar.gz" | cut -f1)
        log_message "Backup completed: ${backup_name}.tar.gz ($size)"
        
        # Cleanup old backups
        case $BACKUP_TYPE in
            daily)   find "$backup_dir" -name "*.tar.gz" -mtime +$DAILY_RETENTION -delete ;;
            weekly)  find "$backup_dir" -name "*.tar.gz" -mtime +$WEEKLY_RETENTION -delete ;;
            monthly) find "$backup_dir" -name "*.tar.gz" -mtime +$MONTHLY_RETENTION -delete ;;
        esac
        
        return 0
    else
        log_message "Backup failed"
        return 1
    fi
}

create_backup
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_backup.sh
sudo chown mongodb:mongodb /opt/mongodb/scripts/mongodb_backup.sh
```
### Point-in-Time Recovery

```bash
# Recovery script
sudo tee /opt/mongodb/scripts/mongodb_restore.sh << 'EOF'
#!/bin/bash

# MongoDB Restore Script
BACKUP_FILE=$1
RECOVERY_TIME=${2:-""}

if [[ -z "$BACKUP_FILE" ]]; then
    echo "Usage: $0 <backup_file.tar.gz> [recovery_timestamp]"
    exit 1
fi

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Extract and restore
TEMP_DIR="/tmp/mongodb_restore_$(date +%s)"
mkdir -p "$TEMP_DIR"

log_message "Extracting backup: $BACKUP_FILE"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

BACKUP_DIR=$(find "$TEMP_DIR" -name "mongodb_*" -type d | head -1)

if [[ ! -d "$BACKUP_DIR" ]]; then
    log_message "ERROR: Backup directory not found"
    exit 1
fi

# Stop MongoDB
log_message "Stopping MongoDB"
sudo systemctl stop mongod

# Backup current data
CURRENT_BACKUP="/tmp/mongodb_current_$(date +%s)"
sudo mkdir -p "$CURRENT_BACKUP"
sudo cp -r /var/lib/mongodb/* "$CURRENT_BACKUP/" 2>/dev/null

# Clear data directory
sudo rm -rf /var/lib/mongodb/*

# Start MongoDB temporarily without auth
log_message "Starting MongoDB in recovery mode"
sudo -u mongodb mongod --dbpath /var/lib/mongodb --port 27999 --logpath /tmp/restore.log --fork

sleep 5

# Restore databases
log_message "Restoring databases"
if [[ -f "$BACKUP_DIR/oplog.bson" && -n "$RECOVERY_TIME" ]]; then
    # Point-in-time recovery with oplog
    mongorestore --port 27999 --oplogReplay --oplogLimit "$RECOVERY_TIME" \
                 --dir "$BACKUP_DIR" --drop
else
    # Standard restore
    mongorestore --port 27999 --dir "$BACKUP_DIR" --drop
fi

# Shutdown temporary MongoDB
mongosh --port 27999 --eval "db.adminCommand('shutdown')"
sleep 3

# Start normal MongoDB
log_message "Starting MongoDB service"
sudo systemctl start mongod

# Cleanup
rm -rf "$TEMP_DIR"

log_message "Restore completed. Previous data backed up to: $CURRENT_BACKUP"
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_restore.sh
```

### Backup Scheduling

```bash
# Setup cron jobs for backups
sudo -u mongodb crontab << 'EOF'
# MongoDB automated backups

# Daily backup at 2 AM
0 2 * * * /opt/mongodb/scripts/mongodb_backup.sh daily

# Weekly backup on Sunday at 3 AM
0 3 * * 0 /opt/mongodb/scripts/mongodb_backup.sh weekly

# Monthly backup on 1st day at 4 AM
0 4 1 * * /opt/mongodb/scripts/mongodb_backup.sh monthly

# Health check every 10 minutes
*/10 * * * * /opt/mongodb/scripts/mongodb_monitor.sh

# Performance monitoring every 15 minutes
*/15 * * * * /opt/mongodb/scripts/mongodb_performance.sh
EOF
```

## High Availability Best Practices

### Replica Set Optimization

```javascript
// Optimal replica set configuration
mongosh "mongodb://admin:AdminPassword123!@mongo1:27017,mongo2:27017,mongo3:27017/admin?replicaSet=rs0"

// Configure read preferences for load distribution
db.setReadPref("secondaryPreferred")

// Set appropriate write concerns
db.setWriteConcern({ 
  w: "majority", 
  j: true, 
  wtimeout: 5000 
})

// Configure replica set priorities
cfg = rs.conf()
cfg.members[0].priority = 2  // Primary preference
cfg.members[1].priority = 1
cfg.members[2].priority = 1
rs.reconfig(cfg)

// Add tags for geographic distribution
cfg.members[0].tags = { "dc": "east", "usage": "production" }
cfg.members[1].tags = { "dc": "east", "usage": "production" }
cfg.members[2].tags = { "dc": "west", "usage": "disaster-recovery" }
rs.reconfig(cfg)
```

### Disaster Recovery Procedures

```bash
# Disaster recovery script
sudo tee /opt/mongodb/scripts/mongodb_dr.sh << 'EOF'
#!/bin/bash

# MongoDB Disaster Recovery Script
DR_ACTION=${1:-"status"}

case $DR_ACTION in
  "status")
    echo "=== MongoDB DR Status ==="
    mongosh --quiet --eval "
      try {
        var status = rs.status();
        print('Replica Set: ' + status.set);
        status.members.forEach(function(member) {
          print(member.name + ' - ' + member.stateStr + ' (health: ' + member.health + ')');
        });
      } catch(e) {
        print('Standalone instance or connection error');
      }
    "
    ;;
    
  "failover")
    echo "=== Initiating Manual Failover ==="
    mongosh --quiet --eval "
      try {
        rs.stepDown(60);
        print('Primary stepped down. New election in progress...');
      } catch(e) {
        print('Failover failed: ' + e.message);
      }
    "
    ;;
    
  "health")
    echo "=== Health Check ==="
    /opt/mongodb/scripts/mongodb_monitor.sh
    ;;
    
  *)
    echo "Usage: $0 {status|failover|health}"
    exit 1
    ;;
esac
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_dr.sh
```

## Troubleshooting

### Common Issues and Solutions

```bash
# Comprehensive troubleshooting script
sudo tee /opt/mongodb/scripts/mongodb_troubleshoot.sh << 'EOF'
#!/bin/bash

# MongoDB Troubleshooting Script
ISSUE_TYPE=${1:-"all"}

echo "=== MongoDB Troubleshooting ==="

check_service() {
    echo -n "Service Status: "
    if systemctl is-active --quiet mongod; then
        echo "✓ Running"
    else
        echo "✗ Stopped"
        systemctl status mongod --no-pager -l
    fi
}

check_logs() {
    echo "=== Recent Errors ==="
    tail -50 /var/log/mongodb/mongod.log | grep -E "(ERROR|WARN|SEVERE)" | tail -5
}

check_connections() {
    echo "=== Connection Status ==="
    mongosh --quiet --eval "
      try {
        var status = db.serverStatus();
        print('Current connections: ' + status.connections.current);
        print('Available connections: ' + status.connections.available);
        print('Max connections: ' + (status.connections.current + status.connections.available));
      } catch(e) {
        print('Cannot retrieve connection status: ' + e.message);
      }
    " 2>/dev/null
}

check_replication() {
    echo "=== Replication Status ==="
    mongosh --quiet --eval "
      try {
        var status = rs.status();
        if (status.ok === 1) {
          var primary = status.members.find(m => m.stateStr === 'PRIMARY');
          var secondaries = status.members.filter(m => m.stateStr === 'SECONDARY');
          print('Primary: ' + (primary ? primary.name : 'NONE'));
          print('Secondaries: ' + secondaries.length);
          
          if (primary && secondaries.length > 0) {
            secondaries.forEach(function(s) {
              var lag = Math.round((primary.optimeDate - s.optimeDate) / 1000);
              print('Lag for ' + s.name + ': ' + lag + ' seconds');
            });
          }
        }
      } catch(e) {
        print('Not a replica set or error: ' + e.message);
      }
    " 2>/dev/null
}

check_performance() {
    echo "=== Performance Issues ==="
    mongosh --quiet --eval "
      try {
        var currentOps = db.currentOp({'secs_running': {\$gte: 5}});
        if (currentOps.inprog.length > 0) {
          print('Long-running operations:');
          currentOps.inprog.forEach(function(op) {
            print('  ' + op.op + ' on ' + op.ns + ' (' + op.secs_running + 's)');
          });
        } else {
          print('No long-running operations');
        }
      } catch(e) {
        print('Cannot check operations: ' + e.message);
      }
    " 2>/dev/null
}

check_disk_space() {
    echo "=== Disk Space ==="
    df -h /var/lib/mongodb | tail -1
    echo "MongoDB data size:"
    du -sh /var/lib/mongodb 2>/dev/null || echo "Cannot access data directory"
}

# Main troubleshooting
case $ISSUE_TYPE in
    "all")
        check_service
        check_connections
        check_replication
        check_performance
        check_disk_space
        check_logs
        ;;
    "service") check_service ;;
    "connections") check_connections ;;
    "replication") check_replication ;;
    "performance") check_performance ;;
    "logs") check_logs ;;
    *)
        echo "Usage: $0 {all|service|connections|replication|performance|logs}"
        ;;
esac
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_troubleshoot.sh
```

### Log Analysis

```bash
# Log analysis script
sudo tee /opt/mongodb/scripts/mongodb_log_analysis.sh << 'EOF'
#!/bin/bash

# MongoDB Log Analysis
LOG_FILE="/var/log/mongodb/mongod.log"
ANALYSIS_LOG="/var/log/mongodb/log_analysis.log"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "MongoDB log file not found: $LOG_FILE"
    exit 1
fi

echo "=== MongoDB Log Analysis Report ===" > "$ANALYSIS_LOG"
echo "Generated: $(date)" >> "$ANALYSIS_LOG"
echo "" >> "$ANALYSIS_LOG"

# Recent errors
echo "1. Recent Errors:" >> "$ANALYSIS_LOG"
tail -1000 "$LOG_FILE" | grep -E "(ERROR|SEVERE|FATAL)" | tail -10 >> "$ANALYSIS_LOG"
echo "" >> "$ANALYSIS_LOG"

# Connection issues
echo "2. Connection Issues:" >> "$ANALYSIS_LOG"
tail -1000 "$LOG_FILE" | grep -i "connection" | grep -E "(refused|failed|timeout)" | tail -5 >> "$ANALYSIS_LOG"
echo "" >> "$ANALYSIS_LOG"

# Slow operations
echo "3. Slow Operations:" >> "$ANALYSIS_LOG"
tail -1000 "$LOG_FILE" | grep -i "slow" | tail -5 >> "$ANALYSIS_LOG"
echo "" >> "$ANALYSIS_LOG"

# Summary
ERROR_COUNT=$(tail -1000 "$LOG_FILE" | grep -c "ERROR")
WARN_COUNT=$(tail -1000 "$LOG_FILE" | grep -c "WARN")

echo "4. Summary:" >> "$ANALYSIS_LOG"
echo "Recent errors: $ERROR_COUNT" >> "$ANALYSIS_LOG"
echo "Recent warnings: $WARN_COUNT" >> "$ANALYSIS_LOG"

echo "Log analysis completed. Report saved to: $ANALYSIS_LOG"
EOF

sudo chmod +x /opt/mongodb/scripts/mongodb_log_analysis.sh
```

## Production Deployment

### Production Checklist

```markdown
# MongoDB Production Deployment Checklist

## Pre-Deployment
- [ ] Hardware requirements verified (CPU, RAM, Storage, Network)
- [ ] OS configured (THP disabled, limits set, kernel parameters)
- [ ] Network connectivity between nodes tested
- [ ] DNS/hostname resolution configured
- [ ] Firewall rules configured appropriately
- [ ] SSL certificates prepared (if required)

## Installation and Configuration
- [ ] MongoDB software installed and version verified
- [ ] Configuration files created and validated
- [ ] Authentication enabled with strong passwords
- [ ] User roles and permissions configured
- [ ] Replica set initialized (if applicable)
- [ ] Sharding configured (if applicable)

## Security
- [ ] Authentication enabled and tested
- [ ] SSL/TLS encryption configured (if required)
- [ ] Network access restricted (firewall, bind IP)
- [ ] Auditing enabled (if required)
- [ ] Regular security updates scheduled

## Monitoring and Maintenance
- [ ] Health monitoring scripts deployed
- [ ] Performance monitoring configured
- [ ] Log rotation configured
- [ ] Alerting system configured
- [ ] Backup strategy implemented and tested

## High Availability
- [ ] Replica set configured with proper priorities
- [ ] Read preferences configured appropriately
- [ ] Disaster recovery procedures documented
- [ ] Failover scenarios tested
- [ ] Geographic distribution configured (if required)

## Performance
- [ ] Indexes created for common queries
- [ ] Query performance analyzed
- [ ] Connection pooling configured
- [ ] Profiling enabled for slow operations
- [ ] Resource utilization optimized

## Backup and Recovery
- [ ] Backup strategy implemented
- [ ] Recovery procedures tested
- [ ] Point-in-time recovery tested (if applicable)
- [ ] Backup retention policies configured
- [ ] Off-site backup storage configured

## Documentation
- [ ] Architecture documented
- [ ] Configuration parameters documented
- [ ] Operational procedures documented
- [ ] Troubleshooting guide created
- [ ] Contact information updated
```

### Connection String Examples

```javascript
// Production connection strings

// Standalone
const mongoUri = "mongodb://appuser:AppPassword123!@mongo-server:27017/myapp?authSource=admin&ssl=true&sslValidate=true";

// Replica Set
const replicaSetUri = "mongodb://appuser:AppPassword123!@mongo1:27017,mongo2:27017,mongo3:27017/myapp?" +
  "replicaSet=rs0&" +
  "authSource=admin&" +
  "readPreference=secondaryPreferred&" +
  "readConcernLevel=majority&" +
  "w=majority&" +
  "wtimeoutMS=5000&" +
  "maxPoolSize=100&" +
  "minPoolSize=10&" +
  "maxIdleTimeMS=30000&" +
  "serverSelectionTimeoutMS=5000&" +
  "ssl=true&" +
  "retryWrites=true&" +
  "retryReads=true";

// Sharded Cluster
const shardedUri = "mongodb://appuser:AppPassword123!@router1:27017,router2:27017/myapp?" +
  "authSource=admin&" +
  "readPreference=secondaryPreferred&" +
  "maxPoolSize=200&" +
  "ssl=true&" +
  "retryWrites=true";

// Node.js driver configuration
const { MongoClient } = require('mongodb');

const client = new MongoClient(replicaSetUri, {
  maxPoolSize: 100,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  family: 4, // Use IPv4
  writeConcern: { w: 'majority', j: true, wtimeout: 5000 },
  readConcern: { level: 'majority' },
  readPreference: 'secondaryPreferred'
});
```

### Final Validation Script

```bash
# Create final validation script
sudo tee /opt/mongodb/scripts/validate_installation.sh << 'EOF'
#!/bin/bash

# MongoDB Installation Validation
echo "=== MongoDB Installation Validation ==="

# Check MongoDB version
echo "1. MongoDB Version:"
mongod --version | head -1

# Check service status
echo -e "\n2. Service Status:"
if systemctl is-active --quiet mongod; then
    echo "✓ MongoDB service is running"
else
    echo "✗ MongoDB service is not running"
fi

# Check connectivity
echo -e "\n3. Database Connectivity:"
if mongosh --quiet --eval "db.runCommand('ping')" >/dev/null 2>&1; then
    echo "✓ Database is accessible"
else
    echo "✗ Cannot connect to database"
fi

# Check authentication
echo -e "\n4. Authentication:"
if grep -q "authorization: enabled" /etc/mongod.conf; then
    echo "✓ Authentication is enabled"
else
    echo "⚠ Authentication is not enabled (development only)"
fi

# Check replica set
echo -e "\n5. Replica Set Status:"
REPLICA_STATUS=$(mongosh --quiet --eval "
try {
    var status = rs.status();
    if (status.ok === 1) {
        print('✓ Replica set: ' + status.set);
    }
} catch(e) {
    print('ℹ Standalone instance');
}
" 2>/dev/null)
echo "$REPLICA_STATUS"

# Check monitoring scripts
echo -e "\n6. Monitoring Scripts:"
for script in mongodb_monitor.sh mongodb_backup.sh mongodb_performance.sh; do
    if [[ -x "/opt/mongodb/scripts/$script" ]]; then
        echo "✓ $script"
    else
        echo "✗ $script missing"
    fi
done

# Check cron jobs
echo -e "\n7. Scheduled Tasks:"
CRON_COUNT=$(sudo -u mongodb crontab -l 2>/dev/null | grep -c mongodb || echo 0)
if [[ $CRON_COUNT -gt 0 ]]; then
    echo "✓ $CRON_COUNT MongoDB cron jobs configured"
else
    echo "⚠ No MongoDB cron jobs found"
fi

# Check data directory
echo -e "\n8. Data Directory:"
if [[ -d /var/lib/mongodb ]]; then
    echo "✓ Data directory exists"
    echo "  Size: $(du -sh /var/lib/mongodb 2>/dev/null | cut -f1)"
else
    echo "✗ Data directory not found"
fi

echo -e "\nValidation completed!"
EOF

sudo chmod +x /opt/mongodb/scripts/validate_installation.sh
```

### Log Rotation Configuration

```bash
# Configure log rotation
sudo tee /etc/logrotate.d/mongodb << 'EOF'
/var/log/mongodb/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 mongodb mongodb
    sharedscripts
    postrotate
        /bin/kill -SIGUSR1 $(cat /var/run/mongod.pid 2>/dev/null) 2>/dev/null || true
    endscript
}
EOF
```

## Author

**Vanderley Sant Anna**  
*Senior DBA & DBRE | Software Engineer (B.Sc.) | Oracle OCP Certified | Data Engineer & DataOps Practitioner | Python for Automation & Data Pipelines*

---

This comprehensive MongoDB installation and configuration guide provides enterprise-ready deployment strategies for modern Linux distributions and Windows Server environments. The included automation scripts, monitoring tools, and best practices ensure reliable, scalable, and maintainable MongoDB deployments with high availability and optimal performance.
