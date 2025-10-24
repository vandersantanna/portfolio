<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# SQL Server for Database Reliability Engineering
*From baselines and error budgets to AG failovers—secure, observable, automatable.*

## Table of Contents
- [1. Executive Summary](#1-executive-summary)
- [2. Role Scope & Value Proposition](#2-role-scope--value-proposition)
- [3. Skills Matrix](#3-skills-matrix)
  - [3.1 Core DBRE Competencies](#31-core-dbre-competencies)
  - [3.2 SQL Server Stack](#32-sql-server-stack)
  - [3.3 Platform & Tooling](#33-platform--tooling)
- [4. Reference Architecture & Environments](#4-reference-architecture--environments)
  - [4.1 Topologies](#41-topologies)
  - [4.2 Cloud & Hybrid (Azure/On-prem/Arc)](#42-cloud--hybrid-azureon-premarc)
  - [4.3 Data Flows & Serving Layers](#43-data-flows--serving-layers)
- [5. Reliability Engineering Fundamentals](#5-reliability-engineering-fundamentals)
  - [5.1 SLOs, SLIs, SLAs](#51-slos-slis-slas)
  - [5.2 Error Budgets & Risk](#52-error-budgets--risk)
  - [5.3 Incident Lifecycle & Postmortems](#53-incident-lifecycle--postmortems)
- [6. Observability & Monitoring](#6-observability--monitoring)
  - [6.1 Metrics, DMVs & Dashboards](#61-metrics-dmvs--dashboards)
  - [6.2 Extended Events, Query Store & Profiling](#62-extended-events-query-store--profiling)
  - [6.3 Logging, Alerting & On-Call Hygiene](#63-logging-alerting--on-call-hygiene)
- [7. Capacity Planning & Performance Engineering](#7-capacity-planning--performance-engineering)
  - [7.1 Baselines & Benchmarking](#71-baselines--benchmarking)
  - [7.2 Query & Schema Tuning](#72-query--schema-tuning)
  - [7.3 Resource, IO & TempDB Optimization](#73-resource-io--tempdb-optimization)
- [8. High Availability & Disaster Recovery](#8-high-availability--disaster-recovery)
  - [8.1 Always On Availability Groups](#81-always-on-availability-groups)
  - [8.2 Failover Cluster Instances (FCI)](#82-failover-cluster-instances-fci)
  - [8.3 Log Shipping, Replication & DR Testing](#83-log-shipping-replication--dr-testing)
- [9. Security, Compliance & Governance](#9-security-compliance--governance)
  - [9.1 Identity & Access (RBAC)](#91-identity--access-rbac)
  - [9.2 Encryption & Secrets](#92-encryption--secrets)
  - [9.3 Auditing, Data Privacy & Masking](#93-auditing-data-privacy--masking)
- [10. Change Management & Release Engineering](#10-change-management--release-engineering)
  - [10.1 GitOps & Infrastructure as Code](#101-gitops--infrastructure-as-code)
  - [10.2 Database CI/CD](#102-database-cicd)
  - [10.3 Safe Deployment Patterns](#103-safe-deployment-patterns)
- [11. Automation & Runbooks](#11-automation--runbooks)
  - [11.1 Provisioning, Patching & Upgrades](#111-provisioning-patching--upgrades)
  - [11.2 Health Checks & Self-Healing](#112-health-checks--self-healing)
  - [11.3 Operational Playbooks](#113-operational-playbooks)
- [12. Data Integration & Replication](#12-data-integration--replication)
  - [12.1 Change Data Capture/Tracking & ETL/ELT](#121-change-data-capturetracking--etlelt)
  - [12.2 Cross-DB & Heterogeneous Replication](#122-cross-db--heterogeneous-replication)
  - [12.3 Streaming & Analytics](#123-streaming--analytics)
- [13. Cost & Efficiency Engineering](#13-cost--efficiency-engineering)
  - [13.1 Licensing & Editions](#131-licensing--editions)
  - [13.2 Right-Sizing & Scaling](#132-right-sizing--scaling)
  - [13.3 Storage & Networking Economics](#133-storage--networking-economics)
- [14. Reliability Case Studies](#14-reliability-case-studies)
- [15. KPIs, Dashboards & Reporting](#15-kpis-dashboards--reporting)
- [16. Standards & Conventions](#16-standards--conventions)
- [17. Roadmap & Continuous Improvement](#17-roadmap--continuous-improvement)
- [18. Appendices & Templates](#18-appendices--templates)
  - [A. Scripts & Snippets (T-SQL, PowerShell)](#a-scripts--snippets-t-sql-powershell)
  - [B. IaC (Bicep/Terraform) & Config](#b-iac-bicepterraform--config)
  - [C. CI/CD Pipelines (GitHub Actions/Azure DevOps)](#c-cicd-pipelines-github-actionsazure-devops)
  - [D. Runbook Templates](#d-runbook-templates)
  - [E. Checklists](#e-checklists)
  - [F. Diagrams (Mermaid)](#f-diagrams-mermaid)
  - [G. Glossary](#g-glossary)

---

## 1. Executive Summary
I design and operate reliable, secure, performant, and cost-efficient **SQL Server** platforms across on-prem, Azure, and hybrid environments. My DBRE practice turns business goals into **SLOs** measured via deep **observability**, delivered safely with **CI/CD**, and protected by **HA/DR** tested routinely with verifiable **RPO/RTO**.

## 2. Role Scope & Value Proposition
- **Scope:** OLTP/Analytics/HTAP workloads; SQL Server 2017–2022, Azure SQL DB/MI; Windows/Linux.
- **Interfaces:** App teams, SRE/Platform, SecOps, Data Eng, Architecture, Leadership.
- **Value:** Translate user-centric SLOs into architecture, automation, and guardrails that cut incidents, accelerate recovery, and stabilize performance.

## 3. Skills Matrix

### 3.1 Core DBRE Competencies
- SLI/SLO/SLA design, error budgets, risk registers, operational excellence.
- Incident response, blameless postmortems, chaos/DR drills, toil elimination.
- Observability (DMVs/XE/PerfMon/Azure Monitor), performance modeling, capacity planning.

### 3.2 SQL Server Stack
- **HA/DR:** Always On AGs (sync/async/read-scale), FCI, log shipping, replication.
- **Perf:** Query Store, IQP, Columnstore, In-Memory OLTP, Resource Governor.
- **Ops:** Backup/restore (full/diff/log, stripes), DBCC CHECKDB, TempDB best practices.

### 3.3 Platform & Tooling
- **Infra:** WSFC, systemd on Linux, storage layout (data/log/temp), NUMA/CPU affinity.
- **Cloud:** Azure SQL DB/MI/VM, Arc-enabled SQL MI; networking with Private Link/VNET/ER.
- **Automation:** PowerShell/dbatools, Ansible (Windows/Linux), Terraform/Bicep.
- **Pipelines:** GitHub Actions, Azure DevOps; DACPAC/SqlPackage, Flyway/Liquibase.
- **Secrets:** Azure Key Vault, Managed Identity, Kerberos/AD/AAD.

---

## 4. Reference Architecture & Environments

### 4.1 Topologies
- **Standalone + DR:** Simple prim-sec via log shipping or async AG.
- **AG for HA/Scale-out:** Sync commit in site for HA + async secondaries for DR/reads.
- **FCI:** Instance-level HA on shared storage (S2D/SAN) with AGs for read scale-out.
- **PaaS:** Azure SQL DB/MI (Hyperscale, Serverless) when managed features fit.

### 4.2 Cloud & Hybrid (Azure/On-prem/Arc)
- Hub-and-spoke; Private Link/Endpoints; ExpressRoute; centralized Key Vault.
- Azure Arc for governance of on-prem/other clouds (policy, updates, inventory).

### 4.3 Data Flows & Serving Layers
OLTP → CDC/CT → ETL/ELT (SSIS/ADF/Fabric) → Lake/Warehouse → BI/ML.  
Freshness & latency SLOs bound batch windows and read-replica lag.

---

## 5. Reliability Engineering Fundamentals

### 5.1 SLOs, SLIs, SLAs
- **SLIs (examples):** p99 read latency < 40 ms; commit latency < 120 ms; error rate < 0.1%; AG sync redo queue < 100 MB; async replica **redo** & **send** queues within targets; restore test time ≤ 20 min.
- **SLOs:** Tier-1 service DB monthly availability 99.95% with p99 read latency < 40 ms.

~~~yaml
# SLO policy (documentation-as-code)
service: orders-sql
slos:
  - name: p99_read_latency_ms
    target: "< 40"
    window: 30d
  - name: ag_async_lag_seconds
    target: "<= 5"
    window: 30d
burn_policies:
  - if_burn_rate: "> 2.0x"   # fast burn
    action: "freeze risky changes; open reliability epic"
~~~

### 5.2 Error Budgets & Risk
- Track consumption; gate features when burning; risk register (prob×impact) with owners and due dates.

### 5.3 Incident Lifecycle & Postmortems
Detect → Triage → Mitigate → Recover → Review.  
Runbooks per alert, postmortems with actionable items, due dates, and follow-through.

---

## 6. Observability & Monitoring

### 6.1 Metrics, DMVs & Dashboards
- **Waits/Perf:** `sys.dm_os_wait_stats`, `sys.dm_exec_query_stats`, `sys.dm_io_virtual_file_stats`.
- **IO:** file latency MB/s, stalls; **AG:** `sys.dm_hadr_*` redo/send queues & health.
- **Dashboards:** SLO compliance, top waits, AG lag, backup/restore, CHECKDB compliance.

~~~sql
-- Top queries by CPU in last hour
SELECT TOP(20)
  qs.sql_handle,
  qs.plan_handle,
  DB_NAME(st.dbid) AS dbname,
  (qs.total_worker_time/NULLIF(qs.execution_count,0))/1000 AS avg_cpu_ms,
  qs.total_worker_time/1000 AS total_cpu_ms,
  qs.execution_count,
  SUBSTRING(st.text, (qs.statement_start_offset/2)+1,
    ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(st.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS stmt_text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
WHERE qs.last_execution_time > DATEADD(HOUR,-1,GETDATE())
ORDER BY total_cpu_ms DESC;
~~~

~~~sql
-- File IO latency per database file
SELECT DB_NAME(mf.database_id) AS dbname, mf.name, vfs.num_of_reads, vfs.io_stall_read_ms,
       CASE WHEN vfs.num_of_reads = 0 THEN 0 ELSE vfs.io_stall_read_ms / vfs.num_of_reads END AS read_ms,
       vfs.num_of_writes, vfs.io_stall_write_ms,
       CASE WHEN vfs.num_of_writes = 0 THEN 0 ELSE vfs.io_stall_write_ms / vfs.num_of_writes END AS write_ms
FROM sys.dm_io_virtual_file_stats(NULL,NULL) vfs
JOIN sys.master_files mf ON vfs.database_id = mf.database_id AND vfs.file_id = mf.file_id
ORDER BY read_ms DESC, write_ms DESC;
~~~

### 6.2 Extended Events, Query Store & Profiling
- **XE:** targeted tracing without heavy overhead.
- **Query Store:** plan history, regressions, forcing, RCSI interactions.
- **SQL Monitor equivalents:** leverage QDS runtime stats, tracked queries.

~~~sql
-- Enable Query Store with capture policy
ALTER DATABASE Sales SET QUERY_STORE = ON;
ALTER DATABASE Sales SET QUERY_STORE (OPERATION_MODE = READ_WRITE, DATA_FLUSH_INTERVAL_SECONDS = 900, MAX_STORAGE_SIZE_MB = 4096, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30));
-- Force a known-good plan for a regressing query
DECLARE @q UNIQUEIDENTIFIER = (SELECT TOP 1 query_id FROM sys.query_store_queries ORDER BY last_execution_time DESC);
DECLARE @p BIGINT = (SELECT TOP 1 plan_id FROM sys.query_store_plan WHERE query_id=@q ORDER BY avg_duration ASC);
EXEC sp_query_store_force_plan @q, @p;
~~~

~~~sql
-- Extended Events session for long-running queries (>2s)
CREATE EVENT SESSION [long_queries] ON SERVER
ADD EVENT sqlserver.rpc_completed(
    ACTION(sqlserver.database_name,sqlserver.sql_text)
    WHERE (duration>2000000)),
ADD EVENT sqlserver.sql_batch_completed(
    ACTION(sqlserver.database_name,sqlserver.sql_text)
    WHERE (duration>2000000))
ADD TARGET package0.ring_buffer
WITH (MAX_MEMORY=64MB,EVENT_RETENTION_MODE=ALLOW_SINGLE_EVENT_LOSS,MAX_DISPATCH_LATENCY=5 SECONDS);
ALTER EVENT SESSION [long_queries] ON SERVER STATE = START;
~~~

### 6.3 Logging, Alerting & On-Call Hygiene
- Centralize to **Azure Monitor/Log Analytics** or ELK; actionable alerts with runbook links; paging for Sev-1/2, tickets for Sev-3.
- Reduce noise: aggregate, dedupe, and add **correlation IDs** from application layer.

~~~sql
-- Example: alertable condition (AG replica not synchronized)
SELECT ag.name, ars.role_desc, ars.synchronization_health_desc
FROM sys.availability_groups ag
JOIN sys.dm_hadr_availability_replica_states ars ON ag.group_id = ars.group_id
WHERE ars.synchronization_health_desc <> 'HEALTHY';
~~~

---

## 7. Capacity Planning & Performance Engineering

### 7.1 Baselines & Benchmarking
- Establish steady-state baselines; use **HammerDB** or TPC-like workloads.
- Forecast CPU/IOPS/memory/log throughput; maintain headroom policies (e.g., ≥30%).

~~~powershell
# HammerDB CLI (tcl) driver example (illustrative)
hammerdbcli <<'TCL'
dbset db mssqlserver
diset tpcc mssql_server  "db-prim"
diset tpcc mssql_windows_auth true
diset tpcc mssql_driver timed
diset tpcc mssql_duration 900
vuset vu 64
buildschema
runtimer
TCL
~~~

### 7.2 Query & Schema Tuning
- Index strategy: clustered vs nonclustered, filtered indexes, included columns.
- Stats: auto update/async; manual refresh on big loads.
- Partitioning & compression (row/page/columnstore) for large tables.

~~~sql
-- Missing index candidates (use with care, validate!)
SELECT TOP 20
  migs.avg_total_user_cost * (migs.avg_user_impact/100.0) * (migs.user_seeks + migs.user_scans) AS improvement,
  mid.statement, mid.equality_columns, mid.inequality_columns, mid.included_columns
FROM sys.dm_db_missing_index_group_stats migs
JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
ORDER BY improvement DESC;
~~~

~~~sql
-- Statistics maintenance (example)
UPDATE STATISTICS dbo.Orders WITH FULLSCAN;
-- Or adopt Ola Hallengren / custom jobs with sampling policies per table size.
~~~

### 7.3 Resource, IO & TempDB Optimization
- **Files:** multiple data files for TempDB; instant file initialization; pre-size to avoid autogrowth storms.
- Separate data/log; align autogrowth in **MB**; monitor VLF count.

~~~sql
-- Create 8 equally sized TempDB data files + pre-size log
USE [master];
ALTER DATABASE tempdb MODIFY FILE (NAME = tempdev, SIZE = 8192MB);
DECLARE @i INT = 2;
WHILE @i <= 8
BEGIN
  EXEC('ALTER DATABASE tempdb ADD FILE (NAME = tempdev' + CAST(@i AS VARCHAR(2)) + ', FILENAME = ''C:\SQLData\tempdb' + CAST(@i AS VARCHAR(2)) + '.ndf'', SIZE = 8192MB, FILEGROWTH = 1024MB)');
  SET @i += 1;
END
ALTER DATABASE tempdb MODIFY FILE (NAME = templog, SIZE = 4096MB, FILEGROWTH = 1024MB);
~~~

~~~powershell
# Enable Instant File Initialization (requires "Perform volume maintenance tasks")
Add-LocalGroupMember -Group "Perform volume maintenance tasks" -Member "NT SERVICE\MSSQLSERVER"
# Restart service afterward for effect
Restart-Service MSSQLSERVER
~~~

---

## 8. High Availability & Disaster Recovery

### 8.1 Always On Availability Groups
- **Design:** Sync commit for HA (automatic failover); async for DR (manual).
- **Routing:** Read-only routing to offload reads; set readable secondaries.
- **Quorum:** Dynamic quorum/witness; monitor lease timeouts; health checks.

~~~sql
-- Create AG (simplified; assumes endpoints, backups/restores done)
CREATE AVAILABILITY GROUP SalesAG
  WITH (AUTOMATED_BACKUP_PREFERENCE = SECONDARY)
  FOR DATABASE SalesDB
  REPLICA ON
    N'PRI-SQL' WITH (ENDPOINT_URL = 'TCP://pri-sql:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC, READ_ONLY_ROUTING_URL = 'TCP://pri-sql:1433'),
    N'SEC-SQL' WITH (ENDPOINT_URL = 'TCP://sec-sql:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC, READ_ONLY_ROUTING_URL = 'TCP://sec-sql:1433'),
    N'DR-SQL'  WITH (ENDPOINT_URL = 'TCP://dr-sql:5022',  AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL,    SEEDING_MODE = AUTOMATIC, READ_ONLY_ROUTING_URL = 'TCP://dr-sql:1433');
GO
ALTER AVAILABILITY GROUP SalesAG GRANT CREATE ANY DATABASE;
GO
-- Read-only routing list
ALTER AVAILABILITY GROUP SalesAG MODIFY REPLICA ON N'PRI-SQL' WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_LIST = (('SEC-SQL','DR-SQL'))));
ALTER AVAILABILITY GROUP SalesAG MODIFY REPLICA ON N'SEC-SQL' WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_LIST = (('PRI-SQL','DR-SQL'))));
~~~

~~~powershell
# dbatools: AG health & failover (manual example)
Install-Module dbatools -Scope CurrentUser -Force
Test-DbaAvailabilityGroup -SqlInstance PRI-SQL -AvailabilityGroup SalesAG
# Manual planned failover from primary to SEC-SQL
Switch-DbaAvailabilityGroup -SqlInstance PRI-SQL -AvailabilityGroup SalesAG -Secondary SEC-SQL -Confirm:$false
~~~

### 8.2 Failover Cluster Instances (FCI)
- **Use when:** need instance-level HA (including msdb/master), or shared storage.
- Combine **FCI + AG** for instance HA + read scaleouts.

### 8.3 Log Shipping, Replication & DR Testing
- **Log shipping:** simple, robust DR; tune copy/restore frequency.
- **Transactional replication:** selective table replication; validate latency & identity handling.
- **DR drills:** quarterly restore validation; record RTO/RPO.

~~~sql
-- Log shipping (outline)
-- 1) Full backup on primary
BACKUP DATABASE SalesDB TO DISK='\\share\SalesDB_full.bak' WITH INIT, COMPRESSION;
-- 2) Restore with NORECOVERY on secondary
RESTORE DATABASE SalesDB FROM DISK='\\share\SalesDB_full.bak' WITH NORECOVERY;
-- 3) Configure LS copy/restore jobs or use GUI/T-SQL procs (sp_add_log_shipping_*)
~~~

---

## 9. Security, Compliance & Governance

### 9.1 Identity & Access (RBAC)
- Integrate with AD/AAD; use contained users for DB-scoped auth where needed.
- Break-glass accounts with MFA; rotate secrets; least privilege roles.

~~~sql
-- Least-privilege read role
CREATE ROLE ro_analytics;
GRANT SELECT TO ro_analytics;
CREATE USER [bi_reader] FOR LOGIN [corp\bi_reader];
EXEC sp_addrolemember 'ro_analytics','bi_reader';
~~~

### 9.2 Encryption & Secrets
- **TDE** for at-rest; **TLS** for in-transit; **Always Encrypted** for client-side sensitive columns.
- Externalize secrets to **Key Vault**; use Managed Identity where possible.

~~~sql
-- Transparent Data Encryption (TDE) example
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Str0ng#Pass!';
CREATE CERTIFICATE MyServerCert WITH SUBJECT = 'DEK Cert';
USE SalesDB;
CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256 ENCRYPTION BY SERVER CERTIFICATE MyServerCert;
ALTER DATABASE SalesDB SET ENCRYPTION ON;
~~~

~~~sql
-- Always Encrypted (simplified; keys typically created via SSMS/PowerShell)
-- Assumes column master key & column encryption key already exist
CREATE TABLE dbo.Customers(
  CustomerId INT IDENTITY PRIMARY KEY,
  SSN CHAR(11) COLLATE Latin1_General_BIN2 ENCRYPTED WITH (COLUMN_ENCRYPTION_KEY = CEK1, ENCRYPTION_TYPE = DETERMINISTIC, ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256') NOT NULL,
  Name NVARCHAR(100) NOT NULL
);
~~~

### 9.3 Auditing, Data Privacy & Masking
- SQL Auditing → Log Analytics/Storage; **RLS** & **DDM**; classification & labeling; GDPR/LGPD processes.

~~~sql
-- SQL Server Audit to file (illustrative)
CREATE SERVER AUDIT AuditToFile TO FILE (FILEPATH = 'D:\SQLAudit\', MAXSIZE = 1 GB, MAX_ROLLOVER_FILES = 20);
ALTER SERVER AUDIT AuditToFile WITH (STATE = ON);
CREATE DATABASE AUDIT SPECIFICATION AuditSelects FOR SERVER AUDIT AuditToFile
ADD (SELECT ON OBJECT::dbo.Customers BY PUBLIC)
WITH (STATE = ON);
~~~

---

## 10. Change Management & Release Engineering

### 10.1 GitOps & Infrastructure as Code
- Provision SQL VMs/MI/DB with **Bicep/Terraform**; enforce **policy-as-code**; detect drift.

### 10.2 Database CI/CD
- **DACPAC** (SqlPackage/DacFx) or **Flyway/Liquibase** migrations.
- Pre-deploy checks: blockers (long TX, schema locks), drift diffs, smoke tests.
- Auto-rollback: reverse scripts or point-in-time restore (PITR) for PaaS.

~~~powershell
# DACPAC deploy (SqlPackage)
SqlPackage.exe /Action:Publish /SourceFile: .\db\SalesDB.dacpac `
  /TargetConnectionString:"Server=tcp:db-prim,1433;Database=SalesDB;Integrated Security=true;" `
  /p:BlockOnPossibleDataLoss=true /p:DropObjectsNotInSource=false /p:CommandTimeout=1200
~~~

~~~properties
# Flyway conf (SQL Server)
flyway.url=jdbc:sqlserver://db-prim:1433;databaseName=SalesDB;encrypt=true;trustServerCertificate=true
flyway.user=app_migrator
flyway.password=${APP_MIGRATOR_PWD}
flyway.locations=filesystem:./db/migrations
flyway.baselineOnMigrate=true
flyway.outOfOrder=false
~~~

~~~sql
-- V1__create_orders_table.sql
CREATE TABLE dbo.Orders(
  Id            INT IDENTITY PRIMARY KEY,
  CustomerId    INT NOT NULL,
  Status        VARCHAR(30) NOT NULL,
  CreatedAt     DATETIME2(3) DEFAULT SYSUTCDATETIME()
);
CREATE INDEX IX_Orders_Status ON dbo.Orders(Status);
~~~

### 10.3 Safe Deployment Patterns
- Blue/green schemas, canary cohorts, feature flags, shadow reads/writes; promotion gates tied to SLOs and error budget burn.

---

## 11. Automation & Runbooks

### 11.1 Provisioning, Patching & Upgrades
- Golden images, cumulative updates, AG/FCI rolling patching; rehearsal in lower envs.

~~~powershell
# dbatools: patching outline
Install-Module dbatools -Scope CurrentUser -Force
# Prechecks
Test-DbaBuild -ComputerName PRI-SQL
# Apply CU (example - verify package & version!)
Invoke-DbaSqlUpgrade -ComputerName PRI-SQL -Version 16 -Path \\share\SQL2022-CU.exe -Authentication Integrated
~~~

### 11.2 Health Checks & Self-Healing
- Daily/weekly health: backups, CHECKDB, job failures, AG state, disk space, VLF counts.
- Auto-remediation: restart stuck AG sync, expand TempDB, cycle error logs, reseed read replicas.

~~~powershell
# Health snapshot (dbatools)
$instance = "PRI-SQL"
Test-DbaMaxMemory -SqlInstance $instance
Test-DbaTempDbConfig -SqlInstance $instance
Test-DbaLastBackup -SqlInstance $instance | Where-Object {$_.Database -ne 'tempdb'}
Get-DbaAgReplica -SqlInstance $instance | Select-Object SqlInstance, AvailabilityGroup, Role, RollupSynchronizationState
~~~

### 11.3 Operational Playbooks
- Start/Stop instance; AG failover/switchover; backup validate; restore dry-run; capacity expansion; onboarding/offboarding; license audit.

---

## 12. Data Integration & Replication

### 12.1 Change Data Capture/Tracking & ETL/ELT
- **CDC** or **Change Tracking** per use case; idempotent loads; retries; watermarking.

~~~sql
-- Enable CDC on database and table
USE SalesDB;
EXEC sys.sp_cdc_enable_db;
EXEC sys.sp_cdc_enable_table @source_schema = N'dbo', @source_name = N'Orders', @role_name = N'cdc_reader', @supports_net_changes = 1;
-- Query changes for ETL
SELECT * FROM cdc.fn_cdc_get_all_changes_dbo_Orders (SYSUTCDATETIME()-1, SYSUTCDATETIME(), 'all');
~~~

### 12.2 Cross-DB & Heterogeneous Replication
- SQL Server ↔ PostgreSQL/MySQL/Snowflake/Fabric; map data types; ensure ordering & consistency; checksum validations.

### 12.3 Streaming & Analytics
- Event Hubs/Kafka ingestion; near-real-time dashboards; materialized aggregates with Columnstore; Synapse/Fabric for lakehouse patterns.

---

## 13. Cost & Efficiency Engineering

### 13.1 Licensing & Editions
- Enterprise vs Standard features; core licensing; passive replica rules; Software Assurance; Azure models (DTU/vCore), Reserved Capacity.

### 13.2 Right-Sizing & Scaling
- vCPU/memory/I/O sizing; Serverless/Hyperscale where fit; consolidation vs isolation; storage tier fit (Premium/Ultra).

### 13.3 Storage & Networking Economics
- Snapshots/retention policies; backup storage tiers; egress considerations; ExpressRoute utilization.

---

## 14. Reliability Case Studies
**Case A — AG Redesign Eliminates Failover Flaps**  
Issue: lease timeouts during spikes → Action: quorum tuning, NIC QoS, read routing, health probes → Result: no Sev-1 in 6 months, RTO < 30s.

**Case B — Query Store Stabilizes Plans**  
Issue: regressions after CU → Action: QDS baselines, plan forcing + targeted fixes → Result: p99 latency −45%, CFR −60%.

**Case C — DR with Log Shipping + PITR**  
Issue: budget-constrained DR → Action: striped backups, frequent log copy/restore, weekly restore tests → Result: RPO < 5 min, RTO 12 min.

---

## 15. KPIs, Dashboards & Reporting
- **Availability:** service-level, error budget burn; **Latency:** p50/p90/p99 reads/writes;  
- **Change:** deploy frequency, lead time, change failure rate; **Ops:** MTTR/MTTD, DR drill pass rate;  
- **Health:** CHECKDB compliance, backup success, AG lag; **Capacity:** headroom & forecasts.

~~~markdown
**Monthly Executive Summary (template)**
- Availability: 99.97% (SLO: 99.95%) ✅
- Error budget burn: 28% (policy < 50%)
- Incidents: Sev-1:0, Sev-2:1, Sev-3:4 (MTTR: 22m)
- Changes: 54 deploys, CFR: 2.9%
- DR: 1 drill passed, RTO 15m (target ≤ 20m)
- Risks: TempDB growth patterns (Q4 mitigation)
~~~

---

## 16. Standards & Conventions
- **Naming/Tagging:** `sql-{env}-{service}-{role}`, AG `ag_{svc}`, listener `lsn_{svc}`, DB `svc_{purpose}`.  
- **Docs:** ADRs, runbook format, code style (T-SQL/PowerShell); comment headers & change IDs.  
- **Git:** trunk-based or GitFlow; semantic versioning; signed commits; CODEOWNERS; approvals via CODEOWNERS rules.

---

## 17. Roadmap & Continuous Improvement
- **Q1:** SLO coverage 100% on tier-1; automate restore testing weekly.  
- **Q2:** Query Store on all DBs; drift detection; policy-as-code enforcement.  
- **Q3:** Observability rev-2 (XE → LA pipelines; traces); TempDB modernization.  
- **Q4:** Cost optimization phase-2; deprecate legacy runbooks; zero-touch patching pilot.

---

## 18. Appendices & Templates

### A. Scripts & Snippets (T-SQL, PowerShell)

~~~sql
-- AWR-like: Top wait classes (SQL Server style)
WITH w AS (
  SELECT wait_type, waiting_tasks_count, wait_time_ms - signal_wait_time_ms AS resource_wait_ms, signal_wait_time_ms
  FROM sys.dm_os_wait_stats
  WHERE wait_type NOT LIKE 'SLEEP%' AND wait_type NOT LIKE 'BROKER_TASK_STOP%' AND wait_type NOT LIKE 'XE_TIMER_EVENT%'
)
SELECT TOP 15 wait_type,
  waiting_tasks_count,
  resource_wait_ms/1000.0 AS resource_wait_s,
  signal_wait_time_ms/1000.0 AS signal_wait_s
FROM w
ORDER BY resource_wait_ms DESC;
~~~

~~~sql
-- CheckDB compliance in last 7 days
SELECT d.name AS database_name, MAX(hc.last_successful_checkdb) AS last_checkdb
FROM sys.databases d
OUTER APPLY (SELECT MAX(CASE WHEN [description] LIKE '%DBCC CHECKDB%' AND [message] LIKE '%completed%' THEN [start_time] END) AS last_successful_checkdb
             FROM msdb.dbo.sysjobhistory h
             JOIN msdb.dbo.sysjobs j ON h.job_id=j.job_id) hc
GROUP BY d.name;
~~~

~~~powershell
# dbatools backup validation (sample)
Get-DbaDatabase -SqlInstance PRI-SQL -ExcludeSystem | ForEach-Object {
  $db = $_.Name
  Backup-DbaDatabase -SqlInstance PRI-SQL -Database $db -Type Full -CompressBackup -CopyOnly -Verify
}
# Restore test to sandbox instance
Restore-DbaDatabase -SqlInstance LAB-SQL -Path \\share\backups\ -WithReplace -MaintenanceSolution
~~~

~~~powershell
# AG async lag metric (export to Prometheus textfile as example)
$lag = (Invoke-DbaQuery -SqlInstance SEC-SQL -Query "
  SELECT DATEDIFF(SECOND,last_commit_time,GETUTCDATE()) AS lag_s
  FROM sys.dm_hadr_database_replica_states WHERE is_primary_replica=0").lag_s
Set-Content -Path "C:\metrics\ag_lag.prom" -Value "sql_ag_async_lag_seconds $lag"
~~~

### B. IaC (Bicep/Terraform) & Config

~~~bicep
// Bicep: Azure SQL Server + DB with Private Endpoint (simplified)
param location string = resourceGroup().location
param sqlName string
param adminLogin string
@secure()
param adminPassword string

resource sql 'Microsoft.Sql/servers@2021-11-01' = {
  name: sqlName
  location: location
  properties: {
    administratorLogin: adminLogin
    administratorLoginPassword: adminPassword
    publicNetworkAccess: 'Disabled'
  }
}

resource db 'Microsoft.Sql/servers/databases@2022-05-01-preview' = {
  name: '${sql.name}/salesdb'
  properties: {
    zoneRedundant: true
    requestedServiceObjectiveName: 'GP_Gen5_4'
  }
}
~~~

~~~hcl
# Terraform (AzureRM): Managed Instance (illustrative)
provider "azurerm" { features {} }
resource "azurerm_mssql_managed_instance" "mi" {
  name                = "mi-sql-sales"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku_name            = "GP_Gen5"
  vcores              = 8
  storage_size_in_gb  = 512
  administrator_login = "sqladmin"
  administrator_login_password = var.admin_password
  license_type        = "BasePrice"
  timezone_id         = "UTC"
  collation           = "SQL_Latin1_General_CP1_CI_AS"
}
~~~

### C. CI/CD Pipelines (GitHub Actions/Azure DevOps)

~~~yaml
# GitHub Actions: DACPAC deploy with OIDC to Azure
name: dacpac-deploy
on:
  push: { paths: ["db/**.dacpac", ".github/workflows/dacpac.yml"] }
jobs:
  publish:
    runs-on: windows-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Azure login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      - name: Deploy DACPAC
        shell: pwsh
        run: |
          & "C:\Program Files\Microsoft SQL Server\160\DAC\bin\SqlPackage.exe" `
            /Action:Publish /SourceFile: .\db\SalesDB.dacpac `
            /TargetConnectionString:"Server=tcp:${{ vars.SQL_SERVER }},1433;Database=SalesDB;Authentication=Active Directory Default;" `
            /p:BlockOnPossibleDataLoss=true /p:DropObjectsNotInSource=false /p:CommandTimeout=1200
~~~

~~~yaml
# Azure DevOps: Multistage DB pipeline (excerpt)
stages:
- stage: Validate
  jobs:
  - job: LintAndDrift
    steps:
    - script: echo "Lint SQL, check drift with SqlPackage /a:DriftReport"
- stage: Migrate
  dependsOn: Validate
  jobs:
  - deployment: Flyway
    environment: prod
    strategy:
      runOnce:
        deploy:
          steps:
          - task: Bash@3
            inputs:
              targetType: 'inline'
              script: |
                curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.0.0/flyway-commandline-10.0.0-linux-x64.tar.gz | tar xz
                ./flyway-10.0.0/flyway -configFiles=db/flyway.conf migrate
~~~

### D. Runbook Templates

~~~markdown
# Runbook: Planned AG Switchover

## Preconditions
- Replicas synchronized; no active long transactions
- Backups healthy in last 24h; change freeze communicated

## Steps
1) Verify health:
   - `SELECT * FROM sys.dm_hadr_cluster_members;`
   - `SELECT synchronization_health_desc FROM sys.dm_hadr_availability_replica_states;`
2) Drain connections (if needed) from primary.
3) Initiate failover to SEC-SQL (PowerShell or SSMS).
4) Validate:
   - Listener resolves to new primary
   - Read-only routing still works
   - SLO probes pass
5) Resume jobs & unlock changes.

## Rollback
- Fail back using same procedure if validation fails.

## Post-actions
- Update runbook log; open postmortem if any deviations or errors occurred.
~~~

### E. Checklists

~~~markdown
## Patch Day Checklist
- [ ] Backups complete & verified
- [ ] Change window approved; stakeholders notified
- [ ] For AG/FCI: rolling patch plan validated
- [ ] Baseline captured (PerfMon, XE, QDS, screenshots)
- [ ] Post-patch validation (waits, Query Store regressions, SLO probes)

## DR Drill Checklist
- [ ] Restore last full/diff/log to clean instance
- [ ] Time the restore (RTO) and measure recovery point (RPO)
- [ ] Application smoke tests against restored DB
- [ ] Record results and deltas vs targets
~~~

### F. Diagrams (Mermaid)

~~~mermaid
flowchart LR
  subgraph Primary[Primary - AG Primary]
    A[App Clients] -->|Read/Write| LSN[AG Listener]
    LSN --> PDB[(SalesDB)]
  end
  LSN -.Read Only.-> RSEC[Readable Secondary]
  RSEC --> BI[Reporting/BI]
  PDB --> BAK[(Backups)]
  BAK --> DR[(DR Site - Async Secondary)]
  classDef strong fill:#eef,stroke:#66f,stroke-width:2px;
  class PDB,RSEC,DR strong;
~~~

### G. Glossary
- **DBRE** — Database Reliability Engineering  
- **SLA/SLO/SLI** — Agreement/Objectives/Indicators  
- **MTTR/MTTD** — Mean Time to Recover/Detect  
- **AG/FCI** — Availability Group / Failover Cluster Instance  
- **CDC/CT** — Change Data Capture / Change Tracking  
- **QDS** — Query Store  
- **RPO/RTO** — Recovery Point/Time Objective
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

