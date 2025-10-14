# Professional Portfolio — DBA • DBRE • DataOps • SRE • Data Engineer • Data Scientist  
**Python Connectors, Cloud Integrations, and Operational Patterns**

> Curated, production-grade cookbook of Python code examples to connect with **Oracle, SQL Server, PostgreSQL, MySQL, MongoDB, Redis, IBM DB2, SQLite**, plus **AWS, Azure, GCP, OCI** integrations. Includes reliability, security, testing, CI/CD, and ops playbooks.

---

## Table of Contents

- [1. Executive Summary \& Positioning](#1-executive-summary--positioning)
- [2. Portfolio Structure \& Repos](#2-portfolio-structure--repos)
- [3. Core Competencies (Cross-Cutting)](#3-core-competencies-cross-cutting)
- [4. Role-Focused Highlights](#4-role-focused-highlights)
- [5. Python Setup \& Conventions](#5-python-setup--conventions)
- [6. Secrets \& Configuration Management](#6-secrets--configuration-management)
- [7. Networking \& Connectivity Patterns](#7-networking--connectivity-patterns)
- [8. Database Connectors (Hands-on Python)](#8-database-connectors-hands-on-python)
  - [8.1 Oracle (python-oracledb)](#81-oracle-python-oracledb)
  - [8.2 SQL Server (pyodbc, AAD Token)](#82-sql-server-pyodbc-aad-token)
  - [8.3 PostgreSQL (psycopg3, asyncpg)](#83-postgresql-psycopg3-asyncpg)
  - [8.4 MySQL (mysql-connector-python)](#84-mysql-mysql-connector-python)
  - [8.5 MongoDB (pymongo, transactions)](#85-mongodb-pymongo-transactions)
  - [8.6 Redis (redis-py, locks, pubsub)](#86-redis-redis-py-locks-pubsub)
  - [8.7 IBM DB2 (ibm_db)](#87-ibm-db2-ibm_db)
  - [8.8 SQLite (sqlite3, WAL)](#88-sqlite-sqlite3-wal)
  - [8.9 SQLAlchemy (Core/ORM, multi-DB)](#89-sqlalchemy-coreorm-multi-db)
- [9. CRUD, Transactions \& Prepared Statements](#9-crud-transactions--prepared-statements)
- [10. Bulk Load \& Data Movement](#10-bulk-load--data-movement)
- [11. Query Performance \& Observability](#11-query-performance--observability)
- [12. CDC \& Streaming](#12-cdc--streaming)
- [13. Data Quality \& Lineage](#13-data-quality--lineage)
- [14. Orchestration \& Scheduling (Airflow)](#14-orchestration--scheduling-airflow)
- [15. Testing Strategy (pytest, dockerized DBs)](#15-testing-strategy-pytest-dockerized-dbs)
- [16. CI/CD for Data \& DB](#16-cicd-for-data--db)
- [17. Cloud Integrations](#17-cloud-integrations)
  - [17.1 AWS (RDS, IAM auth, Secrets Manager, S3)](#171-aws-rds-iam-auth-secrets-manager-s3)
  - [17.2 Azure (Managed Identity, Key Vault, Azure SQL/AAD)](#172-azure-managed-identity-key-vault-azure-sqlaad)
  - [17.3 GCP (Cloud SQL Connector, Secret Manager, GCS)](#173-gcp-cloud-sql-connector-secret-manager-gcs)
  - [17.4 OCI (Autonomous, Wallet, Object Storage)](#174-oci-autonomous-wallet-object-storage)
- [18. Security \& Compliance Checklist](#18-security--compliance-checklist)
- [19. Templates \& Project Scaffolds](#19-templates--project-scaffolds)
- [20. Operational Playbooks \& Runbooks](#20-operational-playbooks--runbooks)
- [21. Appendix: Troubleshooting \& Cheat Sheets](#21-appendix-troubleshooting--cheat-sheets)

---

## 1. Executive Summary & Positioning
- **DBA/DBRE**: Availability, performance, automation, HA/DR, robust backups and recoverability, schema management, capacity planning, secure-by-default.
- **DataOps**: Reproducible pipelines, CI/CD for data, observability, quality gates, lineage, IaC/PaC, change governance.
- **SRE**: SLOs, error budgets, incident response, postmortems, chaos engineering, reliability tooling.
- **Data Engineering**: Ingestion/CDC, batch/stream, transformations, modeling, optimization, scalable storage.
- **Data Science**: Reliable data access, experiment tracking, feature pipelines, handoff to MLOps.

**KPIs**: MTTR, change lead time, deployment frequency, change failure rate, availability, query latency/throughput, freshness, DQ pass rate.

[Back to top](#table-of-contents)

---

## 2. Portfolio Structure & Repos
```
/portfolio
 ├─ /dba
 ├─ /dbre
 ├─ /dataops
 ├─ /sre
 ├─ /data-engineering
 ├─ /data-science
 └─ /cookbook-python-connectors   <-- this file
```
- **README standards**: purpose, architecture, setup, code examples, runbooks, KPIs, links to demos.
- **Conventions**: lowercase-with-dashes, `src/`, `tests/`, `infra/` (IaC), `.github/workflows/`.

[Back to top](#table-of-contents)

---

## 3. Core Competencies (Cross-Cutting)
- OS hardening, filesystems, backup/restore, networking, TLS/mTLS, IAM, secrets, DR/BCP.
- Observability: logs, metrics, traces; structured logging; correlation IDs; sampling.
- Automation: Terraform/Ansible, Python CLIs, GitOps; idempotent workflows.

[Back to top](#table-of-contents)

---

## 4. Role-Focused Highlights
- **DBA**: HA/DR (RAC/ADG/AOAG/Patroni/Galera), patching windows, query tuning, storage planning.
- **DBRE**: SLI/SLO design, runbooks, toil reduction, standardized connectors, readiness probes.
- **DataOps**: DQ checks, reproducible environments, lineage, promotion gates, rollback strategies.
- **SRE**: Golden signals, saturation/error/latency/traffic; autoscaling & capacity alarms; chaos drills.
- **Data Eng**: Lakehouse, CDC, incremental models, partitioning/bloom filters, compaction.
- **DS**: Secure dataset access, feature stores, reproducible notebooks, model registry.

[Back to top](#table-of-contents)

---

## 5. Python Setup & Conventions
```bash
# Recommended tools
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scriptsctivate
pip install --upgrade pip wheel

# Core packages used in this cookbook
pip install python-dotenv pydantic pydantic-settings tenacity structlog rich

# DB connectors
pip install oracledb pyodbc psycopg[binary] asyncpg mysql-connector-python pymongo redis ibm_db sqlalchemy

# Cloud SDKs (install as needed)
pip install boto3 azure-identity azure-keyvault-secrets google-cloud-secret-manager google-cloud-storage             google-cloud-sql-connector[pg8000] oci

# Orchestration & quality (optional)
pip install apache-airflow great-expectations
```

**Patterns**: context managers, timeouts, retries (`tenacity`), strict typing, **parameterized SQL only**, no string concatenation for user inputs.

[Back to top](#table-of-contents)

---

## 6. Secrets & Configuration Management
**Load from `.env` or cloud secret stores.** Prefer least-privilege, short-lived tokens.

```python
# src/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Common
    APP_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    # Oracle
    ORA_USER: str | None = None
    ORA_PASS: str | None = None
    ORA_DSN: str | None = None          # host:port/service or TNS alias
    ORA_WALLET_DIR: str | None = None   # for Autonomous/Wallet-based

    # SQL Server
    MSSQL_SERVER: str | None = None
    MSSQL_DB: str | None = None
    MSSQL_UID: str | None = None
    MSSQL_PWD: str | None = None

    # PostgreSQL
    PG_DSN: str | None = None           # "host=... dbname=... user=... password=... sslmode=require"

    # MySQL
    MYSQL_HOST: str | None = None
    MYSQL_DB: str | None = None
    MYSQL_USER: str | None = None
    MYSQL_PASS: str | None = None
    MYSQL_PORT: int = 3306

    # MongoDB
    MONGO_URI: str | None = None        # "mongodb+srv://.../?retryWrites=true&tls=true"

    # Redis
    REDIS_URL: str | None = None        # "rediss://user:pass@host:port/0"

    # DB2
    DB2_HOST: str | None = None
    DB2_PORT: int = 50000
    DB2_DB: str | None = None
    DB2_UID: str | None = None
    DB2_PWD: str | None = None
    DB2_SEC: bool = True

    # SQLite
    SQLITE_PATH: str = "data/app.db"

    # Clouds
    AWS_REGION: str | None = None
    AZURE_KV_URL: str | None = None
    GCP_PROJECT: str | None = None
    OCI_CONFIG_FILE: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

[Back to top](#table-of-contents)

---

## 7. Networking & Connectivity Patterns
- **TLS everywhere**: `Encrypt=yes;TrustServerCertificate=no` (SQL Server), `sslmode=require` (PostgreSQL).
- **Private endpoints** and VPC/VNet peering; **bastion tunnels** for admin access.
- **Connection pools** for concurrency; set sensible **timeouts** and **keepalive/ping**.

[Back to top](#table-of-contents)

---

## 8. Database Connectors (Hands-on Python)

### 8.1 Oracle (python-oracledb)
> Supports **Thin** (default) and **Thick** modes. For Autonomous (ATP/ADW), use **Wallet** with `config_dir`.

```python
# src/db_oracle.py
from __future__ import annotations
import oracledb
from contextlib import contextmanager
from tenacity import retry, wait_exponential, stop_after_attempt
from .config import settings

# Optional: pool
_pool: oracledb.ConnectionPool | None = None

def _get_pool() -> oracledb.ConnectionPool:
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user=settings.ORA_USER,
            password=settings.ORA_PASS,
            dsn=settings.ORA_DSN,             # e.g. "host:1521/service" or TNS alias like "db_high"
            config_dir=settings.ORA_WALLET_DIR,   # if using wallet/TNS
            min=1, max=8, increment=1, timeout=60,
            session_callback=None, ping_interval=60, homogeneous=True
        )
    return _pool

@contextmanager
def ora_conn():
    pool = _get_pool()
    conn = pool.acquire()
    try:
        yield conn
    finally:
        pool.release(conn)

@retry(wait=wait_exponential(min=1, max=8), stop=stop_after_attempt(5))
def ora_query(sql: str, params: dict | tuple | None = None) -> list[dict]:
    with ora_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

def ora_exec_many(sql: str, rows: list[tuple], batch_size: int = 1000) -> int:
    # Bind arrays for performance
    with ora_conn() as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, rows, batcherrors=True, arraydmlrowcounts=True)
        conn.commit()
        return len(rows)

if __name__ == "__main__":
    print(ora_query("SELECT sysdate as now FROM dual"))
```

**Examples**
```python
# Read with named bind variables
rows = ora_query("SELECT * FROM employees WHERE deptno=:dept", {"dept": 10})

# Bulk insert
data = [(i, f"name_{i}") for i in range(10000)]
count = ora_exec_many("INSERT INTO t_demo (id, name) VALUES (:1, :2)", data)
```

> Tip: For **Autonomous**: put the wallet unzip dir in `ORA_WALLET_DIR` and set `ORA_DSN` to TNS alias (e.g., `db_high`). Ensure mTLS trust and `ssl_server_dn_match=True` (default).

[Back to top](#table-of-contents)

---

### 8.2 SQL Server (pyodbc, AAD Token)
**Classic (username/password, ODBC Driver 18)**
```python
# src/db_mssql.py
import pyodbc
from contextlib import contextmanager
from tenacity import retry, wait_exponential, stop_after_attempt
from .config import settings

CNSTR = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{settings.MSSQL_SERVER},1433;"
    f"Database={settings.MSSQL_DB};"
    "Encrypt=yes;TrustServerCertificate=no;"
    f"UID={settings.MSSQL_UID};PWD={settings.MSSQL_PWD};"
    "Connection Timeout=30;"
)

@contextmanager
def mssql_conn(conn_str: str = CNSTR):
    conn = pyodbc.connect(conn_str)
    try:
        yield conn
    finally:
        conn.close()

@retry(wait=wait_exponential(min=1, max=8), stop=stop_after_attempt(5))
def mssql_query(sql: str, params: tuple | None = None) -> list[dict]:
    with mssql_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params or ())
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
```

**Azure AD (Access Token via `azure-identity`)**
```python
# src/db_mssql_aad.py
import pyodbc
from azure.identity import DefaultAzureCredential
from .config import settings

SQL_COPT_SS_ACCESS_TOKEN = 1256  # ODBC attribute
scope = "https://database.windows.net/.default"

token = DefaultAzureCredential().get_token(scope).token.encode("utf-16-le")
attrs = {SQL_COPT_SS_ACCESS_TOKEN: token}

CNSTR = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{settings.MSSQL_SERVER},1433;"
    f"Database={settings.MSSQL_DB};"
    "Encrypt=yes;TrustServerCertificate=no;"
)

with pyodbc.connect(CNSTR, attrs_before=attrs) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT SUSER_SNAME() AS whoami")
        print(cur.fetchone())
```

**Fast bulk insert**
```python
with mssql_conn() as conn:
    data = [(i, f"name_{i}") for i in range(100000)]
    cur = conn.cursor()
    cur.fast_executemany = True
    cur.executemany("INSERT INTO dbo.t_demo (id, name) VALUES (?, ?)", data)
    conn.commit()
```

[Back to top](#table-of-contents)

---

### 8.3 PostgreSQL (psycopg3, asyncpg)
**psycopg3 (sync)**
```python
# src/db_postgres.py
import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from .config import settings

@contextmanager
def pg_conn():
    # PG_DSN example: "host=... dbname=... user=... password=... sslmode=require"
    with psycopg.connect(settings.PG_DSN, prepare_threshold=None) as conn:
        yield conn

def pg_query(sql: str, params: dict | tuple | None = None) -> list[dict]:
    with pg_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

def pg_copy_from_csv(table: str, file_path: str):
    with pg_conn() as conn, conn.cursor() as cur, open(file_path, "r", encoding="utf-8") as f:
        cur.copy_expert(f"COPY {table} FROM STDIN WITH CSV HEADER", f)
        conn.commit()
```

**asyncpg (async)**
```python
# src/db_postgres_async.py
import asyncio, asyncpg
from .config import settings

async def run():
    conn = await asyncpg.connect(dsn=settings.PG_DSN, timeout=10)
    try:
        rows = await conn.fetch("SELECT now() AS now")
        print(rows)
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run())
```

[Back to top](#table-of-contents)

---

### 8.4 MySQL (mysql-connector-python)
```python
# src/db_mysql.py
import mysql.connector as mysql
from contextlib import contextmanager
from .config import settings

@contextmanager
def my_conn():
    cnx = mysql.connect(
        host=settings.MYSQL_HOST, user=settings.MYSQL_USER, password=settings.MYSQL_PASS,
        database=settings.MYSQL_DB, port=settings.MYSQL_PORT, ssl_disabled=False, connection_timeout=10
    )
    try:
        yield cnx
    finally:
        cnx.close()

def my_query(sql: str, params: tuple | dict | None = None) -> list[dict]:
    with my_conn() as cnx:
        cur = cnx.cursor(dictionary=True, prepared=True)
        cur.execute(sql, params or ())
        return cur.fetchall()

def my_bulk_insert(sql: str, rows: list[tuple]):
    with my_conn() as cnx:
        cur = cnx.cursor(prepared=True)
        cur.executemany(sql, rows)
        cnx.commit()
```

[Back to top](#table-of-contents)

---

### 8.5 MongoDB (pymongo, transactions)
```python
# src/db_mongo.py
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from .config import settings

client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000,
    retryWrites=True,
    tls=True
)

db = client["analytics"]

def ensure_indexes():
    db.events.create_index([("ts", ASCENDING)])
    db.users.create_index([("email", ASCENDING)], unique=True)

def insert_user(user: dict) -> str:
    res = db.users.insert_one(user)
    return str(res.inserted_id)

def transfer_funds(from_uid: str, to_uid: str, amount: float):
    # Example transaction (Replica Set / Sharded required)
    with client.start_session() as s:
        s.start_transaction()
        db.accounts.update_one({"_id": from_uid}, {"$inc": {"balance": -amount}}, session=s)
        db.accounts.update_one({"_id": to_uid}, {"$inc": {"balance": amount}}, session=s)
        s.commit_transaction()
```

[Back to top](#table-of-contents)

---

### 8.6 Redis (redis-py, locks, pubsub)
```python
# src/db_redis.py
import time
from redis import Redis, ConnectionPool
from .config import settings

pool = ConnectionPool.from_url(settings.REDIS_URL, socket_timeout=3, socket_connect_timeout=3)
redis = Redis(connection_pool=pool)

def cache_get(key: str) -> bytes | None:
    return redis.get(key)

def cache_set(key: str, value: bytes, ttl: int = 300):
    redis.set(key, value, ex=ttl)

def acquire_lock(key: str, ttl: int = 10) -> bool:
    # Simple, best-effort lock (single-node). For multi-node, evaluate Redlock/alternatives carefully.
    return bool(redis.set(name=f"lock:{key}", value="1", nx=True, ex=ttl))

def release_lock(key: str):
    redis.delete(f"lock:{key}")

def pub(channel: str, msg: str): redis.publish(channel, msg)

def sub(channel: str):
    pubsub = redis.pubsub()
    pubsub.subscribe(channel)
    for m in pubsub.listen():
        if m["type"] == "message":
            yield m["data"]
```

[Back to top](#table-of-contents)

---

### 8.7 IBM DB2 (ibm_db)
```python
# src/db_db2.py
import ibm_db
from .config import settings

def db2_conn():
    sec = "SECURITY=SSL;" if settings.DB2_SEC else ""
    dsn = (
        f"DATABASE={settings.DB2_DB};HOSTNAME={settings.DB2_HOST};PORT={settings.DB2_PORT};"
        f"PROTOCOL=TCPIP;UID={settings.DB2_UID};PWD={settings.DB2_PWD};{sec}"
    )
    return ibm_db.connect(dsn, "", "")

def db2_query(sql: str, params: tuple | None = None) -> list[dict]:
    conn = db2_conn()
    try:
        stmt = ibm_db.prepare(conn, sql)
        if params:
            for idx, val in enumerate(params, start=1):
                ibm_db.bind_param(stmt, idx, val)
        ibm_db.execute(stmt)
        rows = []
        r = ibm_db.fetch_assoc(stmt)
        while r:
            rows.append(dict(r))
            r = ibm_db.fetch_assoc(stmt)
        return rows
    finally:
        ibm_db.close(conn)
```

[Back to top](#table-of-contents)

---

### 8.8 SQLite (sqlite3, WAL)
```python
# src/db_sqlite.py
import sqlite3
from contextlib import contextmanager
from .config import settings

@contextmanager
def lite():
    conn = sqlite3.connect(settings.SQLITE_PATH, timeout=10, isolation_level=None)  # autocommit
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def lite_query(sql: str, params: tuple | None = None) -> list[dict]:
    with lite() as conn:
        cur = conn.execute(sql, params or ())
        return [dict(row) for row in cur.fetchall()]
```

[Back to top](#table-of-contents)

---

### 8.9 SQLAlchemy (Core/ORM, multi-DB)
```python
# src/sa_base.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[Optional[str]]

def get_engine(url: str):
    return create_engine(url, pool_pre_ping=True, future=True)

def create_schema(engine):
    Base.metadata.create_all(engine)

def find_users(engine, email_like: str):
    with Session(engine) as s:
        return s.query(User).filter(User.email.like(email_like)).all()
```

**URLs**:  
- Postgres: `postgresql+psycopg://user:pass@host:5432/db?sslmode=require`  
- SQL Server (ODBC 18): `mssql+pyodbc:///?odbc_connect=...`  
- MySQL: `mysql+mysqlconnector://user:pass@host:3306/db`  
- Oracle: `oracle+oracledb://user:pass@host:1521/?service_name=svc`  
- SQLite: `sqlite:///data/app.db`

[Back to top](#table-of-contents)

---

## 9. CRUD, Transactions & Prepared Statements
```python
from .db_postgres import pg_conn

def transfer(payer_id: int, payee_id: int, amount: float):
    with pg_conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("BEGIN")
                cur.execute("UPDATE wallet SET balance = balance - %s WHERE id=%s", (amount, payer_id))
                cur.execute("UPDATE wallet SET balance = balance + %s WHERE id=%s", (amount, payee_id))
                cur.execute("COMMIT")
            except Exception:
                cur.execute("ROLLBACK")
                raise
```
**Notes**: Always **parameterize** (`%s`, `:name`, `?`) and set explicit **isolation level** where needed.

[Back to top](#table-of-contents)

---

## 10. Bulk Load & Data Movement
- **PostgreSQL**: `COPY` is fastest.
```python
from .db_postgres import pg_conn
def pg_copy_to(table: str, out_path: str):
    with pg_conn() as conn, conn.cursor() as cur, open(out_path, "w", encoding="utf-8") as f:
        cur.copy_expert(f"COPY {table} TO STDOUT WITH CSV HEADER", f)
```
- **SQL Server**: `fast_executemany=True` for large batches; consider **BCP**/**BULK INSERT**.
- **Oracle**: `executemany` with array binding; increase `arraysize`.
- **MySQL**: `LOAD DATA [LOCAL] INFILE` (ensure server/client flags allow it).
- **S3/Blob/GCS**: offload/export to object storage; push-down COPY from external stages if available.

[Back to top](#table-of-contents)

---

## 11. Query Performance & Observability
- Explain plans: `EXPLAIN`, `EXPLAIN ANALYZE`, `dbms_xplan.display`, `SET STATISTICS IO/TIME ON`.
- Collect metrics (latency, rows, errors), tag with **trace IDs**.
```python
import logging, time
log = logging.getLogger("db")
def timed_query(fn, *a, **kw):
    t0 = time.perf_counter()
    try:
        r = fn(*a, **kw)
        return r
    finally:
        log.info("query_ms=%.2f", (time.perf_counter()-t0)*1000)
```

[Back to top](#table-of-contents)

---

## 12. CDC & Streaming
- **Debezium/Kafka** for MySQL/Postgres/SQL Server CDC.
```python
# Kafka consumer (confluent-kafka)
from confluent_kafka import Consumer
c = Consumer({"bootstrap.servers":"kafka:9092","group.id":"cdc-app","auto.offset.reset":"earliest"})
c.subscribe(["dbserver1.inventory.customers"])
while True:
    msg = c.poll(1.0)
    if msg and not msg.error():
        process(msg.value())
```
- **Oracle**: GoldenGate (concepts) or LogMiner-based tools; sink to Kafka, process with Python.

[Back to top](#table-of-contents)

---

## 13. Data Quality & Lineage
```python
# Great Expectations minimal check
import great_expectations as ge
import pandas as pd
df = pd.DataFrame({"id":[1,2], "email":["a@x","b@x"]})
gdf = ge.from_pandas(df)
gdf.expect_column_values_to_not_be_null("id")
gdf.expect_column_values_to_match_regex("email", r".+@.+")
print(gdf.validate().success)
```
- Lineage: emit OpenLineage events from orchestrators (e.g., Airflow provider).

[Back to top](#table-of-contents)

---

## 14. Orchestration & Scheduling (Airflow)
```python
# dags/db_healthcheck.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from myapp.db_postgres import pg_query

def healthcheck():
    rows = pg_query("SELECT 1")
    assert rows and list(rows[0].values())[0] == 1

with DAG(
    "db_healthcheck",
    start_date=datetime(2025,1,1),
    schedule="*/15 * * * *",
    catchup=False,
    default_args={"retries":2, "retry_delay": timedelta(minutes=2)},
) as dag:
    PythonOperator(task_id="check_pg", python_callable=healthcheck)
```

[Back to top](#table-of-contents)

---

## 15. Testing Strategy (pytest, dockerized DBs)
```python
# tests/test_pg.py
import pytest
from myapp.db_postgres import pg_query

def test_pg_now():
    r = pg_query("SELECT 1 AS ok")
    assert r and r[0]["ok"] == 1
```
- Use **containers** for integration tests (Testcontainers or docker-compose).
- Seed minimal schemas/migrations before tests; clean up after.

[Back to top](#table-of-contents)

---

## 16. CI/CD for Data & DB
**GitHub Actions: run tests + lint**
```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: pytest -q
```
- Promotion gates (DQ pass rates), migrations (Alembic/Flyway/Liquibase), feature flags for rollout/rollback.

[Back to top](#table-of-contents)

---

## 17. Cloud Integrations

### 17.1 AWS (RDS, IAM auth, Secrets Manager, S3)
**IAM auth token for PostgreSQL (RDS / RDS Proxy)**
```python
import boto3, psycopg
from .config import settings

def rds_iam_connect(host: str, port: int, db: str, user: str):
    rds = boto3.client("rds", region_name=settings.AWS_REGION)
    token = rds.generate_db_auth_token(Hostname=host, Port=port, DBUsername=user, Region=settings.AWS_REGION)
    dsn = f"host={host} port={port} dbname={db} user={user} password={token} sslmode=require"
    return psycopg.connect(dsn)
```

**Secrets Manager**
```python
import boto3, json, os
def get_secret(name: str) -> dict:
    sm = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION"))
    val = sm.get_secret_value(SecretId=name)
    return json.loads(val["SecretString"])
```

**S3 export/import**: use `boto3.client("s3")` and DB-native COPY (e.g., Aurora/MySQL `LOAD DATA FROM S3` where available).

[Back to top](#table-of-contents)

---

### 17.2 Azure (Managed Identity, Key Vault, Azure SQL/AAD)
**Key Vault secret**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from .config import settings

cred = DefaultAzureCredential()
kv = SecretClient(vault_url=settings.AZURE_KV_URL, credential=cred)
db_pass = kv.get_secret("mssql-password").value
```

**Azure SQL with AAD token (pyodbc)**
```python
import pyodbc
from azure.identity import DefaultAzureCredential

SQL_COPT_SS_ACCESS_TOKEN = 1256
scope = "https://database.windows.net/.default"
token = DefaultAzureCredential().get_token(scope).token.encode("utf-16-le")

cn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:server.database.windows.net,1433;"
    "Database=dbname;Encrypt=yes;TrustServerCertificate=no;",
    attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token}
)
```

[Back to top](#table-of-contents)

---

### 17.3 GCP (Cloud SQL Connector, Secret Manager, GCS)
**Secret Manager**
```python
from google.cloud import secretmanager
def gcp_secret(name: str, project: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    res = client.access_secret_version(name=f"projects/{project}/secrets/{name}/versions/latest")
    return res.payload.data.decode("utf-8")
```

**Cloud SQL Python Connector (PostgreSQL)**
```python
from google.cloud.sql.connector import Connector, IPTypes
import pg8000.native as pg

def connect_cloudsql(instance_conn_name: str, user: str, password: str, db: str):
    with Connector() as connector:
        conn = connector.connect(
            instance_conn_name, "pg8000",
            user=user, password=password, db=db,
            ip_type=IPTypes.PRIVATE
        )
        cur = conn.cursor()
        cur.execute("SELECT now()")
        print(cur.fetchone())
        conn.close()
```

[Back to top](#table-of-contents)

---

### 17.4 OCI (Autonomous, Wallet, Object Storage)
**Autonomous Database (Wallet, python-oracledb Thin)**
```python
import oracledb, os
WALLET_DIR = os.getenv("ORA_WALLET_DIR")        # unzip Wallet file here
DSN_ALIAS  = os.getenv("ORA_DSN")               # e.g., "adb_high"

conn = oracledb.connect(user=os.getenv("ORA_USER"), password=os.getenv("ORA_PASS"),
                        dsn=DSN_ALIAS, config_dir=WALLET_DIR)
with conn.cursor() as cur:
    cur.execute("SELECT sysdate FROM dual")
    print(cur.fetchone())
```

**OCI SDK: Object Storage upload**
```python
import oci, os
config = oci.config.from_file(os.getenv("OCI_CONFIG_FILE"), "DEFAULT")
oss = oci.object_storage.ObjectStorageClient(config)
ns = oss.get_namespace().data
oss.put_object(namespace_name=ns, bucket_name="backups", object_name="dump.dmp",
               put_object_body=open("dump.dmp","rb"))
```

[Back to top](#table-of-contents)

---

## 18. Security & Compliance Checklist
- **Encryption** in transit (TLS) and at rest (TDE/KMS/CMK).
- **Least privilege**: separate app/service accounts; rotate credentials.
- **Audit**: DB audit, immutable logs, time sync, retention policies.
- **Network**: private endpoints, no public IPs by default, firewall allowlists.
- **Secrets**: centralized secret stores; never commit secrets to git.
- **Backups/DR**: tested restores, RTO/RPO defined; offsite copies.

[Back to top](#table-of-contents)

---

## 19. Templates & Project Scaffolds
**Typer CLI skeleton**
```python
# src/cli.py
import typer
from .db_postgres import pg_query
app = typer.Typer()

@app.command()
def whoami():
    print(pg_query("SELECT current_user"))

if __name__ == "__main__":
    app()
```

**FastAPI microservice (health + DB)**
```python
# src/api.py
from fastapi import FastAPI
from .db_postgres import pg_query
app = FastAPI()

@app.get("/healthz")
def healthz():
    try:
        pg_query("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "fail", "error": str(e)}
```

[Back to top](#table-of-contents)

---

## 20. Operational Playbooks & Runbooks
- **Connection failures**: DNS, firewall, TLS certs, token expiry, pool exhaustion.
- **Latency spikes**: plan cache regression, missing indexes, IO saturation, noisy neighbor.
- **Errors**: deadlocks, lock waits, transaction timeouts, statement timeouts.
- **Checks**: connectivity, auth, schema drift, replication/lag, storage thresholds.
- **Release**: preflight DQ, migrations dry-run, rollback path, comms plan.

[Back to top](#table-of-contents)

---

## 21. Appendix: Troubleshooting & Cheat Sheets

**Connection Strings (quick)**
- **PostgreSQL**: `host=H dbname=D user=U password=P sslmode=require`
- **SQL Server**: `Driver={ODBC Driver 18 for SQL Server};Server=tcp:H,1433;Database=D;Encrypt=yes;TrustServerCertificate=no;UID=U;PWD=P;`
- **Oracle**: `user/pass@host:1521/service` (or TNS alias with wallet)
- **MySQL**: `mysql+mysqlconnector://U:P@H:3306/D`
- **Redis**: `rediss://U:P@H:6379/0`
- **DB2**: `DATABASE=D;HOSTNAME=H;PORT=50000;PROTOCOL=TCPIP;UID=U;PWD=P;SECURITY=SSL;`
- **SQLite**: `sqlite:///data/app.db`

**Common Errors**
- **SSL/TLS**: “certificate verify failed” → verify CA chain, hostnames, time skew.
- **Auth**: expired AAD/IAM tokens → refresh flow, short TTLs by design.
- **Timeouts**: add connect/read timeouts; backoff retries; circuit breaker.

---

> **Next steps**: plug these modules into Airflow/Prefect jobs, wrap with CI (pytest), and enable secrets via your target cloud. Extend with migrations (Alembic/Flyway), metrics exporters, and SLO dashboards.

---
