<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# PostgreSQL Reliability Engineering Guide
*From baselines and error budgets to failovers—secure, observable, automatable, security, and safe releases at scale.*

## Table of Contents
- [1. Executive Summary](#1-executive-summary)
- [2. Role Scope & Value Proposition](#2-role-scope--value-proposition)
- [3. Skills Matrix](#3-skills-matrix)
  - [3.1 Core DBRE Competencies](#31-core-dbre-competencies)
  - [3.2 PostgreSQL Stack](#32-postgresql-stack)
  - [3.3 Platform & Tooling](#33-platform--tooling)
- [4. Reference Architecture & Environments](#4-reference-architecture--environments)
  - [4.1 Topologies](#41-topologies)
  - [4.2 Cloud & Hybrid](#42-cloud--hybrid)
  - [4.3 Data Flows & Serving Layers](#43-data-flows--serving-layers)
- [5. Reliability Fundamentals](#5-reliability-fundamentals)
  - [5.1 SLOs, SLIs, SLAs](#51-slos-slis-slas)
  - [5.2 Error Budgets & Risk](#52-error-budgets--risk)
  - [5.3 Incident Lifecycle & Postmortems](#53-incident-lifecycle--postmortems)
- [6. Observability & Monitoring](#6-observability--monitoring)
  - [6.1 Metrics & Dashboards](#61-metrics--dashboards)
  - [6.2 Query Profiling & Plan Stability](#62-query-profiling--plan-stability)
  - [6.3 Logging, Alerting & On-Call](#63-logging-alerting--on-call)
- [7. Capacity Planning & Performance](#7-capacity-planning--performance)
  - [7.1 Baselines & Benchmarking](#71-baselines--benchmarking)
  - [7.2 Schema & Query Tuning](#72-schema--query-tuning)
  - [7.3 Resources, I/O & Storage](#73-resources-io--storage)
- [8. High Availability & Disaster Recovery](#8-high-availability--disaster-recovery)
  - [8.1 Physical & Logical Replication](#81-physical--logical-replication)
  - [8.2 Failover Orchestration](#82-failover-orchestration)
  - [8.3 Backups, PITR & DR Testing](#83-backups-pitr--dr-testing)
- [9. Security, Compliance & Governance](#9-security-compliance--governance)
  - [9.1 Identity & Access (RBAC, RLS)](#91-identity--access-rbac-rls)
  - [9.2 Encryption & Secrets](#92-encryption--secrets)
  - [9.3 Auditing, Privacy & Data Masking](#93-auditing-privacy--data-masking)
- [10. Change Management & Release Engineering](#10-change-management--release-engineering)
  - [10.1 GitOps & Infrastructure as Code](#101-gitops--infrastructure-as-code)
  - [10.2 Database CI/CD](#102-database-cicd)
  - [10.3 Safe Deployment Patterns](#103-safe-deployment-patterns)
- [11. Automation & Runbooks](#11-automation--runbooks)
  - [11.1 Provisioning, Patching & Upgrades](#111-provisioning-patching--upgrades)
  - [11.2 Health Checks & Auto-Remediation](#112-health-checks--auto-remediation)
  - [11.3 Operational Playbooks](#113-operational-playbooks)
- [12. Data Integration & Replication](#12-data-integration--replication)
  - [12.1 CDC & ETL/ELT](#121-cdc--etlelt)
  - [12.2 FDWs & Heterogeneous Replication](#122-fdws--heterogeneous-replication)
  - [12.3 Streaming & Analytics](#123-streaming--analytics)
- [13. Cost & Efficiency](#13-cost--efficiency)
  - [13.1 Managed vs Self-Managed Trade-offs](#131-managed-vs-self-managed-trade-offs)
  - [13.2 Right-Sizing & Scaling](#132-right-sizing--scaling)
  - [13.3 Storage & Network Economics](#133-storage--network-economics)
- [14. Reliability Case Studies](#14-reliability-case-studies)
- [15. KPIs, Dashboards & Reporting](#15-kpis-dashboards--reporting)
- [16. Standards & Conventions](#16-standards--conventions)
- [17. Roadmap & Continuous Improvement](#17-roadmap--continuous-improvement)
- [18. Appendices & Templates](#18-appendices--templates)
  - [A. Scripts (SQL/Bash)](#a-scripts-sqlbash)
  - [B. IaC & Config (Terraform/Ansible/K8s)](#b-iac--config-terraformansiblek8s)
  - [C. Pipelines (GitHub Actions/Azure DevOps)](#c-pipelines-github-actionsazure-devops)
  - [D. Runbooks & Checklists](#d-runbooks--checklists)
  - [E. Diagrams (Mermaid)](#e-diagrams-mermaid)
  - [F. Glossary](#f-glossary)

---

## 1. Executive Summary
I design, build, and operate **reliable, secure, performant, and cost-efficient** PostgreSQL platforms. My DBRE practice translates business outcomes into **SLOs** backed by **deep observability**, **safe change delivery**, **provable HA/DR** and **PITR**.

---

## 2. Role Scope & Value Proposition
- **Scope:** PostgreSQL 12–17+, OLTP/HTAP, self-managed and managed (RDS/Aurora, Cloud SQL/AlloyDB, Azure PG Flexible, etc.), Kubernetes operators.
- **Interfaces:** Application teams, SRE/Platform, SecOps, Data, Architecture, Leadership.
- **Value:** SLO-driven designs, automated operations, measurable availability/recovery, predictable performance, and audit-ready security.

---

## 3. Skills Matrix

### 3.1 Core DBRE Competencies
- SLI/SLO/SLA design • Error budgets • Incident handling • Postmortems (blameless) • DR/chaos drills • Toil reduction.
- Observability (metrics/logs/traces) • Performance & capacity engineering • Change safety (lower CFR) • FinOps.

### 3.2 PostgreSQL Stack
- **Core:** MVCC, autovacuum/VACUUM, checkpoints/WAL, JIT, parallelism.
- **Indexes:** B-tree, BRIN, GIN/GiST/SP-GiST, Hash; partial, expression, INCLUDE.
- **Features:** Declarative partitioning, JSONB & Full-Text Search, RLS.
- **Extensions:** `pg_stat_statements`, `auto_explain`, `pg_repack`, `pg_partman`, `pg_cron`, PgBouncer, pgpool-II, TimescaleDB, Citus.

### 3.3 Platform & Tooling
- **HA/DR:** Streaming replication (sync/async/quorum), logical replication; Patroni/repmgr/pg_auto_failover/Stolon.
- **Backup:** pgBackRest, Barman, `pg_basebackup`, WAL-G.
- **Observability:** Prometheus + exporters, Grafana, pgwatch2, ELK/Loki, OpenTelemetry.
- **IaC/CI/CD:** Terraform/Ansible/Helm/Kustomize; Flyway/Liquibase/Sqitch; GitHub Actions/Azure DevOps.

---

## 4. Reference Architecture & Environments

### 4.1 Topologies
- **Primary → replicas** (sync/async/quorum); **cascading**; **read scaling**.
- **Logical replication** (publications/subscriptions) for migrations and fan-out.
- **Sharding** (Citus) and **time-series** (TimescaleDB) when appropriate.

~~~mermaid
flowchart LR
  App -->|RW| PGB[(PgBouncer)]
  PGB --> PG0[(Primary)]
  PGB -.RO.-> R1[(Replica 1)]
  PGB -.RO.-> R2[(Replica 2)]
  PG0 -->|WAL| R1
  PG0 -->|WAL| R2
  R2 --> BAK[(Backups + WAL Archive)]
~~~

### 4.2 Cloud & Hybrid
- Private networking, IAM, TLS, proxies/poolers; **managed** (RDS/Aurora/Cloud SQL/Azure PG) vs **self-managed/K8s operators** (Zalando/Crunchy).

### 4.3 Data Flows & Serving Layers
- OLTP → CDC/Streams → Lake/Warehouse → BI/ML; **freshness SLOs** and **lag budgets** shape batch/stream windows.

---

## 5. Reliability Fundamentals

### 5.1 SLOs, SLIs, SLAs
~~~yaml
# SLOs-as-code (example)
service: orders-pg
slos:
  - name: p99_read_latency_ms    ; target: "< 40"  ; window: 30d
  - name: p99_commit_latency_ms  ; target: "< 120" ; window: 30d
  - name: error_rate_pct         ; target: "< 0.1" ; window: 30d
  - name: replica_lag_seconds    ; target: "<= 5"  ; window: 30d
  - name: restore_time_minutes   ; target: "<= 20" ; window: 30d
~~~

### 5.2 Error Budgets & Risk
~~~yaml
burn_policies:
  - if_burn_rate: "> 2.0x"
    action: "freeze risky changes; prioritize reliability backlog; schedule DR drill"
risk_register:
  - risk: "vacuum lag on hot tables"
    prob: "Medium" ; impact: "High" ; owner: "DBRE" ; due: "2025-11-01"
~~~

### 5.3 Incident Lifecycle & Postmortems
~~~markdown
**Lifecycle:** Detect → Triage → Mitigate → Recover → Review  
**Postmortem (template):** Summary | Timeline | Root Causes | Contributing Factors | What Went Well | Action Items (owners/dates)
~~~

---

## 6. Observability & Monitoring

### 6.1 Metrics & Dashboards
~~~yaml
# Prometheus scrape (postgres_exporter + pgbouncer_exporter)
scrape_configs:
  - job_name: postgres
    static_configs: [{ targets: ['pg-primary:9187','pg-rep1:9187','pg-rep2:9187'] }]
  - job_name: pgbouncer
    static_configs: [{ targets: ['pgbouncer:9127'] }]
~~~

~~~sql
-- Workload hot spots: top total exec time (pg_stat_statements)
SELECT queryid, calls,
       round(total_exec_time/1000,2) AS total_s,
       round(mean_exec_time,2) AS avg_ms,
       rows,
       left(regexp_replace(query, '\s+', ' ', 'g'), 160) AS sample
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;
~~~

~~~sql
-- Cache hit & QPS by database
SELECT datname,
       xact_commit + xact_rollback AS txns,
       round(100*(blks_hit::numeric/NULLIF(blks_read+blks_hit,0)),2) AS cache_hit_pct
FROM pg_stat_database
ORDER BY txns DESC;
~~~

~~~sql
-- PG16+: I/O waits by object/context (pg_stat_io)
SELECT backend_type, io_object, io_context,
       round(avg_read_time,2)  AS read_ms,
       round(avg_write_time,2) AS write_ms
FROM pg_stat_io
ORDER BY (avg_read_time + avg_write_time) DESC NULLS LAST
LIMIT 20;
~~~

### 6.2 Query Profiling & Plan Stability
~~~sql
-- EXPLAIN ANALYZE with buffers & WAL stats
EXPLAIN (ANALYZE, BUFFERS, WAL, TIMING, VERBOSE)
SELECT o.id, o.status, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'OPEN'
  AND o.created_at >= now() - interval '7 days'
ORDER BY o.created_at DESC
LIMIT 100;
~~~

~~~sql
-- Extended stats and per-column stats target
CREATE STATISTICS s_orders (dependencies) ON status, created_at FROM orders;
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 2000;
ANALYZE orders;
~~~

~~~sql
-- Track slow statements automatically
LOAD 'auto_explain';
SET auto_explain.log_min_duration = '300ms';
SET auto_explain.log_analyze = on;
SET auto_explain.log_buffers = on;
~~~

### 6.3 Logging, Alerting & On-Call
~~~conf
# postgresql.conf — logging essentials
log_line_prefix = '%m [%p] %q%u@%d '
log_min_duration_statement = 200ms
log_checkpoints = on
log_autovacuum_min_duration = 200ms
~~~

~~~yaml
# Alertmanager — actionable alert with runbook link
groups:
- name: postgres
  rules:
  - alert: ReplicaLagHigh
    expr: pg_replication_lag_seconds > 5
    for: 5m
    labels: { severity: page, service: orders-pg }
    annotations:
      summary: "Replica lag >5s on {{ $labels.instance }}"
      runbook: "runbooks/dr/replica-lag.md"
~~~

---

## 7. Capacity Planning & Performance

### 7.1 Baselines & Benchmarking
~~~bash
# pgbench baseline (example)
createdb bench
pgbench -i -s 100 bench
pgbench -c 64 -j 16 -T 900 bench | tee results/pgbench-$(date +%F).log
~~~

### 7.2 Schema & Query Tuning
~~~sql
-- Partial + expression index + INCLUDE
CREATE INDEX ix_orders_open_recent
  ON orders ((date_trunc('hour', created_at)), created_at DESC)
  INCLUDE (customer_id)
  WHERE status = 'OPEN' AND created_at >= now() - interval '7 days';

-- JSONB GIN and predicate
CREATE INDEX ix_orders_meta_gin ON orders USING gin (metadata jsonb_path_ops);
SELECT id FROM orders WHERE metadata ? 'coupon';
~~~

~~~sql
-- Partitioning & pruning (range by month)
CREATE TABLE events (
  id bigserial PRIMARY KEY,
  occurred_at timestamptz NOT NULL,
  payload jsonb NOT NULL
) PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2025_10 PARTITION OF events
  FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

-- Query benefits from pruning:
EXPLAIN SELECT count(*) FROM events
WHERE occurred_at >= '2025-10-01' AND occurred_at < '2025-11-01';
~~~

### 7.3 Resources, I/O & Storage
~~~conf
# postgresql.conf — baseline (tune per host/workload)
shared_buffers               = 16GB
effective_cache_size         = 48GB
work_mem                     = 64MB
maintenance_work_mem         = 2GB
max_wal_size                 = 32GB
checkpoint_timeout           = 15min
checkpoint_completion_target = 0.9
wal_compression              = on
effective_io_concurrency     = 200
random_page_cost             = 1.1
~~~

~~~sql
-- Autovacuum per-table tuning for a hot table
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_analyze_scale_factor = 0.02,
  autovacuum_vacuum_cost_limit = 4000
);
~~~

---

## 8. High Availability & Disaster Recovery

### 8.1 Physical & Logical Replication
~~~bash
# Physical replication (standby bootstrap)
# On primary:
psql -c "CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '***';"
echo "host replication replicator 10.0.0.0/24 scram-sha-256" >> $PGDATA/pg_hba.conf
pg_ctl reload

# On standby:
pg_basebackup -h pg-primary -U replicator -D $PGDATA -X stream -C -S slot_rep1 -R
# -R writes primary_conninfo and standby.signal
systemctl enable --now postgresql
~~~

~~~sql
-- Logical replication: publication + subscription
CREATE PUBLICATION pub_sales FOR TABLE orders, customers;
CREATE SUBSCRIPTION sub_sales
CONNECTION 'host=pg-primary dbname=app user=replicator password=***'
PUBLICATION pub_sales WITH (create_slot = true, slot_name = 'sub_sales_slot');
~~~

### 8.2 Failover Orchestration
~~~yaml
# Patroni (illustrative minimal)
scope: pg-prod
name: db-1
restapi: { listen: 0.0.0.0:8008, connect_address: db-1:8008 }
etcd: { host: etcd:2379 }
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    synchronous_mode: true
    synchronous_mode_strict: false
    postgresql:
      parameters:
        wal_keep_size: 2048
        max_wal_senders: 20
postgresql:
  listen: 0.0.0.0:5432
  connect_address: db-1:5432
  authentication:
    replication: { username: replicator, password: "***" }
    superuser:   { username: postgres,   password: "***" }
  data_dir: /var/lib/postgresql/data
~~~

~~~ini
; repmgr.conf (snippet)
node_id=1
node_name=pg1
conninfo='host=pg1 dbname=repmgr user=repmgr password=***'
data_directory='/var/lib/pgsql/data'
monitoring_history=yes
failover=automatic
promote_command='repmgr standby promote -f /etc/repmgr.conf'
follow_command='repmgr standby follow -f /etc/repmgr.conf --upstream-node-id=%n'
~~~

### 8.3 Backups, PITR & DR Testing
~~~conf
# pgBackRest — server config (snippet)
[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=8
start-fast=y

[app]
pg1-path=/var/lib/pgsql/data
pg1-port=5432
~~~

~~~bash
# pgBackRest usage
pgbackrest --stanza=app --type=full backup
pgbackrest --stanza=app check
# PITR to timestamp:
pgbackrest --stanza=app restore --type=time "--target=2025-10-08 12:20:00" --target-action=promote
~~~

~~~ini
# Barman — alternative (excerpt)
[barman]
barman_user = barman
barman_home = /var/lib/barman
compression = gzip

[pg-app]
description = "App PG"
conninfo = host=pg-primary user=barman dbname=postgres
backup_method = postgres
streaming_archiver = on
~~~

---

## 9. Security, Compliance & Governance

### 9.1 Identity & Access (RBAC, RLS)
~~~sql
-- Role hierarchy with least privilege
CREATE ROLE ro_analytics NOINHERIT;
GRANT CONNECT ON DATABASE app TO ro_analytics;
GRANT USAGE ON SCHEMA public TO ro_analytics;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro_analytics;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ro_analytics;

-- Row-Level Security per tenant
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::int);
~~~

~~~conf
# pg_hba.conf — enforce SCRAM & TLS
hostssl  app  all  10.0.0.0/24  scram-sha-256
hostnossl app  all  0.0.0.0/0   reject
~~~

### 9.2 Encryption & Secrets
~~~conf
# postgresql.conf — TLS
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file  = 'server.key'
ssl_ciphers   = 'HIGH:!aNULL:!MD5'
~~~

~~~sql
-- pgcrypto example (column encryption at app discretion)
CREATE EXTENSION IF NOT EXISTS pgcrypto;
INSERT INTO customers (name, ssn_enc)
VALUES ('Alice', pgp_sym_encrypt('123-45-6789', current_setting('app.kek')));
~~~

### 9.3 Auditing, Privacy & Data Masking
~~~conf
# pgaudit
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'write, ddl, role'
pgaudit.log_parameter = on
~~~

~~~sql
-- Mask via view
CREATE VIEW v_orders_masked AS
SELECT id, tenant_id, customer_id, status,
       CASE WHEN current_setting('app.role') = 'analyst' THEN '***' ELSE notes END AS notes,
       created_at
FROM orders;
GRANT SELECT ON v_orders_masked TO ro_analytics;
~~~

---

## 10. Change Management & Release Engineering

### 10.1 GitOps & Infrastructure as Code
~~~yaml
# Terraform remote state backends (examples)
# AWS: S3 + DynamoDB lock; GCP: GCS; Azure: Storage; (configure per env)
~~~

~~~yaml
# Policy-as-code gate (pseudo) — block deploys if SLO burn high
if: error_budget_burn_rate > 2.0
then: block_change("SLO burn too high")
~~~

### 10.2 Database CI/CD
~~~properties
# Flyway config
flyway.url=jdbc:postgresql://pg-primary:5432/app?sslmode=require
flyway.user=app_migrator
flyway.password=${APP_MIGRATOR_PWD}
flyway.locations=filesystem:./db/migrations
flyway.baselineOnMigrate=true
flyway.outOfOrder=false
~~~

~~~sql
-- V1__create_orders.sql (Flyway)
CREATE TABLE orders (
  id          BIGSERIAL PRIMARY KEY,
  tenant_id   INT NOT NULL,
  customer_id BIGINT NOT NULL,
  status      TEXT NOT NULL,
  notes       TEXT,
  created_at  timestamptz DEFAULT now()
);
CREATE INDEX ix_orders_status_created ON orders(status, created_at DESC);
~~~

~~~xml
<!-- Liquibase changelog snippet -->
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog">
  <changeSet id="add-orders-idx" author="dbre">
    <createIndex tableName="orders" indexName="ix_orders_customer">
      <column name="customer_id"/>
    </createIndex>
  </changeSet>
</databaseChangeLog>
~~~

~~~yaml
# GitHub Actions — prechecks + migrations + smoke tests
name: db-migrate
on: { push: { paths: ["db/migrations/**"] } }
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Flyway
        run: |
          curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.0.0/flyway-commandline-10.0.0-linux-x64.tar.gz | tar xz
          sudo ln -s $PWD/flyway-10.0.0/flyway /usr/local/bin/flyway
      - name: Precheck (locks/long TX)
        env: { DB_URL: ${{ secrets.DB_URL }} }
        run: |
          psql "$DB_URL" -v ON_ERROR_STOP=1 -c "SELECT pid, now()-xact_start age, query FROM pg_stat_activity WHERE state<>'idle' AND xact_start IS NOT NULL ORDER BY age DESC LIMIT 10;"
      - name: Migrate
        run: flyway -configFiles=db/flyway.conf migrate
      - name: Smoke test
        run: psql "${{ secrets.DB_URL }}" -c "SELECT count(*) FROM orders;"
~~~

### 10.3 Safe Deployment Patterns
~~~markdown
- **Blue/Green schema:** write both, read from old; flip reads post-verify.
- **Canary cohorts:** gradually enable new paths via feature flags.
- **Shadow writes:** dual-write to validate shape/constraints, read from primary path.
- **Rollback/PITR:** validated recovery playbooks with timed RTO/RPO targets.
~~~

---

## 11. Automation & Runbooks

### 11.1 Provisioning, Patching & Upgrades
~~~yaml
# Ansible — install + template postgresql.conf
- hosts: postgres
  become: true
  tasks:
    - name: Install PostgreSQL
      package: { name: [postgresql, postgresql-server], state: present }
    - name: Deploy postgresql.conf
      template: { src: templates/postgresql.conf.j2, dest: /var/lib/pgsql/data/postgresql.conf }
      notify: Restart PG
  handlers:
    - name: Restart PG
      service: { name: postgresql, state: restarted, enabled: yes }
~~~

~~~bash
# Major upgrade rehearsal (pg_upgrade, simplified)
initdb -D /pg/new
pg_upgrade -d /pg/old -D /pg/new -b /usr/pgsql-16/bin -B /usr/pgsql-17/bin -j 8
vacuumdb -j 8 -d app --analyze-in-stages
~~~

### 11.2 Health Checks & Auto-Remediation
~~~sql
-- Long running transactions
SELECT pid, usename, now()-xact_start AS age, state, query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL AND state <> 'idle'
ORDER BY age DESC
LIMIT 20;

-- Wraparound risk
SELECT datname, age(datfrozenxid) AS age FROM pg_database ORDER BY age DESC;
~~~

~~~bash
# Simple watchdog for replica lag (psql)
LAG=$(psql -Atc "SELECT COALESCE(EXTRACT(EPOCH FROM now()-pg_last_xact_replay_timestamp())::int,0)")
[ "${LAG:-0}" -gt 5 ] && /usr/local/bin/page "Replica lag ${LAG}s on $(hostname)"
~~~

### 11.3 Operational Playbooks
~~~markdown
**Promote Replica (Streaming)**
1) Freeze risky changes; drain writes.
2) `pg_ctl promote` (or Patroni planned switchover).
3) Update VIP/DNS/pgBouncer to new writer.
4) Repoint old primary as replica (`pg_rewind` or re-basebackup).
5) Validate probes, dashboards, lag 0; close change ticket.

**PITR Drill (pgBackRest)**
1) `pgbackrest restore --stanza=app --type=time --target="YYYY-MM-DD HH:MM:SS" --target-action=promote`
2) Start instance; run smoke tests; capture RTO/RPO evidence.
3) Document deviations and create action items.
~~~

---

## 12. Data Integration & Replication

### 12.1 CDC & ETL/ELT
~~~json
{
  "name": "debezium-postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "pg-primary",
    "database.port": "5432",
    "database.user": "cdc",
    "database.password": "****",
    "database.dbname": "app",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_app",
    "publication.name": "pub_app",
    "table.include.list": "public.orders,public.customers",
    "tombstones.on.delete": "false"
  }
}
~~~

### 12.2 FDWs & Heterogeneous Replication
~~~sql
-- postgres_fdw example
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE SERVER remote_pg FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'pg-remote', dbname 'ext');
CREATE USER MAPPING FOR app SERVER remote_pg OPTIONS (user 'app', password '***');
CREATE FOREIGN TABLE ext_orders (id bigint, status text)
  SERVER remote_pg OPTIONS (schema_name 'public', table_name 'orders');
SELECT count(*) FROM ext_orders WHERE status = 'OPEN';
~~~

### 12.3 Streaming & Analytics
~~~sql
-- Materialized view refresh strategy
CREATE MATERIALIZED VIEW mv_recent_orders AS
SELECT * FROM orders WHERE created_at >= now() - interval '1 day';
-- Refresh window controlled by freshness SLO
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_recent_orders;
~~~

---

## 13. Cost & Efficiency

### 13.1 Managed vs Self-Managed Trade-offs
~~~markdown
- **Managed:** SLA, backups/PITR, easy HA; limits & cost premiums; vendor features.
- **Self-managed:** full control & tuning; operational overhead; bespoke HA/DR.
~~~

### 13.2 Right-Sizing & Scaling
~~~markdown
- Keep ≥30% headroom for CPU/IO; scale read replicas for analytics/reads.
- Move hot tables to partitions; offload batch to replicas or warehouses.
- Use connection pooling (PgBouncer; transaction mode) to cap backend churn.
~~~

### 13.3 Storage & Network Economics
~~~markdown
- Prefer SSD/NVMe for WAL & hot data; tune checkpoint completion; compress WAL.
- Archive logs to low-cost object storage; control cross-region egress; optimize snapshot retention.
~~~

---

## 14. Reliability Case Studies
~~~markdown
- **A — Eliminate failover flaps:** Patroni quorum tuning + fenced VIP → 0 Sev-1 in 6 months; RTO < 30s.
- **B — Plan stability:** extended stats + partial indexes + auto_explain → p99 −42%, CFR −55%.
- **C — DR proven:** pgBackRest full+incr+WAL; weekly restore timings → RPO < 60s, RTO 12m.
~~~

---

## 15. KPIs, Dashboards & Reporting
~~~markdown
**Monthly Reliability Summary (Template)**
- Availability: 99.97% (SLO: 99.95%) ✅
- Error budget burn: 27% (policy < 50%)
- Incidents: Sev-1:0, Sev-2:1, Sev-3:3 (MTTR: 21m)
- Changes: 52 deploys, CFR: 3.0%
- DR: 1 drill passed — RTO 11m (≤20m), RPO 60s
- Risks: bloat growth in `orders` (mitigate Q4)
~~~

---

## 16. Standards & Conventions
~~~markdown
- **Naming:** `pg-{env}-{service}-{role}`; VIPs; pools `rw`/`ro`; schemas per domain.
- **Docs:** ADRs, runbook templates, SQL/psql style, change tickets linked to SLOs.
- **Git:** trunk-based or GitFlow; signed commits; CODEOWNERS; mandatory reviews.
~~~

---

## 17. Roadmap & Continuous Improvement
~~~markdown
- **Q1:** 100% SLO coverage for tier-1; weekly automated restore tests.
- **Q2:** Unified Patroni/repmgr strategy; policy-as-code; drift detection.
- **Q3:** Observability v2 (pg_stat_io, tracing); partition hot tables.
- **Q4:** Cost optimization; zero-touch patching; retire legacy runbooks.
~~~

---

## 18. Appendices & Templates

### A. Scripts (SQL/Bash)
~~~sql
-- Who blocks whom (locks)
WITH locks AS (
  SELECT bl.pid AS blocked_pid, kl.pid AS locker_pid
  FROM pg_locks bl
  JOIN pg_locks kl ON kl.locktype = bl.locktype
    AND kl.database IS NOT DISTINCT FROM bl.database
    AND kl.relation IS NOT DISTINCT FROM bl.relation
    AND kl.page IS NOT DISTINCT FROM bl.page
    AND kl.tuple IS NOT DISTINCT FROM bl.tuple
    AND kl.virtualxid IS NOT DISTINCT FROM bl.virtualxid
    AND kl.transactionid IS NOT DISTINCT FROM bl.transactionid
    AND kl.classid IS NOT DISTINCT FROM bl.classid
    AND kl.objid IS NOT DISTINCT FROM bl.objid
    AND kl.objsubid IS NOT DISTINCT FROM bl.objsubid
    AND kl.pid <> bl.pid
    AND kl.granted AND NOT bl.granted
)
SELECT l.blocked_pid, a.query AS blocked_query,
       l.locker_pid,  p.query AS locker_query
FROM locks l
JOIN pg_stat_activity a ON a.pid = l.blocked_pid
JOIN pg_stat_activity p ON p.pid = l.locker_pid;
~~~

~~~sql
-- Bloat approximation
WITH s AS (
  SELECT schemaname, relname, n_live_tup, n_dead_tup
  FROM pg_stat_user_tables
)
SELECT schemaname, relname,
       round(n_dead_tup::numeric/NULLIF(n_live_tup,0),3) AS dead_ratio
FROM s
ORDER BY dead_ratio DESC NULLS LAST
LIMIT 20;
~~~

~~~bash
# Log rotate & compress
DATE=$(date +%F)
mv $PGDATA/log/postgresql.log $PGDATA/log/postgresql-$DATE.log
kill -HUP $(head -1 $PGDATA/postmaster.pid)
gzip $PGDATA/log/postgresql-$DATE.log
~~~

### B. IaC & Config (Terraform/Ansible/K8s)
~~~hcl
# Terraform — illustrative VM + security bits (adjust for your cloud/provider)
variable "cidr_app" { default = "10.0.0.0/16" }
# (Network/compute omitted for brevity)
~~~

~~~yaml
# Crunchy PGO (K8s) — PostgresCluster (simplified)
apiVersion: postgres-operator.crunchydata.com/v1beta1
kind: PostgresCluster
metadata: { name: app-pg }
spec:
  instances:
    - name: rw
      replicas: 3
  backups:
    pgbackrest:
      repos:
        - name: repo1
          volume: { size: 500Gi }
  users:
    - name: app
      databases: ["app"]
~~~

~~~ini
# PgBouncer (ini via ConfigMap — key settings)
[databases]
app = host=pg-primary port=5432 dbname=app pool_size=50

[pgbouncer]
auth_type   = scram-sha-256
pool_mode   = transaction
max_client_conn = 1000
default_pool_size = 50
~~~

### C. Pipelines (GitHub Actions/Azure DevOps)
~~~yaml
# Azure DevOps — Liquibase + smoke tests
stages:
- stage: Validate
  jobs:
  - job: Lint
    steps:
    - script: echo "Lint SQL & schema"
- stage: Migrate
  dependsOn: Validate
  jobs:
  - job: Liquibase
    steps:
    - bash: |
        curl -L https://download.liquibase.com/download/liquibase-4.27.0.tar.gz | tar xz
        ./liquibase --url="$(DB_URL)" --changelog-file=db/changelog.xml update
    - bash: psql "$(DB_URL)" -c "SELECT 1;"
~~~

### D. Runbooks & Checklists
~~~markdown
## Patch Day
- [ ] Backups OK + restore test < 24h
- [ ] Change window approved; stakeholders notified
- [ ] Rolling plan (Patroni/repmgr or primary→replicas)
- [ ] Baseline captures (dashboards, pg_stat_* snapshots)
- [ ] Post-patch validation (SLO probes, lag, errors)
~~~

~~~markdown
## DR Drill
- [ ] Full restore + PITR on clean host
- [ ] Time RTO; compute RPO
- [ ] Smoke tests (app connectivity, critical queries)
- [ ] Record findings vs targets; open actions
~~~

### E. Diagrams (Mermaid)
~~~mermaid
flowchart TB
  subgraph ControlPlane[Failover Control Plane]
    ETC[(etcd/Consul)]
  end
  subgraph DataPlane[PostgreSQL Cluster]
    P0[(Primary)]
    R1[(Replica 1)]
    R2[(Replica 2)]
  end
  P0 -- WAL --> R1
  P0 -- WAL --> R2
  ETC --- P0
  ETC --- R1
  ETC --- R2
  LB((VIP/DNS/Proxy)) --> P0
  LB -.RO.-> R1
  LB -.RO.-> R2
~~~

### F. Glossary
- **DBRE:** Database Reliability Engineering  
- **SLA/SLO/SLI:** Agreement/Objectives/Indicators  
- **MTTR/MTTD:** Mean Time to Recover/Detect  
- **PITR:** Point-in-Time Recovery  
- **RLS:** Row-Level Security  
- **FDW:** Foreign Data Wrapper  
- **CFR:** Change Failure Rate
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


