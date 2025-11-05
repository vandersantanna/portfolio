<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Oracle Database 19c Installation and Configuration Guide
*Install once, configure right, run mission-critical.*

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Pre-installation Tasks](#pre-installation-tasks)
- [Single Instance Installation](#single-instance-installation)
- [Oracle Grid Infrastructure](#oracle-grid-infrastructure)
- [Real Application Clusters (RAC)](#real-application-clusters-rac)
- [Data Guard Configuration](#data-guard-configuration)
- [Database Creation](#database-creation)
- [Post-Installation Configuration](#post-installation-configuration)
- [Security Configuration](#security-configuration)
- [Performance Tuning](#performance-tuning)
- [Backup and Recovery](#backup-and-recovery)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [High Availability Best Practices](#high-availability-best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

> Oracle installation and configuration is quite unique. It's impossible not to compare it to other databases, but in reality, the comparison ends there. There are several prerequisites and steps that, if not followed, will generally lead to one or more errors and future configuration problems. For this reason, it's good to plan before installing and follow a guide that leads through the correct steps. I hope this is the guide for you.

> Oracle Database 19c is not the most recent version. We can mention 23ai and 26ai. But Oracle Database 19c is still an extremely popular version, and for this reason, I focused on this version. One step at a time.

Oracle Database 19c provides enterprise-grade database capabilities with advanced high availability features. This guide covers installation and configuration including Real Application Clusters (RAC) and Data Guard for maximum availability and disaster recovery. Let's move on.

**Key Features:**
- Automatic Storage Management (ASM)
- Real Application Clusters (RAC)
- Data Guard for disaster recovery
- Advanced security features
- In-memory database capabilities
- Machine learning integration

**High Availability Components:**
- **RAC**: Clustered database for scalability and availability
- **Data Guard**: Disaster recovery and data protection
- **ASM**: Automatic storage management
- **Grid Infrastructure**: Cluster management foundation

[Back to top](#table-of-contents)

## Prerequisites

### Supported Operating Systems

**Oracle Linux / Red Hat Enterprise Linux:**
- Oracle Linux 7.4+ or 8.1+
- RHEL 7.4+ or 8.1+

**SUSE Linux Enterprise Server:**
- SLES 12 SP4+ or 15.1+

### Hardware Requirements

**Minimum Requirements:**
```bash
# CPU
CPU_CORES=2
CPU_ARCHITECTURE="x86_64"

# Memory
RAM_MINIMUM="8 GB"
RAM_RECOMMENDED="16 GB or more"

# Storage
DISK_SPACE_DATABASE="12 GB minimum"
DISK_SPACE_GRID="8 GB for Grid Infrastructure"
SWAP_SPACE="RAM * 1.5 (up to 32GB)"

# Network
NETWORK_INTERFACES="2 (public and private for RAC)"
```

**Production Minimum Recommendations:**
 ```bash
# For RAC environments
CPU_CORES_RAC="8+ per node"
RAM_RAC="32 GB+ per node"
STORAGE_SHARED="Shared storage (SAN, NFS, ASM)"
NETWORK_REDUNDANCY="Bonded interfaces recommended"
```

[Back to top](#table-of-contents)

## System Requirements

### Kernel Parameters

```bash
# Configure kernel parameters for Oracle
sudo tee -a /etc/sysctl.conf << 'EOF'
# Oracle Database kernel parameters
fs.file-max = 6815744
kernel.sem = 250 32000 100 128
kernel.shmmni = 4096
kernel.shmall = 1073741824
kernel.shmmax = 4398046511104
kernel.panic_on_oops = 1
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576
net.ipv4.conf.all.rp_filter = 2
net.ipv4.conf.default.rp_filter = 2
fs.aio-max-nr = 1048576
net.ipv4.ip_local_port_range = 9000 65500
EOF

# Apply kernel parameters
sudo sysctl -p
```

### System Limits

```bash
# Configure system limits for Oracle users
sudo tee -a /etc/security/limits.conf << 'EOF'
# Oracle Database limits
oracle   soft   nofile    1024
oracle   hard   nofile    65536
oracle   soft   nproc     16384
oracle   hard   nproc     16384
oracle   soft   stack     10240
oracle   hard   stack     32768
oracle   hard   memlock   134217728
oracle   soft   memlock   134217728

# Grid Infrastructure limits
grid     soft   nofile    1024
grid     hard   nofile    65536
grid     soft   nproc     16384
grid     hard   nproc     16384
grid     soft   stack     10240
grid     hard   stack     32768
grid     hard   memlock   134217728
grid     soft   memlock   134217728
EOF
```

[Back to top](#table-of-contents)

## Pre-installation Tasks

### User and Group Creation

```bash
# Create Oracle groups
sudo groupadd -g 54321 oinstall
sudo groupadd -g 54322 dba
sudo groupadd -g 54323 oper
sudo groupadd -g 54324 backupdba
sudo groupadd -g 54325 dgdba
sudo groupadd -g 54326 kmdba
sudo groupadd -g 54327 asmdba
sudo groupadd -g 54328 asmoper
sudo groupadd -g 54329 asmadmin
sudo groupadd -g 54330 racdba

# Create Oracle users
sudo useradd -u 54321 -g oinstall -G dba,asmdba,backupdba,dgdba,kmdba,racdba oracle
sudo useradd -u 54322 -g oinstall -G asmadmin,asmdba,asmoper,dba grid

# Set passwords
sudo passwd oracle
sudo passwd grid
```

### Directory Structure Creation

```bash
# Create Oracle base directories
sudo mkdir -p /u01/app/oracle/product/19.3.0/dbhome_1
sudo mkdir -p /u01/app/grid/product/19.3.0/grid
sudo mkdir -p /u01/app/oraInventory
sudo mkdir -p /u01/app/oracle/admin
sudo mkdir -p /u01/app/oracle/audit
sudo mkdir -p /u01/app/oracle/cfgtoollogs
sudo mkdir -p /u01/app/oracle/checkpoints
sudo mkdir -p /u01/app/oracle/diag
sudo mkdir -p /u01/app/oracle/oradata

# Set ownership and permissions
sudo chown -R oracle:oinstall /u01/app/oracle
sudo chown -R grid:oinstall /u01/app/grid
sudo chown -R grid:oinstall /u01/app/oraInventory
sudo chmod -R 775 /u01/app
```

### Environment Configuration

```bash
# Oracle user environment
sudo -u oracle tee /home/oracle/.bash_profile << 'EOF'
# Oracle Environment
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib

# Grid Infrastructure environment
export GRID_HOME=/u01/app/grid/product/19.3.0/grid

# Other settings
export EDITOR=vi
export TMP=/tmp
export TMPDIR=$TMP
export LANG=en_US.UTF-8

# Aliases
alias cdob='cd $ORACLE_BASE'
alias cdoh='cd $ORACLE_HOME'
alias tns='cd $ORACLE_HOME/network/admin'
alias envo='env | grep ORACLE'

umask 022
EOF

# Grid user environment  
sudo -u grid tee /home/grid/.bash_profile << 'EOF'
# Grid Infrastructure Environment
export ORACLE_BASE=/u01/app/grid
export GRID_HOME=/u01/app/grid/product/19.3.0/grid
export ORACLE_HOME=$GRID_HOME
export PATH=$GRID_HOME/bin:$PATH
export LD_LIBRARY_PATH=$GRID_HOME/lib:/lib:/usr/lib

# Other settings
export EDITOR=vi
export TMP=/tmp
export TMPDIR=$TMP
export LANG=en_US.UTF-8

umask 022
EOF
```

### Package Installation

**Oracle Linux / RHEL:**
```bash
# Install Oracle preinstall package
sudo yum install -y oracle-database-preinstall-19c

# Or install packages manually
sudo yum install -y binutils compat-libcap1 compat-libstdc++-33 \
    gcc gcc-c++ glibc glibc-devel ksh libaio libaio-devel \
    libgcc libstdc++ libstdc++-devel libXi libXtst make \
    sysstat unixODBC unixODBC-devel
```

**Additional RAC Requirements:**
```bash
# Install cluster verification utility prerequisites
sudo yum install -y cvuqdisk

# Install additional packages for RAC
sudo yum install -y nfs-utils smartmontools
```

### Storage Configuration

**For Single Instance (Local Storage):**
```bash
# Create directories for database files
sudo mkdir -p /u01/app/oracle/oradata/ORCL
sudo mkdir -p /u01/app/oracle/fast_recovery_area
sudo mkdir -p /u01/app/oracle/admin/ORCL/adump

# Set permissions
sudo chown -R oracle:oinstall /u01/app/oracle/oradata
sudo chown -R oracle:oinstall /u01/app/oracle/fast_recovery_area
sudo chown -R oracle:oinstall /u01/app/oracle/admin
```

**For RAC (Shared Storage):**
```bash
# Configure shared storage (example using multipath)
# This assumes shared SAN storage is available

# Configure multipath
sudo tee /etc/multipath.conf << 'EOF'
defaults {
    user_friendly_names yes
    find_multipaths yes
}

blacklist {
    devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
    devnode "^hd[a-z]"
    devnode "^sda"
}

multipaths {
    multipath {
        wwid    "36000000000000001"
        alias   asm_disk1
    }
    multipath {
        wwid    "36000000000000002"  
        alias   asm_disk2
    }
    multipath {
        wwid    "36000000000000003"
        alias   asm_disk3
    }
}
EOF

# Restart multipath service
sudo systemctl restart multipathd
sudo systemctl enable multipathd

# Configure udev rules for ASM disks
sudo tee /etc/udev/rules.d/99-oracle-asmdevices.rules << 'EOF'
KERNEL=="dm-*", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/$name", RESULT=="36000000000000001", OWNER="grid", GROUP="asmadmin", MODE="0660", NAME="asm-disk1"
KERNEL=="dm-*", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/$name", RESULT=="36000000000000002", OWNER="grid", GROUP="asmadmin", MODE="0660", NAME="asm-disk2"
KERNEL=="dm-*", SUBSYSTEM=="block", PROGRAM=="/usr/lib/udev/scsi_id -g -u -d /dev/$name", RESULT=="36000000000000003", OWNER="grid", GROUP="asmadmin", MODE="0660", NAME="asm-disk3"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

[Back to top](#table-of-contents)

## Single Instance Installation

### Download and Extract Oracle Software

```bash
# Download Oracle Database 19c from Oracle Technology Network
# Files needed:
# - LINUX.X64_193000_db_home.zip

# Create installation directory and extract
sudo -u oracle mkdir -p /u01/app/oracle/product/19.3.0/dbhome_1
cd /u01/app/oracle/product/19.3.0/dbhome_1

# Extract the zip file (as oracle user)
sudo -u oracle unzip -q /path/to/LINUX.X64_193000_db_home.zip

# Set permissions
sudo chown -R oracle:oinstall /u01/app/oracle/product/19.3.0/dbhome_1
```

### Silent Installation

```bash
# Create response file for silent installation
sudo -u oracle tee /tmp/db_install.rsp << 'EOF'
oracle.install.option=INSTALL_DB_SWONLY
UNIX_GROUP_NAME=oinstall
INVENTORY_LOCATION=/u01/app/oraInventory
ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
ORACLE_BASE=/u01/app/oracle
oracle.install.db.InstallEdition=EE
oracle.install.db.OSDBA_GROUP=dba
oracle.install.db.OSOPER_GROUP=oper
oracle.install.db.OSBACKUPDBA_GROUP=backupdba
oracle.install.db.OSDGDBA_GROUP=dgdba
oracle.install.db.OSKMDBA_GROUP=kmdba
oracle.install.db.OSRACDBA_GROUP=racdba
SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
DECLINE_SECURITY_UPDATES=true
EOF

# Run silent installation
sudo -u oracle /u01/app/oracle/product/19.3.0/dbhome_1/runInstaller -silent \
    -responseFile /tmp/db_install.rsp

# Run root scripts after installation completes
sudo /u01/app/oraInventory/orainstRoot.sh
sudo /u01/app/oracle/product/19.3.0/dbhome_1/root.sh
```

### GUI Installation (Alternative)

```bash
# For GUI installation, ensure X11 forwarding is enabled
# SSH with X11 forwarding
ssh -X oracle@server

# Set DISPLAY variable
export DISPLAY=:0.0

# Start installer
cd /u01/app/oracle/product/19.3.0/dbhome_1
./runInstaller

# Follow GUI prompts:
# 1. Configure Security Updates
# 2. Installation Option: Install database software only
# 3. Database Installation Options: Single instance
# 4. Database Edition: Enterprise Edition
# 5. Installation Location: /u01/app/oracle/product/19.3.0/dbhome_1
# 6. Create Inventory: /u01/app/oraInventory
# 7. Operating System Groups: Use created groups
# 8. Prerequisite Checks: Fix any issues
# 9. Summary: Review and install
# 10. Execute Configuration Scripts as root
```

[Back to top](#table-of-contents)

## Oracle Grid Infrastructure

### Grid Infrastructure Installation

```bash
# Download Grid Infrastructure software
# File needed: LINUX.X64_193000_grid_home.zip

# Extract Grid Infrastructure
sudo -u grid mkdir -p /u01/app/grid/product/19.3.0/grid
cd /u01/app/grid/product/19.3.0/grid
sudo -u grid unzip -q /path/to/LINUX.X64_193000_grid_home.zip

# Create response file for Grid Infrastructure
sudo -u grid tee /tmp/grid_install.rsp << 'EOF'
oracle.install.option=HA_CONFIG
INVENTORY_LOCATION=/u01/app/oraInventory
oracle.install.asm.OSDBA=asmdba
oracle.install.asm.OSOPER=asmoper
oracle.install.asm.OSASM=asmadmin

# For standalone server (single instance with ASM)
oracle.install.crs.config.gpnp.configureGNS=false
oracle.install.crs.config.autoConfigureClusterNodeVIP=false
oracle.install.crs.config.clusterName=local-cluster
oracle.install.crs.config.localnode=server1

# ASM Configuration
oracle.install.asm.configureAFD=false
oracle.install.asm.storageOption=ASM
oracle.install.asmOnNAS.configureGIMRDataDG=false

# ASM Disk Groups
oracle.install.asm.diskGroup.name=DATA
oracle.install.asm.diskGroup.redundancy=EXTERNAL
oracle.install.asm.diskGroup.disks=/dev/asm-disk1,/dev/asm-disk2
oracle.install.asm.diskGroup.diskDiscoveryString=/dev/asm-*
oracle.install.asm.monitorPassword=Oracle123

# Network Interface
oracle.install.crs.config.networkInterfaceList=eth0:10.0.1.0:1,eth1:192.168.1.0:5

SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
DECLINE_SECURITY_UPDATES=true
EOF

# Install Grid Infrastructure
sudo -u grid /u01/app/grid/product/19.3.0/grid/runInstaller -silent \
    -responseFile /tmp/grid_install.rsp

# Run configuration scripts as root
sudo /u01/app/oraInventory/orainstRoot.sh
sudo /u01/app/grid/product/19.3.0/grid/root.sh
```

### ASM Disk Group Configuration

```bash
# Switch to grid user
sudo su - grid

# Start ASM instance
asmcmd

# Create additional disk groups
sqlplus / as sysasm

-- Create FRA disk group
CREATE DISKGROUP FRA EXTERNAL REDUNDANCY 
DISK '/dev/asm-disk3'
ATTRIBUTE 'compatible.rdbms' = '19.0.0', 
'compatible.asm' = '19.0.0';

-- Verify disk groups
SELECT name, state, type FROM v$asm_diskgroup;

-- Exit
exit
```

[Back to top](#table-of-contents)

## Real Application Clusters (RAC)

### RAC Prerequisites

**Network Configuration:**
```bash
# Configure hostname resolution (/etc/hosts on all nodes)
sudo tee -a /etc/hosts << 'EOF'
# Public network
10.0.1.10    rac1.domain.com    rac1
10.0.1.11    rac2.domain.com    rac2

# Private network  
192.168.1.10    rac1-priv.domain.com    rac1-priv
192.168.1.11    rac2-priv.domain.com    rac2-priv

# Virtual IPs
10.0.1.12    rac1-vip.domain.com    rac1-vip
10.0.1.13    rac2-vip.domain.com    rac2-vip

# SCAN IPs
10.0.1.14    rac-scan.domain.com    rac-scan
10.0.1.15    rac-scan.domain.com    
10.0.1.16    rac-scan.domain.com
EOF
```

**SSH Connectivity:**
```bash
# Configure SSH equivalency for grid and oracle users between nodes
# Run on each node for both grid and oracle users

# Generate SSH keys
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

# Copy public keys to other nodes
ssh-copy-id grid@rac2
ssh-copy-id oracle@rac2

# Test connectivity (should not prompt for password)
ssh rac2 date
```

### Grid Infrastructure for RAC

```bash
# Create RAC-specific response file
sudo -u grid tee /tmp/grid_rac_install.rsp << 'EOF'
oracle.install.option=CRS_CONFIG
INVENTORY_LOCATION=/u01/app/oraInventory
oracle.install.asm.OSDBA=asmdba
oracle.install.asm.OSOPER=asmoper
oracle.install.asm.OSASM=asmadmin

# Cluster Configuration
oracle.install.crs.config.gpnp.configureGNS=false
oracle.install.crs.config.autoConfigureClusterNodeVIP=true
oracle.install.crs.config.clusterName=rac-cluster
oracle.install.crs.config.clusterNodes=rac1:rac1-vip,rac2:rac2-vip
oracle.install.crs.config.networkInterfaceList=eth0:10.0.1.0:1,eth1:192.168.1.0:5

# SCAN Configuration
oracle.install.crs.config.gpnp.scanName=rac-scan
oracle.install.crs.config.gpnp.scanPort=1521

# Storage Configuration
oracle.install.asm.configureAFD=false
oracle.install.asm.storageOption=ASM
oracle.install.asmOnNAS.configureGIMRDataDG=true

# OCR and Voting Disk
oracle.install.asm.diskGroup.name=OCR
oracle.install.asm.diskGroup.redundancy=NORMAL
oracle.install.asm.diskGroup.disks=/dev/asm-disk1,/dev/asm-disk2,/dev/asm-disk3
oracle.install.asm.diskGroup.diskDiscoveryString=/dev/asm-*

# ASM Password
oracle.install.asm.monitorPassword=Oracle123

SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
DECLINE_SECURITY_UPDATES=true
EOF

# Install Grid Infrastructure on first node
sudo -u grid /u01/app/grid/product/19.3.0/grid/runInstaller -silent \
    -responseFile /tmp/grid_rac_install.rsp

# Run root scripts on first node
sudo /u01/app/oraInventory/orainstRoot.sh
sudo /u01/app/grid/product/19.3.0/grid/root.sh

# Run root script on second node
ssh rac2 "sudo /u01/app/grid/product/19.3.0/grid/root.sh"
```

### RAC Database Installation

```bash
# Create RAC database response file
sudo -u oracle tee /tmp/db_rac_install.rsp << 'EOF'
oracle.install.option=INSTALL_DB_SWONLY
UNIX_GROUP_NAME=oinstall
INVENTORY_LOCATION=/u01/app/oraInventory
ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
ORACLE_BASE=/u01/app/oracle
oracle.install.db.InstallEdition=EE
oracle.install.db.CLUSTER_NODES=rac1,rac2
oracle.install.db.isRACOneInstall=false
oracle.install.db.OSDBA_GROUP=dba
oracle.install.db.OSOPER_GROUP=oper
oracle.install.db.OSBACKUPDBA_GROUP=backupdba
oracle.install.db.OSDGDBA_GROUP=dgdba
oracle.install.db.OSKMDBA_GROUP=kmdba
oracle.install.db.OSRACDBA_GROUP=racdba
SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
DECLINE_SECURITY_UPDATES=true
EOF

# Install RAC database software
sudo -u oracle /u01/app/oracle/product/19.3.0/dbhome_1/runInstaller -silent \
    -responseFile /tmp/db_rac_install.rsp

# Run root scripts on all nodes
sudo /u01/app/oracle/product/19.3.0/dbhome_1/root.sh
ssh rac2 "sudo /u01/app/oracle/product/19.3.0/dbhome_1/root.sh"
```

### Create RAC Database

```bash
# Create RAC database using DBCA
sudo -u oracle dbca -silent -createDatabase \
    -templateName General_Purpose.dbc \
    -gdbname RACDB -sid RACDB \
    -responseFile NO_VALUE \
    -characterSet AL32UTF8 \
    -sysPassword Oracle123 \
    -systemPassword Oracle123 \
    -createAsContainerDatabase false \
    -databaseType MULTIPURPOSE \
    -memoryMgmtType auto_smp \
    -totalMemory 4096 \
    -storageType ASM \
    -diskGroupName +DATA \
    -recoveryGroupName +FRA \
    -redoLogFileSize 100 \
    -emConfiguration NONE \
    -nodeinfo rac1,rac2

# Verify RAC database
sudo -u oracle srvctl status database -d RACDB
sudo -u oracle srvctl config database -d RACDB
```

### RAC Services Configuration

```bash
# Create application services for load balancing
sudo -u oracle srvctl add service -d RACDB -s READ_WRITE_SERVICE \
    -r RACDB1,RACDB2 -P BASIC \
    -e SELECT -m BASIC -z 180 -w 5

sudo -u oracle srvctl add service -d RACDB -s READ_ONLY_SERVICE \
    -r RACDB2 -a RACDB1 -P BASIC \
    -e SELECT -m BASIC -z 180 -w 5

# Start services
sudo -u oracle srvctl start service -d RACDB -s READ_WRITE_SERVICE
sudo -u oracle srvctl start service -d RACDB -s READ_ONLY_SERVICE

# Check service status
sudo -u oracle srvctl status service -d RACDB
```

[Back to top](#table-of-contents)

## Data Guard Configuration

### Primary Database Setup

```bash
# Configure primary database for Data Guard
sudo -u oracle sqlplus / as sysdba

-- Enable archive log mode
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;

-- Configure Data Guard parameters
ALTER SYSTEM SET LOG_ARCHIVE_CONFIG='DG_CONFIG=(PRIMARY,STANDBY)' SCOPE=BOTH;
ALTER SYSTEM SET LOG_ARCHIVE_DEST_1='LOCATION=+FRA VALID_FOR=(ALL_LOGFILES,ALL_ROLES) DB_UNIQUE_NAME=PRIMARY' SCOPE=BOTH;
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=STANDBY LGWR ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=STANDBY' SCOPE=BOTH;
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_1=ENABLE SCOPE=BOTH;
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_2=ENABLE SCOPE=BOTH;
ALTER SYSTEM SET REMOTE_LOGIN_PASSWORDFILE=EXCLUSIVE SCOPE=SPFILE;
ALTER SYSTEM SET LOG_ARCHIVE_FORMAT='%t_%s_%r.arc' SCOPE=SPFILE;
ALTER SYSTEM SET LOG_ARCHIVE_MAX_PROCESSES=30 SCOPE=BOTH;
ALTER SYSTEM SET STANDBY_FILE_MANAGEMENT=AUTO SCOPE=BOTH;
ALTER SYSTEM SET DB_FILE_NAME_CONVERT='+DATA/STANDBY/','+DATA/PRIMARY/' SCOPE=SPFILE;
ALTER SYSTEM SET LOG_FILE_NAME_CONVERT='+FRA/STANDBY/','+FRA/PRIMARY/' SCOPE=SPFILE;

-- Add standby redo logs
ALTER DATABASE ADD STANDBY LOGFILE GROUP 4 ('+FRA') SIZE 100M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 5 ('+FRA') SIZE 100M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 6 ('+FRA') SIZE 100M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 7 ('+FRA') SIZE 100M;

-- Create pfile for standby
CREATE PFILE='/tmp/initSTANDBY.ora' FROM SPFILE;
```

### Network Configuration for Data Guard

```bash
# Configure TNS entries on both primary and standby servers
sudo -u oracle tee -a $ORACLE_HOME/network/admin/tnsnames.ora << 'EOF'
PRIMARY =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = primary-server)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = PRIMARY)
    )
  )

STANDBY =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = standby-server)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = STANDBY)
    )
  )
EOF

# Test connectivity
sudo -u oracle tnsping PRIMARY
sudo -u oracle tnsping STANDBY
```

### Physical Standby Creation

```bash
# On standby server - create directories
sudo -u oracle mkdir -p /u01/app/oracle/admin/STANDBY/adump

# Modify init parameter file for standby
sudo -u oracle tee /tmp/initSTANDBY.ora << 'EOF'
*.audit_file_dest='/u01/app/oracle/admin/STANDBY/adump'
*.audit_trail='db'
*.compatible='19.0.0'
*.control_files='+DATA/STANDBY/control01.ctl','+FRA/STANDBY/control02.ctl'
*.db_block_size=8192
*.db_domain=''
*.db_name='PRIMARY'
*.db_unique_name='STANDBY'
*.diagnostic_dest='/u01/app/oracle'
*.dispatchers='(PROTOCOL=TCP) (SERVICE=STANDBYXDB)'
*.fal_client='STANDBY'
*.fal_server='PRIMARY'
*.log_archive_config='DG_CONFIG=(PRIMARY,STANDBY)'
*.log_archive_dest_1='LOCATION=+FRA VALID_FOR=(ALL_LOGFILES,ALL_ROLES) DB_UNIQUE_NAME=STANDBY'
*.log_archive_dest_2='SERVICE=PRIMARY LGWR ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=PRIMARY'
*.log_archive_dest_state_1='ENABLE'
*.log_archive_dest_state_2='ENABLE'
*.log_archive_format='%t_%s_%r.arc'
*.log_archive_max_processes=30
*.memory_target=4g
*.open_cursors=300
*.processes=300
*.remote_login_passwordfile='EXCLUSIVE'
*.standby_file_management='AUTO'
*.undo_tablespace='UNDOTBS1'
*.db_file_name_convert='+DATA/PRIMARY/','+DATA/STANDBY/'
*.log_file_name_convert='+FRA/PRIMARY/','+FRA/STANDBY/'
EOF

# Start standby instance in nomount mode
sudo -u oracle sqlplus / as sysdba
STARTUP NOMOUNT PFILE='/tmp/initSTANDBY.ora';
EXIT;

# Duplicate database using RMAN
sudo -u oracle rman

CONNECT TARGET sys/Oracle123@PRIMARY;
CONNECT AUXILIARY sys/Oracle123@STANDBY;

DUPLICATE TARGET DATABASE
  FOR STANDBY
  FROM ACTIVE DATABASE
  DORECOVER
  SPFILE
    SET db_unique_name='STANDBY'
    SET log_archive_dest_1='LOCATION=+FRA VALID_FOR=(ALL_LOGFILES,ALL_ROLES) DB_UNIQUE_NAME=STANDBY'
    SET log_archive_dest_2='SERVICE=PRIMARY LGWR ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=PRIMARY'
    SET fal_client='STANDBY'
    SET fal_server='PRIMARY'
  NOFILENAMECHECK;

EXIT;
```

### Start Data Guard Broker

```bash
# Enable Data Guard Broker on primary database
sudo -u oracle sqlplus / as sysdba

ALTER SYSTEM SET DG_BROKER_START=TRUE SCOPE=BOTH;
EXIT;

# Enable Data Guard Broker on standby database
sudo -u oracle sqlplus / as sysdba

ALTER SYSTEM SET DG_BROKER_START=TRUE SCOPE=BOTH;
EXIT;

# Configure Data Guard Broker
sudo -u oracle dgmgrl

CONNECT sys/Oracle123@PRIMARY;

CREATE CONFIGURATION 'DG_CONFIG' AS 
  PRIMARY DATABASE IS 'PRIMARY' 
  CONNECT IDENTIFIER IS PRIMARY;

ADD DATABASE 'STANDBY' AS 
  CONNECT IDENTIFIER IS STANDBY 
  MAINTAINED AS PHYSICAL;

ENABLE CONFIGURATION;

SHOW CONFIGURATION;

# Configure automatic failover
EDIT DATABASE 'STANDBY' SET PROPERTY 'FastStartFailoverTarget'='PRIMARY';
EDIT DATABASE 'PRIMARY' SET PROPERTY 'FastStartFailoverTarget'='STANDBY';

# Enable fast-start failover (optional)
ENABLE FAST_START FAILOVER CONDITION "Corrupted Controlfile";
ENABLE FAST_START FAILOVER CONDITION "Inaccessible Logfile";
ENABLE FAST_START FAILOVER CONDITION "Stuck Archiver";

EXIT;
```

### Data Guard Monitoring

```bash
# Create monitoring script
sudo -u oracle tee /u01/app/oracle/scripts/dg_monitor.sh << 'EOF'
#!/bin/bash

# Data Guard monitoring script

ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
PATH=$ORACLE_HOME/bin:$PATH
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE=/u01/app/oracle/admin/dg_monitor.log

echo "[$TIMESTAMP] Data Guard Status Check" >> $LOG_FILE

# Check configuration status
dgmgrl -silent sys/Oracle123@PRIMARY << 'DGMGRL_EOF' >> $LOG_FILE 2>&1
SHOW CONFIGURATION;
SHOW DATABASE 'PRIMARY';
SHOW DATABASE 'STANDBY';
DGMGRL_EOF

# Check apply lag
sqlplus -s / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT 'Apply Lag: ' || TO_CHAR(EXTRACT(DAY FROM applied_scn_time_lag)*24*60 + 
       EXTRACT(HOUR FROM applied_scn_time_lag)*60 + 
       EXTRACT(MINUTE FROM applied_scn_time_lag), '999.9') || ' minutes'
FROM gv$dataguard_stats WHERE name = 'apply lag';

SELECT 'Transport Lag: ' || TO_CHAR(EXTRACT(DAY FROM datum_time_lag)*24*60 + 
       EXTRACT(HOUR FROM datum_time_lag)*60 + 
       EXTRACT(MINUTE FROM datum_time_lag), '999.9') || ' minutes'
FROM gv$dataguard_stats WHERE name = 'transport lag';
SQL_EOF

echo "[$TIMESTAMP] Data Guard check completed" >> $LOG_FILE
echo "" >> $LOG_FILE
EOF

chmod +x /u01/app/oracle/scripts/dg_monitor.sh

# Add to crontab for regular monitoring
(crontab -u oracle -l 2>/dev/null; echo "*/5 * * * * /u01/app/oracle/scripts/dg_monitor.sh") | crontab -u oracle -
```

[Back to top](#table-of-contents)

## Database Creation

### Single Instance Database Creation

```bash
# Using DBCA (GUI)
sudo -u oracle dbca

# Using DBCA (Silent Mode)
sudo -u oracle dbca -silent -createDatabase \
    -templateName General_Purpose.dbc \
    -gdbname ORCL -sid ORCL \
    -responseFile NO_VALUE \
    -characterSet AL32UTF8 \
    -nationalCharacterSet AL16UTF16 \
    -sysPassword Oracle123 \
    -systemPassword Oracle123 \
    -createAsContainerDatabase true \
    -numberOfPDBs 1 \
    -pdbName ORCLPDB1 \
    -pdbAdminPassword Oracle123 \
    -databaseType MULTIPURPOSE \
    -memoryMgmtType auto_smp \
    -totalMemory 4096 \
    -storageType FS \
    -datafileDestination /u01/app/oracle/oradata \
    -redoLogFileSize 100 \
    -recoveryAreaDestination /u01/app/oracle/fast_recovery_area \
    -recoveryAreaSize 8192 \
    -enableArchive true \
    -emConfiguration NONE

# Verify database creation
sudo -u oracle sqlplus / as sysdba
SELECT name, open_mode FROM v$database;
SHOW PDBS;
```

### Custom Database Creation Script

```bash
# Create custom database creation script
sudo -u oracle tee /u01/app/oracle/scripts/create_db.sql << 'EOF'
-- Custom Oracle 19c Database Creation Script

CREATE DATABASE ORCL
   USER SYS IDENTIFIED BY Oracle123
   USER SYSTEM IDENTIFIED BY Oracle123
   LOGFILE GROUP 1 ('/u01/app/oracle/oradata/ORCL/redo01.log') SIZE 100M BLOCKSIZE 512,
           GROUP 2 ('/u01/app/oracle/oradata/ORCL/redo02.log') SIZE 100M BLOCKSIZE 512,
           GROUP 3 ('/u01/app/oracle/oradata/ORCL/redo03.log') SIZE 100M BLOCKSIZE 512
   MAXLOGFILES 16
   MAXLOGMEMBERS 3
   MAXLOGHISTORY 1816
   MAXDATAFILES 1024
   MAXINSTANCES 8
   CHARACTER SET AL32UTF8
   NATIONAL CHARACTER SET AL16UTF16
   DATAFILE '/u01/app/oracle/oradata/ORCL/system01.dbf' SIZE 700M REUSE AUTOEXTEND ON NEXT 10240K MAXSIZE UNLIMITED
   EXTENT MANAGEMENT LOCAL
   SYSAUX DATAFILE '/u01/app/oracle/oradata/ORCL/sysaux01.dbf' SIZE 550M REUSE AUTOEXTEND ON NEXT 10240K MAXSIZE UNLIMITED
   DEFAULT TABLESPACE users
      DATAFILE '/u01/app/oracle/oradata/ORCL/users01.dbf' SIZE 500M REUSE AUTOEXTEND ON MAXSIZE UNLIMITED
   DEFAULT TEMPORARY TABLESPACE tempts1
      TEMPFILE '/u01/app/oracle/oradata/ORCL/temp01.dbf' SIZE 20M REUSE AUTOEXTEND ON NEXT 640K MAXSIZE UNLIMITED
   UNDO TABLESPACE undotbs1
      DATAFILE '/u01/app/oracle/oradata/ORCL/undotbs01.dbf' SIZE 200M REUSE AUTOEXTEND ON NEXT 5120K MAXSIZE UNLIMITED;

-- Create additional tablespaces
CREATE TABLESPACE tools DATAFILE '/u01/app/oracle/oradata/ORCL/tools01.dbf' 
SIZE 100M AUTOEXTEND ON NEXT 10M MAXSIZE 1G;

-- Run catalog and catproc scripts
@?/rdbms/admin/catalog.sql
@?/rdbms/admin/catproc.sql

-- Connect as SYSTEM and run pupbld.sql
CONNECT system/Oracle123
@?/sqlplus/admin/pupbld.sql

-- Create SPFILE
CREATE SPFILE FROM PFILE;
EOF

# Create init.ora file
sudo -u oracle tee /u01/app/oracle/product/19.3.0/dbhome_1/dbs/initORCL.ora << 'EOF'
db_name='ORCL'
memory_target=4G
processes=300
audit_file_dest='/u01/app/oracle/admin/ORCL/adump'
audit_trail ='db'
db_block_size=8192
db_domain=''
db_recovery_file_dest='/u01/app/oracle/fast_recovery_area'
db_recovery_file_dest_size=8G
diagnostic_dest='/u01/app/oracle'
dispatchers='(PROTOCOL=TCP) (SERVICE=ORCLXDB)'
open_cursors=300
remote_login_passwordfile='EXCLUSIVE'
undo_tablespace='UNDOTBS1'
control_files=('/u01/app/oracle/oradata/ORCL/control01.ctl','/u01/app/oracle/fast_recovery_area/ORCL/control02.ctl')
compatible='19.0.0'
EOF
```

[Back to top](#table-of-contents)

## Post-Installation Configuration

### Database Configuration

```sql
-- Connect to database
sudo -u oracle sqlplus / as sysdba

-- Configure basic parameters
ALTER SYSTEM SET PROCESSES=500 SCOPE=SPFILE;
ALTER SYSTEM SET SESSIONS=555 SCOPE=SPFILE;
ALTER SYSTEM SET DB_CACHE_SIZE=1G SCOPE=SPFILE;
ALTER SYSTEM SET SHARED_POOL_SIZE=512M SCOPE=SPFILE;
ALTER SYSTEM SET LARGE_POOL_SIZE=64M SCOPE=SPFILE;
ALTER SYSTEM SET JAVA_POOL_SIZE=64M SCOPE=SPFILE;
ALTER SYSTEM SET PGA_AGGREGATE_TARGET=1G SCOPE=SPFILE;

-- Enable archiving
ALTER DATABASE ARCHIVELOG;

-- Configure FRA
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST='/u01/app/oracle/fast_recovery_area' SCOPE=BOTH;
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST_SIZE=8G SCOPE=BOTH;

-- Enable flashback database
ALTER DATABASE FLASHBACK ON;

-- Configure automatic workload repository (AWR)
EXEC DBMS_WORKLOAD_REPOSITORY.MODIFY_SNAPSHOT_SETTINGS(interval=>30, retention=>7*24*60);

-- Create additional undo tablespace for RAC
CREATE UNDO TABLESPACE UNDOTBS2 DATAFILE '/u01/app/oracle/oradata/ORCL/undotbs02.dbf' 
SIZE 200M AUTOEXTEND ON NEXT 5M MAXSIZE UNLIMITED;

-- Configure cluster parameters for RAC
ALTER SYSTEM SET CLUSTER_DATABASE=TRUE SCOPE=SPFILE;
ALTER SYSTEM SET CLUSTER_DATABASE_INSTANCES=2 SCOPE=SPFILE;
ALTER SYSTEM SET INSTANCE_NUMBER=1 SCOPE=SPFILE SID='ORCL1';
ALTER SYSTEM SET INSTANCE_NUMBER=2 SCOPE=SPFILE SID='ORCL2';
ALTER SYSTEM SET UNDO_TABLESPACE='UNDOTBS1' SCOPE=SPFILE SID='ORCL1';
ALTER SYSTEM SET UNDO_TABLESPACE='UNDOTBS2' SCOPE=SPFILE SID='ORCL2';
```

### Network Configuration

```bash
# Configure listener.ora
sudo -u oracle tee $ORACLE_HOME/network/admin/listener.ora << 'EOF'
LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (SID_NAME = PLSExtProc)
      (ORACLE_HOME = /u01/app/oracle/product/19.3.0/dbhome_1)
      (PROGRAM = extproc)
    )
    (SID_DESC =
      (GLOBAL_DBNAME = ORCL)
      (ORACLE_HOME = /u01/app/oracle/product/19.3.0/dbhome_1)
      (SID_NAME = ORCL)
    )
  )

ADR_BASE_LISTENER = /u01/app/oracle
EOF

# Configure tnsnames.ora
sudo -u oracle tee $ORACLE_HOME/network/admin/tnsnames.ora << 'EOF'
ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = ORCL)
    )
  )

