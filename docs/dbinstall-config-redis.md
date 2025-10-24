<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Redis – Complete Installation and Configuration Guide
*High‑Performance In‑Memory Cache for Modern Applications*

## 📋 Table of Contents

1. [🎯 Overview](#-overview)
2. [✅ Prerequisites](#-prerequisites)
3. [🐧 Linux Installation](#-linux-installation)
4. [🍎 macOS Installation](#-macos-installation)
5. [🪟 Windows Installation](#-windows-installation)
6. [⚙️ Basic Configuration](#️-basic-configuration)
7. [🔧 Advanced Configuration](#-advanced-configuration)
8. [🔒 Security](#-security)
9. [📊 Monitoring](#-monitoring)
10. [🚀 Performance](#-performance)
11. [🔄 Backup & Recovery](#-backup--recovery)
12. [🌐 Redis Cluster](#-redis-cluster)
13. [🛡️ Redis Sentinel](#️-redis-sentinel)
14. [🐳 Docker](#-docker)
15. [☁️ Cloud](#️-cloud)
16. [🧪 Tests](#-tests)
17. [❗ Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

**Redis** (Remote Dictionary Server) is an open‑source in‑memory data store used as a cache, message broker, and database. It’s known for exceptional speed and versatility.

### 🌟 Key Features

- **⚡ Ultra‑Fast Performance**: Microsecond‑level operations  
- **🗂️ Rich Data Structures**: Strings, Lists, Sets, Hashes, Sorted Sets  
- **🔄 Configurable Persistence**: RDB snapshots and AOF logs  
- **🌐 Clustering**: Automatic data sharding and distribution  
- **🛡️ High Availability**: Redis Sentinel for failover  
- **📡 Pub/Sub**: Real‑time messaging  
- **🔍 Modules**: Extensibility via RedisJSON, RediSearch, etc.  
- **🐳 Container Ready**: First‑class Docker support  
- **☁️ Cloud Native**: Integrations with AWS, Azure, and GCP

### 📈 Use Cases

- **Application Cache**: Lower latency and load on primary DB  
- **Session Store**: Scalable session management  
- **Message Broker**: Queues and pub/sub patterns  
- **Real‑time Analytics**: Counters and metrics  
- **Leaderboards**: Real‑time rankings  
- **Rate Limiting**: Request throttle and quotas

---

## ✅ Prerequisites

### 🖥️ Supported Operating Systems

| System | Versions | Status | Notes |
|-------|----------|--------|-------|
| **Ubuntu** | 18.04+ | ✅ Official | Recommended for production |
| **CentOS/RHEL** | 7+ | ✅ Official | Enterprise support |
| **Debian** | 9+ | ✅ Official | Stable and reliable |
| **Amazon Linux** | 2 | ✅ Official | Optimized for AWS |
| **macOS** | 10.14+ | ✅ Official | Via Homebrew |
| **Windows** | 10/11 | ⚠️ Via WSL | Prefer WSL2 |
| **Docker** | Any | ✅ Official | Multi‑platform |

### 🔧 Hardware Requirements

#### **Minimum (Development)**
- **RAM**: 1 GB
- **CPU**: 1 core
- **Storage**: 5 GB
- **Network**: 100 Mbps

#### **Recommended (Production)**
- **RAM**: 8 GB+ (SSD swap preferred)
- **CPU**: 4+ cores
- **Storage**: NVMe SSD
- **Network**: 1 Gbps+

### 📦 System Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y build-essential tcl wget curl

# CentOS/RHEL
sudo yum groupinstall -y "Development Tools"
sudo yum install -y tcl wget curl

# macOS
xcode-select --install
```

## 🐧 Linux Installation

### 📦 Method 1: Package Manager (Recommended)

#### Ubuntu/Debian
```bash
# Update repositories
sudo apt update

# Install Redis
sudo apt install -y redis-server redis-tools

# Verify installation
redis-cli --version
sudo systemctl status redis-server
```

#### CentOS/RHEL 8+
```bash
# Enable EPEL
sudo dnf install -y epel-release

# Install Redis
sudo dnf install -y redis redis-tools

# Start and enable
sudo systemctl start redis
sudo systemctl enable redis
```

#### CentOS/RHEL 7
```bash
# Enable EPEL
sudo yum install -y epel-release

# Install Redis
sudo yum install -y redis redis-tools

# Start and enable
sudo systemctl start redis
sudo systemctl enable redis
```

### 🔧 Method 2: Build from Source

#### Download and Build
```bash
# Create a working directory
mkdir ~/redis-build && cd ~/redis-build

# Download stable release
wget http://download.redis.io/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable

# Compile
make

# Run tests (optional but recommended)
make test

# Install
sudo make install

# Create directories
sudo mkdir -p /etc/redis
sudo mkdir -p /var/lib/redis
sudo mkdir -p /var/log/redis
```

#### Create Redis User
```bash
# Create redis user
sudo useradd --system --home /var/lib/redis --shell /bin/false redis

# Set permissions
sudo chown redis:redis /var/lib/redis
sudo chown redis:redis /var/log/redis
sudo chmod 750 /var/lib/redis
sudo chmod 755 /var/log/redis
```

### ⚙️ Initial Configuration

#### Main Configuration File
```bash
# Copy default config
sudo cp redis.conf /etc/redis/redis.conf

# Backup original config
sudo cp /etc/redis/redis.conf /etc/redis/redis.conf.backup
```

#### Essential Settings
```bash
# Edit config
sudo nano /etc/redis/redis.conf

# Key changes:
```

```conf
# /etc/redis/redis.conf

# Bind to specific interfaces (security)
bind 127.0.0.1 ::1

# Default port
port 6379

# Run as daemon
daemonize yes

# PID file
pidfile /var/run/redis/redis-server.pid

# Log level
loglevel notice

# Log file
logfile /var/log/redis/redis-server.log

# Working directory
dir /var/lib/redis

# RDB dump filename
dbfilename dump.rdb

# Memory settings
maxmemory 2gb
maxmemory-policy allkeys-lru

# Networking
timeout 0
tcp-keepalive 300

# RDB persistence
save 900 1
save 300 10
save 60 10000

# AOF configuration
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
```

### 🔄 Systemd Service

#### Create service file
```bash
sudo nano /etc/systemd/system/redis.service
```

```ini
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

#### Enable and start service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable autostart
sudo systemctl enable redis

# Start Redis
sudo systemctl start redis

# Check status
sudo systemctl status redis

# Tail logs
sudo journalctl -u redis -f
```

### 🧪 Installation Verification

#### Basic Tests
```bash
# Connect to Redis
redis-cli

# Inside redis-cli:
127.0.0.1:6379> ping
# Response: PONG

127.0.0.1:6379> set test "Hello Redis"
# Response: OK

127.0.0.1:6379> get test
# Response: "Hello Redis"

127.0.0.1:6379> info server
# Shows server info

127.0.0.1:6379> exit
```

#### Check Performance
```bash
# Basic benchmark
redis-benchmark -q -n 100000

# Specific benchmark
redis-benchmark -t set,get -n 100000 -q

# Latency test
redis-cli --latency-history -h 127.0.0.1 -p 6379
```

## 🍎 macOS Installation

### 🍺 Method 1: Homebrew (Recommended)

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update Homebrew
brew update

# Install Redis
brew install redis

# Verify installation
redis-server --version
redis-cli --version
```

### 🚀 Start & Control

```bash
# Start Redis manually
redis-server

# Run as a service (background)
brew services start redis

# Stop service
brew services stop redis

# Restart service
brew services restart redis

# Service status
brew services list | grep redis
```

### ⚙️ macOS Configuration

```bash
# Find configuration file
find /usr/local -name "redis.conf" 2>/dev/null
# or
find /opt/homebrew -name "redis.conf" 2>/dev/null

# Edit configuration
nano /usr/local/etc/redis.conf
# or on Apple Silicon:
nano /opt/homebrew/etc/redis.conf
```

### 🔧 Method 2: Manual Build

```bash
# Install dependencies
xcode-select --install

# Download and build
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make

# Install
sudo make install

# Create directories
sudo mkdir -p /usr/local/etc/redis
sudo mkdir -p /usr/local/var/db/redis
sudo mkdir -p /usr/local/var/log
```

## 🪟 Windows Installation

### 🐧 Method 1: WSL2 (Recommended)

```powershell
# Install WSL2
wsl --install

# Reboot and set up Ubuntu
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04

# Enter WSL
wsl
```

```bash
# Inside WSL – follow Linux install
sudo apt update
sudo apt install -y redis-server redis-tools

# Start Redis
sudo service redis-server start

# Verify
redis-cli ping
```

### 🐳 Method 2: Docker Desktop

```powershell
# Install Docker Desktop
# Download: https://www.docker.com/products/docker-desktop

# Run Redis
docker run --name redis-server -p 6379:6379 -d redis:latest

# Connect
docker exec -it redis-server redis-cli
```

### 📦 Method 3: Native Binaries (Development)

```powershell
# Download Windows binaries
# https://github.com/microsoftarchive/redis/releases

# Extract to C:\Redis
# Add to System PATH

# Run
redis-server.exe

# In another terminal
redis-cli.exe
```

---

## 🐳 Docker

### 🚀 Basic Setup

#### Simple Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis-server
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  redis_data:
```

#### Run
```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f redis

# Connect
docker-compose exec redis redis-cli

# Stop
docker-compose down
```

### 🔧 Advanced Docker Setup

#### Full Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis-server
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - ./redis.conf:/etc/redis/redis.conf:ro
      - redis_data:/data
      - redis_logs:/var/log/redis
    command: redis-server /etc/redis/redis.conf
    sysctls:
      - net.core.somaxconn=65535
    ulimits:
      memlock: -1
      nofile:
        soft: 65535
        hard: 65535
    environment:
      - REDIS_REPLICATION_MODE=master
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: redis-commander
    restart: unless-stopped
    environment:
      - REDIS_HOSTS=local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis

volumes:
  redis_data:
  redis_logs:

networks:
  default:
    name: redis-network
```

#### Redis Config for Docker
```conf
# redis.conf
bind 0.0.0.0
port 6379
daemonize no
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
maxmemory 1gb
maxmemory-policy allkeys-lru
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 100
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
```

---

## ⚙️ Basic Configuration

### 📝 Configuration Structure

```conf
# /etc/redis/redis.conf

################################## NETWORK #####################################
# Network interface
bind 127.0.0.1 ::1

# Port
port 6379

# Idle connection timeout (0 = disabled)
timeout 0

# TCP keepalive
tcp-keepalive 300

################################# GENERAL #####################################
# Run as daemon
daemonize yes

# PID file
pidfile /var/run/redis/redis-server.pid

# Log level: debug, verbose, notice, warning
loglevel notice

# Log file
logfile /var/log/redis/redis-server.log

# Number of databases
databases 16

################################ SNAPSHOTTING  ################################
# Save snapshot if:
# - At least 1 key changed in 900 seconds (15 min)
# - At least 10 keys changed in 300 seconds (5 min)
# - At least 10000 keys changed in 60 seconds
save 900 1
save 300 10
save 60 10000

# Stop writes if snapshot fails
stop-writes-on-bgsave-error yes

# Compress RDB snapshots
rdbcompression yes

# RDB checksum
rdbchecksum yes

# RDB filename
dbfilename dump.rdb

# Working directory
dir /var/lib/redis

################################# REPLICATION #################################
# Replica configuration (if applicable)
# replicaof <masterip> <masterport>

# Master password (if applicable)
# masterauth <master-password>

################################## SECURITY ###################################
# Require password
# requirepass yourpassword

# Dangerous commands
# rename-command FLUSHDB ""
# rename-command FLUSHALL ""
# rename-command DEBUG ""

################################### CLIENTS ####################################
# Max connected clients
# maxclients 10000

############################## MEMORY MANAGEMENT #############################
# Memory limit
maxmemory 2gb

# Policy when memory limit is reached
maxmemory-policy allkeys-lru

############################# LAZY FREEING ####################################
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no

############################ KERNEL OOM CONTROL ##############################
oom-score-adj no

############################## APPEND ONLY MODE ###############################
# Enable AOF
appendonly yes

# AOF filename
appendfilename "appendonly.aof"

# Fsync frequency
appendfsync everysec

# Don’t fsync during rewrite
no-appendfsync-on-rewrite no

# Auto AOF rewrite
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Load truncated AOF
aof-load-truncated yes

# Use RDB+AOF preamble
aof-use-rdb-preamble yes

################################ LUA SCRIPTING  ###############################
# Lua script timeout
lua-time-limit 5000

################################## SLOW LOG ###################################
# Slow command log (microseconds)
slowlog-log-slower-than 10000

# Slow log max length
slowlog-max-len 128

################################ LATENCY MONITOR ##############################
# Latency monitor (microseconds)
latency-monitor-threshold 100
```

### 🔒 Basic Security Settings

```conf
# Strong password
requirepass "Sup3rS3cur3P@ssw0rd!"

# Bind only necessary interfaces
bind 127.0.0.1 10.0.0.100

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
rename-command CONFIG "CONFIG_09f911029d74e35bd84156c5635688c0"

# Protected mode
protected-mode yes

# Client timeout
timeout 300
```

### 📊 Performance Settings

```conf
# Memory optimizations
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Client output buffers
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

# Background operation frequency
hz 10

# Active rehashing
activerehashing yes

# AOF incremental fsync
aof-rewrite-incremental-fsync yes
```

## 🔧 Advanced Configuration

### 🏗️ Redis Sentinel (High Availability)

#### Master Configuration
```conf
# /etc/redis/redis-master.conf
port 6379
bind 0.0.0.0
requirepass "master-password"
masterauth "master-password"
```

#### Replica Configuration
```conf
# /etc/redis/redis-replica.conf
port 6380
bind 0.0.0.0
replicaof 192.168.1.100 6379
requirepass "replica-password"
masterauth "master-password"
```

#### Sentinel Configuration
```conf
# /etc/redis/sentinel.conf
port 26379
bind 0.0.0.0
sentinel monitor mymaster 192.168.1.100 6379 2
sentinel auth-pass mymaster master-password
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000
sentinel deny-scripts-reconfig yes
```

#### Start Sentinel
```bash
redis-sentinel /etc/redis/sentinel.conf
```

---

## 🌐 Redis Cluster

### 🔧 Cluster Configuration (6 Nodes)

#### Base Cluster Config
```conf
# /etc/redis/redis-cluster-700X.conf (for each node)
port 7001  # 7001, 7002, 7003, 7004, 7005, 7006
bind 0.0.0.0
cluster-enabled yes
cluster-config-file nodes-7001.conf  # unique per node
cluster-node-timeout 15000
appendonly yes
```

#### Cluster Bootstrap Script
```bash
#!/bin/bash
# cluster-setup.sh

# Create directories
for port in {7001..7006}; do
    mkdir -p /etc/redis/cluster/$port
    mkdir -p /var/lib/redis/cluster/$port
    mkdir -p /var/log/redis/cluster
done

# Copy configs
for port in {7001..7006}; do
    sed "s/7001/$port/g" /etc/redis/redis-cluster-template.conf > /etc/redis/cluster/$port/redis.conf
done

# Start nodes
for port in {7001..7006}; do
    redis-server /etc/redis/cluster/$port/redis.conf
done

# Create cluster
redis-cli --cluster create \
    127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 \
    127.0.0.1:7004 127.0.0.1:7005 127.0.0.1:7006 \
    --cluster-replicas 1
```

#### Cluster Management
```bash
# Check status
redis-cli --cluster check 127.0.0.1:7001

# Cluster info
redis-cli -c -p 7001
127.0.0.1:7001> CLUSTER NODES
127.0.0.1:7001> CLUSTER INFO

# Add node
redis-cli --cluster add-node 127.0.0.1:7007 127.0.0.1:7001

# Remove node
redis-cli --cluster del-node 127.0.0.1:7001 <node-id>

# Rebalance
redis-cli --cluster rebalance 127.0.0.1:7001
```

---

## 🔒 Security

### 🛡️ Advanced Security Configuration

```conf
# /etc/redis/redis-secure.conf

# Authentication
requirepass "Sup3rS3cur3P@ssw0rd!2024"
masterauth "Sup3rS3cur3P@ssw0rd!2024"

# Network Security
bind 127.0.0.1 10.0.0.100
protected-mode yes
port 0  # Disable default port
tls-port 6380  # Use TLS

# TLS Configuration
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file /etc/redis/tls/redis.key
tls-ca-cert-file /etc/redis/tls/ca.crt
tls-protocols "TLSv1.2 TLSv1.3"

# Command Security
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
rename-command EVAL ""
rename-command CONFIG "CONFIG_$(openssl rand -hex 16)"
rename-command SHUTDOWN "SHUTDOWN_$(openssl rand -hex 16)"

# Access Control Lists (Redis 6+)
user default off
user admin on >admin-password ~* &* +@all
user readonly on >readonly-password ~* &* +@read
user app on >app-password ~app:* &* +@read +@write -@dangerous
```

### 🔐 Configure TLS/SSL

```bash
# Generate certificates
mkdir -p /etc/redis/tls
cd /etc/redis/tls

# Private CA
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt

# Server certificate
openssl genrsa -out redis.key 4096
openssl req -new -key redis.key -out redis.csr
openssl x509 -req -in redis.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out redis.crt -days 365 -sha256

# Permissions
chown redis:redis /etc/redis/tls/*
chmod 600 /etc/redis/tls/*.key
chmod 644 /etc/redis/tls/*.crt
```

---

## 📊 Monitoring

### 📈 Monitoring Tools

#### Redis INFO
```bash
# General info
redis-cli info

# Specific sections
redis-cli info memory
redis-cli info stats
redis-cli info replication
redis-cli info persistence
redis-cli info clients
redis-cli info server
```

#### Monitoring Commands
```bash
# Real-time monitor
redis-cli monitor

# Command stats
redis-cli --stat

# Latency
redis-cli --latency
redis-cli --latency-history

# Big keys
redis-cli --bigkeys

# Memory per key
redis-cli --memkeys

# Pattern scan
redis-cli --scan --pattern "user:*"
```

### 📊 Monitoring Scripts

#### Metrics Script
```bash
#!/bin/bash
# redis-metrics.sh

REDIS_CLI="redis-cli"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Redis Metrics - $DATE ==="

# Basic info
echo "--- Server Info ---"
$REDIS_CLI info server | grep -E "(redis_version|uptime_in_days|process_id)"

# Memory
echo -e "\n--- Memory Usage ---"
$REDIS_CLI info memory | grep -E "(used_memory_human|used_memory_peak_human|mem_fragmentation_ratio)"

# Stats
echo -e "\n--- Stats ---"
$REDIS_CLI info stats | grep -E "(total_connections_received|total_commands_processed|instantaneous_ops_per_sec)"

# Clients
echo -e "\n--- Clients ---"
$REDIS_CLI info clients | grep -E "(connected_clients|blocked_clients)"

# Persistence
echo -e "\n--- Persistence ---"
$REDIS_CLI info persistence | grep -E "(rdb_last_save_time|aof_enabled)"

# Keyspace
echo -e "\n--- Keyspace ---"
$REDIS_CLI info keyspace
```

#### Basic Alerts
```bash
#!/bin/bash
# redis-alerts.sh

REDIS_CLI="redis-cli"
MEMORY_THRESHOLD=80
CLIENT_THRESHOLD=1000

# Memory usage
MEMORY_USAGE=$($REDIS_CLI info memory | grep used_memory_rss | cut -d: -f2 | tr -d '\r')
MAX_MEMORY=$($REDIS_CLI config get maxmemory | tail -1)

if [ "$MAX_MEMORY" != "0" ]; then
    MEMORY_PERCENT=$((MEMORY_USAGE * 100 / MAX_MEMORY))
    if [ $MEMORY_PERCENT -gt $MEMORY_THRESHOLD ]; then
        echo "ALERT: Redis memory usage is ${MEMORY_PERCENT}% (threshold: ${MEMORY_THRESHOLD}%)"
    fi
fi

# Connected clients
CLIENTS=$($REDIS_CLI info clients | grep connected_clients | cut -d: -f2 | tr -d '\r')
if [ $CLIENTS -gt $CLIENT_THRESHOLD ]; then
    echo "ALERT: Too many clients connected: $CLIENTS (threshold: $CLIENT_THRESHOLD)"
fi
```

---

## 🔄 Backup & Recovery

### 💾 RDB Backup

#### Manual Backup
```bash
#!/bin/bash
# redis-backup.sh

BACKUP_DIR="/backup/redis"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_CLI="redis-cli"

# Create backup dir
mkdir -p $BACKUP_DIR

# Force snapshot
$REDIS_CLI BGSAVE

# Wait for completion
while [ $($REDIS_CLI LASTSAVE) -eq $($REDIS_CLI LASTSAVE) ]; do
    sleep 1
done

# Copy dump
cp /var/lib/redis/dump.rdb $BACKUP_DIR/dump_$DATE.rdb

# Compress
gzip $BACKUP_DIR/dump_$DATE.rdb

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "dump_*.rdb.gz" -mtime +7 -delete

echo "Backup completed: dump_$DATE.rdb.gz"
```

#### Automated Backup with Cron
```bash
# Add to crontab
crontab -e

# Daily backup at 02:00
0 2 * * * /scripts/redis-backup.sh

# Hourly backups during business hours
0 9-18 * * 1-5 /scripts/redis-backup.sh
```

### 📁 AOF Backup

#### AOF Backup Script
```bash
#!/bin/bash
# redis-aof-backup.sh

BACKUP_DIR="/backup/redis/aof"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_CLI="redis-cli"

mkdir -p $BACKUP_DIR

# Rewrite AOF
$REDIS_CLI BGREWRITEAOF

# Wait for completion
while [ $($REDIS_CLI info persistence | grep aof_rewrite_in_progress | cut -d: -f2 | tr -d '\r') -eq 1 ]; do
    sleep 1
done

# Copy AOF
cp /var/lib/redis/appendonly.aof $BACKUP_DIR/appendonly_$DATE.aof
gzip $BACKUP_DIR/appendonly_$DATE.aof

echo "AOF backup completed: appendonly_$DATE.aof.gz"
```

### 🔄 Recovery

#### RDB Recovery
```bash
#!/bin/bash
# redis-restore-rdb.sh

BACKUP_FILE="$1"
REDIS_DATA_DIR="/var/lib/redis"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.rdb.gz>"
    exit 1
fi

# Stop Redis
sudo systemctl stop redis

# Current backup
mv $REDIS_DATA_DIR/dump.rdb $REDIS_DATA_DIR/dump.rdb.backup.$(date +%s)

# Restore backup
gunzip -c $BACKUP_FILE > $REDIS_DATA_DIR/dump.rdb
chown redis:redis $REDIS_DATA_DIR/dump.rdb

# Start Redis
sudo systemctl start redis

echo "Recovery completed from $BACKUP_FILE"
```

#### AOF Recovery
```bash
#!/bin/bash
# redis-restore-aof.sh

BACKUP_FILE="$1"
REDIS_DATA_DIR="/var/lib/redis"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.aof.gz>"
    exit 1
fi

# Stop Redis
sudo systemctl stop redis

# Current backup
mv $REDIS_DATA_DIR/appendonly.aof $REDIS_DATA_DIR/appendonly.aof.backup.$(date +%s)

# Restore backup
gunzip -c $BACKUP_FILE > $REDIS_DATA_DIR/appendonly.aof
chown redis:redis $REDIS_DATA_DIR/appendonly.aof

# Integrity check
redis-check-aof --fix $REDIS_DATA_DIR/appendonly.aof

# Start Redis
sudo systemctl start redis

echo "AOF recovery completed from $BACKUP_FILE"
```

## 🚀 Performance

### ⚡ Operating System Optimizations

#### Kernel Settings
```bash
# /etc/sysctl.conf
# Optimizations for Redis

# Memory overcommit
vm.overcommit_memory = 1

# Transparent Huge Pages (disable)
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# Network optimizations
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535

# File descriptors
fs.file-max = 65535
```

#### Persistent Settings
```bash
# /etc/security/limits.conf
redis soft nofile 65535
redis hard nofile 65535
redis soft nproc 65535
redis hard nproc 65535

# Apply settings
sudo sysctl -p
sudo systemctl restart redis
```

### 🔧 Performance Tuning

#### Redis Performance Config
```conf
# /etc/redis/redis-performance.conf

# TCP settings
tcp-backlog 65535
tcp-keepalive 60

# Client settings
timeout 300
maxclients 50000

# Memory settings
maxmemory 8gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Persistence tuning
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum no  # Disable for performance

# AOF tuning
appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Background operations
hz 10
activerehashing yes

# Data structure optimizations
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Lazy freeing
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
lazyfree-lazy-server-del yes
replica-lazy-flush yes

# Client buffer limits
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

### 📊 Benchmarking

#### Benchmark Scripts
```bash
#!/bin/bash
# redis-benchmark-suite.sh

echo "=== Redis Performance Benchmark ==="
date

# Basic benchmark
echo -e "\n--- Basic Operations ---"
redis-benchmark -q -n 100000 -c 50 -t set,get,incr,lpush,rpush,lpop,rpop,sadd,hset,spop,zadd,zpopmin,lrange

# Pipeline benchmark
echo -e "\n--- Pipeline Performance ---"
redis-benchmark -q -n 100000 -c 50 -P 16 -t set,get

# Different data sizes
echo -e "\n--- Data Size Performance ---"
for size in 10 100 1000 10000; do
    echo "Data size: $size bytes"
    redis-benchmark -q -n 10000 -d $size -t set,get
done

# Operation-specific
echo -e "\n--- Detailed Operation Benchmark ---"
redis-benchmark -n 100000 -t set
redis-benchmark -n 100000 -t get
redis-benchmark -n 100000 -t incr
redis-benchmark -n 100000 -t lpush
redis-benchmark -n 100000 -t rpush
redis-benchmark -n 100000 -t lpop
redis-benchmark -n 100000 -t rpop
redis-benchmark -n 100000 -t sadd
redis-benchmark -n 100000 -t hset
redis-benchmark -n 100000 -t spop
redis-benchmark -n 100000 -t zadd
redis-benchmark -n 100000 -t zpopmin
redis-benchmark -n 100000 -t lrange -r 100
```

---

## 🧪 Tests

### 🔍 Test Scripts

#### Functional Test
```bash
#!/bin/bash
# redis-functional-test.sh

REDIS_CLI="redis-cli"
TEST_KEY="test:$(date +%s)"

echo "=== Redis Functional Tests ==="

# Connectivity test
echo -n "Testing connectivity... "
if $REDIS_CLI ping | grep -q PONG; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
    exit 1
fi

# Basic operations
echo -n "Testing basic operations... "
$REDIS_CLI set $TEST_KEY "test_value" > /dev/null
if [ "$($REDIS_CLI get $TEST_KEY)" = "test_value" ]; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
fi

# Expiration
echo -n "Testing expiration... "
$REDIS_CLI setex ${TEST_KEY}_exp 2 "expire_test" > /dev/null
sleep 3
if [ "$($REDIS_CLI get ${TEST_KEY}_exp)" = "" ]; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
fi

# Data structures
echo -n "Testing data structures... "
$REDIS_CLI lpush ${TEST_KEY}_list "item1" "item2" > /dev/null
$REDIS_CLI sadd ${TEST_KEY}_set "member1" "member2" > /dev/null
$REDIS_CLI hset ${TEST_KEY}_hash "field1" "value1" > /dev/null

if [ "$($REDIS_CLI llen ${TEST_KEY}_list)" = "2" ] && \
   [ "$($REDIS_CLI scard ${TEST_KEY}_set)" = "2" ] && \
   [ "$($REDIS_CLI hlen ${TEST_KEY}_hash)" = "1" ]; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
fi

# Cleanup
$REDIS_CLI del $TEST_KEY ${TEST_KEY}_list ${TEST_KEY}_set ${TEST_KEY}_hash > /dev/null

echo "All tests completed!"
```

#### Load Test
```bash
#!/bin/bash
# redis-load-test.sh

REDIS_CLI="redis-cli"
CONCURRENT_CLIENTS=50
OPERATIONS_PER_CLIENT=1000

echo "=== Redis Load Test ==="
echo "Clients: $CONCURRENT_CLIENTS"
echo "Operations per client: $OPERATIONS_PER_CLIENT"

# Per-client test function
test_client() {
    local client_id=$1
    local prefix="load_test_${client_id}"

    for i in $(seq 1 $OPERATIONS_PER_CLIENT); do
        $REDIS_CLI set "${prefix}_${i}" "value_${i}" > /dev/null
        $REDIS_CLI get "${prefix}_${i}" > /dev/null
        $REDIS_CLI del "${prefix}_${i}" > /dev/null
    done
}

# Run clients in parallel
echo "Starting load test..."
start_time=$(date +%s)

for client in $(seq 1 $CONCURRENT_CLIENTS); do
    test_client $client &
done

# Wait for completion
wait

end_time=$(date +%s)
total_time=$((end_time - start_time))
total_ops=$((CONCURRENT_CLIENTS * OPERATIONS_PER_CLIENT * 3))  # 3 ops per iteration

echo "Load test completed!"
echo "Total time: ${total_time}s"
echo "Total operations: $total_ops"
echo "Operations per second: $((total_ops / total_time))"
```

---

## ❗ Troubleshooting

### 🔍 Common Issues

#### Performance Issues
```bash
# Inspect slow queries
redis-cli slowlog get 10

# Check memory usage
redis-cli info memory

# Check latency
redis-cli --latency

# Big memory‑hungry keys
redis-cli --bigkeys

# Real‑time monitor
redis-cli monitor
```

#### Connection Issues
```bash
# Check if Redis is running
systemctl status redis

# Check listening ports
netstat -tlnp | grep 6379

# Connectivity test
telnet localhost 6379

# Review logs
tail -f /var/log/redis/redis-server.log

# Validate configuration
redis-cli config get "*"
```

#### Memory Issues
```bash
# Memory usage
redis-cli info memory | grep used_memory_human

# Fragmentation
redis-cli info memory | grep mem_fragmentation_ratio

# Purge expired memory
redis-cli --eval "return redis.call('memory', 'purge')" 0
```

### 🛠️ Diagnostic Scripts

#### Full Diagnostic
```bash
#!/bin/bash
# redis-diagnostic.sh

echo "=== Redis Diagnostic Report ==="
date
echo

# Process check
echo "--- Process Status ---"
if pgrep redis-server > /dev/null; then
    echo "✅ Redis process is running"
    ps aux | grep redis-server | grep -v grep
else
    echo "❌ Redis process is not running"
fi
echo

# Connectivity
echo "--- Connectivity Test ---"
if redis-cli ping | grep -q PONG; then
    echo "✅ Redis is responding"
else
    echo "❌ Redis is not responding"
fi
echo

# Server info
echo "--- Server Information ---"
redis-cli info server | grep -E "(redis_version|uptime_in_days|os)"
echo

# Memory
echo "--- Memory Usage ---"
redis-cli info memory | grep -E "(used_memory_human|used_memory_peak_human|mem_fragmentation_ratio)"
echo

# Performance stats
echo "--- Performance Stats ---"
redis-cli info stats | grep -E "(total_commands_processed|instantaneous_ops_per_sec|keyspace_hits|keyspace_misses)"
echo

# Clients
echo "--- Client Information ---"
redis-cli info clients
echo

# Critical config
echo "--- Critical Configuration ---"
redis-cli config get maxmemory
redis-cli config get maxmemory-policy
redis-cli config get save
echo

# Slow log
echo "--- Recent Slow Queries ---"
redis-cli slowlog get 5
echo

# Keyspace
echo "--- Keyspace Information ---"
redis-cli info keyspace
```
---

## 🎯 Conclusion

This guide provides a solid foundation for installing, configuring, and operating Redis in production environments. Redis is a powerful tool that, when properly tuned, can significantly improve application performance.

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


