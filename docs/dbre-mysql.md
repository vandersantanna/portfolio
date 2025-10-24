<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# MySQL Reliability Engineering Guide
*SLO-driven operations—GTID replication, InnoDB Cluster, PITR, and safe releases at scale.*

## Table of Contents
- [1. Executive Summary](#1-executive-summary)
- [2. Role Scope & Value Proposition](#2-role-scope--value-proposition)
- [3. Skills Matrix](#3-skills-matrix)
  - [3.1 Core DBRE Competencies](#31-core-dbre-competencies)
  - [3.2 MySQL Stack](#32-mysql-stack)
  - [3.3 Platform & Tooling](#33-platform--tooling)
- [4. Reference Architecture & Environments](#4-reference-architecture--environments)
  - [4.1 Topologies](#41-topologies)
  - [4.2 Cloud & Hybrid](#42-cloud--hybrid)
  - [4.3 Data Flows & Serving Layers](#43-data-flows--serving-layers)
- [5. Reliability Engineering Fundamentals](#5-reliability-engineering-fundamentals)
  - [5.1 SLOs, SLIs, SLAs](#51-slos-slis-slas)
  - [5.2 Error Budgets & Risk](#52-error-budgets--risk)
  - [5.3 Incident Lifecycle & Postmortems](#53-incident-lifecycle--postmortems)
- [6. Observability & Monitoring](#6-observability--monitoring)
  - [6.1 Metrics & Dashboards](#61-metrics--dashboards)
  - [6.2 Slow Query Analysis & Profiling](#62-slow-query-analysis--profiling)
  - [6.3 Logging, Alerting & On-Call Hygiene](#63-logging-alerting--on-call-hygiene)
- [7. Capacity Planning & Performance Engineering](#7-capacity-planning--performance-engineering)
  - [7.1 Baselines & Benchmarking](#71-baselines--benchmarking)
  - [7.2 Query & Schema Tuning](#72-query--schema-tuning)
  - [7.3 Resource, IO & Storage Optimization](#73-resource-io--storage-optimization)
- [8. High Availability & Disaster Recovery](#8-high-availability--disaster-recovery)
  - [8.1 Replication (GTID, Semi-Sync, Multi-Source)](#81-replication-gtid-semi-sync-multi-source)
  - [8.2 Group Replication & InnoDB Cluster](#82-group-replication--innodb-cluster)
  - [8.3 Galera/PXC & NDB (when applicable)](#83-galerapxc--ndb-when-applicable)
  - [8.4 Backup, PITR & DR Testing](#84-backup-pitr--dr-testing)
- [9. Security, Compliance & Governance](#9-security-compliance--governance)
  - [9.1 Identity & Access (RBAC)](#91-identity--access-rbac)
  - [9.2 Encryption & Secrets](#92-encryption--secrets)
  - [9.3 Auditing, Data Privacy & Masking](#93-auditing-data-privacy--masking)
- [10. Change Management & Release Engineering](#10-change-management--release-engineering)
  - [10.1 GitOps & Infrastructure as Code](#101-gitops--infrastructure-as-code)
  - [10.2 Database CI/CD](#102-database-cicd)
  - [10.3 Online Schema Change & Safe Deploy Patterns](#103-online-schema-change--safe-deploy-patterns)
- [11. Automation & Runbooks](#11-automation--runbooks)
  - [11.1 Provisioning, Patching & Upgrades](#111-provisioning-patching--upgrades)
  - [11.2 Health Checks & Self-Healing](#112-health-checks--self-healing)
  - [11.3 Operational Playbooks](#113-operational-playbooks)
- [12. Data Integration & Replication](#12-data-integration--replication)
  - [12.1 CDC & ETL/ELT](#121-cdc--etlelt)
  - [12.2 Cross-DB & Heterogeneous Replication](#122-cross-db--heterogeneous-replication)
  - [12.3 Streaming & Analytics](#123-streaming--analytics)
- [13. Cost & Efficiency Engineering](#13-cost--efficiency-engineering)
  - [13.1 Editions & Support Models](#131-editions--support-models)
  - [13.2 Right-Sizing & Scaling](#132-right-sizing--scaling)
  - [13.3 Storage & Networking Economics](#133-storage--networking-economics)
- [14. Reliability Case Studies](#14-reliability-case-studies)
- [15. KPIs, Dashboards & Reporting](#15-kpis-dashboards--reporting)
- [16. Standards & Conventions](#16-standards--conventions)
- [17. Roadmap & Continuous Improvement](#17-roadmap--continuous-improvement)
- [18. Appendices & Templates](#18-appendices--templates)
  - [A. Scripts & Snippets](#a-scripts--snippets)
  - [B. Terraform & Ansible (AWS/GCP/Azure/On-prem)](#b-terraform--ansible-awsgcpazureonprem)
  - [C. CI/CD Pipelines (GitHub Actions/Azure DevOps)](#c-cicd-pipelines-github-actionsazure-devops)
  - [D. Runbook Templates](#d-runbook-templates)
  - [E. Checklists](#e-checklists)
  - [F. Diagrams (Mermaid)](#f-diagrams-mermaid)
  - [G. Glossary](#g-glossary)

---

## 1. Executive Summary
I design and operate reliable, secure, performant, and cost-efficient **MySQL** platforms across on-prem, public cloud, and hybrid. My DBRE practice turns business goals into **SLOs** measured by deep **observability**, delivered safely with **CI/CD**, and protected by verified **HA/DR** and **PITR**. Outcomes: fewer incidents, faster recovery, predictable performance, auditable compliance.

## 2. Role Scope & Value Proposition
- **Scope:** OLTP/HTAP workloads; MySQL 8.x, Percona Server; InnoDB Cluster/ClusterSet, Group Replication, GTID async & semi-sync replication; Aurora/RDS/Cloud SQL/Azure Flexible Server.
- **Interfaces:** Application teams, SRE/Platform, SecOps, Data Engineering, Architecture, and Leadership.
- **Value:** User-centric SLOs → architecture and automation; observability-first; safe change delivery; DR you can prove with numbers.

---

## 3. Skills Matrix

### 3.1 Core DBRE Competencies
- SLI/SLO/SLA design; error budgets; risk registers; change failure rate reduction.
- Incident response; blameless postmortems; chaos/DR drills; toil elimination.
- Observability (Performance Schema/`sys`, PMM, Prometheus, OpenTelemetry); capacity planning; cost optimization.

### 3.2 MySQL Stack
- **Engines & Features:** InnoDB focus (redo/undo/flush); histograms; EXPLAIN ANALYZE; optimizer hints.
- **HA/DR:** GTID, semi-sync, multi-source; Group Replication/InnoDB Cluster/ClusterSet; Galera/PXC (when suitable); NDB for niche low-latency sharding.
- **Ops:** XtraBackup/Enterprise Backup; Orchestrator; MySQL Shell & Router; ProxySQL/Haproxy/Keepalived.

### 3.3 Platform & Tooling
- **Infra:** Linux (NUMA/HugePages/I/O schedulers), systemd, NVMe/SAN, XFS.
- **Cloud:** AWS Aurora/RDS, GCP Cloud SQL, Azure MySQL Flexible Server (Private networking, IAM).
- **Automation:** Terraform, Ansible, Packer, Bash, Python.
- **Pipelines:** GitHub Actions/Azure DevOps; Flyway/Liquibase migrations.
- **Secrets/KMS:** Vault, AWS KMS, Azure Key Vault, GCP KMS.

---

## 4. Reference Architecture & Environments

### 4.1 Topologies
- **Primary–Replica (GTID)**: async or semi-sync; read scale-out; Orchestrator-managed failover.
- **InnoDB Cluster** (Group Replication + Router): single- or multi-primary; automatic routing.
- **ClusterSet**: DR/geo-distribution between InnoDB Clusters.
- **Galera/PXC**: virtually synchronous (certification-based) cluster for specific patterns.
- **NDB**: in-memory sharded cluster for real-time telecom/OLTP niches.

### 4.2 Cloud & Hybrid
- **Aurora MySQL**: 1 writer + readers; fast failover; backtracking; Global Database.
- **RDS/Cloud SQL/Azure Flexible**: managed patching, backups, HA options; Private Link/VPC-SC/Private Endpoint.
- Hybrid networking: VPN/Direct Connect/ExpressRoute; identity/KMS segmentation; end-to-end TLS.

### 4.3 Data Flows & Serving Layers
OLTP → CDC (Debezium/Maxwell/Canal) → Stream (Kafka/Kinesis/PubSub) → Lake/Warehouse → BI/ML.  
Freshness SLOs & replica lag budgets drive flow design and batch windows.

---

## 5. Reliability Engineering Fundamentals

### 5.1 SLOs, SLIs, SLAs
- **SLIs (examples):** p99 read latency < 40 ms; commit latency < 120 ms; error rate < 0.1%; replica `Seconds_Behind_Source` ≤ 5s; backup success ≥ 99.9%; restore test time ≤ 20 min.
- **SLOs:** Tier-1 checkout DB availability 99.95% monthly; ADQ (apply delay) ≤ 2s for read-replica.

~~~yaml
# SLO policy (documentation-as-code)
service: orders-mysql
slos:
  - name: p99_read_latency_ms
    target: "< 40"
    window: 30d
  - name: replica_lag_seconds
    target: "<= 5"
    window: 30d
  - name: restore_time_minutes
    target: "<= 20"
    window: 30d
burn_policies:
  - if_burn_rate: "> 2.0x"
    action: "freeze risky changes; open reliability epic; schedule DR drill"
~~~

### 5.2 Error Budgets & Risk
- Track budget consumption; restrict risky changes while burning.
- Risk register per system (probability × impact) with mitigation owners & due dates.

### 5.3 Incident Lifecycle & Postmortems
Detect → Triage → Mitigate → Recover → Review.  
Blameless postmortems with clear actions, owners, deadlines; link alerts → runbooks → tickets.

---

## 6. Observability & Monitoring

### 6.1 Metrics & Dashboards
- **Instance:** QPS/TPS, threads, `Threads_running`, `Threads_connected`, buffer pool hit %, redo write rate, page flushes, I/O latency.
- **Replication:** `performance_schema.replication_*` tables; `SHOW REPLICA STATUS\G` (or `SHOW SLAVE STATUS\G` on older versions).
- **Business:** SLO compliance, error-budget burn, capacity headroom.

~~~sql
-- Top statements by total latency (Performance Schema digest)
SELECT SUBSTRING(digest_text,1,120) AS query_sample,
       ROUND(SUM_TIMER_WAIT/1e12,2) AS exec_time_s,
       COUNT_STAR AS exec_count,
       ROUND(AVG_TIMER_WAIT/1e9,2) AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 15;
~~~

~~~sql
-- File IO latency by file (InnoDB)
SELECT file_name, io_type, count_read, count_write,
       ROUND(sum_timer_read/1e9,2) AS read_ms,
       ROUND(sum_timer_write/1e9,2) AS write_ms
FROM performance_schema.file_summary_by_instance
ORDER BY (sum_timer_read + sum_timer_write) DESC
LIMIT 20;
~~~

~~~yaml
# Prometheus scrape (mysqld_exporter example)
scrape_configs:
  - job_name: 'mysql'
    static_configs:
      - targets: ['db-prim:9104','db-rep1:9104','db-rep2:9104']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
~~~

### 6.2 Slow Query Analysis & Profiling
- Enable slow log with `long_query_time`, `log_slow_admin_statements`, `log_slow_replica_statements`.
- Use **pt-query-digest** to aggregate and rank.
- Use `EXPLAIN ANALYZE` to measure plan/row estimates and timing.

~~~bash
# pt-query-digest on rotating slow logs
pt-query-digest /var/log/mysql/slow.log > /var/reports/slow-$(date +%F).txt
grep -E "Query_time:|# Profile" /var/reports/slow-$(date +%F).txt | head -n 40
~~~

~~~sql
-- EXPLAIN ANALYZE sample
EXPLAIN ANALYZE
SELECT o.id, o.status, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'OPEN' AND o.created_at >= NOW() - INTERVAL 7 DAY
ORDER BY o.created_at DESC
LIMIT 100;
~~~

### 6.3 Logging, Alerting & On-Call Hygiene
- Centralize logs: Loki/ELK/Cloud-native; add correlation IDs from app layer.
- Actionable alerts with runbook links; severity tiers (page vs ticket).

~~~yaml
# Alertmanager: replica lag high
groups:
- name: mysql
  rules:
  - alert: MySQLReplicaLagHigh
    expr: mysql_slave_status_seconds_behind_master > 5
    for: 5m
    labels: { severity: page }
    annotations:
      summary: "Replica lag >5s on {{ $labels.instance }}"
      runbook: "runbooks/dr/replica-lag.md"
~~~

---

## 7. Capacity Planning & Performance Engineering

### 7.1 Baselines & Benchmarking
- Tools: **sysbench**, tpcc-mysql; measure p50/p90/p99 latency; track redo/IO/CPU.
- Forecast CPU/IOPS/memory/storage for 30–90 days; keep headroom ≥ 30%.

~~~bash
# sysbench OLTP read/write baseline
sysbench oltp_read_write --mysql-host=db-prim --mysql-user=bench --mysql-password=**** \
  --mysql-db=sbtest --tables=16 --table-size=2000000 --time=900 --threads=64 prepare
sysbench oltp_read_write --mysql-host=db-prim --mysql-user=bench --mysql-password=**** \
  --mysql-db=sbtest --tables=16 --table-size=2000000 --time=900 --threads=64 run \
  | tee results/sysbench-$(date +%F).log
sysbench oltp_read_write --mysql-host=db-prim --mysql-user=bench --mysql-password=**** \
  --mysql-db=sbtest cleanup
~~~

### 7.2 Query & Schema Tuning
- Index strategies (covering/composite/functional); statistics & histograms; partitioning; compression (InnoDB page).
- Anti-pattern catalog: full scans, temp spills, hot PKs, big transactions.

~~~sql
-- Create histogram to improve cardinality estimates
ANALYZE TABLE orders UPDATE HISTOGRAM ON status WITH 8 BUCKETS;

-- Composite covering index for frequent filter + join
CREATE INDEX ix_orders_status_created ON orders(status, created_at);

-- Plan hint (use cautiously)
SELECT /*+ SET_VAR(optimizer_switch='mrr_cost_based=off') */ COUNT(*)
FROM orders
WHERE created_at >= NOW() - INTERVAL 1 DAY;
~~~

### 7.3 Resource, IO & Storage Optimization
- **InnoDB buffer pool** ≈ 60–75% of RAM (depends on workload); proper `innodb_log_file_size` × N for redo throughput.
- Pre-size ibtmp, monitor FTS/temp usage; place data/log/tmp on appropriate volumes; use `O_DIRECT` when suitable.

~~~ini
# my.cnf performance baseline (illustrative, tune per host)
[mysqld]
innodb_buffer_pool_size = 48G
innodb_buffer_pool_instances = 8
innodb_log_file_size = 4G
innodb_log_files_in_group = 2
innodb_flush_log_at_trx_commit = 1
innodb_flush_method = O_DIRECT
innodb_io_capacity = 4000
innodb_io_capacity_max = 8000
tmp_table_size = 512M
max_heap_table_size = 512M
log_error_verbosity = 2
slow_query_log = ON
long_query_time = 0.2
~~~

---

## 8. High Availability & Disaster Recovery

### 8.1 Replication (GTID, Semi-Sync, Multi-Source)
- Use **GTID** for reliable failover; **semi-sync** for lower data loss (commit waits for ack).
- Multi-source for fan-in; keep channel names; orchestrate with **Orchestrator**.

~~~ini
# my.cnf (source & replica essentials)
[mysqld]
server_id=101                         # unique per node
gtid_mode=ON
enforce_gtid_consistency=ON
binlog_format=ROW
log_slave_updates=ON
binlog_row_image=FULL
plugin_load_add="semisync_master.so;semisync_slave.so"
rpl_semi_sync_master_enabled=ON
rpl_semi_sync_slave_enabled=ON
rpl_semi_sync_master_timeout=1000
~~~

~~~sql
-- On replica: set channel and start replication (8.0 terminology)
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='db-prim', SOURCE_PORT=3306,
  SOURCE_USER='repl', SOURCE_PASSWORD='********',
  SOURCE_AUTO_POSITION=1
  FOR CHANNEL 'primary';
START REPLICA FOR CHANNEL 'primary';
SHOW REPLICA STATUS FOR CHANNEL 'primary'\G
~~~

~~~bash
# Orchestrator: discover and visualize topology
orchestrator-client -c discover -i db-prim:3306
orchestrator-client -c topology -i db-prim:3306
# Planned failover
orchestrator-client -c relocate-replicas -i db-prim:3306 -d db-new-prim:3306
~~~

### 8.2 Group Replication & InnoDB Cluster
- Quorum-based, single-/multi-primary; use MySQL Shell `dba` API and MySQL Router.

~~~bash
# MySQL Shell (interactive JS) - create InnoDB Cluster
mysqlsh --uri admin@db1:3306
\js
var cluster = dba.createCluster('ProdCluster', {multiPrimary:false});
cluster.addInstance('admin@db2:3306', {recoveryMethod:'clone'});
cluster.addInstance('admin@db3:3306', {recoveryMethod:'incremental'});
cluster.status();
~~~

~~~bash
# MySQL Router bootstrap (on app host)
mysqlrouter --bootstrap admin@db1:3306 --directory /etc/mysqlrouter --user mysqlrouter
systemctl enable --now mysqlrouter
# App connects to mysqlrouter RW/RO ports
~~~

### 8.3 Galera/PXC & NDB (when applicable)
- **Galera/PXC**: near-synchronous certification; needs even/odd quorum; watch for BF aborts on hot rows; tune wsrep flow control.
- **NDB**: in-memory sharding for ultra-low latency write-heavy workloads with constrained SQL features.

### 8.4 Backup, PITR & DR Testing
- **XtraBackup** full + incremental; binlog-based **PITR**.
- Quarterly restore validations; measurable RPO/RTO; immutable/S3/Object-Lock for retention.

~~~bash
# Full backup with XtraBackup (Percona)
xtrabackup --backup --target-dir=/backups/full-$(date +%F) --user=backup --password=****
# Incremental
xtrabackup --backup --incremental-basedir=/backups/full-2025-10-01 --target-dir=/backups/inc-$(date +%F) --user=backup --password=****
# Prepare (apply logs)
xtrabackup --prepare --target-dir=/backups/full-2025-10-01
# Restore (service down, copy-back)
systemctl stop mysqld
xtrabackup --copy-back --target-dir=/backups/full-2025-10-01
chown -R mysql:mysql /var/lib/mysql
systemctl start mysqld
~~~

~~~bash
# PITR using mysqlbinlog (from last full restore)
mysqlbinlog --start-datetime="2025-10-08 12:05:00" --stop-datetime="2025-10-08 12:20:00" \
  /backups/binlogs/mysql-bin.000123 /backups/binlogs/mysql-bin.000124 \
  | mysql -u root -p
~~~

---

## 9. Security, Compliance & Governance

### 9.1 Identity & Access (RBAC)
- Use roles; least privilege; rotate credentials; break-glass with MFA; `caching_sha2_password` default.

~~~sql
-- Read-only analytics role
CREATE ROLE ro_analytics;
GRANT SELECT ON sales.* TO ro_analytics;
CREATE USER 'bi_reader'@'10.%' IDENTIFIED BY 'Strong#Pass!';
GRANT ro_analytics TO 'bi_reader'@'10.%';
SET DEFAULT ROLE ro_analytics FOR 'bi_reader'@'10.%';
~~~

### 9.2 Encryption & Secrets
- TLS for in-transit; at-rest via filesystem/disk encryption; **keyring** plugins for TDE-like features (tablespace keys).
- Secret stores: Vault/KMS/Secrets Manager; short-lived creds for CI.

~~~ini
# my.cnf TLS + keyring (illustrative)
[mysqld]
ssl_ca=/etc/mysql/ssl/ca.pem
ssl_cert=/etc/mysql/ssl/server-cert.pem
ssl_key=/etc/mysql/ssl/server-key.pem
early-plugin-load=keyring_file.so
keyring_file_data=/var/lib/mysql-keyring/keyring
require_secure_transport=ON
~~~

### 9.3 Auditing, Data Privacy & Masking
- Audit plugins (Enterprise Audit, Percona Audit Log); immutable storage.
- Data minimization; app-level masking; pseudonymization in lower envs; GDPR/LGPD processes.

~~~sql
-- Percona Audit Log plugin (example)
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
SET GLOBAL audit_log_strategy = 'ASYNCHRONOUS';
SET GLOBAL audit_log_format = 'JSON';
~~~

---

## 10. Change Management & Release Engineering

### 10.1 GitOps & Infrastructure as Code
- Provision MySQL/ProxySQL/Router via **Terraform/Ansible/Packer**; policy-as-code; drift detection.

### 10.2 Database CI/CD
- **Flyway/Liquibase** migrations; pre-deploy checks (locks/long TXs), drift diffs, smoke tests; auto-rollback (reverse scripts or PITR).

~~~properties
# Flyway config (MySQL)
flyway.url=jdbc:mysql://db-prim:3306/sales?useSSL=true&requireSSL=true
flyway.user=app_migrator
flyway.password=${APP_MIGRATOR_PWD}
flyway.locations=filesystem:./db/migrations
flyway.baselineOnMigrate=true
flyway.outOfOrder=false
~~~

~~~sql
-- V1__create_orders_table.sql
CREATE TABLE orders (
  id           BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_id  BIGINT NOT NULL,
  status       VARCHAR(30) NOT NULL,
  created_at   TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
  KEY ix_orders_status_created (status, created_at),
  KEY ix_orders_customer (customer_id, created_at)
) ENGINE=InnoDB;
~~~

### 10.3 Online Schema Change & Safe Deploy Patterns
- **gh-ost** or **pt-online-schema-change** for live schema changes; throttle on lag; blue/green schemas; canary cohorts; feature flags; promotion gates tied to SLOs.

~~~bash
# gh-ost adding column safely (throttled by replica lag)
gh-ost --user=ddl --password=**** --host=db-prim --database=sales --table=orders \
  --alter="ADD COLUMN source VARCHAR(16) NOT NULL DEFAULT 'web'" \
  --allow-on-master --exact-rowcount --default-retries=120 \
  --max-lag-millis=3000 --chunk-size=1000 --cut-over=default --verbose --execute
~~~

---

## 11. Automation & Runbooks

### 11.1 Provisioning, Patching & Upgrades
- Golden images; repo channels; rolling GR/PXC patch strategy; rehearse version upgrades in lower envs.

~~~yaml
# Ansible: MySQL packages + base config (excerpt)
- hosts: mysql
  become: true
  tasks:
    - name: Install MySQL 8
      package:
        name: [mysql-server, mysql-client]
        state: present
    - name: Deploy my.cnf
      template:
        src: templates/my.cnf.j2
        dest: /etc/my.cnf
      notify: Restart MySQL
  handlers:
    - name: Restart MySQL
      service: { name: mysqld, state: restarted, enabled: yes }
~~~

### 11.2 Health Checks & Self-Healing
- Daily/weekly checks: backups, replication status, disk usage, error logs, dictionary stats.
- Auto-remediation: restart stuck applier, expand ibtmp, rotate slow logs, reseed replicas with XtraBackup.

~~~bash
# Bash: replication lag watchdog (pages if >5s for 5min)
LAG=$(mysql -Nse "SHOW REPLICA STATUS\G" | awk -F': ' '/Seconds_Behind_Source/ {print $2}')
if [ "${LAG:-0}" -gt 5 ]; then
  echo "Replica lag ${LAG}s" | /usr/local/bin/page "mysql-replica-lag"
fi
~~~

### 11.3 Operational Playbooks
- Start/Stop; primary promotion; GR member rejoin; backup validate; restore dry-run; capacity expansion; onboarding/offboarding; license/support audit.  
Each with **pre-checks**, **numbered steps**, **success criteria**, **rollback**, **post-actions**.

---

## 12. Data Integration & Replication

### 12.1 CDC & ETL/ELT
- Debezium/Maxwell/Canal; idempotent loads; retries & backoff; watermarking; outbox pattern.

~~~json
{
  "name": "debezium-mysql-source",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "db-prim",
    "database.port": "3306",
    "database.user": "cdc",
    "database.password": "****",
    "database.include.list": "sales",
    "table.include.list": "sales.orders",
    "include.schema.changes": "false",
    "database.server.id": "5401",
    "database.server.name": "salesdb",
    "tombstones.on.delete": "false",
    "snapshot.mode": "initial"
  }
}
~~~

### 12.2 Cross-DB & Heterogeneous Replication
- MySQL ↔ PostgreSQL/Oracle/SQL Server/Snowflake/BigQuery; map types; ensure ordering; periodic **checksum** validation.

~~~bash
# pt-table-checksum & pt-table-sync (consistent replicas)
pt-table-checksum --user=admin --password=**** --host=db-prim --databases sales
pt-table-sync --execute --user=admin --password=**** --host=db-rep1 --replicate percona.checksums
~~~

### 12.3 Streaming & Analytics
- Kafka/Kinesis/PubSub ingestion; materialized aggregates; ClickHouse/StarRocks/Trino/Spark integrations; lakehouse patterns with partitioned sinks.

---

## 13. Cost & Efficiency Engineering

### 13.1 Editions & Support Models
- Community vs Enterprise; **Percona** support; managed cloud (RDS/Aurora/Cloud SQL/Azure Flexible) trade-offs and SLAs.

### 13.2 Right-Sizing & Scaling
- vCPU/memory/I/O sizing; vertical vs horizontal scale; read replicas vs sharding; Aurora Serverless v2 when bursty.

### 13.3 Storage & Networking Economics
- NVMe/SAN tiers, provisioned IOPS; snapshot/backup retention cost; cross-region egress budgeting; Global Database (Aurora) vs DIY replicas.

---

## 14. Reliability Case Studies
**Case A — InnoDB Cluster replacing fragile master–replica**  
Problem: frequent failovers & stale reads → Action: InnoDB Cluster + Router, SLOs + dashboards → Result: 99.97% 6-month availability, replica lag < 2s, CFR −40%.

**Case B — ProxySQL read/write split + plan fixes**  
Problem: p99 spikes under flash sales → Action: RO routing + EXPLAIN ANALYZE tuning + histograms → Result: p99 latency −45%, headroom +30%.

**Case C — DR with XtraBackup + PITR**  
Problem: RPO unproven; slow restores → Action: nightly full + hourly inc; PITR rehearsals; immutable backups → Result: RPO < 60s, RTO 12m.

---

## 15. KPIs, Dashboards & Reporting
- **Availability:** service-level & aggregate; **Latency:** p50/p90/p99; **Error budget burn**  
- **Change:** deploy frequency, lead time, change failure rate; **Ops:** MTTR/MTTD, DR drill pass rate  
- **Health:** backup success & restore time, CHECK TABLE cadence, replica lag; **Capacity:** headroom & forecast

~~~markdown
**Monthly Executive Summary (template)**
- Availability: 99.97% (SLO: 99.95%) ✅
- Error budget burn: 26% (policy < 50%)
- Incidents: Sev-1:0, Sev-2:1, Sev-3:3 (MTTR: 19m)
- Changes: 48 deploys, CFR: 3.1%
- DR: 1 drill passed, RTO 11m (target ≤ 20m)
- Risks: Hot partition on orders (Q4 sharding plan)
~~~

---

## 16. Standards & Conventions
- **Naming:** `mysql-{env}-{service}-{role}`, Router ports labeled `rw`/`ro`, ProxySQL hostgroups `10/20/30`.
- **Docs:** ADRs, runbook format, code style (SQL/Bash/Python); headers include change ID & SLO link.
- **Git:** trunk-based or GitFlow; semantic versioning; signed commits; CODEOWNERS; mandatory reviews.

---

## 17. Roadmap & Continuous Improvement
- **Q1:** 100% SLO coverage on tier-1; automated weekly restore tests.  
- **Q2:** Orchestrator + Router rollout; drift detection & policy-as-code.  
- **Q3:** Observability v2 (OpenTelemetry traces); partitioning strategy for hot tables.  
- **Q4:** Cost optimization phase-2; zero-touch patching for clusters; deprecate legacy runbooks.

---

## 18. Appendices & Templates

### A. Scripts & Snippets

~~~sql
-- Top waits at engine level (Performance Schema)
SELECT EVENT_NAME, COUNT_STAR, SUM_TIMER_WAIT/1e12 AS total_s, AVG_TIMER_WAIT/1e9 AS avg_ms
FROM performance_schema.events_waits_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'wait/io/%' OR EVENT_NAME LIKE 'wait/lock/%'
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
~~~

~~~sql
-- Replica health quick check (8.0+)
SELECT CHANNEL_NAME, SERVICE_STATE, LAST_ERROR_NUMBER, LAST_ERROR_MESSAGE,
       LAST_APPLIED_TRANSACTION, LAST_QUEUED_TRANSACTION,
       TIMESTAMPDIFF(SECOND, LAST_APPLIED_TRANSACTION_END_APPLY_TIMESTAMP, NOW()) AS since_last_apply_s
FROM performance_schema.replication_applier_status_by_worker
ORDER BY CHANNEL_NAME, WORKER_ID
LIMIT 20;
~~~

~~~sql
-- Hot tables by handler reads (approximate)
SELECT object_schema, object_name, count_read, count_write
FROM performance_schema.table_io_waits_summary_by_table
ORDER BY (count_read + count_write) DESC
LIMIT 15;
~~~

~~~bash
# Rotate slow log daily with compression
date=$(date +%F)
mysql -e "SET GLOBAL slow_query_log=0;"; \
mv /var/log/mysql/slow.log /var/log/mysql/slow-$date.log; \
mysql -e "SET GLOBAL slow_query_log=1;"; \
gzip /var/log/mysql/slow-$date.log
~~~

~~~python
# Simple exporter: expose Seconds_Behind_Source (illustrative)
from prometheus_client import start_http_server, Gauge
import time, MySQLdb
g = Gauge('mysql_replica_lag_seconds','Replica lag')
def loop():
    while True:
        db = MySQLdb.connect(host="db-rep1", user="metrics", passwd="****")
        c = db.cursor()
        c.execute("SHOW REPLICA STATUS")
        row = c.fetchone()
        lag = row[c.description.index(('Seconds_Behind_Source',))] if row else 0
        g.set(lag or 0)
        db.close()
        time.sleep(15)
if __name__ == "__main__":
    start_http_server(9105); loop()
~~~

### B. Terraform & Ansible (AWS/GCP/Azure/On-prem)

~~~hcl
# Terraform (AWS): RDS MySQL (simplified)
provider "aws" { region = "us-east-1" }
resource "aws_db_subnet_group" "mysql" {
  name       = "mysql-subnets"
  subnet_ids = [aws_subnet.app1.id, aws_subnet.app2.id]
}
resource "aws_db_instance" "mysql" {
  identifier              = "rds-mysql-sales"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = "db.m6i.large"
  allocated_storage       = 200
  storage_type            = "gp3"
  db_subnet_group_name    = aws_db_subnet_group.mysql.name
  multi_az                = true
  username                = "admin"
  password                = var.admin_password
  vpc_security_group_ids  = [aws_security_group.db.id]
  backup_retention_period = 7
  deletion_protection     = true
  publicly_accessible     = false
}
~~~

~~~hcl
# Terraform (GCP): Cloud SQL for MySQL (simplified)
provider "google" { project = var.project }
resource "google_sql_database_instance" "mysql" {
  name             = "mysql-sales"
  database_version = "MYSQL_8_0"
  region           = "us-central1"
  settings {
    tier = "db-custom-4-16384"
    availability_type = "REGIONAL"
    disk_size = 200
    ip_configuration { ipv4_enabled = false, private_network = google_compute_network.vpc.self_link }
    backup_configuration { enabled = true, point_in_time_recovery_enabled = true }
  }
}
~~~

~~~hcl
# Terraform (Azure): Flexible Server (simplified)
provider "azurerm" { features {} }
resource "azurerm_mysql_flexible_server" "mysql" {
  name                = "mysql-sales"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku_name            = "GP_Standard_D4ds_v4"
  administrator_login = "mysqladmin"
  administrator_password = var.admin_password
  zone                = "1"
  backup_retention_days = 7
  high_availability { mode = "ZoneRedundant" }
  storage { size_gb = 200 }
  network { delegated_subnet_id = azurerm_subnet.db.id, private_dns_zone_id = azurerm_private_dns_zone.mysql.id }
}
~~~

~~~yaml
# Ansible: ProxySQL config (excerpt)
- hosts: proxysql
  become: true
  tasks:
    - name: Deploy proxysql.cnf
      template:
        src: templates/proxysql.cnf.j2
        dest: /etc/proxysql.cnf
      notify: Restart ProxySQL
  handlers:
    - name: Restart ProxySQL
      service: { name: proxysql, state: restarted, enabled: yes }
~~~

### C. CI/CD Pipelines (GitHub Actions/Azure DevOps)

~~~yaml
# GitHub Actions: Flyway deploy with OIDC to AWS Secrets Manager
name: db-migrate
on:
  push: { paths: ["db/migrations/**"] }
jobs:
  migrate:
    runs-on: ubuntu-latest
    permissions: { id-token: write, contents: read }
    steps:
      - uses: actions/checkout@v4
      - name: Setup Flyway
        run: |
          curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.0.0/flyway-commandline-10.0.0-linux-x64.tar.gz | tar xz
          sudo ln -s $PWD/flyway-10.0.0/flyway /usr/local/bin/flyway
      - name: Retrieve DB secrets (illustrative)
        run: echo "Use OIDC to fetch short-lived credentials"
      - name: Pre-deploy checks
        run: |
          mysql -h $DB_HOST -u $DB_USER -p$DB_PASS -e "SHOW PROCESSLIST\G" | head
      - name: Flyway migrate
        run: flyway -configFiles=db/flyway.conf migrate
~~~

~~~yaml
# Azure DevOps: Liquibase deploy + smoke tests (excerpt)
stages:
- stage: Validate
  jobs:
  - job: Lint
    steps:
    - script: echo "Lint SQL, run unit checks"
- stage: Migrate
  dependsOn: Validate
  jobs:
  - job: Liquibase
    steps:
    - task: Bash@3
      inputs:
        targetType: 'inline'
        script: |
          curl -L https://download.liquibase.com/download/liquibase-4.27.0.tar.gz | tar xz
          ./liquibase --url="jdbc:mysql://$(DB_HOST)/sales" --username=$(DB_USER) --password=$(DB_PASS) \
            --changeLogFile=db/changelog.xml update
    - task: Bash@3
      inputs:
        targetType: 'inline'
        script: |
          mysql -h $(DB_HOST) -u $(DB_USER) -p$(DB_PASS) -e "SELECT 1;"
~~~

### D. Runbook Templates

~~~markdown
# Runbook: Planned Primary Promotion (GTID Replica)

## Preconditions
- Backups ≤ 24h; replicas caught up (lag < 5s)
- Maintenance window & stakeholders notified

## Steps
1. Freeze risky changes.
2. On candidate: `STOP REPLICA; RESET REPLICA ALL;`
3. Update ProxySQL/Router to point RW to new primary.
4. Repoint old primary as replica using `CHANGE REPLICATION SOURCE TO ... SOURCE_AUTO_POSITION=1; START REPLICA;`
5. Validate health: read/write probes, lag 0, dashboards green.

## Rollback
- Re-promote original primary if validation fails; replay steps in reverse.

## Post-actions
- Update inventory, Orchestrator, DNS; close change ticket with metrics (RTO, errors).
~~~

~~~markdown
# Runbook: Group Replication Member Rejoin

## Preconditions
- Cluster healthy; donor selected; network stable.

## Steps
1. Ensure config parity (`server_id`, `group_replication_group_seeds`, `group_replication_bootstrap_group=OFF`).
2. Start mysqld; run MySQL Shell `cluster.rejoinInstance('admin@dbX:3306')`.
3. Monitor `cluster.status()` until ONLINE; verify Router endpoints.

## Rollback
- Remove instance from cluster; rebuild with clone/incremental.

## Post-actions
- Record outage time; root-cause; action items for prevention.
~~~

~~~markdown
# Runbook: PITR from XtraBackup + Binlogs

## Preconditions
- Full + incremental set available; binlogs complete.

## Steps
1. Restore last full backup; apply incs; `--prepare`.
2. Start mysqld with restored data; block application access.
3. Apply binlogs with `mysqlbinlog --start-datetime ... --stop-datetime ... | mysql`.
4. Run smoke tests; reopen app traffic.

## Post-actions
- Record RTO/RPO; attach logs to change ticket; schedule a retrospective.
~~~

### E. Checklists

~~~markdown
## Patch Day Checklist
- [ ] Backups complete & verified (test restore OK)
- [ ] Change window approved; stakeholders notified
- [ ] Rolling plan for cluster (GR/PXC or primary/replica)
- [ ] Baseline captured (PMM dashboards, perf schema snapshots)
- [ ] Post-patch validation (SLO probes, lag, errors)

## DR Drill Checklist
- [ ] Restore latest full + increments to clean host
- [ ] Time the restore (RTO) & compute recovery point (RPO)
- [ ] Smoke test application against restored DB
- [ ] Record results vs SLO targets; track regressions
~~~

### F. Diagrams (Mermaid)

~~~mermaid
flowchart LR
  subgraph Primary[Primary]
    A[App] -->|RW| PROXY[(ProxySQL/Router)]
    PROXY --> DB1[(MySQL Primary)]
  end
  PROXY -.RO.-> R1[(Replica 1)]
  PROXY -.RO.-> R2[(Replica 2)]
  DB1 -->|Binlog/GTID| R1
  DB1 -->|Binlog/GTID| R2
  R2 --> BAK[(Backups + Binlogs)]
  BAK --> DR[(DR Site)]
  classDef strong fill:#eef,stroke:#66f,stroke-width:2px;
  class DB1,R1,R2 strong;
~~~

~~~mermaid
flowchart TB
  subgraph InnoDBCluster[InnoDB Cluster]
    C1[(DB1)]:::strong --- C2[(DB2)]:::strong --- C3[(DB3)]:::strong
  end
  ROUTER[(MySQL Router)] -->|RW/RO| InnoDBCluster
  classDef strong fill:#efe,stroke:#090,stroke-width:2px;
~~~

### G. Glossary
- **DBRE** — Database Reliability Engineering  
- **SLA/SLO/SLI** — Agreement/Objectives/Indicators  
- **MTTR/MTTD** — Mean Time to Recover/Detect  
- **GTID** — Global Transaction ID  
- **GR** — Group Replication; **InnoDB Cluster/ClusterSet** — GR-based HA/DR solutions  
- **PXC/Galera** — Percona XtraDB Cluster / Galera replication  
- **PITR** — Point-in-Time Recovery  
- **PMM** — Percona Monitoring & Management

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