ORCLPDB1 =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = ORCLPDB1)
    )
  )
EOF

# Start listener
sudo -u oracle lsnrctl start

# Check listener status
sudo -u oracle lsnrctl status
```

### Automatic Startup Configuration

```bash
# Configure automatic startup
sudo tee /etc/oratab << 'EOF'
ORCL:/u01/app/oracle/product/19.3.0/dbhome_1:Y
EOF

# Create startup script
sudo tee /etc/systemd/system/oracle.service << 'EOF'
[Unit]
Description=Oracle Database
After=network.target

[Service]
Type=forking
User=oracle
Group=oinstall
Environment="ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1"
Environment="ORACLE_SID=ORCL"
ExecStart=/u01/app/oracle/scripts/start_oracle.sh
ExecStop=/u01/app/oracle/scripts/stop_oracle.sh
TimeoutSec=300

[Install]
WantedBy=multi-user.target
EOF

# Create startup/shutdown scripts
sudo -u oracle mkdir -p /u01/app/oracle/scripts

sudo -u oracle tee /u01/app/oracle/scripts/start_oracle.sh << 'EOF'
#!/bin/bash
export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

# Start listener
lsnrctl start

# Start database
sqlplus / as sysdba << SQL_EOF
STARTUP;
EXIT;
SQL_EOF
EOF

