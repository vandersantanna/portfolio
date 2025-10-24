<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Rust for Data Infrastructure
*Safe concurrency, low-latency I/O, and production-grade ops for DBE/DBRE/DBA/DataOps.*

## Table of Contents

- [1. Executive Summary & Positioning](#1-executive-summary--positioning)
- [2. Toolchain & Project Layout](#2-toolchain--project-layout)
- [3. Async, Concurrency & Performance](#3-async-concurrency--performance)
- [4. Error Handling & Resilience](#4-error-handling--resilience)
- [5. Configuration & Secrets](#5-configuration--secrets)
- [6. Observability](#6-observability)
- [7. Security](#7-security)
- [8. Database Access Strategy](#8-database-access-strategy)
- [9. Connectors by Database (Rust)](#9-connectors-by-database-rust)
  - [9.1 PostgreSQL (sqlx, tokio-postgres)](#91-postgresql-sqlx-tokio-postgres)
  - [9.2 MySQL/MariaDB (mysql_async, sqlx)](#92-mysqlmariadb-mysql_async-sqlx)
  - [9.3 SQLite (rusqlite, sqlx)](#93-sqlite-rusqlite-sqlx)
  - [9.4 SQL Server (tiberius, odbc-api)](#94-sql-server-tiberius-odbc-api)
  - [9.5 Oracle (oracle crate, ODPI-C)](#95-oracle-oracle-crate-odpi-c)
  - [9.6 MongoDB (official async driver)](#96-mongodb-official-async-driver)
  - [9.7 Redis (redis, async)](#97-redis-redis-async)
  - [9.8 IBM DB2 (ODBC via odbc-api)](#98-ibm-db2-odbc-via-odbc-api)
  - [9.9 Abstractions (SQLx, Diesel, SeaORM)](#99-abstractions-sqlx-diesel-seaorm)
- [10. CRUD, Transactions & Prepared Statements](#10-crud-transactions--prepared-statements)
- [11. Data Processing (Polars, Arrow, Parquet)](#11-data-processing-polars-arrow-parquet)
- [12. Streaming & CDC (Kafka/NATS)](#12-streaming--cdc-kafkanats)
- [13. Pipelines & Orchestration](#13-pipelines--orchestration)
- [14. Testing & Quality](#14-testing--quality)
- [15. CI/CD & Packaging](#15-cicd--packaging)
- [16. Cloud Integrations](#16-cloud-integrations)
  - [16.1 AWS (SDK, Secrets, S3, STS)](#161-aws-sdk-secrets-s3-sts)
  - [16.2 Azure (Key Vault, Storage, Managed Identity)](#162-azure-key-vault-storage-managed-identity)
  - [16.3 GCP (Secret Manager, GCS, Workload Identity)](#163-gcp-secret-manager-gcs-workload-identity)
  - [16.4 OCI (Object Storage, Autonomous)](#164-oci-object-storage-autonomous)
- [17. SRE & Reliability Patterns](#17-sre--reliability-patterns)
- [18. Supply Chain Security & Compliance](#18-supply-chain-security--compliance)
- [19. Operational Runbooks](#19-operational-runbooks)
- [20. Templates & Scaffolds](#20-templates--scaffolds)
- [21. Appendix: Cheat Sheets & References](#21-appendix-cheat-sheets--references)

---

## 1. Executive Summary & Positioning

> A production-oriented **Rust** cookbook for database connectivity, cloud integrations, performance, reliability, and operational patterns. Includes end‑to‑end examples for PostgreSQL, MySQL, SQLite, SQL Server, Oracle, MongoDB, Redis, IBM DB2 (via ODBC), plus AWS, Azure, GCP, and OCI.

Rust brings **predictable performance**, **memory safety**, and **low-latency I/O** to data‑intensive systems. It fits roles across DBA/DBRE/DataOps/SRE/Data Eng/DS when you need:
- High‑throughput ETL/ELT, CDC consumers, and near‑real‑time services.
- Strong safety guarantees for long‑running daemons and infra tooling.
- Portable, static binaries for minimal containers and fast cold starts.
**KPIs**: predictable p95/p99, CPU/heap stability, MTTR, error budgets, throughput (rows/s), DQ pass rate, cost per TB processed.

[Back to top](#table-of-contents)

---

## 2. Toolchain & Project Layout
```bash
# Install toolchains
curl https://sh.rustup.rs -sSf | sh
rustup default stable
rustup component add clippy rustfmt

# New workspace
cargo new --vcs git data-platform --bin
cd data-platform
mkdir -p crates apps infra .cargo
```

**Workspace layout**
```
/data-platform
 ├─ /apps
 │   ├─ etl-cli/           # CLI tools (ingestion/exports)
 │   └─ api/               # Microservices (axum/actix-web)
 ├─ /crates
 │   ├─ db/                # Reusable DB utilities (pools, errors, models)
 │   ├─ processing/        # Polars/Arrow pipelines
 │   └─ observability/     # tracing, otel, metrics
 ├─ /infra                 # Docker, compose, K8s, IaC
 ├─ Cargo.toml             # Workspace members
 └─ rust-toolchain.toml    # Pin toolchain
```

**Cargo profiles**
```toml
# Cargo.toml (workspace)
[workspace]
members = ["apps/etl-cli", "apps/api", "crates/db", "crates/processing", "crates/observability"]

[profile.release]
lto = "thin"
codegen-units = 1
panic = "abort"
strip = true
```

[Back to top](#table-of-contents)

---

## 3. Async, Concurrency & Performance
- Runtime: **tokio** (default) or async-std.
- Parallel compute: **rayon** (data‑parallel iterators).
- Zero‑copy buffers: **bytes**; avoid unnecessary allocations.
- Custom allocators: `mimalloc`/`jemalloc` (benchmark before adopting).
- Use pools (DB, HTTP), backpressure, bounded channels.

```toml
# apps/api/Cargo.toml (excerpt)
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "macros", "signal"] }
bytes = "1"
rayon = "1"
```

[Back to top](#table-of-contents)

---

## 4. Error Handling & Resilience
- Domain errors with `thiserror`; context with `anyhow`/`eyre`.
- Retries with exponential backoff; timeouts & cancellation.
- Graceful shutdown: signal handlers, draining, closing pools.

```toml
[dependencies]
thiserror = "1"
anyhow = "1"
backoff = "0.4"
```

```rust
use anyhow::{Context, Result};
use backoff::{ExponentialBackoff, Operation};

fn fragile_op() -> Result<String> { Ok("ok".to_string()) }

fn with_retry() -> Result<String> {
    let mut op = || { fragile_op().context("fragile_op failed") };
    op.retry(&mut ExponentialBackoff::default())
}
```

[Back to top](#table-of-contents)

---

## 5. Configuration & Secrets
- Layers: env vars → files (`.env`, `config/`) → secret stores.
- Separate operational config from secrets; rotate credentials.
```toml
[dependencies]
config = "0.14"
serde = { version = "1", features = ["derive"] }
dotenvy = "0.15"
```

```rust
// crates/db/src/settings.rs
use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct Settings {
    pub app_env: String,
    pub log_level: String,
    pub pg_url: Option<String>,
    pub mysql_url: Option<String>,
    pub sqlite_path: Option<String>,
    pub mssql_conn: Option<String>,
    pub oracle_conn: Option<String>,
    pub mongo_uri: Option<String>,
    pub redis_url: Option<String>,
    pub odbc_conn: Option<String>, // DB2 or generic ODBC
}

pub fn load() -> Settings {
    dotenvy::dotenv().ok();
    config::Config::builder()
        .add_source(config::File::with_name("config/default").required(false))
        .add_source(config::Environment::default().separator("__"))
        .build().unwrap()
        .try_deserialize().unwrap()
}
```

[Back to top](#table-of-contents)

---

## 6. Observability
- Structured logs (`tracing`), JSON for ingestion, span/trace IDs.
- Metrics: `metrics` + Prometheus exporter.
- Tracing: OpenTelemetry, OTLP to your collector.

```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
opentelemetry = "0.22"
tracing-opentelemetry = "0.23"
metrics = "0.24"
metrics-exporter-prometheus = "0.14"
```

```rust
use tracing::{info, instrument};
#[instrument(skip_all)]
fn work() {
    info!(event="work_started", stage=1);
}
```

[Back to top](#table-of-contents)

---

## 7. Security
- TLS/mTLS with `rustls` where possible; disable legacy ciphers.
- Input validation (serde), principle of least privilege.
- Secrets never logged; redact fields in logs.
```toml
rustls = "0.23"
tokio-rustls = "0.26"
```

[Back to top](#table-of-contents)

---

## 8. Database Access Strategy
- Prefer **async** drivers with pooling and prepared statements.
- Use **SQLx** for compile‑time checked queries (enable offline mode with `sqlx-data.json`) or **Diesel** for sync ORM.
- For vendors lacking native crates, use **ODBC** (`odbc-api`) with DSN/connection strings.
- Always set timeouts; instrument with `tracing`.

[Back to top](#table-of-contents)

---

## 9. Connectors by Database (Rust)

### 9.1 PostgreSQL (sqlx, tokio-postgres)
```toml
# apps/api/Cargo.toml (excerpt)
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "tls-rustls", "macros"] }
tokio-postgres = { version = "0.7", features = ["runtime", "tls", "with-uuid-1"] }
deadpool-postgres = "0.12"
```
```rust
// crates/db/src/pg.rs
use sqlx::{Pool, Postgres};
use std::time::Duration;

pub async fn pg_pool(url: &str) -> Result<Pool<Postgres>, sqlx::Error> {
    sqlx::postgres::PgPoolOptions::new()
        .max_connections(8)
        .acquire_timeout(Duration::from_secs(5))
        .connect(url).await
}

pub async fn whoami(pool: &Pool<Postgres>) -> Result<String, sqlx::Error> {
    let (user,): (String,) = sqlx::query_as("SELECT current_user")
        .fetch_one(pool).await?;
    Ok(user)
}
```

**COPY (fast load)**
```rust
use tokio_postgres::{NoTls};
// With tokio-postgres CopyIn/Out APIs (example outline)
```

[Back to top](#table-of-contents)

---

### 9.2 MySQL/MariaDB (mysql_async, sqlx)
```toml
mysql_async = { version = "0.34", features = ["sha256-password"] }
sqlx = { version = "0.7", features = ["mysql", "runtime-tokio", "tls-rustls", "macros"] }
```
```rust
use mysql_async::{prelude::*, Pool};

pub async fn mysql_example(url: &str) -> mysql_async::Result<Vec<(u64, String)>> {
    let pool = Pool::new(url);
    let mut conn = pool.get_conn().await?;
    conn.exec_batch(r"INSERT INTO t_demo (id, name) VALUES (:id, :name)",
        (0..10).map(|i| params! { "id" => i, "name" => format!("name_{i}") })
    ).await?;
    let rows: Vec<(u64, String)> = conn.query("SELECT id, name FROM t_demo").await?;
    pool.disconnect().await?;
    Ok(rows)
}
```

[Back to top](#table-of-contents)

---

### 9.3 SQLite (rusqlite, sqlx)
```toml
rusqlite = { version = "0.31", features = ["bundled", "unlock_notify"] }
sqlx = { version = "0.7", features = ["sqlite", "runtime-tokio", "macros"] }
```
```rust
use rusqlite::{Connection, params};

pub fn lite_query(path: &str) -> rusqlite::Result<Vec<(i64, String)>> {
    let conn = Connection::open(path)?;
    conn.pragma_update(None, "journal_mode", &"WAL")?;
    conn.execute("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, name TEXT)", [])?;
    conn.execute("INSERT INTO t (name) VALUES (?1)", params!["alice"])?;
    let mut stmt = conn.prepare("SELECT id, name FROM t")?;
    let rows = stmt.query_map([], |r| Ok((r.get(0)?, r.get(1)?)))?
                   .collect::<Result<Vec<_>, _>>()?;
    Ok(rows)
}
```

[Back to top](#table-of-contents)

---

### 9.4 SQL Server (tiberius, odbc-api)
```toml
tiberius = { version = "0.12", features = ["rustls"] }
odbc-api = "5"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

**Tiberius (TDS)**
```rust
use tiberius::{Client, Config, AuthMethod};
use tokio::net::TcpStream;
use tokio_rustls::TlsConnector;
use tokio_util::compat::TokioAsyncWriteCompatExt;

pub async fn mssql_query(host: &str, user: &str, pass: &str, db: &str) -> anyhow::Result<()> {
    let mut config = Config::new();
    config.host(host);
    config.port(1433);
    config.authentication(AuthMethod::sql_server(user.to_string(), pass.to_string()));
    config.database(db);
    config.trust_cert(); // or configure rustls with proper CA

    let tcp = TcpStream::connect((host, 1433)).await?;
    tcp.set_nodelay(true)?;
    let connector = TlsConnector::from(std::sync::Arc::new(rustls::ClientConfig::builder()
        .with_safe_defaults()
        .with_custom_certificate_verifier(std::sync::Arc::new(rustls_native_certs::load_native_certs().unwrap()))
        .with_no_client_auth()));
    let tls = connector.connect(host.try_into()?, tcp).await?;
    let mut client = Client::connect(config, tls.compat_write()).await?;

    let stream = client.query("SELECT @@VERSION", &[]).await?;
    let rows: Vec<_> = stream.into_first_result().await?;
    println!("rows={:?}", rows);
    Ok(())
}
```

**ODBC (works with SQL Server/DB2/others)**
```rust
use odbc_api::{Environment, ConnectionOptions};
pub fn odbc_query(conn_str: &str) -> anyhow::Result<()> {
    let env = Environment::new()?;
    let conn = env.connect_with_connection_string(conn_str, ConnectionOptions::default())?;
    let cursor = conn.execute("SELECT 1 AS ok", ())?
        .expect("query should return a result set");
    for row in cursor {
        let row = row?;
        println!("ok={}", row.get::<i32>(0)?);
    }
    Ok(())
}
```

[Back to top](#table-of-contents)

---

### 9.5 Oracle (oracle crate, ODPI-C)
```toml
oracle = "0.6"
```
```rust
use oracle::{Connection, Result};

pub fn oracle_now(conn_str: &str, user: &str, pass: &str) -> Result<()> {
    let conn = Connection::connect(user, pass, conn_str)?; // e.g., "host:1521/service"
    let rows = conn.query("SELECT sysdate FROM dual", &[])?;
    for r in rows { println!("{:?}", r?); }
    Ok(())
}
```
> Requires Oracle Instant Client (ODPI-C). For Wallet/TNS, set environment (e.g., `TNS_ADMIN`) and use service names.

[Back to top](#table-of-contents)

---

### 9.6 MongoDB (official async driver)
```toml
mongodb = { version = "2", features = ["tokio-runtime"] }
serde = { version = "1", features = ["derive"] }
```

```rust
use mongodb::{Client, bson::doc};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User { email: String, balance: f64 }

pub async fn mongo_example(uri: &str) -> mongodb::error::Result<()> {
    let client = Client::with_uri_str(uri).await?;
    let db = client.database("analytics");
    let users = db.collection::<User>("users");
    users.insert_one(User{email:"a@x".into(), balance: 10.0}, None).await?;
    let u = users.find_one(doc!{"email":"a@x"}, None).await?;
    println!("found={:?}", u);
    Ok(())
}
```

[Back to top](#table-of-contents)

---

### 9.7 Redis (redis, async)
```toml
redis = { version = "0.25", features = ["tokio-comp"] }
```

```rust
use redis::AsyncCommands;

pub async fn redis_demo(url: &str) -> redis::RedisResult<()> {
    let client = redis::Client::open(url)?; // e.g., rediss://user:pass@host:6379/0
    let mut con = client.get_async_connection().await?;
    con.set_ex("k1", b"hello", 60).await?;
    let v: Vec<u8> = con.get("k1").await?;
    println!("val={:?}", v);
    Ok(())
}
```

[Back to top](#table-of-contents)

---

### 9.8 IBM DB2 (ODBC via odbc-api)
Use ODBC CLI/driver and connection strings.
```rust
use odbc_api::{Environment, ConnectionOptions};

pub fn db2_via_odbc(conn_str: &str) -> anyhow::Result<()> {
    let env = Environment::new()?;
    let conn = env.connect_with_connection_string(conn_str, ConnectionOptions::default())?;
    let cursor = conn.execute("SELECT CURRENT TIMESTAMP FROM SYSIBM.SYSDUMMY1", ())?
        .expect("result set expected");
    for row in cursor { println!("{:?}", row?); }
    Ok(())
}
```

[Back to top](#table-of-contents)

---

### 9.9 Abstractions (SQLx, Diesel, SeaORM)
```toml
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "mysql", "sqlite", "tls-rustls", "macros"] }
diesel = { version = "2", features = ["postgres","sqlite","mysql"] }
sea-orm = { version = "1", features = ["runtime-tokio-rustls", "sqlx-postgres", "sqlx-mysql", "sqlx-sqlite"] }
```

- **SQLx**: async, compile‑time validated queries (enable offline mode).
- **Diesel**: synchronous ORM; strong type‑safety; migrations.
- **SeaORM**: async ORM built atop SQLx.

[Back to top](#table-of-contents)

---

## 10. CRUD, Transactions & Prepared Statements
```rust
use sqlx::{Pool, Postgres, postgres::PgPoolOptions, Row};

pub async fn transfer(pool: &Pool<Postgres>, from: i64, to: i64, amount: i64) -> anyhow::Result<()> {
    let mut tx = pool.begin().await?;
    sqlx::query("UPDATE wallet SET balance = balance - $1 WHERE id=$2")
        .bind(amount).bind(from).execute(&mut *tx).await?;
    sqlx::query("UPDATE wallet SET balance = balance + $1 WHERE id=$2")
        .bind(amount).bind(to).execute(&mut *tx).await?;
    tx.commit().await?;
    Ok(())
}
```

[Back to top](#table-of-contents)

---

## 11. Data Processing (Polars, Arrow, Parquet)
```toml
polars = { version = "0.43", features = ["lazy", "parquet", "csv"] }
arrow = "53"
parquet = "53"
```

```rust
use polars::prelude::*;

pub fn aggregate_csv(path: &str) -> PolarsResult<DataFrame> {
    LazyCsvReader::new(path)
        .finish()?
        .groupby(["country"])
        .agg([col("amount").sum()])
        .collect()
}
```

[Back to top](#table-of-contents)

---

## 12. Streaming & CDC (Kafka/NATS)
```toml
rdkafka = { version = "0.36", features = ["tokio"] }
nats = "0.25"
```

```rust
use rdkafka::{consumer::{StreamConsumer}, ClientConfig};
use futures::StreamExt;

pub async fn kafka_consume(brokers: &str, topic: &str, group: &str) -> anyhow::Result<()> {
    let consumer: StreamConsumer = ClientConfig::new()
        .set("bootstrap.servers", brokers)
        .set("group.id", group)
        .set("auto.offset.reset", "earliest")
        .create()?;
    consumer.subscribe(&[topic])?;
    let mut stream = consumer.stream();
    while let Some(Ok(m)) = stream.next().await {
        if let Some(p) = m.payload() { println!("msg={}", String::from_utf8_lossy(p)); }
        consumer.commit_message(&m, rdkafka::consumer::CommitMode::Async)?;
    }
    Ok(())
}
```

[Back to top](#table-of-contents)

---

## 13. Pipelines & Orchestration
- Rust daemons scheduled by **cron/Kubernetes Jobs** or invoked by Airflow/Prefect.
- Use `tokio-cron-scheduler` for in‑process schedules.
```toml
tokio-cron-scheduler = "0.10"
```

```rust
use tokio_cron_scheduler::{JobScheduler, Job};
pub async fn schedule() -> anyhow::Result<()> {
    let sched = JobScheduler::new().await?;
    let job = Job::new_async("0 0/15 * * * *", |_uuid, _l| Box::pin(async move {
        println!("run healthcheck");
    }))?;
    sched.add(job).await?;
    sched.start().await?;
    Ok(())
}
```

[Back to top](#table-of-contents)

---

## 14. Testing & Quality
- Unit & integration tests: `cargo test`.
- **testcontainers-rs** to spin real DBs.
- Property tests: `proptest`/`quickcheck`.
- Benchmarks: `criterion`.

```toml
testcontainers = "0.16"
proptest = "1"
criterion = { version = "0.5", features = ["html_reports"] }
```

```rust
// tests/pg_it.rs
use testcontainers::{clients::Cli, images::postgres::Postgres};
#[test]
fn pg_smoke() {
    let docker = Cli::default();
    let node = docker.run(Postgres::default());
    let url = format!("postgres://postgres:postgres@localhost:{}/postgres",
                      node.get_host_port_ipv4(5432));
    // connect with sqlx and assert SELECT 1
}
```

[Back to top](#table-of-contents)

---

## 15. CI/CD & Packaging
- GitHub Actions/GitLab CI with **matrix** (OS/toolchains).
- Cache Cargo, **cross-compile** (musl), SBOM artifacts, release assets.
```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix: { toolchain: [stable] }
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo fmt --all -- --check
      - run: cargo clippy --all-targets -- -D warnings
      - run: cargo test --all --locked
```

[Back to top](#table-of-contents)

---

## 16. Cloud Integrations

### 16.1 AWS (SDK, Secrets, S3, STS)
```toml
aws-config = "1"
aws-sdk-s3 = "1"
aws-sdk-secretsmanager = "1"
```

```rust
use aws_sdk_s3 as s3;
pub async fn put_s3(bucket: &str, key: &str, body: Vec<u8>) -> anyhow::Result<()> {
    let cfg = aws_config::load_from_env().await;
    let client = s3::Client::new(&cfg);
    client.put_object().bucket(bucket).key(key).body(body.into()).send().await?;
    Ok(())
}
```

**Secrets Manager**
```rust
use aws_sdk_secretsmanager as sm;
pub async fn get_secret(name: &str) -> anyhow::Result<String> {
    let cfg = aws_config::load_from_env().await;
    let c = sm::Client::new(&cfg);
    let v = c.get_secret_value().secret_id(name).send().await?;
    Ok(v.secret_string().unwrap_or_default().to_string())
}
```

[Back to top](#table-of-contents)

---

### 16.2 Azure (Key Vault, Storage, Managed Identity)
```toml
azure_identity = "0.20"
azure_security_keyvault = "0.20"
azure_storage = { version = "0.22", features = ["blob"] }
```

```rust
use azure_identity::DefaultAzureCredential;
use azure_security_keyvault::SecretClient;
pub async fn kv_get(vault_url: &str, name: &str) -> anyhow::Result<String> {
    let cred = DefaultAzureCredential::default();
    let client = SecretClient::new(vault_url, cred)?;
    let resp = client.get(name).await?;
    Ok(resp.value)
}
```

[Back to top](#table-of-contents)

---

### 16.3 GCP (Secret Manager, GCS, Workload Identity)
Use REST/clients (community crates vary). Example with **yup-oauth2** + reqwest.
```toml
reqwest = { version = "0.12", features = ["json", "rustls-tls"] }
serde_json = "1"
yup-oauth2 = "8"
```

```rust
// Simplified example: fetch access token and call Secret Manager REST
```

[Back to top](#table-of-contents)

---

### 16.4 OCI (Object Storage, Autonomous)
Use signed requests or SDKs. Example with **reqwest** for Object Storage presigned PUT (outline).

```rust
// Outline: generate signed request (requires key fingerprint/tenancy/user OCIDs), then upload via reqwest.
```

[Back to top](#table-of-contents)

---

## 17. SRE & Reliability Patterns
- Health/readiness endpoints; graceful shutdown.
- Circuit breakers, rate limiting (Tower middlewares).
- SLI/SLO and error budgets as metrics.
```toml
axum = "0.7"
tower = { version = "0.5", features = ["limit", "timeout"] }
```

```rust
use axum::{routing::get, Router};
use std::net::SocketAddr;
#[tokio::main]
async fn main() {
    let app = Router::new().route("/healthz", get(|| async { "ok" }));
    let addr = SocketAddr::from(([0,0,0,0], 8080));
    axum::Server::bind(&addr).serve(app.into_make_service()).await.unwrap();
}
```

[Back to top](#table-of-contents)

---

## 18. Supply Chain Security & Compliance
- `cargo audit`, `cargo deny` for vulnerabilities and license policy.
- SBOM (CycloneDX) and artifact attestation.
```bash
cargo install cargo-audit cargo-deny cargo-cyclonedx
cargo audit
cargo deny check
cargo cyclonedx -o sbom.json
```

[Back to top](#table-of-contents)

---

## 19. Operational Runbooks
- **Connectivity errors**: DNS/TLS/CA, firewall, expired tokens, pool exhaustion.
- **Performance**: Nagle/latency, missing indexes, IO saturation, GC/alloc churn.
- **Failures**: deadlocks, lock waits, transaction timeouts; add statement timeouts.
- **Release**: blue/green, feature flags, rollout/rollback, data migrations.

[Back to top](#table-of-contents)

---

## 20. Templates & Scaffolds

**CLI ETL (clap + sqlx + polars)**
```toml
clap = { version = "4", features = ["derive"] }
anyhow = "1"
```

```rust
use clap::Parser;
#[derive(Parser, Debug)]
struct Args { #[arg(long)] input: String, #[arg(long)] pg: String }

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    let df = crate::processing::aggregate_csv(&args.input)?;
    let pool = crate::db::pg::pg_pool(&args.pg).await?;
    // upsert df rows into Postgres...
    Ok(())
}
```

**Microservice (axum + tracing + otel)**
```rust
use axum::{routing::get, Router};
use tracing::{info};
#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().json().with_env_filter("info").init();
    let app = Router::new()
        .route("/healthz", get(|| async {"ok"}))
        .route("/whoami", get(|| async {"service@v1"}));
    info!("listening on :8080");
    axum::Server::bind(&"0.0.0.0:8080".parse().unwrap())
        .serve(app.into_make_service()).await.unwrap();
}
```

[Back to top](#table-of-contents)

---

## 21. Appendix: Cheat Sheets & References

**Connection URLs (examples)**
- Postgres (SQLx): `postgres://USER:PASS@HOST:5432/db?sslmode=require`
- MySQL (mysql_async): `mysql://USER:PASS@HOST:3306/db`
- SQLite: `sqlite:////data/app.db`
- SQL Server (ODBC): `Driver={ODBC Driver 18 for SQL Server};Server=tcp:HOST,1433;Encrypt=yes;TrustServerCertificate=no;Database=DB;UID=U;PWD=P;`
- Oracle: `USER/PASS@HOST:1521/SERVICE`
- MongoDB: `mongodb+srv://USER:PASS@cluster0.example.mongodb.net/?retryWrites=true&tls=true`
- Redis: `rediss://USER:PASS@HOST:6379/0`
- DB2 (ODBC): `DATABASE=D;HOSTNAME=H;PORT=50000;PROTOCOL=TCPIP;UID=U;PWD=P;SECURITY=SSL;`

**Timeouts & Pooling (rules of thumb)**
- Connect timeout 3–10s; statement timeout aligned to SLOs.
- Bounded pools (8–64); instrument wait time; avoid thundering herds.
- Retry only idempotent ops; add jitter.

**Notes**
- Some crates evolve quickly; pin versions and review release notes.
- For SQLx compile‑time checks without live DB, use `SQLX_OFFLINE=true` with `sqlx-data.json`.

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
