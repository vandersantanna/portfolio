# Python Automation for DBA • DBRE • DataOps — Portfolio

> A practical, code-first portfolio demonstrating how to design, build, and operate production-grade automation with Python for multi-DBMS environments (Oracle, SQL Server, PostgreSQL, MySQL, MongoDB, Redis) across on-prem and cloud (AWS, Azure, GCP, OCI).

---

## Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Architecture Overview](#2-architecture-overview)
- [3. Python for Operations: Foundations](#3-python-for-operations-foundations)
- [4. Project Structure & Standards](#4-project-structure--standards)
- [5. Observability by Design](#5-observability-by-design)
- [6. Configuration & Secrets Management](#6-configuration--secrets-management)
- [7. Database Connectivity Abstractions](#7-database-connectivity-abstractions)
- [8. Orchestration](#8-orchestration)
- [9. CI/CD for Data & DB Automation](#9-cicd-for-data--db-automation)
- [10. Infrastructure as Code (IaC) & Platform as Code (PaC)](#10-infrastructure-as-code-iac--platform-as-code-pac)
- [11. Provisioning & Bootstrapping](#11-provisioning--bootstrapping)
- [12. Backup & Recovery Automation](#12-backup--recovery-automation)
- [13. HA/DR Orchestration](#13-hadr-orchestration)
- [14. Patching & Upgrades](#14-patching--upgrades)
- [15. Performance Diagnostics & Tuning](#15-performance-diagnostics--tuning)
- [16. Capacity Planning & Cost Optimization](#16-capacity-planning--cost-optimization)
- [17. Security & Compliance Automation](#17-security--compliance-automation)
- [18. SLOs, Error Budgets & DBRE Practices](#18-slos-error-budgets--dbre-practices)
- [19. Release Management & Database Migrations](#19-release-management--database-migrations)
- [20. DataOps Pipelines](#20-dataops-pipelines)
- [21. Data Quality, Testing & Governance](#21-data-quality-testing--governance)
- [22. Streaming & Real-Time Operations](#22-streaming--real-time-operations)
- [23. ChatOps & Incident Automation](#23-chatops--incident-automation)
- [24. Job Queues & Schedulers](#24-job-queues--schedulers)
- [25. Cross-Engine Playbooks (DB-Specific)](#25-cross-engine-playbooks-db-specific)
- [26. Cloud Integrations](#26-cloud-integrations)
- [27. Packaging & Distribution](#27-packaging--distribution)
- [28. Testing Strategy](#28-testing-strategy)
- [29. Supply Chain Security](#29-supply-chain-security)
- [30. Sample Portfolio Projects (Case Studies)](#30-sample-portfolio-projects-case-studies)
- [31. How to Run (Quickstart)](#31-how-to-run-quickstart)
- [32. KPIs & Reporting](#32-kpis--reporting)
- [33. Roadmap & Next Steps](#33-roadmap--next-steps)
- [34. Appendices](#34-appendices)
  - [A. Reusable Code Templates](#a-reusable-code-templates)
  - [B. Operational Checklists](#b-operational-checklists)
  - [C. Reference Diagrams (Mermaid)](#c-reference-diagrams-mermaid)
  - [D. Glossary](#d-glossary)

---

## 1. Executive Summary

**Scope.** End-to-end Python automation for:
- **DBA:** provisioning, patching, backups, recovery drills, performance checks, HA/DR runbooks.
- **DBRE:** SLOs/SLIs, burn-rate alerts, toil reduction, incident automation, chaos drills.
- **DataOps:** ingestion/CDC, transformations (dbt), quality gates, orchestration, lineage.

**Outcomes & KPIs.**
- **Lead Time for Changes** ↓  
- **Change Failure Rate** ↓  
- **MTTR** ↓ with automated triage & runbooks  
- **Data Freshness & SLAs** ↑ with observable pipelines  
- **Availability vs SLO** tracked and enforced with error budgets

```mermaid
graph LR
A[Change] --> B[CI/CD]
B --> C[Automations]
C --> D[DB/Pipeline]
D --> E[Observability]
E --> F[SLO Report]
```

---

## 2. Architecture Overview

- **Control plane:** orchestration (Airflow/Prefect), CI/CD, secrets, IaC, policy.
- **Data plane:** DB engines, storage, compute, network.
- **Scheduling vs event-driven:** cron/DAGs, message queues, cloud events.
- **Resilience:** retries with backoff, idempotent tasks, saga/compensation.

**Design tenets:** _stateless workers, declarative configs, least privilege, immutability, progressive delivery, observability-first_.

---

## 3. Python for Operations: Foundations

- **Tooling:** Poetry/uv, pyproject.toml, Black, Ruff, mypy, pre-commit.
- **CLI frameworks:** Typer/Click for operator UX.
- **Config:** pydantic-settings, YAML/TOML, `.env`.
- **Concurrency:** asyncio for IO-bound, multiprocessing for CPU-bound.
- **Reliability:** `tenacity` retries, circuit breakers, timeouts, idempotency keys.

```python
# src/ops/cli.py
import asyncio, json, os, sys
import typer
from tenacity import retry, stop_after_attempt, wait_exponential
app = typer.Typer(no_args_is_help=True, add_completion=False)

@retry(stop=stop_after_attempt(5), wait=wait_exponential(1, 16))
async def do_work(item: str) -> str:
    # Simulate idempotent operation with timeout
    await asyncio.wait_for(asyncio.sleep(0.2), timeout=5)
    return f"ok:{item}"

@app.command()
def run(batch: int = 10):
    results = asyncio.run(asyncio.gather(*(do_work(f"t{i}") for i in range(batch))))
    typer.echo(json.dumps({"count": len(results), "sample": results[:3]}))

if __name__ == "__main__":
    app()
```

---

## 4. Project Structure & Standards

```
python-automation-ops/
├── pyproject.toml
├── Makefile
├── .pre-commit-config.yaml
├── src/ops/...
├── tests/...
└── infra/ (terraform/ansible/docker)
```

```toml
# pyproject.toml (excerpt)
[project]
name = "python-automation-ops"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["typer","pydantic-settings","tenacity","oracledb","psycopg[binary]","pyodbc","mysqlclient","pymongo","redis","prometheus-client","opentelemetry-api","opentelemetry-sdk","opentelemetry-exporter-otlp"]
```

```yaml
# .pre-commit-config.yaml
repos:
- repo: https://github.com/psf/black
  rev: 24.8.0
  hooks: [{id: black}]
- repo: https://github.com/charliermarsh/ruff-pre-commit
  rev: v0.6.9
  hooks: [{id: ruff, args: ["--fix"]}]
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.11.2
  hooks: [{id: mypy}]
```

---

## 5. Observability by Design

- **Structured logs** (JSON), correlation IDs.
- **Metrics** via Prometheus client: custom DB probes.
- **Tracing** with OpenTelemetry (OTLP).

```python
# src/ops/obs.py
import json, logging, os, time
from prometheus_client import Counter, Gauge, start_http_server
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO"), format="%(message)s")
log = logging.getLogger("ops")

DB_LAT = Gauge("db_query_latency_ms", "DB query latency", ["engine","op"])
FAILS = Counter("ops_failures_total", "Failures", ["stage"])

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTLP_ENDPOINT","http://otel:4318/v1/traces"))))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

def json_log(**kv): log.info(json.dumps(kv))

def observe_latency(engine, op, ms):
    DB_LAT.labels(engine, op).set(ms)

def start_metrics(port=9100):
    start_http_server(port)
    json_log(event="metrics_server_started", port=port)
```

---

## 6. Configuration & Secrets Management

- **pydantic-settings** + `.env` for local, cloud KMS for prod.
- **Rotations** & short-lived tokens (IAM/OIDC).

```python
# src/ops/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"
    otlp_endpoint: str = "http://localhost:4318/v1/traces"
    oracle_dsn: str
    sqlserver_dsn: str
    postgres_dsn: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

---

## 7. Database Connectivity Abstractions

- **Drivers:** `oracledb`, `pyodbc` (SQL Server), `psycopg`, `mysqlclient`, `pymongo`, `redis`.
- **Patterns:** pooled connections, parameterized SQL, timeouts, circuit breakers.

```python
# src/ops/db/core.py
import contextlib, time
from typing import Iterator, Any
import oracledb, psycopg, mysql.connector, pyodbc

@contextlib.contextmanager
def oracle_conn(dsn: str) -> Iterator[oracledb.Connection]:
    conn = oracledb.connect(dsn, timeout=5)
    try: yield conn
    finally: conn.close()

def safe_exec(cursor, sql: str, params: tuple[Any,...] = ()):
    start = time.time()
    cursor.execute(sql, params)
    return cursor.fetchall(), (time.time() - start) * 1000.0
```

**Safe examples (parametrized):**

```python
# Postgres
with psycopg.connect(settings.postgres_dsn, connect_timeout=5) as conn:
    with conn.cursor() as cur:
        rows, ms = safe_exec(cur, "SELECT * FROM users WHERE id = %s", (42,))
```

---

## 8. Orchestration

**Airflow DAG skeleton (idempotent DB op):**
```python
# dags/db_backup_verify.py
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta

with DAG("db_backup_verify", start_date=datetime(2024,1,1),
         schedule_interval="0 3 * * *", catchup=False, default_args={"retries": 3, "retry_delay": timedelta(minutes=5)}) as dag:

    @task
    def run_backup():
        # call Python CLI / shell out to RMAN/pgBackRest
        return "ok"

    @task
    def verify_restore():
        # restore to ephemeral instance, run checksum
        return "ok"

    run_backup() >> verify_restore()
```

**Prefect flow:**
```python
from prefect import flow, task

@task(retries=3, retry_delay_seconds=60)
def snapshot_db(): ...
@task
def verify(): ...

@flow
def nightly_backup():
    a = snapshot_db()
    b = verify(wait_for=[a])
    return b
```

---

## 9. CI/CD for Data & DB Automation

- **Pipelines:** lint → typecheck → unit/integration → package → publish.
- **OIDC** to clouds (no long-lived secrets).
- **Promotion:** dev → test → prod with gates & change windows.

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]
jobs:
  build:
    permissions: {id-token: write, contents: read}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv pip install -e .[dev]
      - run: ruff check .
      - run: black --check .
      - run: mypy src
      - run: pytest -q
```

```yaml
# .gitlab-ci.yml (excerpt)
stages: [lint, test, build, release]
lint:
  stage: lint
  image: python:3.11
  script: [ "pip install -e .[dev]", "ruff check .", "black --check .", "mypy src" ]
```

---

## 10. Infrastructure as Code (IaC) & Platform as Code (PaC)

**Terraform** to provision DB services, networks, KMS; **Ansible** for OS/DB config; **Policy as Code** with OPA/Conftest.

```hcl
# infra/terraform/main.tf (excerpt)
provider "aws" { region = var.region }
module "vpc" { source = "terraform-aws-modules/vpc/aws"; name = "dbre"; cidr = "10.0.0.0/16" }
module "rds" { source = "terraform-aws-modules/rds/aws"; identifier = "pg"; engine = "postgres"; engine_version = "16" }
```

```yaml
# infra/ansible/site.yaml
- hosts: db
  become: true
  roles:
    - role: postgres
      vars: {pg_version: 16, shared_buffers: "8GB"}
```

```rego
# policy/service.rego (OPA)
package svc
deny[msg] {
  input.resource == "db"
  not input.encrypted
  msg := "DB must be encrypted at rest"
}
```

---

## 11. Provisioning & Bootstrapping

- Automated installs, users/roles, parameter baselines, tablespaces.
- Golden images (Packer) or containers for ephemeral CI.

```bash
# Makefile (excerpt)
bootstrap:
	python -m ops.cli run --batch 1
provision-db:
	ansible-playbook infra/ansible/site.yaml -i infra/ansible/inventory
```

---

## 12. Backup & Recovery Automation

- **Strategies:** full/incremental, PITR, snapshot vs logical.
- **Verification:** automated restore drills; checksum and canary queries.

```bash
# PostgreSQL pgBackRest (bash)
pgbackrest --stanza=main backup --type=diff
pgbackrest --stanza=main restore --type=time --target="2025-10-12 02:00:00" --delta
```

```sql
-- Oracle RMAN script (snippet)
RUN {
  ALLOCATE CHANNEL c1 DEVICE TYPE DISK;
  BACKUP INCREMENTAL LEVEL 1 DATABASE PLUS ARCHIVELOG;
  CROSSCHECK BACKUP;
  DELETE NOPROMPT OBSOLETE;
}
```

---

## 13. HA/DR Orchestration

- **Oracle:** Data Guard/FSFO; **SQL Server:** AlwaysOn AG; **PostgreSQL:** Patroni; **MySQL:** Group Replication.
- Fencing/quorum, lag monitoring, automated **switchover/failover** with controlled DNS cutover.

```python
# src/ops/hadr/failover.py
from typing import Literal
import socket, subprocess
Role = Literal["primary","standby"]

def promote_postgres(patroni_url: str): subprocess.check_call(["patronictl","switchover","--force","--master","pg1","--candidate","pg2"])
def dns_cutover(name: str, new_ip: str): # call provider API
    print(f"Update {name} -> {new_ip}")
```

---

## 14. Patching & Upgrades

- Rolling strategies, pre/post checks, automated rollback.
- Blue/green for DB (read replicas → promote).

```bash
# SQL Server patching (PowerShell concept)
Install-WindowsUpdate -KBArticleID KB503XXXX -AcceptAll -AutoReboot
```

---

## 15. Performance Diagnostics & Tuning

- **Workload capture:** AWR/ASH, Query Store, `pg_stat_statements`.
- **Regression detection:** compare plan hash/latency percentiles.

```sql
-- PostgreSQL: detect slow queries (example)
SELECT query, calls, mean_exec_time, stddev_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

```python
# src/ops/perf/regression.py
import statistics as stats
def is_regressed(p50_old, p50_new, threshold=1.3): return (p50_new / p50_old) >= threshold
```

---

## 16. Capacity Planning & Cost Optimization

- Growth modeling, headroom alerts; IOPS/throughput right-sizing.
- Cloud cost telemetry & anomaly detection with tags.

```python
# src/ops/capacity/model.py
def forecast(next_days:int, series:list[float])->list[float]:
    # naive trend + seasonality placeholder
    slope = (series[-1]-series[0])/max(1,len(series)-1)
    return [series[-1]+slope*(i+1) for i in range(next_days)]
```

---

## 17. Security & Compliance Automation

- TDE/KMS, TLS in transit, RBAC, audit trails, CIS checks.
- Evidence collection for audits.

```bash
# Secrets scanning in CI
gitleaks detect --source . --no-git -v
```

---

## 18. SLOs, Error Budgets & DBRE Practices

- SLIs: availability, latency, freshness.
- Burn-rate alerts (fast/slow) + runbooks; toil tracking.

```yaml
# slo.yaml (concept)
availability:
  objective: 99.9
  window_days: 30
latency_p95_ms:
  objective: 200
freshness_minutes:
  objective: 5
```

---

## 19. Release Management & Database Migrations

- Schema versioning: Flyway/Liquibase/Alembic/DACPAC.
- Expand/contract, feature flags, backfills.

```sql
-- Flyway V002__add_index_users_email.sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);
```

```python
# Alembic revision (snippet)
def upgrade(): op.add_column("orders", sa.Column("region", sa.String(length=32), nullable=True))
def downgrade(): op.drop_column("orders", "region")
```

---

## 20. DataOps Pipelines

- Ingestion/CDC (Airbyte, Debezium), batch vs streaming.
- Transformations with **dbt**, environments & promotions.

```yaml
# dbt_project.yml (excerpt)
name: analytics
profile: analytics
models:
  analytics:
    +materialized: incremental
    +on_schema_change: append_new_columns
```

---

## 21. Data Quality, Testing & Governance

- Great Expectations/Deequ, data contracts, lineage (OpenLineage/Marquez).

```python
# great_expectations (example)
from great_expectations.dataset import PandasDataset
df = PandasDataset({"a":[1,2,3]})
df.expect_column_values_to_not_be_null("a")
```

---

## 22. Streaming & Real-Time Operations

- Kafka topics/partitions, consumer groups, DLQs, exactly-once patterns.

```python
# src/ops/stream/consumer.py
from kafka import KafkaConsumer
c = KafkaConsumer("events", bootstrap_servers=["kafka:9092"], enable_auto_commit=False)
for msg in c:
    try:
        process(msg.value)
        c.commit()
    except Exception:
        send_to_dlq(msg)
```

---

## 23. ChatOps & Incident Automation

- Slack/Teams bots, triage playbooks, pager integration.

```python
# src/ops/chatops/slack_bot.py
import os, requests
def notify(text:str):
    requests.post(os.environ["SLACK_WEBHOOK"], json={"text": text})
```

---

## 24. Job Queues & Schedulers

- Celery/RQ for distributed workers; priority queues; idempotent tasks.

```python
# src/ops/queue/celery_app.py
from celery import Celery
app = Celery(__name__, broker="redis://redis:6379/0", backend="redis://redis:6379/1")
@app.task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def run_backup(db_name:str): ...
```

---

## 25. Cross-Engine Playbooks (DB-Specific)

### 25.1 Oracle
- ASM/ACFS, RMAN, Data Guard, AWR/ASH, PDB/CDB.
```sql
-- AWR top waits (example)
SELECT * FROM dba_hist_system_event WHERE event LIKE 'db file%read%' FETCH FIRST 10 ROWS ONLY;
```

### 25.2 SQL Server
- AlwaysOn AG, Ola jobs, Query Store, Agent jobs.
```sql
-- Query Store regression candidates
SELECT TOP 20 qsq.query_sql_text, rs.avg_duration, rs.last_duration
FROM sys.query_store_runtime_stats rs
JOIN sys.query_store_plan p ON p.plan_id = rs.plan_id
JOIN sys.query_store_query_text qsq ON qsq.query_text_id = (SELECT query_text_id FROM sys.query_store_query WHERE query_id = p.query_id);
```

### 25.3 PostgreSQL
- Patroni, pgBackRest, autovacuum tuning, logical replication.
```sql
-- Autovacuum health
SELECT schemaname, relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;
```

### 25.4 MySQL/MariaDB
- XtraBackup, Group Replication, Performance Schema.
```sql
-- Top waits
SELECT EVENT_NAME, COUNT_STAR, SUM_TIMER_WAIT FROM performance_schema.events_waits_summary_global_by_event_name ORDER BY SUM_TIMER_WAIT DESC LIMIT 20;
```

### 25.5 MongoDB
- Replica sets, sharding, balancer.
```javascript
// Replica set status
rs.status()
```

### 25.6 Redis
- Cluster/Sentinel, RDB/AOF, eviction.
```bash
redis-cli INFO memory
```

---

## 26. Cloud Integrations

- **AWS:** RDS/Aurora, Lambda, CloudWatch, Backup, KMS.  
- **Azure:** SQL MI/DB, Functions, Monitor/Log Analytics, Key Vault.  
- **GCP:** Cloud SQL/AlloyDB, Cloud Run, Cloud Logging/Monitoring, KMS.  
- **OCI:** Autonomous DB, Exadata Cloud, Events/Functions, Vault.

```yaml
# CloudWatch agent config (excerpt)
metrics:
  metrics_collected:
    procstat:
      measurement: [cpu_usage, memory_rss]
      resources: ["python"]
```

---

## 27. Packaging & Distribution

- Docker multi-stage builds, distroless; PEX/zipapps for on-prem; SBOM/signing.

```dockerfile
# Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install uv && uv pip install -e .
COPY src ./src
ENTRYPOINT ["python","-m","ops.cli"]
```

---

## 28. Testing Strategy

- Unit/integration (pytest), **Testcontainers** for DBs, golden datasets, chaos experiments.

```python
# tests/test_db.py
import pytest, psycopg
def test_query_ok():
    with psycopg.connect("postgresql://test:test@localhost:5432/test") as c:
        with c.cursor() as cur:
            cur.execute("SELECT 1")
            assert cur.fetchone()[0] == 1
```

---

## 29. Supply Chain Security

- Code scans (bandit), deps (pip-audit), container (trivy/grype), SBOMs, provenance (SLSA).

```bash
pip-audit -r requirements.txt
trivy image ghcr.io/org/python-automation-ops:latest
```

---

## 30. Sample Portfolio Projects (Case Studies)

1. **Automated Backups & Restore Drills (Multi-DBMS).**  
   - Nightly snapshots + weekly restore verification + checksum.  
   - Prometheus metrics & Slack alerts.

2. **Zero-Downtime Schema Migrations.**  
   - Expand/contract patterns with feature flags and batched backfills.  

3. **Cross-Region DR Orchestration.**  
   - Lag thresholds, controlled switchover, DNS cutover, synthetic checks.

4. **Data Quality Gates in CDC + dbt.**  
   - Great Expectations blocking deploys when expectations fail.

5. **Performance Regression Detector.**  
   - Query latency p50/p95 tracking; alerts when regression ≥ 30%.

---

## 31. How to Run (Quickstart)

**Prerequisites**
- Python ≥ 3.11, Docker, Make, access to target DBs, cloud credentials (OIDC preferred).

```bash
git clone https://github.com/yourorg/python-automation-ops
cd python-automation-ops
uv pip install -e .[dev]
cp .env.example .env  # fill DSNs & endpoints
make bootstrap
```

---

## 32. KPIs & Reporting

- **DORA for Data/DB Ops:** lead time, deployment frequency, change failure rate, MTTR.
- **Pipeline SLAs:** freshness, timeliness, success rate.
- **SLO Compliance:** availability/latency burn charts.

```python
# src/ops/report/kpi_rollup.py
def rollup(events:list[dict])->dict:
    # produce weekly KPIs
    return {"deploy_freq": 42, "cfr": 0.02, "mttr_min": 18}
```

---

## 33. Roadmap & Next Steps

- **Short-term:** more engine-specific probes; add blue/green migration helpers.
- **Mid-term:** canary load harness, chaos experiments library.
- **Long-term:** policy-driven orchestration, fleet-wide drift remediation.

---

## 34. Appendices

### A. Reusable Code Templates

**A.1 CLI Skeleton (Typer)**
```python
import typer
app = typer.Typer()

@app.command()
def hello(name: str = "world"):
    typer.echo(f"hello {name}")

if __name__ == "__main__":
    app()
```

**A.2 Prometheus Exporter**
```python
from prometheus_client import start_http_server, Gauge
import time, random
g = Gauge("ops_example_metric","Example")
if __name__ == "__main__":
    start_http_server(9100)
    while True:
        g.set(random.random())
        time.sleep(5)
```

**A.3 Airflow DAG Template**
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG("template", start_date=datetime(2024,1,1), schedule="@daily", catchup=False) as dag:
    BashOperator(task_id="echo", bash_command="echo hello")
```

**A.4 Celery Worker**
```python
from celery import Celery
app = Celery("app", broker="redis://redis:6379/0")
@app.task
def add(a,b): return a+b
```

**A.5 OpenTelemetry Tracing**
```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("db-op"):
    # do work
    ...
```

---

### B. Operational Checklists

**B.1 Backup Drill (Weekly)**
- [ ] Latest full + incrementals available and verified
- [ ] Restore to isolated env succeeds
- [ ] Checksum and sample business queries pass
- [ ] RPO/RTO within targets
- [ ] Evidence archived (logs/metrics/screenshots)

**B.2 Failover (Planned)**
- [ ] Lag < threshold; replicas healthy
- [ ] Clients configured for retries/transparent failover
- [ ] DNS cutover runbook rehearsed
- [ ] Post-failover validation (reads/writes, latency)
- [ ] Failback plan defined and tested

**B.3 Schema Migration**
- [ ] Expand changes deployed safely (nullable/additive)
- [ ] Backfill in controlled batches with throttling
- [ ] Contract after validation window
- [ ] Rollback plan verified

---

### C. Reference Diagrams (Mermaid)

**C.1 Control vs Data Plane**
```mermaid
flowchart TB
subgraph Control Plane
  CI[CI/CD] --> ORCH[Airflow/Prefect]
  ORCH --> SECRETS[Vault/KMS]
  ORCH --> OBS[Prometheus/Grafana]
end
subgraph Data Plane
  APP[Apps] --> DB[(DB Cluster)]
  PIPE[Data Pipelines] --> DL[Data Lake]
end
ORCH -->|Jobs| DB
OBS -->|SLIs| CI
```

**C.2 DR Switchover**
```mermaid
sequenceDiagram
participant P as Primary
participant S as Standby
participant D as DNS
P->>S: Stop writes; ship logs; sync
S->>S: Promote to primary
S->>D: Update endpoint
D->>Client: New IP/target
```

---

### D. Glossary

- **DBRE:** Database Reliability Engineering (SRE principles applied to databases).  
- **SLO/SLI:** Objective/Indicator for reliability (e.g., availability, latency).  
- **Error Budget:** Allowed unreliability before change freeze or remediation.  
- **Idempotency:** Operation can run multiple times with same end state.  
- **CDC:** Change Data Capture — streaming mutations out of OLTP.  
- **Expand/Contract:** Safe two-phase schema change pattern.

---

## License

MIT (adjust as needed).

---

## Contact

- Email: your.name@example.com  
- LinkedIn/GitHub: your-profile

---