sudo -u oracle tee /u01/app/oracle/scripts/stop_oracle.sh << 'EOF'
#!/bin/bash
export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

# Stop database
sqlplus / as sysdba << SQL_EOF
SHUTDOWN IMMEDIATE;
EXIT;
SQL_EOF

# Stop listener
lsnrctl stop
EOF

sudo chmod +x /u01/app/oracle/scripts/start_oracle.sh
sudo chmod +x /u01/app/oracle/scripts/stop_oracle.sh

# Enable and start service
sudo systemctl enable oracle
sudo systemctl start oracle
sudo systemctl status oracle
```

[Back to top](#table-of-contents)

## Security Configuration

### Database Security Setup

```sql
-- Connect as SYSDBA
sudo -u oracle sqlplus / as sysdba

-- Create application user
CREATE USER app_user IDENTIFIED BY AppUser123 
DEFAULT TABLESPACE users 
TEMPORARY TABLESPACE temp 
QUOTA UNLIMITED ON users;

GRANT CONNECT, RESOURCE TO app_user;
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO app_user;

-- Create DBA user
CREATE USER dba_user IDENTIFIED BY DbaUser123;
GRANT DBA TO dba_user;

-- Configure password profiles
CREATE PROFILE app_profile LIMIT
    SESSIONS_PER_USER 10
    IDLE_TIME 30
    CONNECT_TIME 120
    PASSWORD_LIFE_TIME 90
    PASSWORD_GRACE_TIME 7
    PASSWORD_REUSE_MAX 5
    PASSWORD_REUSE_TIME 365
    PASSWORD_VERIFY_FUNCTION ora_complexity_check
    FAILED_LOGIN_ATTEMPTS 3
    PASSWORD_LOCK_TIME 1/24;

