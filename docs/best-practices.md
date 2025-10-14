# Best Practices & Guidelines for Modern Data Platforms (DBA • DBRE • SRE • DataOps • Data Engineering • Data Science • Database Development)

> One-page, GitHub-ready reference for teams working with **Oracle, SQL Server, PostgreSQL, MySQL, MongoDB, Redis, DB2** across **AWS, Azure, GCP, OCI**. Focused on reliability, security, performance, cost, and automation.

---

## Table of Contents

- [1. Audience & Scope](#1-audience--scope)
- [2. Core Principles](#2-core-principles)
- [3. Architecture & Environment Matrix](#3-architecture--environment-matrix)
- [4. Security & Compliance](#4-security--compliance)
  - [4.1 Identity & Access](#41-identity--access)
  - [4.2 Network & Secrets](#42-network--secrets)
  - [4.3 Encryption (at rest & in transit)](#43-encryption-at-rest--in-transit)
  - [4.4 Auditing & Data Governance](#44-auditing--data-governance)
- [5. High Availability & Disaster Recovery](#5-high-availability--disaster-recovery)
- [6. Backup, Restore & DR Drills](#6-backup-restore--dr-drills)
- [7. Performance & Capacity Management](#7-performance--capacity-management)
- [8. Observability & Troubleshooting](#8-observability--troubleshooting)
- [9. Schema, Changes & Release Engineering](#9-schema-changes--release-engineering)
- [10. DataOps Essentials](#10-dataops-essentials)
- [11. Role-Specific Playbooks](#11-role-specific-playbooks)
  - [11.1 DBA](#111-dba)
  - [11.2 DBRE](#112-dbre)
  - [11.3 SRE](#113-sre)
  - [11.4 Data Engineer](#114-data-engineer)
  - [11.5 Data Scientist](#115-data-scientist)
  - [11.6 Database Developer](#116-database-developer)
- [12. Engine-Specific Guidelines](#12-engine-specific-guidelines)
  - [12.1 Oracle](#121-oracle)
  - [12.2 SQL Server](#122-sql-server)
  - [12.3 PostgreSQL](#123-postgresql)
  - [12.4 MySQL](#124-mysql)
  - [12.5 MongoDB](#125-mongodb)
  - [12.6 Redis](#126-redis)
  - [12.7 DB2](#127-db2)
- [13. Cloud-Specific Guidance](#13-cloud-specific-guidance)
  - [13.1 AWS](#131-aws)
  - [13.2 Azure](#132-azure)
  - [13.3 GCP](#133-gcp)
  - [13.4 OCI](#134-oci)
- [14. Cost Optimization](#14-cost-optimization)
- [15. Templates & Reusable Artifacts](#15-templates--reusable-artifacts)
- [16. Checklists](#16-checklists)
- [17. References & Further Reading](#17-references--further-reading)

---

## 1. Audience & Scope

- **Who**: DBA, DBRE, SRE, DataOps Engineers, Data Engineers, Data Scientists, and Database Developers.
- **What**: Common guidelines for operating, developing, and scaling data platforms spanning **transactional (OLTP)**, **analytical (OLAP/Lakehouse)**, and **streaming** workloads.
- **Where**: Hybrid/on-prem and **AWS, Azure, GCP, OCI**.
- **Why**: Consistent reliability, security, performance, and cost control with automation-first practices.

[Back to top](#table-of-contents)

---

## 2. Core Principles

1. **Security by default**: least privilege, encrypted everywhere, zero trust networking.
2. **Reliability as a feature**: SLOs/SLA, error budgets, tested failovers, game days.
3. **Automation > toil**: IaC/PaC, immutable infra, repeatable runbooks, GitOps.
4. **Observability-first**: metrics, logs, traces and actionable alerts (not noise).
5. **Change safely**: review gates, small batches, blue/green, canaries, rollbacks.
6. **Performance-conscious**: capacity plans, baselines, workload-aware tuning.
7. **Cost-aware**: right-size, autoscale, lifecycle policies, reserved/savings plans.
8. **Data governance**: lineage, quality tests, PII handling, retention, compliance.
9. **Documentation & ownership**: clear RACI, on-call, SOPs, postmortems, learnings.

[Back to top](#table-of-contents)

---

## 3. Architecture & Environment Matrix

| Layer | Options / Notes |
|---|---|
| **Compute** | VMs, Kubernetes, managed DB services (RDS/Aurora, Azure SQL, Cloud SQL, Autonomous/ExaCS), HPC nodes for ETL/ML. |
| **Storage** | SSD/NVMe for hot OLTP; object storage (S3/Blob/GCS/OCI) for backups, data lake; file shares for some engines/tools. |
| **Network** | Private subnets, SG/NSG/Firewall rules, peering, PrivateLink/Endpoints, WAF, Bastion/SSM Session Manager. |
| **Security** | Cloud KMS/HSM, Key Vault/Secrets Manager/Secret Manager; IAM/AAD; Vault/External Secrets in K8s. |
| **CI/CD** | GitHub Actions, GitLab CI, Azure DevOps, Jenkins; versioned migrations (Liquibase/Flyway/Alembic/SSDT). |
| **Observability** | CloudWatch, Azure Monitor, Cloud Logging/Monitoring, OCI Observability; Prometheus/Grafana; Engine-specific exporters. |
| **DR** | Cross-AZ/region replicas, snapshots, logs ship, object-store-based PITR; runbooks + drills. |

[Back to top](#table-of-contents)

---

## 4. Security & Compliance

### 4.1 Identity & Access
- **Principle of Least Privilege**: role-based, task-scoped, time-bound access.
- **Short-lived credentials** with Just-in-Time (JIT) elevation (PIM/Access Requests).
- **Separation of duties**: DBA vs Security vs Dev; CI/CD bots with constrained roles.
- **Use IAM roles/managed identities** for apps instead of embedded keys.

**Examples**
```bash
# AWS: Assume-role for automation (GitHub OIDC example)
aws sts assume-role-with-web-identity --role-arn arn:aws:iam::123:role/gha-rds-admin   --role-session-name gha --web-identity-token "$OIDC_TOKEN"
```

```bash
# Azure: Managed Identity to access Key Vault (VM/AKS pod identity)
az keyvault secret show --vault-name kv-prod --name "db-password"
```

### 4.2 Network & Secrets
- **Private-only endpoints** for databases; disallow public IP unless justified and gated.
- **TLS everywhere**, server cert rotation, client certs where supported.
- **Secrets**: store in **KMS/Key Vault/Secret Manager**; never in code or plain CI variables.
- **Bastion/SSM** instead of direct SSH/RDP; log all admin sessions.

```yaml
# Kubernetes: external-secrets (pull from cloud secret store)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: app-db-credentials }
spec:
  secretStoreRef: { name: prod-store, kind: ClusterSecretStore }
  target: { name: app-db-secret }
  data:
    - secretKey: DB_PASSWORD
      remoteRef: { key: prod/app-db/password }
```

### 4.3 Encryption (at rest & in transit)
- **At rest**: native TDE (Oracle/SQL Server), storage-level encryption, tablespace/filegroup encryption.
- **In transit**: enforce TLS 1.2+; pin CA or use managed trust.
- **Keys**: externalize to **KMS/HSM**; rotation policy; dual control for key ops.

Snippets (illustrative):

```sql
-- SQL Server TDE (at-rest) - simplified
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongPass!OnlyForExample';
CREATE CERTIFICATE TDECert WITH SUBJECT = 'TDE Cert';
CREATE DATABASE ENCRYPTION KEY
  WITH ALGORITHM = AES_256
  ENCRYPTION BY SERVER CERTIFICATE TDECert;
ALTER DATABASE MyDB SET ENCRYPTION ON;
```

```sql
-- Oracle (conceptual): wallet + TDE tablespace
-- Configure sqlnet.ora/wallet, then:
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "WalletPass";
ADMINISTER KEY MANAGEMENT SET ENCRYPTION KEY IDENTIFIED BY "WalletPass";
ALTER TABLESPACE USERS ENCRYPTION ONLINE USING 'AES256' ENCRYPT;
```

```bash
# PostgreSQL in-transit TLS (server)
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file  = 'server.key'
```

```ini
# MySQL in-transit TLS (my.cnf)
ssl_ca=/etc/mysql/ca.pem
ssl_cert=/etc/mysql/server-cert.pem
ssl_key=/etc/mysql/server-key.pem
```

```yaml
# MongoDB (mongod.conf)
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongo.pem
    CAFile: /etc/ssl/ca.pem
```

```conf
# Redis TLS + ACLs (redis.conf)
tls-port 6379
port 0
aclfile /etc/redis/users.acl
```

### 4.4 Auditing & Data Governance
- **Enable DB audit** for privileged ops and DDL; centralize logs.
- **Data classification** (PII, PCI, HIPAA, LGPD/GDPR tags).
- **Retention & deletion** policies; legal holds; masking/tokenization for non-prod.
- **Lineage** via Data Catalog/Atlas/OpenLineage; monitor **data quality** gates.

[Back to top](#table-of-contents)

---

## 5. High Availability & Disaster Recovery

- Define **SLOs** (availability, latency) and **RTO/RPO** targets by service tier.
- Use **multi-AZ** for HA; **cross-region** async replicas for DR.
- Prefer **managed** HA when feasible; test **automatic failover** and split-brain protections.

**Patterns by Engine**
- **Oracle**: RAC for HA, **Data Guard** (SYNC/ASYNC; FSFO) for DR.
- **SQL Server**: **Always On AG** (readable secondaries), sync across AZs.
- **PostgreSQL**: streaming replication + **Patroni/pg_auto_failover**; logical for migrations.
- **MySQL**: **InnoDB Cluster** / Group Replication; or Aurora MySQL.
- **MongoDB**: **Replica Sets** (odd number members); **Sharding** for scale.
- **Redis**: **Cluster** or Sentinel; watch quorum and persistence config.
- **DB2**: **HADR** + TSA; pureScale for cluster HA.

**DR Drills**
- Schedule **quarterly** failover/failback rehearsals with runbooks, success criteria, and postmortems.

[Back to top](#table-of-contents)

---

## 6. Backup, Restore & DR Drills

- **3-2-1** rule (3 copies, 2 media, 1 offsite/object store).
- Backups **encrypted**, tested, and **documented** (who/what/where/how/when).
- Keep **catalogs** off the database host; validate **restore time** against RTO.

**Snippets**
```bash
# Oracle RMAN (conceptual)
rman target /
BACKUP AS COMPRESSED BACKUPSET DATABASE PLUS ARCHIVELOG;
LIST BACKUP SUMMARY;
RESTORE DATABASE; RECOVER DATABASE;
```

```sql
-- SQL Server FULL + LOG
BACKUP DATABASE MyDB TO DISK = 's3://bucket/MyDB_full.bak' WITH COMPRESSION;
BACKUP LOG MyDB TO DISK = 's3://bucket/MyDB_log.trn';
```

```bash
# PostgreSQL (logical + base backups)
pg_dump -Fc -d appdb > appdb.dump
pg_basebackup -D /backups/base -Ft -X stream
# WAL archival with wal-g/wal-e recommended
```

```bash
# MySQL with Percona XtraBackup
xtrabackup --backup --target-dir=/backups/full --encrypt=AES256 --encrypt-key=...
xtrabackup --prepare --target-dir=/backups/full
```

```bash
# MongoDB
mongodump --archive=/backups/$(date +%F).gz --gzip --db appdb
mongorestore --archive=/backups/file.gz --gzip --nsInclude=appdb.*
```

```conf
# Redis persistence (choose one or both)
save 900 1
save 300 10
appendonly yes
```

```bash
# DB2
db2 BACKUP DATABASE APPDB TO /backups WITH 2 BUFFERS BUFFER 1024 PARALLELISM 4 COMPRESS
```

[Back to top](#table-of-contents)

---

## 7. Performance & Capacity Management

- Establish **baselines** (tps/qps, latency P50/P95/P99, CPU/mem/io).
- **Workload-aware** tuning (OLTP vs OLAP vs mixed).
- **Index hygiene**: missing vs unused; fragmentation; fill factor; partitioning.
- **Stats** freshness and plan stability (hints only if necessary).
- **Capacity plans**: growth models, autoscaling triggers, headroom policy (e.g., 30%).

**Quick Checks**
```sql
-- PostgreSQL: Top slow queries (pg_stat_statements)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements ORDER BY total_time DESC LIMIT 20;
```

```sql
-- SQL Server: Query store (if enabled)
SELECT TOP 20 qsqt.query_sql_text, rs.avg_duration, rs.count_executions
FROM sys.query_store_query_text qsqt
JOIN sys.query_store_query qsq ON qsq.query_text_id = qsqt.query_text_id
JOIN sys.query_store_runtime_stats rs ON rs.query_id = qsq.query_id
ORDER BY rs.avg_duration DESC;
```

```sql
-- MySQL: Slow queries (require slow_query_log=ON)
SHOW GLOBAL STATUS LIKE 'Slow_queries';
```

```sql
-- Oracle: AWR-ish sample (requires licenses/features)
SELECT * FROM dba_hist_sysmetric_summary WHERE metric_name LIKE '%Response%';
```

```bash
# MongoDB: index usage
db.collection.getIndexes()
db.collection.aggregate([{ $indexStats: {} }])
```

**Tuning Starters**
- **PostgreSQL**: `shared_buffers ~25% RAM`, `effective_cache_size ~50-75% RAM`, tune `work_mem`, `maintenance_work_mem`, enable `auto_explain`.
- **MySQL**: `innodb_buffer_pool_size` large; set `innodb_flush_log_at_trx_commit=1` for durability; enable slow log.
- **SQL Server**: configure **TempDB** files, `MAXDOP`, memory cap, **TF 1117/1118** (older versions), **Query Store**.
- **Oracle**: AWR/ASH, SGA/PGA sizing, Adaptive Features awareness, segment advisor.
- **MongoDB**: design for **working set in RAM**, compound indexes matching query patterns.
- **Redis**: choose `maxmemory-policy` (e.g., `allkeys-lru`), avoid big values; pipeline operations.

[Back to top](#table-of-contents)

---

## 8. Observability & Troubleshooting

- **Golden signals**: latency, traffic, errors, saturation.
- **DB metrics**: connections, cache hit ratio, lock waits, replication lag, checkpoint/write stalls.
- Centralize logs (JSON), **correlate** with traces (OpenTelemetry).
- Alerts with **actionable** playbooks and rate limiting to prevent alert fatigue.

**Prometheus Example**
```yaml
groups:
- name: db-alerts
  rules:
  - alert: PostgresReplicationLag
    expr: pg_replication_lag_seconds > 15
    for: 5m
    labels: { severity: page }
    annotations:
      summary: "Postgres replication lag > 15s"
      runbook: "https://runbooks.local/postgres/replication-lag"
```

[Back to top](#table-of-contents)

---

## 9. Schema, Changes & Release Engineering

- **Everything-as-code**: schema + reference data under VCS.
- **Migrations**: **Liquibase/Flyway** (RDBMS), **SSDT/DACPAC** (SQL Server), **Alembic** (SQLAlchemy).
- **Pre-prod** validation: shadow writes, replay, canary migrations, online DDL (pt-osc/gh-ost/Native Online).
- **Rollback** strategy: backward-compatible changes, feature flags, dual writes (if necessary).
- **Data contracts** between producers/consumers; versioned.

**GitHub Actions Example (Flyway)**
```yaml
name: db-migrations
on: [push]
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21' }
      - name: Run Flyway
        run: |
          ./flyway -url=jdbc:postgresql://db:5432/app -user=$USER -password=$PASS migrate
        env:
          USER: ${{ secrets.DB_USER }}
          PASS: ${{ secrets.DB_PASS }}
```

[Back to top](#table-of-contents)

---

## 10. DataOps Essentials

- **Pipelines**: orchestrate with Airflow/Dagster/Prefect; idempotent tasks; retries with jitter; lineage.
- **CDC**: Debezium/GoldenGate; define SLAs for end-to-end latency and freshness.
- **DQ checks**: Great Expectations/dbt tests; fail fast with clear remediation.
- **Lakehouse**: Iceberg/Delta/Hudi; ACID tables; schema evolution; Z-ordering/partitioning.
- **Streaming**: Kafka/Pulsar/MSK/Event Hubs; exactly-once where needed; backpressure handling.
- **ML Ops handoff**: curated features, reproducible datasets, model registry (MLflow/SageMaker), drift monitors.

[Back to top](#table-of-contents)

---

## 11. Role-Specific Playbooks

### 11.1 DBA
- **Daily**: backup status, replication lag, disk/archivelog usage, blocked sessions.
- **Weekly**: stats health, index maintenance (engine-appropriate), security review.
- **Monthly**: restore drills, parameter drift audit, capacity review.
- **Standards**: naming, RBAC roles, maintenance windows.

### 11.2 DBRE
- Define **SLOs**, error budgets; automate **game days**; chaos tests for failover.
- **Capacity models**, growth budgets; performance regression gates in CI.
- Curate **golden runbooks**, toil reduction roadmap.

### 11.3 SRE
- Incident lifecycle (detect → triage → mitigate → recover → postmortem).
- **Blameless** culture; action items tracked; SLO burn alerts; on-call rotations.

### 11.4 Data Engineer
- Contract-first pipelines; **idempotence**; backfills safe + throttled.
- **Schema evolution** strategy; reproducible jobs; cost-aware partitioning.

### 11.5 Data Scientist
- **Access least-privilege**, curated datasets; avoid prod connections.
- Reproducible experiments (seed, env, data snapshot); model explainability; drift monitors.

### 11.6 Database Developer
- **SQL standards**: formatting, CTEs, bind variables; avoid anti-patterns (N+1, select *).
- **Testing**: unit tests on stored code; performance tests; plan checks; feature flags.

[Back to top](#table-of-contents)

---

## 12. Engine-Specific Guidelines

### 12.1 Oracle
- **HA/DR**: RAC for HA, **Data Guard** for DR (consider FSFO).
- **Storage**: ASM best practices; separate FRA; controlfile multiplexing.
- **Performance**: AWR/ASH; SQL Plan Baselines; Adaptive features awareness.
- **Security**: **TDE**; DB Vault (as needed); unified auditing.
- **Maintenance**: baseline with AWR; patch cycles; Segment Advisor.

### 12.2 SQL Server
- **HA/DR**: **Always On AG**; tune quorum/witness; listener for apps.
- **TempDB**: multiple data files; trace flags (older versions); instant file init.
- **Performance**: Query Store; memory & MAXDOP; implicit conversions watch.
- **Security**: TDE; row-level security, dynamic data masking (use judiciously).
- **Maintenance**: Ola Hallengren scripts (or equivalent) for backup/index/stats.

### 12.3 PostgreSQL
- **HA/DR**: streaming repl + Patroni; logical for online upgrades.
- **Tuning**: `shared_buffers`, `work_mem`, autovacuum thresholds; `pg_stat_statements`.
- **Extensions**: `pg_partman`, `pg_hint_plan` (careful), `hypopg` for what-if.
- **Backups**: base backups + WAL archive; `pgBackRest`/`wal-g`.
- **Security**: TLS, SCRAM, row-level security (RLS).

### 12.4 MySQL
- **HA/DR**: Group Replication/InnoDB Cluster; Percona variants; GTID-based async.
- **Tuning**: `innodb_buffer_pool_size`, redo logs; slow query log + pt-query-digest.
- **DDL**: online DDL when possible; gh-ost/pt-osc for large tables.
- **Backups**: XtraBackup; binlog-based PITR.

### 12.5 MongoDB
- **HA**: replica sets with odd voters; avoid arbiter unless justified.
- **Schema**: design for access patterns; avoid unbounded doc growth.
- **Indexes**: compound, TTL, partial; watch index cardinality.
- **Backups**: filesystem snapshots or Ops Manager/Cloud Manager; logical for subsets.

### 12.6 Redis
- **Mode**: choose between Sentinel vs Cluster; persistence RDB/AOF with fsync policy.
- **Memory**: `maxmemory` + eviction policy; avoid big keys; Lua with care.
- **Security**: ACLs, TLS, protected mode; avoid exposure to public internet.

### 12.7 DB2
- **HA/DR**: **HADR** with log shipping; TSA automation; pureScale for clustered HA.
- **Performance**: bufferpools, DPF/BLU (columnar) awareness; RUNSTATS.
- **Backup**: compressed backups; log archiving; rollforward.

[Back to top](#table-of-contents)

---

## 13. Cloud-Specific Guidance

### 13.1 AWS
- Prefer **RDS/Aurora** for managed engines; **EC2** only when features demand it.
- **Networking**: private subnets, SGs, **RDS Proxy** for connection pooling.
- **Storage**: GP3/IO2 for IOPS; snapshots + cross-region copy; S3 for backups.
- **Security**: IAM roles, **KMS** CMKs; Secrets Manager; CloudTrail + GuardDuty.
- **Observability**: CloudWatch + Enhanced Monitoring; Performance Insights.

### 13.2 Azure
- **Services**: Azure SQL (DB/MI), Flexible Server (Postgres/MySQL), Cosmos DB, Azure Cache for Redis.
- **Networking**: **Private Endpoints**, NSGs; Azure Bastion; Azure Firewall.
- **Security**: **Key Vault**, AAD auth; Defender for Cloud; Purview for governance.
- **Ops**: Auto-failover groups; Geo-redundant backups; Workload Groups (SQL).

### 13.3 GCP
- **Services**: Cloud SQL, AlloyDB, Memorystore, BigQuery for analytics.
- **Networking**: Private Service Connect; VPC-SC; Cloud Armor.
- **Security**: CMEK with **Cloud KMS**; Secret Manager; IAM Conditions.
- **Ops**: Point-in-time recovery; high-availability instances; Cloud Monitoring.

### 13.4 OCI
- **Services**: Autonomous DB (ATP/ADW), Base DB (VM/BM/Exadata), GoldenGate, OKE.
- **Networking**: Private subnets; Service Gateway; Bastion; NSGs.
- **Security**: Vault/KMS; Database Vault; Data Safe for auditing/classification.
- **Ops**: Data Guard; Backup to Object Storage; ExaCS for high throughput.

[Back to top](#table-of-contents)

---

## 14. Cost Optimization

- **Right-size** instances; use storage tiers; compress backups.
- **Reserved/Savings plans**; stop dev/test after hours; serverless where feasible.
- **Observe**: cost dashboards, anomaly alerts; allocate by tags/projects.
- **License**: BYOL vs included (Oracle/SQL Server); consolidate where lawful.

[Back to top](#table-of-contents)

---

## 15. Templates & Reusable Artifacts

**SLO YAML**
```yaml
service: orders-db
slo:
  availability: 99.95
  latency_ms_p95: 20
targets:
  rto_minutes: 15
  rpo_minutes: 5
dashboards:
  - grafana: https://grafana.local/d/abc123/orders-db
runbooks:
  - https://runbooks.local/orders-db
```

**Incident Postmortem (Markdown)**
```markdown
# Postmortem: <Incident Title>
- Start: 2025-10-14 10:31Z
- Duration: 28m
- Impact: <who/what>
- Root Cause: <summary>
- Timeline: <events>
- What Went Well:
- What Went Poorly:
- Action Items (owner, due):
```

**Runbook Skeleton**
```markdown
# Runbook: <Task>
## Preconditions
## Steps
1. ...
2. ...
## Validate
## Rollback
```

**Prometheus Rules (More)**
```yaml
- alert: DBHighCPU
  expr: avg_over_time(node_cpu_seconds_total{mode="idle"}[5m]) < 0.2
  for: 10m
  labels: { severity: ticket }
  annotations:
    summary: "DB node CPU high"
```

**Terraform – RDS (snippet)**
```hcl
resource "aws_db_instance" "pg" {
  engine               = "postgres"
  engine_version       = "16"
  instance_class       = "db.m6g.large"
  allocated_storage    = 200
  storage_type         = "gp3"
  storage_encrypted    = true
  kms_key_id           = aws_kms_key.db.arn
  db_subnet_group_name = aws_db_subnet_group.main.name
  multi_az             = true
  backup_retention_period = 7
  deletion_protection  = true
  publicly_accessible  = false
}
```

**GitLab CI – Liquibase (snippet)**
```yaml
stages: [validate, migrate]
migrate:
  image: liquibase/liquibase:latest
  script:
    - liquibase --url=jdbc:postgresql://db:5432/app --username=$DB_USER --password=$DB_PASS update
  rules: [ { if: '$CI_COMMIT_BRANCH == "main"' } ]
```

[Back to top](#table-of-contents)

---

## 16. Checklists

**Go-Live (RDBMS)**
- [ ] SLOs/RTO/RPO defined and reviewed.
- [ ] HA topology validated (AZ/region, quorum).
- [ ] Backups encrypted, restore test passed within RTO.
- [ ] TLS enforced; secrets externalized; least privilege.
- [ ] Baseline metrics/alerts in place; dashboard linked in README.
- [ ] Capacity headroom ≥ 30%; auto-scaling tested (where relevant).
- [ ] Runbooks ready; on-call updated; ownership clear.

**Weekly Ops**
- [ ] Backup success + random restore test.
- [ ] Replication lag within SLO; no slot bloat (Postgres).
- [ ] Index/fragmentation review (engine-appropriate).
- [ ] Security updates/patches reviewed.
- [ ] Cost report reviewed; anomalies triaged.

**Monthly**
- [ ] DR drill (tabletop or live).
- [ ] Parameter drift audit; configuration as code validated.
- [ ] Access review (DB + cloud); rotate credentials where applicable.
- [ ] Performance regression check; vacuum/optimize windows planned.

[Back to top](#table-of-contents)

---

## 17. References & Further Reading

- SRE Book (Google); Database Reliability Engineering (Laine Campbell, Charity Majors).
- Vendor docs: Oracle, Microsoft SQL Server, PostgreSQL, MySQL, MongoDB, Redis, IBM DB2.
- Cloud provider security & architecture blueprints (AWS, Azure, GCP, OCI).
- Tools: Liquibase, Flyway, dbt, Great Expectations, Debezium, Airflow, Dagster, Prometheus, Grafana, OpenTelemetry.

---

### License

MIT — share, adapt, and improve. PRs welcome.
