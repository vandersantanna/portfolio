<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Docker for Database Platforms
*Secure images, consistent builds, persistence, and observability done right.*

## Table of Contents

- [1. Executive Summary & Value Proposition](#1-executive-summary--value-proposition)
- [2. Target Roles & Use-Cases (DBRE, DBA, DataOps)](#2-target-roles--use-cases-dbre-dba-dataops)
- [3. Tech Stack Overview (Docker, Compose, CI, Registries)](#3-tech-stack-overview-docker-compose-ci-registries)
- [4. Docker Fundamentals for Data Workloads](#4-docker-fundamentals-for-data-workloads)
- [5. Image Strategy & Base Images](#5-image-strategy--base-images)
- [6. Supply Chain Security](#6-supply-chain-security)
- [7. Registry & Tagging Strategy](#7-registry--tagging-strategy)
- [8. Build Automation (CI/CD)](#8-build-automation-cicd)
- [9. Local Dev Environments](#9-local-dev-environments)
- [10. Orchestration Path & Migration Strategy](#10-orchestration-path--migration-strategy)
- [11. Storage & Persistence](#11-storage--persistence)
- [12. Backup & Recovery Patterns](#12-backup--recovery-patterns)
- [13. Networking & Security](#13-networking--security)
- [14. Secrets Management](#14-secrets-management)
- [15. Observability for Containerized Databases](#15-observability-for-containerized-databases)
- [16. Healthchecks, Probes & Reliability](#16-healthchecks-probes--reliability)
- [17. Resource Sizing & Performance](#17-resource-sizing--performance)
- [18. Platform & Compatibility](#18-platform--compatibility)
- [19. High Availability Topologies in Containers](#19-high-availability-topologies-in-containers)
- [20. DataOps Pipelines in Containers](#20-dataops-pipelines-in-containers)
- [21. CI/CD for Database Changes](#21-cicd-for-database-changes)
- [22. Governance, Cost & Compliance](#22-governance-cost--compliance)
- [23. DR & Multi-Region Strategies](#23-dr--multi-region-strategies)
- [24. Runbooks & On-Call Playbooks](#24-runbooks--on-call-playbooks)
- [25. Portfolio Showcases (Hands-On Projects)](#25-portfolio-showcases-hands-on-projects)
- [26. Reusable Templates & Snippets Library](#26-reusable-templates--snippets-library)
- [27. Checklists (Security, Backup/DR, Perf, Observability)](#27-checklists-security-backupdr-perf-observability)
- [28. FAQ & Anti-Patterns](#28-faq--anti-patterns)
- [29. Roadmap & Next Steps](#29-roadmap--next-steps)


---

## 1. Executive Summary & Value Proposition

>A curated, hands-on portfolio page showing how I apply Docker to database reliability, operations, and data engineering workflows. Each section includes a short explanation and three concise, copy-ready examples (Dockerfiles, Compose snippets, CLI, CI, checklists).

Containerization accelerates DBRE/DBA/DataOps workflows by standardizing environments, reducing drift, and enabling reproducible builds, tests, and operations. This guide demonstrates practical patterns for secure images, persistent storage, observability, CI/CD for schema changes, and disaster recovery testing—all with minimal toil and maximum reliability.

**Examples**
1) Minimal, reproducible DB client tool image:
```dockerfile
# docker/db-tools/Dockerfile
FROM debian:stable-slim
RUN apt-get update && apt-get install -y --no-install-recommends     postgresql-client mysql-client curl ca-certificates && rm -rf /var/lib/apt/lists/*
USER 65532:65532
ENTRYPOINT ["bash","-lc"]
```
2) Smoke test a database container locally:
```bash
docker run --rm -d --name pg -e POSTGRES_PASSWORD=pg -p 5432:5432 postgres:16
pg_isready -h 127.0.0.1 -p 5432
```
3) One-liner nightly backup job via `cron` container:
```bash
docker run --rm --env-file env/pg.env   -v $PWD/backups:/backups   ghcr.io/vsantanna/pg-backup:latest bash -lc 'pg_dump -Fc -h $PGHOST -U $PGUSER $PGDATABASE > /backups/$(date +%F).dump'
```

---

## 2. Target Roles & Use-Cases (DBRE, DBA, DataOps)
This portfolio aligns with DBRE (reliability), DBA (operations, HA/DR), and DataOps (pipelines, automation). Use-cases include portable labs, CI migrations, observability PoCs, and repeatable DR drills.

**Examples**
1) DBRE: SLO lab with containerized Prometheus + exporters:
```yaml
# compose.slo.yaml
services:
  prometheus:
    image: prom/prometheus
    volumes: [ "./prometheus.yml:/etc/prometheus/prometheus.yml" ]
    ports: [ "9090:9090" ]
  postgres:
    image: postgres:16
    environment: [ "POSTGRES_PASSWORD=pg" ]
    ports: [ "5432:5432" ]
  pg_exporter:
    image: wrouesnel/postgres_exporter
    environment: [ "DATA_SOURCE_NAME=postgresql://postgres:pg@postgres:5432/postgres?sslmode=disable" ]
```
2) DBA: Restore rehearsal:
```bash
docker run --rm -v $PWD/backups:/bkp postgres:16 bash -lc  'pg_restore -h host.docker.internal -U postgres -d restoredb /bkp/2025-10-10.dump'
```
3) DataOps: dbt run inside ephemeral container:
```bash
docker run --rm -v $PWD/dbt:/dbt -w /dbt   ghcr.io/dbt-labs/dbt-postgres:1.8.7 bash -lc "dbt deps && dbt run --profiles-dir ."
```

---

## 3. Tech Stack Overview (Docker, Compose, CI, Registries)
Core tools: Docker Engine, Buildx, Compose; CI orchestrators (GitHub Actions/GitLab CI); registries (ECR/GCR/ACR/Artifact Registry/GHCR). Complement with security scanners and policy enforcement.

**Examples**
1) Enable Buildx and build multi-arch:
```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/vsantanna/db-tools:1.0 .
```
2) Compose profile-based stacks:
```yaml
# compose.yaml
services:
  db: { image: postgres:16, environment: ["POSTGRES_PASSWORD=pg"] }
  app: { image: myorg/app:latest, depends_on: [db] }
profiles: { dev: {}, test: {} }
```
3) Login + push to GHCR:
```bash
echo $GHCR_PAT | docker login ghcr.io -u vsantanna --password-stdin
docker push ghcr.io/vsantanna/db-tools:1.0
```

---

## 4. Docker Fundamentals for Data Workloads
Understand layers, union filesystems, copy-on-write, and how they impact IO-heavy DBs. Prefer minimal images and externalize data through volumes.

**Examples**
1) Layer-aware Dockerfile (minimize invalidation):
```dockerfile
FROM postgres:16
COPY docker/healthcheck.sh /usr/local/bin/
HEALTHCHECK --interval=15s --timeout=3s CMD healthcheck.sh
```
2) Volume mapping for data:
```bash
docker volume create pgdata
docker run -d --name pg -v pgdata:/var/lib/postgresql/data postgres:16
```
3) Read-only root filesystem:
```bash
docker run -d --read-only --tmpfs /tmp --tmpfs /run myorg/readonly-db-client:latest
```

---

## 5. Image Strategy & Base Images
Choose stable bases (Debian/Ubuntu/Oracle Linux) or distroless for tools; apply multi-stage builds and drop privileges.

**Examples**
1) Multi-stage w/ tools only:
```dockerfile
FROM golang:1.22 AS build
WORKDIR /src; COPY . .
RUN CGO_ENABLED=0 go build -o /out/dbcheck ./cmd/dbcheck

FROM gcr.io/distroless/static
USER 65532:65532
COPY --from=build /out/dbcheck /usr/local/bin/dbcheck
ENTRYPOINT ["dbcheck"]
```
2) Non-root user:
```dockerfile
RUN useradd -u 10001 -r -s /sbin/nologin appuser
USER 10001
```
3) Slim variant + cleanup:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends curl     && rm -rf /var/lib/apt/lists/*
```

---

## 6. Supply Chain Security
Generate SBOMs, scan images, sign and verify. Enforce policies in CI and at deploy time.

**Examples**
1) SBOM + vulnerability scan:
```bash
syft ghcr.io/vsantanna/db-tools:1.0 -o spdx-json > sbom.json
trivy image --exit-code 1 --severity CRITICAL,HIGH ghcr.io/vsantanna/db-tools:1.0
```
2) Sign & verify with Cosign:
```bash
cosign sign ghcr.io/vsantanna/db-tools:1.0
cosign verify ghcr.io/vsantanna/db-tools:1.0
```
3) Policy test with Conftest:
```bash
conftest test k8s/deployment.yaml -p policy/
```

---

## 7. Registry & Tagging Strategy
Use semantic tags, immutable digests, and retention policies to cut storage costs and prevent rollbacks surprises.

**Examples**
1) Semantic + commit SHA tags:
```bash
docker tag app:latest ghcr.io/vsantanna/app:1.4.2
docker tag app:latest ghcr.io/vsantanna/app:1.4.2-2f1a6d7
```
2) Pin by digest (immutable):
```yaml
image: "ghcr.io/vsantanna/app@sha256:8b9e..."
```
3) Registry GC & retention (concept commands):
```bash
gh api repos/{owner}/{repo}/packages/container/app/versions --paginate | jq .
# Apply retention rules in registry UI / IaC module
```

---

## 8. Build Automation (CI/CD)
Cache builds, use BuildKit/Buildx, and fail early on security scans.

**Examples**
1) GitHub Actions (build, scan, push):
```yaml
# .github/workflows/build.yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GHCR_PAT }} }
      - uses: docker/build-push-action@v6
        with: { context: ., push: true, tags: ghcr.io/vsantanna/db-tools:latest }
      - run: trivy image --exit-code 1 ghcr.io/vsantanna/db-tools:latest
```
2) GitLab CI cache + multi-arch:
```yaml
build:
  image: docker:27
  services: [docker:27-dind]
  script:
    - docker buildx create --use
    - docker buildx build --platform linux/amd64,linux/arm64 -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA --push .
```
3) Reproducible build args:
```bash
docker build --build-arg VERSION=1.4.2 --build-arg BUILD_DATE=$(date -u +%F) .
```

---

## 9. Local Dev Environments
Compose stacks, Dev Containers, and Makefiles provide fast feedback and parity with CI.

**Examples**
1) Dev container (VS Code):
```json
// .devcontainer/devcontainer.json
{ "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": { "ghcr.io/devcontainers/features/docker-in-docker:2": {} } }
```
2) Makefile targets:
```make
up: ; docker compose up -d
down: ; docker compose down -v
logs: ; docker compose logs -f
```
3) Reusable Compose for DB + Adminer:
```yaml
services:
  db: { image: postgres:16, environment: ["POSTGRES_PASSWORD=pg"], ports: ["5432:5432"] }
  adminer: { image: adminer, ports: ["8080:8080"], depends_on: [db] }
```

---

## 10. Orchestration Path & Migration Strategy
Start with Compose for local/dev, graduate to Kubernetes/Helm for production-grade HA, networking, and policies.

**Examples**
1) Compose → K8s conversion (kompose quick start):
```bash
kompose convert -f compose.yaml -o k8s/
```
2) Helm value parity:
```yaml
# values-db.yaml
image:
  repository: postgres
  tag: "16"
persistence:
  enabled: true
  size: 50Gi
```
3) Swarm legacy note (one-liner):
```bash
docker stack deploy -c compose.yaml dbstack
```

---

## 11. Storage & Persistence
Use named volumes for portability, bind mounts for dev, and choose drivers based on IO patterns. Consider NFS/SMB/ZFS; test fsync behavior.

**Examples**
1) Named volume with options:
```bash
docker volume create pgdata --opt type=none --opt o=size=100g --opt device=/data/pg
```
2) NFS mount for backups:
```yaml
services:
  backup:
    image: alpine
    volumes: [ "nfs-bkp:/bkp" ]
volumes:
  nfs-bkp:
    driver_opts: { type: "nfs", o: "addr=10.0.0.10,nolock,soft,rw", device: ":/exports/bkp" }
```
3) tmpfs to protect secrets at rest:
```bash
docker run --tmpfs /run --tmpfs /tmp myorg/db-job:latest
```

---

## 12. Backup & Recovery Patterns
Codify dumps and physical backups, encrypt artifacts, and rehearse restores regularly (chaos drills).

**Examples**
1) PostgreSQL + pgBackRest (sidecar pattern):
```yaml
services:
  postgres: { image: postgres:16, volumes: [ "pgdata:/var/lib/postgresql/data" ] }
  pgbackrest: { image: ghcr.io/pgbackrest/pgbackrest, volumes: [ "pgdata:/pgdata", "./bkp:/bkp" ] }
```
2) MySQL XtraBackup:
```bash
docker run --rm percona/percona-xtrabackup:8.0 --version
# exec into mysql container -> xtrabackup --backup --target-dir=/bkp
```
3) SQL Server backup to mounted share:
```sql
BACKUP DATABASE MyDb TO DISK = N'/var/opt/mssql/backup/mydb.bak' WITH COMPRESSION, INIT;
```

---

## 13. Networking & Security
Leverage user-defined networks, firewall rules, rootless mode, seccomp/AppArmor/SELinux profiles.

**Examples**
1) Isolated network:
```bash
docker network create --driver bridge dbnet
docker run -d --network dbnet --name pg postgres:16
```
2) Custom seccomp:
```bash
docker run --security-opt seccomp=./seccomp-profile.json myorg/db-client:latest
```
3) TLS for Postgres (mount certs):
```yaml
services:
  postgres:
    image: postgres:16
    volumes: [ "./certs:/certs:ro" ]
    environment: ["SSL_CERT_FILE=/certs/server.crt","SSL_KEY_FILE=/certs/server.key"]
```

---

## 14. Secrets Management
Avoid `.env` leaks. Use Docker Secrets, SOPS, or Vault for encryption and rotation.

**Examples**
1) Docker Secrets in Compose:
```yaml
services:
  pg:
    image: postgres:16
    secrets: [ "pgpass" ]
secrets:
  pgpass:
    file: ./secrets/pgpass.txt
```
2) SOPS-encrypted env:
```bash
sops -e .env > .env.enc     # encrypt
sops -d .env.enc | docker --env-file - run myorg/app:latest
```
3) Vault agent sidecar (concept):
```hcl
template { source = "dbcreds.ctmpl" destination = "/secrets/db.env" }
```

---

## 15. Observability for Containerized Databases
Collect logs, metrics, and traces; define SLIs/SLOs and alert rules. Use exporters and centralized storage.

**Examples**
1) Postgres exporter:
```bash
docker run -d -p 9187:9187  -e DATA_SOURCE_NAME="postgresql://postgres:pg@host.docker.internal:5432/postgres?sslmode=disable"  wrouesnel/postgres_exporter
```
2) Loki log pipeline (vector):
```toml
# vector.toml
[sources.docker] type = "docker_logs"
[sinks.loki] type = "loki"; inputs = ["docker"]; endpoint = "http://loki:3100"
```
3) Prometheus alert for replication lag:
```yaml
- alert: PostgresReplicationLagHigh
  expr: pg_replication_lag_bytes > 104857600
  for: 5m
```

---

## 16. Healthchecks, Probes & Reliability
Use container `HEALTHCHECK`, graceful shutdown, restart policies, and dependency ordering (wait-for scripts).

**Examples**
1) Dockerfile healthcheck:
```dockerfile
HEALTHCHECK --interval=15s --timeout=3s CMD pg_isready -h 127.0.0.1 -p 5432 || exit 1
```
2) Compose restart/backoff:
```yaml
services:
  pg:
    image: postgres:16
    restart: unless-stopped
    healthcheck: { test: ["CMD-SHELL","pg_isready -U postgres"], interval: "15s", retries: 5 }
```
3) Graceful trap:
```bash
trap "pg_ctl -D /var/lib/postgresql/data stop -m fast" SIGTERM
```

---

## 17. Resource Sizing & Performance
Set CPU/memory, consider NUMA, storage drivers, fs tuning, and sysctl for DBs.

**Examples**
1) Limits/requests:
```bash
docker run -d --cpus="2.0" --memory="4g" postgres:16
```
2) Kernel parameters (host):
```bash
sudo sysctl -w vm.swappiness=1 fs.file-max=200000 net.core.somaxconn=1024
```
3) IO scheduler (host tuning note):
```bash
# Example (requires root and correct device):
echo mq-deadline | sudo tee /sys/block/nvme0n1/queue/scheduler
```

---

## 18. Platform & Compatibility
Consider Linux vs Windows containers (SQL Server), amd64 vs arm64 (Raspberry Pi labs), and feature parity differences.

**Examples**
1) SQL Server on Linux container:
```bash
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=Pass@word!' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
```
2) Multi-arch build artifact tags:
```bash
docker buildx build --platform linux/arm64 -t ghcr.io/vsantanna/pg-tools:arm64 --push .
```
3) Linux vs Windows (note):
```text
Windows containers required for Windows-based SQL Server features; otherwise prefer Linux for size/perf.
```

---

## 19. High Availability Topologies in Containers
Use containers for HA labs and PoCs. For production, prefer orchestrators (K8s) and managed storage/networking.

**Examples**
1) PostgreSQL Patroni (3-node lab):
```yaml
# patroni-compose.yaml (abridged)
services: { patroni1: { image: zalando/patroni }, patroni2: { image: zalando/patroni }, patroni3: { image: zalando/patroni } }
```
2) MySQL InnoDB Cluster:
```bash
# mysqlsh within container
dba.createCluster('prodCluster')
```
3) Redis Sentinel:
```yaml
services:
  redis: { image: redis:7, command: ["redis-server","--appendonly","yes"] }
  sentinel: { image: bitnami/redis-sentinel:latest, environment: ["REDIS_MASTER_HOST=redis"] }
```

---

## 20. DataOps Pipelines in Containers
Containerize ingestion (CDC), orchestration, transform, and quality checks for reproducibility and isolation.

**Examples**
1) Debezium + Kafka (CDC):
```yaml
services:
  kafka: { image: redpanda/redpanda }
  debezium: { image: debezium/connect:2.7, environment: ["BOOTSTRAP_SERVERS=kafka:9092"] }
```
2) Airbyte connector run:
```bash
docker run --rm airbyte/source-postgres:latest --help
```
3) Airflow + dbt + Great Expectations:
```yaml
services:
  airflow: { image: apache/airflow:2.9.3, volumes: ["./dags:/opt/airflow/dags"] }
```

---

## 21. CI/CD for Database Changes
Automate migrations, static checks, approvals, and rollbacks. Use ephemeral DBs for integration tests.

**Examples**
1) Flyway migration in CI:
```bash
docker run --rm -v $PWD/sql:/flyway/sql flyway/flyway -url=jdbc:postgresql://db:5432/app -user=app -password=*** migrate
```
2) Liquibase drift report:
```bash
docker run --rm -v $PWD/changelog:/liquibase/changelog liquibase/liquibase diff
```
3) SQL Server DACPAC in container:
```bash
docker run --rm mcr.microsoft.com/dotnet/sdk:8.0   dotnet tool install -g dotnet-sqlpackage && sqlpackage /?
```

---

## 22. Governance, Cost & Compliance
Track who built what, enforce policies, and control egress/storage costs (retention, compression, dedupe).

**Examples**
1) Provenance labels:
```dockerfile
LABEL org.opencontainers.image.revision=$GIT_SHA       org.opencontainers.image.source="https://github.com/vsantanna/db-tools"
```
2) Retention policy (registry/IaC snippet):
```yaml
retention:
  keep_last: 10
  protect_tags: ["^v\d+\.\d+\.\d+$"]
```
3) Audit log shipping:
```bash
docker logs pg | gzip -c > logs/pg-$(date +%F).log.gz
```

---

## 23. DR & Multi-Region Strategies
Automate backup shipping, verify RPO/RTO with timed drills, and codify infra rebuild with IaC.

**Examples**
1) Encrypted backup with `restic`:
```bash
restic -r s3:s3.amazonaws.com/mybucket/pg -p .restic.pwd backup backups/
```
2) Cross-region copy (example CLI pattern):
```bash
aws s3 cp s3://west/pg/ s3://east/pg/ --recursive --storage-class STANDARD_IA
```
3) Timed DR drill:
```bash
time docker compose -f restore.yaml up --abort-on-container-exit
```

---

## 24. Runbooks & On-Call Playbooks
Document incident workflows, safe / reversible steps, and templates for consistent execution under pressure.

**Examples**
1) Connection storm mitigation (snippet):
```bash
psql -c "ALTER SYSTEM SET max_connections=800; SELECT pg_reload_conf();"
```
2) Replication lag triage:
```bash
psql -c "SELECT now()-pg_last_xact_replay_timestamp() AS lag;"
```
3) Disk pressure response:
```bash
du -sh /var/lib/postgresql/data/* | sort -h
```

---

## 25. Portfolio Showcases (Hands-On Projects)
A few focused, end-to-end labs to demonstrate skills and decisions trade-offs.

**Examples**
1) Postgres HA (Patroni) on Compose: init cluster, add replica, failover; collect metrics with exporter and assert SLOs in Prometheus.
2) Airflow + dbt + Great Expectations: containerized pipeline against Postgres, with CI hooks to run `dbt test` and GE validations on PRs.
3) Observability stack: Prometheus + Grafana + Loki with database exporters, log labels, and alert rules for backups/lag/CPU saturation.

---

## 26. Reusable Templates & Snippets Library
Small, opinionated building blocks for repeat usage in labs and client work.

**Examples**
1) Hardened DB client Dockerfile:
```dockerfile
FROM debian:stable-slim
RUN adduser --system --uid 65532 app
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client ca-certificates && rm -rf /var/lib/apt/lists/*
USER app
ENTRYPOINT ["psql"]
```
2) Compose healthchecks library:
```yaml
x-health: &pghealth { test: ["CMD-SHELL","pg_isready -U postgres"], interval: 10s, timeout: 3s, retries: 5 }
services:
  pg: { image: postgres:16, healthcheck: *pghealth }
```
3) Generic `.env.example`:
```env
PGHOST=localhost
PGUSER=postgres
PGPASSWORD=pg
PGDATABASE=app
```

---

## 27. Checklists (Security, Backup/DR, Perf, Observability)
Compact, pragmatic checklists reduce errors and cut MTTR. Treat them as living documents.

**Examples**
1) Security (excerpt):
```text
[ ] Non-root user
[ ] Read-only rootfs (when possible)
[ ] Image signed & verified
[ ] Secrets via Docker Secrets/SOPS/Vault
```
2) Backup/DR (excerpt):
```text
[ ] Nightly backups succeed & are encrypted
[ ] Weekly restore tests (timed)
[ ] Offsite copy / multi-region verified
```
3) Performance (excerpt):
```text
[ ] CPU/mem limits aligned to workload
[ ] Storage driver + fs tuned
[ ] Connection pool & max_connections sane
```

---

## 28. FAQ & Anti-Patterns
Curated pitfalls and clarifications to steer teams toward reliability and maintainability.

**Examples**
1) Anti-patterns:
```text
- Running prod databases with bind mounts on laptops
- Baking secrets into images or .env committed to git
- Ignoring fsync / WAL durability settings for speed
```
2) “Can I run prod DBs in Docker?”  
Short answer: Yes with care—use orchestrators, reliable storage, network policies, backup/DR, and hard SLOs.  
3) “Why multi-arch?”  
To ensure parity across dev (arm64 laptops) and prod (amd64 servers) and speed up local onboarding.

---

## 29. Roadmap & Next Steps
Iterate from portable labs to production-grade orchestrations; add policy-as-code, performance baselines, and deeper HA/DR automation.

**Examples**
1) Add OPA Gatekeeper policies for image provenance and resource limits.  
2) Integrate disaster-recovery drills into CI (spin up restore envs per release).  
3) Expand exporters coverage (Oracle, SQL Server, MongoDB) with standardized dashboards.

---

## Appendix A — Sample Full Compose (Dev DB Stack, Abridged)
A compact stack you can run locally to explore backups, healthchecks, and metrics.

```yaml
version: "3.9"
services:
  postgres:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=pg
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL","pg_isready -U postgres"]
      interval: 10s
      timeout: 3s
      retries: 5
    ports: ["5432:5432"]

  pg_exporter:
    image: wrouesnel/postgres_exporter
    environment:
      - DATA_SOURCE_NAME=postgresql://postgres:pg@postgres:5432/postgres?sslmode=disable
    depends_on: [postgres]
    ports: ["9187:9187"]

  adminer:
    image: adminer
    depends_on: [postgres]
    ports: ["8080:8080"]

volumes:
  pgdata:
```
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