ALTER USER app_user PROFILE app_profile;

-- Enable advanced security features
ALTER SYSTEM SET AUDIT_TRAIL=DB,EXTENDED SCOPE=SPFILE;
ALTER SYSTEM SET AUDIT_FILE_DEST='/u01/app/oracle/admin/ORCL/adump' SCOPE=SPFILE;

-- Configure Transparent Data Encryption (TDE)
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/u01/app/oracle/admin/ORCL/wallet' IDENTIFIED BY WalletPassword123;
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY WalletPassword123;
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY WalletPassword123 WITH BACKUP;

-- Configure SQL*Net encryption
ALTER SYSTEM SET SQLNET.ENCRYPTION_SERVER=REQUIRED SCOPE=SPFILE;
ALTER SYSTEM SET SQLNET.ENCRYPTION_TYPES_SERVER='(AES256, AES192, AES128)' SCOPE=SPFILE;
```

### Network Security Configuration

```bash
# Configure sqlnet.ora for security
sudo -u oracle tee $ORACLE_HOME/network/admin/sqlnet.ora << 'EOF'
# Network Security Configuration
SQLNET.AUTHENTICATION_SERVICES = (NTS)
SQLNET.ENCRYPTION_SERVER = REQUIRED
SQLNET.ENCRYPTION_TYPES_SERVER = (AES256, AES192, AES128)
SQLNET.CRYPTO_CHECKSUM_SERVER = REQUIRED
SQLNET.CRYPTO_CHECKSUM_TYPES_SERVER = (SHA256, SHA1)

# Connection timeout and security
SQLNET.INBOUND_CONNECT_TIMEOUT = 60
SQLNET.EXPIRE_TIME = 10

# TDE Wallet location
ENCRYPTION_WALLET_LOCATION = 
  (SOURCE = 
    (METHOD = FILE) 
    (METHOD_DATA = 
      (DIRECTORY = /u01/app/oracle/admin/ORCL/wallet)
    )
  )

# Security enhancements
SQLNET.ALLOWED_LOGON_VERSION_SERVER = 12
SQLNET.ALLOWED_LOGON_VERSION_CLIENT = 12
EOF
```

### Firewall Configuration

```bash
# Configure firewall for Oracle (RHEL/CentOS)
sudo firewall-cmd --permanent --add-port=1521/tcp
sudo firewall-cmd --permanent --add-port=5500/tcp
sudo firewall-cmd --reload

# For RAC additional ports
sudo firewall-cmd --permanent --add-port=3872/tcp    # Oracle Cluster Registry
sudo firewall-cmd --permanent --add-port=42424/tcp   # Grid Infrastructure Management Repository
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --reload

# Ubuntu firewall
sudo ufw allow 1521/tcp
sudo ufw allow 5500/tcp
```

[Back to top](#table-of-contents)

## Performance Tuning

### Memory Configuration

```sql
-- Memory tuning parameters
ALTER SYSTEM SET MEMORY_TARGET=0 SCOPE=SPFILE;
ALTER SYSTEM SET MEMORY_MAX_TARGET=0 SCOPE=SPFILE;
ALTER SYSTEM SET SGA_TARGET=3G SCOPE=SPFILE;
ALTER SYSTEM SET SGA_MAX_SIZE=3G SCOPE=SPFILE;
ALTER SYSTEM SET PGA_AGGREGATE_TARGET=1G SCOPE=SPFILE;

-- Buffer cache configuration
ALTER SYSTEM SET DB_CACHE_SIZE=2G SCOPE=SPFILE;
ALTER SYSTEM SET SHARED_POOL_SIZE=512M SCOPE=SPFILE;
ALTER SYSTEM SET LARGE_POOL_SIZE=128M SCOPE=SPFILE;
ALTER SYSTEM SET JAVA_POOL_SIZE=128M SCOPE=SPFILE;

-- Additional performance parameters
ALTER SYSTEM SET OPTIMIZER_MODE=ALL_ROWS SCOPE=BOTH;
ALTER SYSTEM SET OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES=TRUE SCOPE=BOTH;
ALTER SYSTEM SET CURSOR_SHARING=EXACT SCOPE=BOTH;
ALTER SYSTEM SET SESSION_CACHED_CURSORS=200 SCOPE=SPFILE;
ALTER SYSTEM SET OPEN_CURSORS=1000 SCOPE=SPFILE;
```

### Storage Optimization

```sql
-- Configure ASM for optimal performance
ALTER DISKGROUP DATA MOUNT;
ALTER DISKGROUP DATA SET ATTRIBUTE 'au_size'='4M';
ALTER DISKGROUP DATA SET ATTRIBUTE 'compatible.asm'='19.0.0';
ALTER DISKGROUP DATA SET ATTRIBUTE 'compatible.rdbms'='19.0.0';

-- Create performance-optimized tablespace
CREATE TABLESPACE perf_tbs 
DATAFILE '+DATA' SIZE 1G AUTOEXTEND ON NEXT 100M MAXSIZE 10G
EXTENT MANAGEMENT LOCAL 
SEGMENT SPACE MANAGEMENT AUTO;

-- Configure redo log sizing
ALTER DATABASE ADD LOGFILE GROUP 4 ('+DATA', '+FRA') SIZE 1G;
ALTER DATABASE ADD LOGFILE GROUP 5 ('+DATA', '+FRA') SIZE 1G;
ALTER DATABASE ADD LOGFILE GROUP 6 ('+DATA', '+FRA') SIZE 1G;
ALTER DATABASE DROP LOGFILE GROUP 1;
ALTER DATABASE DROP LOGFILE GROUP 2;
ALTER DATABASE DROP LOGFILE GROUP 3;
```

### Database Performance Monitoring

```bash
# Create performance monitoring script
sudo -u oracle tee /u01/app/oracle/scripts/perf_monitor.sh << 'EOF'
#!/bin/bash

ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
ORACLE_SID=ORCL
PATH=$ORACLE_HOME/bin:$PATH
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE=/u01/app/oracle/admin/perf_monitor.log

echo "[$TIMESTAMP] Performance Monitoring Report" >> $LOG_FILE

# Database performance metrics
sqlplus -s / as sysdba << 'SQL_EOF' >> $LOG_FILE
SET PAGESIZE 50 FEEDBACK OFF
SELECT 'Database Status: ' || status FROM v$instance;

SELECT 'Total Sessions: ' || COUNT(*) FROM v$session;
SELECT 'Active Sessions: ' || COUNT(*) FROM v$session WHERE status = 'ACTIVE';

SELECT 'Buffer Cache Hit Ratio: ' || 
       ROUND((1 - (phy.value / (db.value + cons.value))) * 100, 2) || '%'
FROM v$sysstat phy, v$sysstat db, v$sysstat cons
WHERE phy.name = 'physical reads'
AND db.name = 'db block gets'
AND cons.name = 'consistent gets';

SELECT 'Library Cache Hit Ratio: ' ||
       ROUND((1 - SUM(reloads) / SUM(pins)) * 100, 2) || '%'
FROM v$librarycache;

SELECT 'PGA Used: ' || ROUND(value/1024/1024, 2) || ' MB'
FROM v$pgastat WHERE name = 'total PGA allocated';

SELECT 'SGA Used: ' || ROUND(SUM(value)/1024/1024, 2) || ' MB'
FROM v$sga;

-- Top 5 wait events
SELECT 'Top Wait Events:'
FROM dual;

SELECT event, time_waited, total_waits
FROM (
  SELECT event, time_waited, total_waits
  FROM v$system_event
  WHERE event NOT IN ('SQL*Net message from client', 'rdbms ipc message', 'pmon timer', 'smon timer')
  ORDER BY time_waited DESC
)
WHERE ROWNUM <= 5;
SQL_EOF

echo "[$TIMESTAMP] Performance monitoring completed" >> $LOG_FILE
echo "" >> $LOG_FILE
EOF

chmod +x /u01/app/oracle/scripts/perf_monitor.sh

# Add to crontab
(crontab -u oracle -l 2>/dev/null; echo "*/15 * * * * /u01/app/oracle/scripts/perf_monitor.sh") | crontab -u oracle -
```

[Back to top](#table-of-contents)

## Backup and Recovery

### RMAN Configuration

```bash
# Configure RMAN for automated backups
sudo -u oracle rman target /

# Configure RMAN settings
CONFIGURE RETENTION POLICY TO REDUNDANCY 2;
CONFIGURE BACKUP OPTIMIZATION ON;
CONFIGURE DEFAULT DEVICE TYPE TO DISK;
CONFIGURE CHANNEL DEVICE TYPE DISK FORMAT '+FRA/%d_backup_%U';
CONFIGURE COMPRESSION ALGORITHM 'MEDIUM';
CONFIGURE DEVICE TYPE DISK PARALLELISM 2 BACKUP TYPE TO COMPRESSED BACKUPSET;
CONFIGURE ARCHIVELOG DELETION POLICY TO APPLIED ON ALL STANDBY;

# Configure control file autobackup
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '+FRA/controlfile_backup_%F';

EXIT;
```

### Automated Backup Scripts

```bash
# Create backup script directory
sudo -u oracle mkdir -p /u01/app/oracle/scripts/backup

# Level 0 backup script
sudo -u oracle tee /u01/app/oracle/scripts/backup/level0_backup.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE=/u01/app/oracle/admin/backup_level0_${TIMESTAMP}.log

rman target / << 'RMAN_EOF' > $LOG_FILE 2>&1
RUN {
  ALLOCATE CHANNEL c1 DEVICE TYPE DISK;
  ALLOCATE CHANNEL c2 DEVICE TYPE DISK;
  
  BACKUP INCREMENTAL LEVEL 0 DATABASE 
    FORMAT '+FRA/level0_backup_%d_%T_%s_%p'
    PLUS ARCHIVELOG
    FORMAT '+FRA/arch_backup_%d_%T_%s_%p';
    
  BACKUP CURRENT CONTROLFILE 
    FORMAT '+FRA/controlfile_%d_%T_%s_%p';
    
  RELEASE CHANNEL c1;
  RELEASE CHANNEL c2;
}

DELETE NOPROMPT OBSOLETE;
DELETE NOPROMPT EXPIRED BACKUP;

CROSSCHECK BACKUP;
CROSSCHECK ARCHIVELOG ALL;
RMAN_EOF

# Check backup status
if [ $? -eq 0 ]; then
    echo "Level 0 backup completed successfully" >> $LOG_FILE
else
    echo "Level 0 backup failed" >> $LOG_FILE
    # Send alert (configure mail system first)
    # echo "RMAN Level 0 backup failed on $(hostname)" | mail -s "Backup Alert" admin@company.com
fi
EOF

# Level 1 backup script
sudo -u oracle tee /u01/app/oracle/scripts/backup/level1_backup.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE=/u01/app/oracle/admin/backup_level1_${TIMESTAMP}.log

rman target / << 'RMAN_EOF' > $LOG_FILE 2>&1
RUN {
  ALLOCATE CHANNEL c1 DEVICE TYPE DISK;
  
  BACKUP INCREMENTAL LEVEL 1 DATABASE 
    FORMAT '+FRA/level1_backup_%d_%T_%s_%p'
    PLUS ARCHIVELOG
    FORMAT '+FRA/arch_backup_%d_%T_%s_%p';
    
  RELEASE CHANNEL c1;
}

DELETE NOPROMPT OBSOLETE;
CROSSCHECK BACKUP;
RMAN_EOF

if [ $? -eq 0 ]; then
    echo "Level 1 backup completed successfully" >> $LOG_FILE
else
    echo "Level 1 backup failed" >> $LOG_FILE
fi
EOF

# Archive log backup script
sudo -u oracle tee /u01/app/oracle/scripts/backup/archlog_backup.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE=/u01/app/oracle/admin/archlog_backup_${TIMESTAMP}.log

rman target / << 'RMAN_EOF' > $LOG_FILE 2>&1
RUN {
  ALLOCATE CHANNEL c1 DEVICE TYPE DISK;
  
  BACKUP ARCHIVELOG ALL 
    FORMAT '+FRA/arch_backup_%d_%T_%s_%p'
    DELETE INPUT;
    
  RELEASE CHANNEL c1;
}

CROSSCHECK ARCHIVELOG ALL;
DELETE NOPROMPT EXPIRED ARCHIVELOG ALL;
RMAN_EOF

if [ $? -eq 0 ]; then
    echo "Archive log backup completed successfully" >> $LOG_FILE
else
    echo "Archive log backup failed" >> $LOG_FILE
fi
EOF

# Make scripts executable
chmod +x /u01/app/oracle/scripts/backup/*.sh

# Schedule backups with cron
sudo -u oracle crontab -e
# Add these lines:
# 0 2 * * 0 /u01/app/oracle/scripts/backup/level0_backup.sh
# 0 2 * * 1-6 /u01/app/oracle/scripts/backup/level1_backup.sh  
# 0 */4 * * * /u01/app/oracle/scripts/backup/archlog_backup.sh
```

### Recovery Testing

```bash
# Create recovery test script
sudo -u oracle tee /u01/app/oracle/scripts/recovery_test.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE=/u01/app/oracle/admin/recovery_test_${TIMESTAMP}.log

echo "Starting recovery test at $TIMESTAMP" > $LOG_FILE

# Create test tablespace and table
sqlplus / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
CREATE TABLESPACE recovery_test 
DATAFILE '+DATA' SIZE 100M AUTOEXTEND ON;

CREATE TABLE recovery_test.test_recovery (
    id NUMBER PRIMARY KEY,
    test_data VARCHAR2(100),
    created_date DATE DEFAULT SYSDATE
);

INSERT INTO recovery_test.test_recovery VALUES (1, 'Before backup', SYSDATE);
COMMIT;

-- Force checkpoint
ALTER SYSTEM CHECKPOINT;
SQL_EOF

# Take backup
rman target / << 'RMAN_EOF' >> $LOG_FILE 2>&1
BACKUP TABLESPACE recovery_test FORMAT '+FRA/recovery_test_%U';
RMAN_EOF

# Insert more data
sqlplus / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
INSERT INTO recovery_test.test_recovery VALUES (2, 'After backup', SYSDATE);
COMMIT;
ALTER SYSTEM SWITCH LOGFILE;
SQL_EOF

# Simulate failure by taking tablespace offline
sqlplus / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
ALTER TABLESPACE recovery_test OFFLINE IMMEDIATE;
SQL_EOF

# Perform recovery
rman target / << 'RMAN_EOF' >> $LOG_FILE 2>&1
RESTORE TABLESPACE recovery_test;
RECOVER TABLESPACE recovery_test;
RMAN_EOF

# Bring tablespace online and verify data
sqlplus / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
ALTER TABLESPACE recovery_test ONLINE;

SELECT * FROM recovery_test.test_recovery;

-- Cleanup
DROP TABLE recovery_test.test_recovery;
DROP TABLESPACE recovery_test INCLUDING CONTENTS AND DATAFILES;
SQL_EOF

echo "Recovery test completed at $(date '+%Y%m%d_%H%M%S')" >> $LOG_FILE
EOF

chmod +x /u01/app/oracle/scripts/recovery_test.sh
```

[Back to top](#table-of-contents)

## Monitoring and Maintenance

### Database Health Monitoring

```bash
# Create comprehensive health check script
sudo -u oracle tee /u01/app/oracle/scripts/health_check.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE=/u01/app/oracle/admin/health_check.log
ALERT_EMAIL="dba@company.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_message() {
    local level=$1
    local message=$2
    echo -e "${level}[$TIMESTAMP] $message${NC}"
    echo "[$TIMESTAMP] $message" >> $LOG_FILE
}

# Check database availability
check_database_status() {
    local status=$(sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT status FROM v$instance;
SQL_EOF
)
    
    if [[ "$status" == "OPEN" ]]; then
        log_message $GREEN "✓ Database is OPEN and available"
        return 0
    else
        log_message $RED "✗ Database is not available (Status: $status)"
        return 1
    fi
}

# Check tablespace usage
check_tablespace_usage() {
    local max_usage=85
    
    sqlplus -s / as sysdba << 'SQL_EOF' > /tmp/tablespace_usage.tmp
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT tablespace_name || '|' || ROUND(used_percent, 2) AS usage_info
FROM dba_tablespace_usage_metrics
WHERE used_percent > 85;
SQL_EOF
    
    if [[ -s /tmp/tablespace_usage.tmp ]]; then
        log_message $YELLOW "⚠ High tablespace usage detected:"
        while IFS='|' read -r tbs usage; do
            log_message $YELLOW "  $tbs: ${usage}% used"
        done < /tmp/tablespace_usage.tmp
        rm -f /tmp/tablespace_usage.tmp
        return 1
    else
        log_message $GREEN "✓ All tablespaces within normal usage limits"
        rm -f /tmp/tablespace_usage.tmp
        return 0
    fi
}

# Check ASM disk group usage
check_asm_usage() {
    if [[ -n "$GRID_HOME" ]]; then
        export ORACLE_HOME=$GRID_HOME
        local asm_status=$(sqlplus -s / as sysasm << 'SQL_EOF'
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT name || '|' || ROUND((total_mb - free_mb) / total_mb * 100, 2) AS usage_info
FROM v$asm_diskgroup
WHERE ROUND((total_mb - free_mb) / total_mb * 100, 2) > 85;
SQL_EOF
)
        
        if [[ -n "$asm_status" ]]; then
            log_message $YELLOW "⚠ High ASM disk group usage:"
            echo "$asm_status" | while IFS='|' read -r dg usage; do
                log_message $YELLOW "  $dg: ${usage}% used"
            done
            return 1
        else
            log_message $GREEN "✓ All ASM disk groups within normal usage"
            return 0
        fi
        export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
    fi
}

# Check alert log for errors
check_alert_log() {
    local error_count=$(tail -1000 $ORACLE_BASE/diag/rdbms/$(echo $ORACLE_SID | tr '[:upper:]' '[:lower:]')/$ORACLE_SID/trace/alert_$ORACLE_SID.log | grep -i "ORA-" | grep -v "ORA-00000" | wc -l)
    
    if [[ $error_count -gt 0 ]]; then
        log_message $YELLOW "⚠ Found $error_count ORA errors in recent alert log entries"
        return 1
    else
        log_message $GREEN "✓ No critical errors in alert log"
        return 0
    fi
}

# Check backup status
check_backup_status() {
    local days_since_backup=$(sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT TRUNC(SYSDATE - MAX(completion_time))
FROM v$rman_backup_job_details
WHERE status = 'COMPLETED' AND input_type = 'DB FULL';
SQL_EOF
)
    
    if [[ $days_since_backup -gt 7 ]]; then
        log_message $YELLOW "⚠ Last full backup was $days_since_backup days ago"
        return 1
    else
        log_message $GREEN "✓ Recent backup available (${days_since_backup} days ago)"
        return 0
    fi
}

# Check Data Guard status (if configured)
check_dataguard_status() {
    local dg_status=$(sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT COUNT(*) FROM v$archive_dest WHERE status = 'VALID' AND target = 'STANDBY';
SQL_EOF
)
    
    if [[ $dg_status -gt 0 ]]; then
        local lag=$(sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 0 FEEDBACK OFF HEADING OFF
SELECT EXTRACT(DAY FROM applied_scn_time_lag)*24*60 + 
       EXTRACT(HOUR FROM applied_scn_time_lag)*60 + 
       EXTRACT(MINUTE FROM applied_scn_time_lag)
FROM gv$dataguard_stats WHERE name = 'apply lag' AND ROWNUM = 1;
SQL_EOF
)
        
        if [[ $(echo "$lag > 30" | bc -l) -eq 1 ]]; then
            log_message $YELLOW "⚠ Data Guard apply lag is ${lag} minutes"
            return 1
        else
            log_message $GREEN "✓ Data Guard is synchronized (lag: ${lag} minutes)"
            return 0
        fi
    else
        log_message $GREEN "✓ Data Guard not configured (single instance)"
        return 0
    fi
}

# Main health check execution
main() {
    log_message $NC "Starting Oracle Database health check..."
    
    local failed_checks=0
    
    check_database_status || ((failed_checks++))
    check_tablespace_usage || ((failed_checks++))
    check_asm_usage || ((failed_checks++))
    check_alert_log || ((failed_checks++))
    check_backup_status || ((failed_checks++))
    check_dataguard_status || ((failed_checks++))
    
    if [[ $failed_checks -eq 0 ]]; then
        log_message $GREEN "✓ All health checks passed"
        exit 0
    else
        log_message $RED "✗ $failed_checks health check(s) failed"
        # Send alert email (configure mail system first)
        # echo "Oracle Database health check failed on $(hostname). Check $LOG_FILE for details." | mail -s "Oracle Health Alert" $ALERT_EMAIL
        exit 1
    fi
}

main
EOF

chmod +x /u01/app/oracle/scripts/health_check.sh
```

### Automatic Maintenance Tasks

```bash
# Create maintenance script
sudo -u oracle tee /u01/app/oracle/scripts/maintenance.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE=/u01/app/oracle/admin/maintenance.log

echo "[$TIMESTAMP] Starting Oracle maintenance tasks" >> $LOG_FILE

# Update optimizer statistics
sqlplus / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
-- Gather dictionary stats
EXEC DBMS_STATS.GATHER_DICTIONARY_STATS(cascade=>TRUE);

-- Gather fixed object stats
EXEC DBMS_STATS.GATHER_FIXED_OBJECTS_STATS();

-- Gather system stats
EXEC DBMS_STATS.GATHER_SYSTEM_STATS('START');
EXEC DBMS_UTIL.DB_VERSION(version,compatibility);
EXEC DBMS_STATS.GATHER_SYSTEM_STATS('STOP');

-- Update schema statistics
EXEC DBMS_STATS.GATHER_SCHEMA_STATS(ownname=>'APP_USER', cascade=>TRUE, degree=>4);
SQL_EOF

# Rebuild fragmented indexes
sqlplus / as sysdba << 'SQL_EOF' >> $LOG_FILE 2>&1
DECLARE
    v_sql VARCHAR2(4000);
BEGIN
    FOR rec IN (
        SELECT owner, index_name
        FROM dba_indexes
        WHERE owner NOT IN ('SYS', 'SYSTEM', 'SYSAUX', 'DBSNMP', 'OUTLN', 'CTXSYS', 'XDB')
        AND index_type = 'NORMAL'
        AND status = 'VALID'
    ) LOOP
        BEGIN
            v_sql := 'ALTER INDEX ' || rec.owner || '.' || rec.index_name || ' REBUILD ONLINE';
            EXECUTE IMMEDIATE v_sql;
            DBMS_OUTPUT.PUT_LINE('Rebuilt index: ' || rec.owner || '.' || rec.index_name);
        EXCEPTION
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('Failed to rebuild: ' || rec.owner || '.' || rec.index_name || ' - ' || SQLERRM);
        END;
    END LOOP;
END;
/
SQL_EOF

# Clean up old audit files (older than 30 days)
find /u01/app/oracle/admin/*/adump -name "*.aud" -mtime +30 -delete 2>> $LOG_FILE

# Clean up old trace files (older than 7 days)
find $ORACLE_BASE/diag -name "*.trc" -mtime +7 -delete 2>> $LOG_FILE
find $ORACLE_BASE/diag -name "*.trm" -mtime +7 -delete 2>> $LOG_FILE

echo "[$TIMESTAMP] Oracle maintenance tasks completed" >> $LOG_FILE
EOF

chmod +x /u01/app/oracle/scripts/maintenance.sh
```

### Monitoring with Enterprise Manager (Optional)

```bash
# Install Oracle Enterprise Manager Database Express
sqlplus / as sysdba << 'SQL_EOF'
-- Configure Database Express
EXEC DBMS_XDB_CONFIG.SETHTTPSPORT(5500);

-- Enable Database Express
ALTER USER HR IDENTIFIED BY hr ACCOUNT UNLOCK;

-- Check HTTPS port
SELECT DBMS_XDB_CONFIG.GETHTTPSPORT() FROM DUAL;
SQL_EOF

# Access Database Express at: https://hostname:5500/em
```

[Back to top](#table-of-contents)

## High Availability Best Practices

### RAC Best Practices

```bash
# RAC-specific configuration script
sudo -u oracle tee /u01/app/oracle/scripts/rac_optimization.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL1  # Run on first node
export PATH=$ORACLE_HOME/bin:$PATH

# Configure RAC-optimized parameters
sqlplus / as sysdba << 'SQL_EOF'
-- Cluster-specific parameters
ALTER SYSTEM SET CLUSTER_INTERCONNECTS='192.168.1.10:192.168.1.11' SCOPE=SPFILE;
ALTER SYSTEM SET GCS_SERVER_PROCESSES=4 SCOPE=SPFILE;
ALTER SYSTEM SET PARALLEL_EXECUTION_MESSAGE_SIZE=16384 SCOPE=SPFILE;

-- Cache Fusion optimization
ALTER SYSTEM SET DML_LOCKS=10000 SCOPE=SPFILE;
ALTER SYSTEM SET ENQUEUE_RESOURCES=32000 SCOPE=SPFILE;
ALTER SYSTEM SET PROCESSES=1000 SCOPE=SPFILE;

-- Memory optimization for RAC
ALTER SYSTEM SET SGA_TARGET=4G SCOPE=SPFILE;
ALTER SYSTEM SET PGA_AGGREGATE_TARGET=2G SCOPE=SPFILE;

-- Archive destination for both nodes
ALTER SYSTEM SET LOG_ARCHIVE_DEST_1='LOCATION=+FRA' SCOPE=BOTH;

-- Enable automatic workload management
ALTER SYSTEM SET PARALLEL_ADAPTIVE_MULTI_USER=TRUE SCOPE=BOTH;
ALTER SYSTEM SET PARALLEL_SERVERS_TARGET=32 SCOPE=BOTH;
SQL_EOF

echo "RAC optimization parameters applied. Restart required."
EOF

chmod +x /u01/app/oracle/scripts/rac_optimization.sh
```

### Data Guard Best Practices

```bash
# Data Guard optimization script
sudo -u oracle tee /u01/app/oracle/scripts/dg_optimization.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

# Optimize Data Guard performance
sqlplus / as sysdba << 'SQL_EOF'
-- Network optimization
ALTER SYSTEM SET TCP.SEND_BUF_SIZE=1048576 SCOPE=BOTH;
ALTER SYSTEM SET TCP.RECV_BUF_SIZE=1048576 SCOPE=BOTH;

-- Archive process optimization
ALTER SYSTEM SET LOG_ARCHIVE_MAX_PROCESSES=8 SCOPE=BOTH;
ALTER SYSTEM SET LOG_ARCHIVE_MIN_SUCCEED_DEST=1 SCOPE=BOTH;

-- Standby database optimization
ALTER SYSTEM SET DB_WRITER_PROCESSES=4 SCOPE=SPFILE;
ALTER SYSTEM SET LOG_PARALLELISM=4 SCOPE=SPFILE;

-- Configure compression for network transmission
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=STANDBY LGWR ASYNC COMPRESSION=ENABLE VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=STANDBY' SCOPE=BOTH;

-- Enable real-time query on standby
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE USING CURRENT LOGFILE DISCONNECT FROM SESSION;
SQL_EOF

echo "Data Guard optimization completed"
EOF

chmod +x /u01/app/oracle/scripts/dg_optimization.sh
```

### Automatic Failover Configuration

```bash
# Configure automatic failover for Data Guard
sudo -u oracle tee /u01/app/oracle/scripts/setup_fast_start_failover.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export PATH=$ORACLE_HOME/bin:$PATH

# Configure Fast-Start Failover using Data Guard Broker
dgmgrl << 'DGMGRL_EOF'
CONNECT sys/Oracle123@PRIMARY;

-- Configure failover conditions
EDIT CONFIGURATION SET PROPERTY 'FastStartFailoverThreshold'=30;
EDIT CONFIGURATION SET PROPERTY 'FastStartFailoverLagLimit'=30;
EDIT CONFIGURATION SET PROPERTY 'CommunicationTimeout'=180;
EDIT CONFIGURATION SET PROPERTY 'NetTimeout'=30;
EDIT CONFIGURATION SET PROPERTY 'FastStartFailoverAutoReinstate'=TRUE;

-- Enable observer
START OBSERVER;

-- Enable fast-start failover
ENABLE FAST_START FAILOVER;

SHOW CONFIGURATION;
SHOW FAST_START FAILOVER;

EXIT;
DGMGRL_EOF

echo "Fast-Start Failover configuration completed"
EOF

chmod +x /u01/app/oracle/scripts/setup_fast_start_failover.sh
```

[Back to top](#table-of-contents)

## Troubleshooting

### Common Installation Issues

**Issue: ORA-00845: MEMORY_TARGET not supported**
```bash
# Check shared memory size
df -h /dev/shm

# Increase shared memory if needed
sudo mount -t tmpfs tmpfs /dev/shm -o size=4g

# Make permanent in /etc/fstab
echo "tmpfs /dev/shm tmpfs size=4g 0 0" | sudo tee -a /etc/fstab
```

**Issue: Grid Infrastructure installation fails**
```bash
# Check cluster verification
cd $GRID_HOME
./runcluvfy.sh stage -pre crsinst -n node1,node2

# Fix common issues
sudo systemctl stop firewalld
sudo systemctl disable firewalld

# Check time synchronization
sudo systemctl start chronyd
sudo systemctl enable chronyd
```

**Issue: ASM disk discovery problems**
```bash
# Check ASM disk permissions
ls -la /dev/asm-*

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Test ASM disk discovery
sudo -u grid sqlplus / as sysasm
SELECT path FROM v$asm_disk WHERE path LIKE '/dev/asm%';
```

### Performance Troubleshooting

```sql
-- Check for blocking sessions
SELECT 
    s1.sid AS blocking_sid,
    s1.serial# AS blocking_serial,
    s1.username AS blocking_user,
    s1.machine AS blocking_machine,
    s2.sid AS blocked_sid,
    s2.serial# AS blocked_serial,
    s2.username AS blocked_user,
    s2.machine AS blocked_machine,
    s2.seconds_in_wait,
    s2.event
FROM v$session s1, v$session s2
WHERE s1.sid = s2.blocking_session
ORDER BY s2.seconds_in_wait DESC;

-- Check top SQL by CPU usage
SELECT sql_id, child_number, plan_hash_value,
       executions, cpu_time/1000000 as cpu_seconds,
       elapsed_time/1000000 as elapsed_seconds,
       buffer_gets, disk_reads
FROM v$sql
WHERE cpu_time > 1000000
ORDER BY cpu_time DESC;

-- Check wait events
SELECT event, total_waits, total_timeouts, time_waited,
       average_wait, time_waited_micro
FROM v$system_event
WHERE wait_class != 'Idle'
ORDER BY time_waited DESC;
```

### RAC Troubleshooting

```bash
# Check cluster status
sudo -u grid crsctl stat res -t

# Check voting disk
sudo -u grid crsctl query css votedisk

# Check OCR status
sudo -u grid ocrcheck

# Check cluster interconnect
sudo -u grid oifcfg getif

# Check RAC database status
sudo -u oracle srvctl status database -d RACDB
sudo -u oracle srvctl config database -d RACDB

# Check cluster synchronization services
sudo -u grid crsctl check css
sudo -u grid crsctl check crs
sudo -u grid crsctl check evm
```

### Data Guard Troubleshooting

```bash
# Check Data Guard status
dgmgrl sys/Oracle123@PRIMARY "SHOW CONFIGURATION"
dgmgrl sys/Oracle123@PRIMARY "SHOW DATABASE VERBOSE PRIMARY"
dgmgrl sys/Oracle123@PRIMARY "SHOW DATABASE VERBOSE STANDBY"

# Check archive gap
sqlplus sys/Oracle123@PRIMARY as sysdba << 'SQL_EOF'
SELECT thread#, low_sequence#, high_sequence#
FROM v$archive_gap;
SQL_EOF

# Check apply lag
sqlplus sys/Oracle123@STANDBY as sysdba << 'SQL_EOF'
SELECT EXTRACT(DAY FROM applied_scn_time_lag)*24*60 + 
       EXTRACT(HOUR FROM applied_scn_time_lag)*60 + 
       EXTRACT(MINUTE FROM applied_scn_time_lag) AS apply_lag_minutes
FROM gv$dataguard_stats WHERE name = 'apply lag';
SQL_EOF

# Manual log apply (if needed)
sqlplus sys/Oracle123@STANDBY as sysdba << 'SQL_EOF'
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE CANCEL;
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE USING CURRENT LOGFILE DISCONNECT FROM SESSION;
SQL_EOF
```

### Log Analysis Scripts

```bash
# Create log analysis script
sudo -u oracle tee /u01/app/oracle/scripts/analyze_logs.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

ALERT_LOG=$ORACLE_BASE/diag/rdbms/$(echo $ORACLE_SID | tr '[:upper:]' '[:lower:]')/$ORACLE_SID/trace/alert_$ORACLE_SID.log
TIMESTAMP=$(date '+%Y-%m-%d')

echo "Oracle Log Analysis Report - $TIMESTAMP"
echo "======================================"

# Check for errors in alert log
echo -e "\n1. Recent Errors in Alert Log:"
tail -1000 $ALERT_LOG | grep -i "ORA-" | tail -10

# Check for deadlocks
echo -e "\n2. Recent Deadlocks:"
tail -5000 $ALERT_LOG | grep -A 20 -B 5 "deadlock"

# Check for checkpoint issues
echo -e "\n3. Checkpoint Information:"
tail -1000 $ALERT_LOG | grep -i "checkpoint"

# Check tablespace issues
echo -e "\n4. Tablespace Issues:"
sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 50
SELECT tablespace_name, status, contents
FROM dba_tablespaces
WHERE status != 'ONLINE';
SQL_EOF

# Check invalid objects
echo -e "\n5. Invalid Database Objects:"
sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 50
SELECT owner, object_name, object_type, status
FROM dba_objects
WHERE status != 'VALID'
AND owner NOT IN ('SYS', 'SYSTEM', 'PUBLIC');
SQL_EOF

echo -e "\nLog analysis completed."
EOF

chmod +x /u01/app/oracle/scripts/analyze_logs.sh
```

[Back to top](#table-of-contents)

## Final Configuration and Validation

### Complete System Validation

```bash
# Create comprehensive validation script
sudo -u oracle tee /u01/app/oracle/scripts/validate_installation.sh << 'EOF'
#!/bin/bash

export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
export ORACLE_SID=ORCL
export PATH=$ORACLE_HOME/bin:$PATH

echo "Oracle 19c Installation Validation"
echo "================================="

# Check Oracle software installation
echo -e "\n1. Oracle Software Version:"
sqlplus -v

# Check database status
echo -e "\n2. Database Status:"
sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 0 FEEDBACK OFF
SELECT 'Database Name: ' || name FROM v$database;
SELECT 'Database Status: ' || status FROM v$instance;
SELECT 'Archive Mode: ' || log_mode FROM v$database;
SELECT 'Database Role: ' || database_role FROM v$database;
SQL_EOF

# Check tablespaces
echo -e "\n3. Tablespace Status:"
sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 20 FEEDBACK OFF
COL tablespace_name FORMAT A20
COL status FORMAT A10
COL contents FORMAT A10
SELECT tablespace_name, status, contents FROM dba_tablespaces;
SQL_EOF

# Check listener status
echo -e "\n4. Listener Status:"
lsnrctl status

# Check scheduled jobs (if any)
echo -e "\n5. Scheduled Jobs:"
sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 10 FEEDBACK OFF
SELECT job_name, state, last_start_date, next_run_date
FROM dba_scheduler_jobs
WHERE owner = 'SYS' AND enabled = 'TRUE';
SQL_EOF

# Check Data Guard configuration (if applicable)
echo -e "\n6. Data Guard Configuration:"
sqlplus -s / as sysdba << 'SQL_EOF'
SET PAGESIZE 10 FEEDBACK OFF
SELECT dest_id, status, destination, error FROM v$archive_dest WHERE status != 'INACTIVE';
SQL_EOF

# For RAC installations
if [[ -n "$GRID_HOME" ]]; then
    echo -e "\n7. Cluster Status:"
    export ORACLE_HOME=$GRID_HOME
    crsctl stat res -t | head -20
    export ORACLE_HOME=/u01/app/oracle/product/19.3.0/dbhome_1
fi

echo -e "\nValidation completed successfully!"
EOF

chmod +x /u01/app/oracle/scripts/validate_installation.sh

# Run validation
sudo -u oracle /u01/app/oracle/scripts/validate_installation.sh
```

### Cron Job Setup for All Scripts

```bash
# Setup all cron jobs for oracle user
sudo -u oracle tee /tmp/oracle_crontab << 'EOF'
# Oracle Database Automated Tasks

# Health checks every 15 minutes
*/15 * * * * /u01/app/oracle/scripts/health_check.sh >/dev/null 2>&1

# Performance monitoring every 15 minutes
*/15 * * * * /u01/app/oracle/scripts/perf_monitor.sh >/dev/null 2>&1

# Archive log backup every 4 hours
0 */4 * * * /u01/app/oracle/scripts/backup/archlog_backup.sh >/dev/null 2>&1

# Level 1 backup daily (Monday-Saturday)
0 2 * * 1-6 /u01/app/oracle/scripts/backup/level1_backup.sh >/dev/null 2>&1

# Level 0 backup weekly (Sunday)
0 2 * * 0 /u01/app/oracle/scripts/backup/level0_backup.sh >/dev/null 2>&1

# Maintenance tasks weekly (Sunday)
0 4 * * 0 /u01/app/oracle/scripts/maintenance.sh >/dev/null 2>&1

# Data Guard monitoring (if configured) every 5 minutes
*/5 * * * * /u01/app/oracle/scripts/dg_monitor.sh >/dev/null 2>&1

# Recovery test monthly (first Sunday)
0 6 1-7 * 0 /u01/app/oracle/scripts/recovery_test.sh >/dev/null 2>&1

# Log analysis daily
0 8 * * * /u01/app/oracle/scripts/analyze_logs.sh >/dev/null 2>&1
EOF

# Install cron jobs
sudo -u oracle crontab /tmp/oracle_crontab

# Verify cron jobs
sudo -u oracle crontab -l
```

[Back to top](#table-of-contents)

## Documentation and Best Practices Summary

### Production Checklist

- [ ] Hardware requirements verified
- [ ] Operating system configured with required packages
- [ ] Oracle users and groups created
- [ ] Shared storage configured (for RAC)
- [ ] Network configuration completed
- [ ] Grid Infrastructure installed and configured
- [ ] Oracle Database software installed
- [ ] Database created and configured
- [ ] Security implemented (TDE, profiles, auditing)
- [ ] Backup strategy implemented and tested
- [ ] Data Guard configured (if required)
- [ ] Monitoring scripts deployed
- [ ] Performance tuning applied
- [ ] Automated maintenance scheduled
- [ ] Documentation completed

### Key Configuration Files

```bash
# Important Oracle configuration files
/u01/app/oracle/product/19.3.0/dbhome_1/network/admin/listener.ora
/u01/app/oracle/product/19.3.0/dbhome_1/network/admin/tnsnames.ora
/u01/app/oracle/product/19.3.0/dbhome_1/network/admin/sqlnet.ora
/u01/app/oracle/product/19.3.0/dbhome_1/dbs/spfileORCL.ora
/etc/oratab
/etc/security/limits.conf
/etc/sysctl.conf
```

This comprehensive guide provides a complete installation and configuration framework for Oracle Database 19c with high availability features including RAC and Data Guard. Regular monitoring, maintenance, and testing ensure optimal database performance and availability.

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
