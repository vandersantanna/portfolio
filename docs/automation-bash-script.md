# Bash Automation Portfolio (DBA · DBRE · DataOps)

> **Scope:** Complete single-file Markdown `.md` with concise code samples and checklists per topic. Designed for real-world automation in DBA/DBRE/DataOps.

---

## Table of Contents

- [1. Executive Summary & Value Proposition](#1-executive-summary--value-proposition)
- [2. Principles, Patterns & Style Guide](#2-principles-patterns--style-guide)
- [3. Toolchain & Environment](#3-toolchain--environment)
- [4. Safety, Idempotency & Resilience](#4-safety-idempotency--resilience)
- [5. Argument Parsing, I/O & Error Handling](#5-argument-parsing-io--error-handling)
- [6. Logging, Metrics & Tracing](#6-logging-metrics--tracing)
- [7. Configuration, Secrets & Credentials](#7-configuration-secrets--credentials)
- [8. Scheduling, Orchestration & Runners](#8-scheduling-orchestration--runners)
- [9. Concurrency, Parallelism & Work Queues](#9-concurrency-parallelism--work-queues)
- [10. Filesystem, Streams & Data Handling](#10-filesystem-streams--data-handling)
- [11. Text, CSV, JSON, YAML Processing](#11-text-csv-json-yaml-processing)
- [12. Networking, APIs & Webhooks](#12-networking-apis--webhooks)
- [13. SSH, Fleet Automation & Remote Exec](#13-ssh-fleet-automation--remote-exec)
- [14. Packaging, Distribution & Versioning](#14-packaging-distribution--versioning)
- [15. Testing, Linting & Quality Gates](#15-testing-linting--quality-gates)
- [16. CI/CD Integration (GitHub, GitLab, Jenkins)](#16-cicd-integration-github-gitlab-jenkins)
- [17. Cloud & Containers (AWS, Azure, GCP, OCI, Docker, K8s)](#17-cloud--containers-aws-azure-gcp-oci-docker-k8s)
- [18. Database Automations: Oracle, PostgreSQL, MySQL, SQL Server, MongoDB, Redis](#18-database-automations-oracle-postgresql-mysql-sql-server-mongodb-redis)
- [19. Backup, Restore, HA/DR & Disaster Recovery Playbooks](#19-backup-restore-hadr--disaster-recovery-playbooks)
- [20. DataOps Pipelines: Ingestion, CDC, Transform, Validate](#20-dataops-pipelines-ingestion-cdc-transform-validate)
- [21. Observability, Health Checks & SLOs](#21-observability-health-checks--slos)
- [22. Compliance, Auditing & Governance](#22-compliance-auditing--governance)
- [23. Templates, Scaffolds & Boilerplates](#23-templates-scaffolds--boilerplates)
- [24. Reusable Libraries & Helper Utilities](#24-reusable-libraries--helper-utilities)
- [25. Sample Projects & Use Cases](#25-sample-projects--use-cases)
- [26. Migration, Cutover & Rollback Tooling](#26-migration-cutover--rollback-tooling)
- [27. Incident Response, War Rooms & Postmortems](#27-incident-response-war-rooms--postmortems)
- [28. Security Hardening & Key Management](#28-security-hardening--key-management)
- [29. Roadmap, Extensions & Wish List](#29-roadmap-extensions--wish-list)
- [30. Appendix: Cheat Sheets & References](#30-appendix-cheat-sheets--references)

---

## 1. Executive Summary & Value Proposition

**What Bash excels at**: glue code, orchestration, logics around CLI tools, fast prototypes, lightweight agents.  
**KPIs**: Lead Time ↓, MTTR ↓, Change Failure Rate ↓, Data Freshness ↑, Success Rate ↑.

**Mini example – “glue” orchestration:**

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
log(){ printf '%s %s\n' "$(date -Is)" "$*" >&2; }
src="sftp://ingest/incoming/"; dst="/data/staging"
log "Syncing…"; rclone sync "$src" "$dst" --transfers=8 --checkers=16 --stats=15s
log "Validating…"; find "$dst" -type f -name '*.csv' -print0 | xargs -0 -n1 -P4 ./validate_csv.sh
log "Loading…"; ./load_to_db.sh "$dst"
```

**Checklist**

- [ ] Clear SLOs (latency, freshness, success %)
- [ ] Idempotent runs & safe retries
- [ ] Observability baked in (logs/metrics/traces)
- [ ] Rollback path and failure isolation

[Back to top](#table-of-contents)

---

## 2. Principles, Patterns & Style Guide

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
shopt -s lastpipe 2>/dev/null || true

# Safe defaults
IFS=$'\n\t'; umask 027

# Traps & cleanup
tmpdir="$(mktemp -d)"
cleanup(){ rm -rf "$tmpdir"; }
trap cleanup EXIT INT TERM

# Retry with exponential backoff
retry(){
  local max="${1:-5}" i=0
  shift
  until "$@"; do
    ((i++>=max)) && return 1
    sleep "$((2**i))"
  done
}
```

**Checklist**

- [ ] `set -Eeuo pipefail` and `IFS` hardened
- [ ] `trap` ensures cleanup
- [ ] No unquoted expansions; avoid `eval`
- [ ] Shellcheck + shfmt enforced

[Back to top](#table-of-contents)

---

## 3. Toolchain & Environment

```bash
need(){ command -v "$1" >/dev/null 2>&1 || { echo "Missing dep: $1" >&2; exit 127; }; }
for bin in awk sed grep find xargs jq yq rsync curl; do need "$bin"; done

# GNU vs BSD differences example (sed -i)
sed_in_place(){
  if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i '' "$@"; fi
}
```

**Checklist**

- [ ] Reproducible runner (Docker/systemd-run/nix)
- [ ] Minimal dependency set documented
- [ ] Cross-distro quirks handled

[Back to top](#table-of-contents)

---

## 4. Safety, Idempotency & Resilience

```bash
lock="/var/lock/myjob.lock"
exec 9>"$lock"; flock -n 9 || { echo "Already running"; exit 0; }

STATE="/var/lib/myjob/state.json"
if [[ -f "$STATE" ]]; then echo "Resuming…"; fi

# Timeout wrapper
with_timeout(){ perl -e 'alarm shift; exec @ARGV' "$@"; }

with_timeout 900 ./do_work.sh || { echo "Timed out" >&2; exit 124; }
```

**Checklist**

- [ ] `flock` guards
- [ ] State files & checkpoints
- [ ] Timeouts and dead letter handling

[Back to top](#table-of-contents)

---

## 5. Argument Parsing, I/O & Error Handling

```bash
usage(){ echo "Usage: $0 -i INPUT -o OUTPUT [--json]"; }
json=false; in= out=
while (( "$#" )); do
  case "$1" in
    -i) in="$2"; shift 2;;
    -o) out="$2"; shift 2;;
    --json) json=true; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown: $1" >&2; usage; exit 2;;
  esac
done

err(){ printf '{"level":"error","msg":"%s"}\n' "$*" >&2; }
ok(){  printf '{"level":"info","msg":"%s"}\n' "$*"; }
```

**Checklist**

- [ ] Exit codes consistent
- [ ] Human vs machine-readable output modes
- [ ] Strict argument validation

[Back to top](#table-of-contents)

---

## 6. Logging, Metrics & Tracing

```bash
log(){ printf '%s %-5s %s\n' "$(date -Is)" "$1" "$2" >&2; }
log INFO "Starting job"

# Prometheus textfile exporter
metrics="/var/lib/node_exporter/textfile/myjob.prom"
{
  echo "# HELP myjob_processed_rows Total processed rows"
  echo "# TYPE myjob_processed_rows counter"
  echo "myjob_processed_rows 1234"
} > "$metrics"

# Simple trace correlation
TRACE_ID="${TRACE_ID:-$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)}"
log INFO "trace_id=$TRACE_ID step=download"
```

**Checklist**

- [ ] Log levels & structure
- [ ] Textfile metrics where no agent exists
- [ ] Trace IDs carried via env/args

[Back to top](#table-of-contents)

---

## 7. Configuration, Secrets & Credentials

```bash
# Load .env
set -a; [ -f ".env" ] && . ".env"; set +a

# Secret fetch (example: AWS SSM)
get_secret(){
  aws ssm get-parameter --name "$1" --with-decryption --query Parameter.Value --output text
}
DB_PASS="$(get_secret "/prod/db/password")"
redact(){ sed -E "s/${DB_PASS:0:3}[A-Za-z0-9]+/***REDACTED***/g"; }
```

**Checklist**

- [ ] No secrets in history/logs
- [ ] Central secret store (Vault/KMS/SSM/Key Vault)
- [ ] Principle of least privilege

[Back to top](#table-of-contents)

---

## 8. Scheduling, Orchestration & Runners

```bash
# Cron (UTC)
# m h dom mon dow  cmd
0 * * * * /opt/pipelines/hourly_sync.sh >>/var/log/hourly_sync.log 2>&1

# systemd timer
# /etc/systemd/system/myjob.timer
# [Timer]
# OnCalendar=*:0/15
# Persistent=true
# /etc/systemd/system/myjob.service
# ExecStart=/opt/myjob/run.sh
```

**Checklist**

- [ ] Timezone & DST aware
- [ ] Missed runs handled (Persistent timers)
- [ ] Blackout windows & concurrency controls

[Back to top](#table-of-contents)

---

## 9. Concurrency, Parallelism & Work Queues

```bash
# Parallel file processing
find /data/in -name '*.csv' -print0 | xargs -0 -n1 -P4 ./process_one.sh

# GNU parallel (if available)
export -f process_one
parallel -j8 process_one ::: /data/in/*.csv

# Simple disk-backed queue
queue="/var/lib/queue"
mkdir -p "$queue"/{todo,doing,done}
for job in "$queue"/todo/*; do
  mv "$job" "$queue/doing/" && ./worker.sh "$queue/doing/$(basename "$job")"
done
```

**Checklist**

- [ ] Bounded parallelism
- [ ] Backpressure/rate limits
- [ ] At-least-once semantics

[Back to top](#table-of-contents)

---

## 10. Filesystem, Streams & Data Handling

```bash
# Atomic write
atomic_write(){
  local target="$1" tmp
  tmp="$(mktemp "${target}.XXXX")" && cat >"$tmp" && mv -f "$tmp" "$target"
}

# Large files
split -b 2G bigfile.dat bigfile.part.
cat bigfile.part.* > bigfile.reassembled

# Watcher
inotifywait -m /data/incoming -e create -e moved_to | while read -r dir ev file; do
  ./handle_new_file.sh "$dir/$file"
done
```

**Checklist**

- [ ] Atomic operations; checksum verification
- [ ] Backups and retention policy
- [ ] Watchers for near-real-time ingest

[Back to top](#table-of-contents)

---

## 11. Text, CSV, JSON, YAML Processing

```bash
# CSV: count rows, skip header
rows=$(awk 'NR>1{c++} END{print c+0}' file.csv)

# JSON: jq selection
jq -r '.items[] | select(.active==true) | .id' items.json

# YAML → JSON → field
yq -o=json '.spec.template' k8s.yaml | jq -r '.metadata.name'
```

**Checklist**

- [ ] Locale-safe processing (LC_ALL=C)
- [ ] Quoting/escaping rules for CSV
- [ ] Streaming where possible

[Back to top](#table-of-contents)

---

## 12. Networking, APIs & Webhooks

```bash
# Curl with retries and timeouts
curl --retry 5 --retry-all-errors --max-time 20 --connect-timeout 5 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"ok"}' \
  https://api.example.com/v1/heartbeat

# Verify signature (HMAC) from webhook
sig_check(){
  local payload="$1" sig="$2"
  printf '%s' "$payload" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" -binary | xxd -p -c 256 | grep -qi "^$sig$"
}
```

**Checklist**

- [ ] Timeouts + retries + backoff
- [ ] TLS/mTLS verification
- [ ] Webhook auth/verification

[Back to top](#table-of-contents)

---

## 13. SSH, Fleet Automation & Remote Exec

```bash
# ~/.ssh/config uses ProxyJump bastion
# Host db-*.prod
#   User ec2-user
#   ProxyJump bastion
#   IdentityFile ~/.ssh/id_ed25519

# Run a command on host list in parallel
export -f remote_check
remote_check(){ ssh -o BatchMode=yes "$1" 'uptime; df -h /'; }
parallel -a hosts.txt -j20 remote_check
```

**Checklist**

- [ ] SSH CA / short-lived certs
- [ ] Bastion & restricted commands
- [ ] Idempotent remote changes

[Back to top](#table-of-contents)

---

## 14. Packaging, Distribution & Versioning

```bash
VERSION="1.3.0"
if [[ "${1:-}" == "--version" ]]; then echo "$VERSION"; exit 0; fi

# Simple tarball package
pkg(){ tar czf "mytool-${VERSION}.tar.gz" mytool.sh lib/ README.md; }
```

**Checklist**

- [ ] SemVer + changelog
- [ ] Checksums/signatures
- [ ] Reproducible builds

[Back to top](#table-of-contents)

---

## 15. Testing, Linting & Quality Gates

```bash
# bats test: test/test_sample.bats
@test "sum works" {
  run bash -c 'echo $((2+3))'
  [ "$status" -eq 0 ]
  [ "$output" -eq 5 ]
}

# pre-commit hooks (shellcheck/shfmt)
# .pre-commit-config.yaml (excerpt)
# - repo: https://github.com/shellcheck-py/shellcheck-py
#   hooks: [{id: shellcheck}]
```

**Checklist**

- [ ] bats tests in CI
- [ ] shellcheck/shfmt mandatory
- [ ] Golden-file fixtures for CLI tools

[Back to top](#table-of-contents)

---

## 16. CI/CD Integration (GitHub, GitLab, Jenkins)

```bash
# GitHub Actions (excerpt)
# .github/workflows/ci.yaml
# jobs:
#   test:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v4
#       - run: sudo apt-get update && sudo apt-get install -y shellcheck bats
#       - run: shellcheck -x **/*.sh
#       - run: bats -r test

# Jenkins pipeline step
# sh 'bats -r test && shellcheck **/*.sh'
```

**Checklist**

- [ ] Artifacts & SBOM
- [ ] OIDC to cloud; no long-lived secrets
- [ ] Release gating on tests

[Back to top](#table-of-contents)

---

## 17. Cloud & Containers (AWS, Azure, GCP, OCI, Docker, K8s)

```bash
# AWS example: copy to S3 with KMS
aws s3 cp report.csv "s3://bucket/reports/" --sse aws:kms --sse-kms-key-id "$KMS_KEY"

# Docker build/push
docker build -t registry/mytool:$(date +%Y%m%d) .
docker push registry/mytool:$(date +%Y%m%d)

# K8s rollout
kubectl set image deploy/app app=registry/app:${TAG}
kubectl rollout status deploy/app --timeout=120s
```

**Checklist**

- [ ] Auth via profiles/SPs; no hardcoded keys
- [ ] Least privileges per operation
- [ ] Rollback plan (image pinning)

[Back to top](#table-of-contents)

---

## 18. Database Automations: Oracle, PostgreSQL, MySQL, SQL Server, MongoDB, Redis

```bash
# Oracle health (requires sqlplus)
sqlplus -s "sys/$SYS_PASS@//$HOST:1521/$SID as sysdba" <<'SQL'
SET HEADING OFF FEEDBACK OFF PAGES 0
SELECT name, open_mode FROM v$database;
EXIT
SQL

# PostgreSQL basic check
PGPASSWORD="$PG_PASS" psql "host=$PGHOST dbname=$PGDB user=$PGUSER sslmode=require" -c "SELECT NOW();"

# MySQL dump
mysqldump -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASS" --single-transaction "$MYSQL_DB" | gzip > backup.sql.gz

# SQL Server query
/opt/mssql-tools18/bin/sqlcmd -S "$MSSQL_HOST" -U "$MSSQL_USER" -P "$MSSQL_PASS" -Q "SELECT @@VERSION" -C

# MongoDB
mongo --quiet --eval 'db.runCommand({ping:1})'

# Redis
redis-cli -h "$REDIS_HOST" ping
```

**Checklist**

- [ ] Credential rotation hooks
- [ ] Safe timeouts & retries
- [ ] Read-only probes separate from mutating tasks

[Back to top](#table-of-contents)

---

## 19. Backup, Restore, HA/DR & Disaster Recovery Playbooks

```bash
# PostgreSQL PITR prep
pg_basebackup -D /backups/base -X stream -C -S slot_main
# Verify backup
pg_verifybackup /backups/base

# Offsite sync (rclone)
rclone copy /backups remote:db-backups --max-age 30d --backup-dir remote:db-backups/archive/$(date +%F)

# RMAN (Oracle) example skeleton
# rman target / <<'RMAN'
# BACKUP DATABASE PLUS ARCHIVELOG TAG 'nightly';
# LIST BACKUP SUMMARY;
# RMAN
```

**Checklist**

- [ ] Verified restores (not just backups)
- [ ] Retention & immutability (object lock)
- [ ] DR drill automation & reports

[Back to top](#table-of-contents)

---

## 20. DataOps Pipelines: Ingestion, CDC, Transform, Validate

```bash
# Batch ingest: SFTP → staging
lftp -e "mirror --use-pget-n=8 /remote/incoming /data/staging; bye" -u "$SFTP_USER","$SFTP_PASS" sftp://server

# Validate
find /data/staging -name '*.csv' -print0 | xargs -0 -n1 -P4 ./validate_csv.sh

# Load (psql)
for f in /data/staging/*.csv; do
  psql "$PG_DSN" -c "\COPY raw.table FROM '$f' CSV HEADER"
done
```

**Checklist**

- [ ] Schema drift detection
- [ ] Row-count reconciliation & data quality checks
- [ ] Idempotent re-runs

[Back to top](#table-of-contents)

---

## 21. Observability, Health Checks & SLOs

```bash
# Synthetic read
psql "$PG_DSN" -tA -c "SELECT 1" >/dev/null || exit 2

# Latency sampling
start=$(date +%s%3N); curl -sS https://svc/healthz >/dev/null; end=$(date +%s%3N)
echo "latency_ms $((end-start))" >> "$metrics"
```

**Checklist**

- [ ] SLOs defined; SLI collection implemented
- [ ] Alert thresholds w/ noise controls
- [ ] Runbook links in alerts

[Back to top](#table-of-contents)

---

## 22. Compliance, Auditing & Governance

```bash
# Command provenance
exec > >(tee -a /var/log/myjob/cmd.log) 2>&1
echo "ACTOR=${ACTOR:-unknown} TRACE_ID=$TRACE_ID $(date -Is)"

# Evidence bundle
bundle="/tmp/evidence-$(date +%s).tar.gz"
tar czf "$bundle" /var/log/myjob metrics/ configs/ manifests/
```

**Checklist**

- [ ] Change approvals recorded
- [ ] Evidence packages archived
- [ ] Access logs retained to policy

[Back to top](#table-of-contents)

---

## 23. Templates, Scaffolds & Boilerplates

```bash
# new.sh — scaffold a new script
cat > "$1" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'; umask 027
trap 'echo "ERR at $BASH_SOURCE:$LINENO" >&2' ERR
main(){ echo "Hello $*"; }
main "$@"
EOF
chmod +x "$1"
```

**Checklist**

- [ ] SPDX header
- [ ] trap/cleanup, logging, usage
- [ ] Unit tests created with scaffold

[Back to top](#table-of-contents)

---

## 24. Reusable Libraries & Helper Utilities

```bash
# lib/common.sh
log(){ printf '%s %-5s %s\n' "$(date -Is)" "$1" "$2" >&2; }
die(){ log ERROR "$*"; exit 1; }
require(){ command -v "$1" >/dev/null || die "Missing $1"; }
lock_acquire(){ exec 9>"$1"; flock -n 9; }
json_get(){ jq -r "$1"; }
notify_slack(){ curl -sS -X POST -H 'Content-type: application/json' --data "{\"text\":\"$*\"}" "$SLACK_WEBHOOK"; }
```

**Checklist**

- [ ] Library documented & versioned
- [ ] Minimal side effects
- [ ] Covered by tests

[Back to top](#table-of-contents)

---

## 25. Sample Projects & Use Cases

- **Ops:** Kernel param drift detection → opens a ticket via API.  
- **DBA:** Auto index maintenance nightly with safety limits.  
- **DBRE:** Rolling restarts w/ health checks & canary.  
- **DataOps:** SFTP ingest → validate → load → reconcile → publish.  
- **CloudOps:** Multi-account S3 backup sync with KMS & lifecycle.  
- **SecOps:** Key rotation + secret scanning pipeline.

**Example – rolling restart snippet:**

```bash
for pod in $(kubectl get po -l app=myapp -o name); do
  kubectl delete "$pod"
  kubectl rollout status deploy/myapp --timeout=120s || exit 1
done
```

[Back to top](#table-of-contents)

---

## 26. Migration, Cutover & Rollback Tooling

```bash
preflight(){
  need psql; psql "$PG_DSN" -c "SELECT 1" >/dev/null
  dns_ttl_ok=$(dig +short -t SOA example.com | awk '{print $6}')
  (( dns_ttl_ok <= 300 )) || die "High DNS TTL"
}
cutover(){
  # drain traffic, switch DNS, warm caches
  ./drain.sh && ./switch_dns.sh && ./warmup.sh
}
rollback(){ ./switch_dns_back.sh && ./restore_snapshot.sh; }
```

**Checklist**

- [ ] Preflight verifies dependencies & readiness
- [ ] Cutover scripted end-to-end
- [ ] Rollback tested and fast

[Back to top](#table-of-contents)

---

## 27. Incident Response, War Rooms & Postmortems

```bash
triage(){
  ts=$(date -Is); mkdir -p "/tmp/triage-$ts"
  top -b -n1 > "/tmp/triage-$ts/top.txt"
  df -h > "/tmp/triage-$ts/df.txt"
  ss -tunap > "/tmp/triage-$ts/net.txt"
  journalctl -xe --since "5 min ago" > "/tmp/triage-$ts/journal.txt"
}
```

**Checklist**

- [ ] One-liner triage & evidence capture
- [ ] War room scripts (comms, status, ETA)
- [ ] Postmortem template generated

[Back to top](#table-of-contents)

---

## 28. Security Hardening & Key Management

```bash
# PATH hardening
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
case ":$PATH:" in *::*|*::*) echo "Path has empties" >&2; exit 1;; esac

# Disable globbing when processing user input
set -f; read -r user_input; set +f

# Verify downloads
curl -fsSL "$URL" -o file && echo "$SHA256  file" | sha256sum -c -
```

**Checklist**

- [ ] Path hardening & no writable in PATH
- [ ] Signed artifacts & checksum verification
- [ ] Short-lived credentials

[Back to top](#table-of-contents)

---

## 29. Roadmap, Extensions & Wish List

- POSIX-only mode for BusyBox distros
- OTel span/trace exporters for long jobs
- Multi-cloud secret backends adapters
- Rich TUI front-ends (fzf/gum) for operators

[Back to top](#table-of-contents)

---

## 30. Appendix: Cheat Sheets & References

**Bash options**: `-e` exit on error, `-u` undefined vars, `-o pipefail` pipeline fail.  
**Arrays**: `arr=(a b); echo "${arr[1]}"`.  
**mapfile**: `mapfile -t lines < file`.  
**find+xargs**: `find . -type f -print0 | xargs -0 -I{} sh -c 'echo {}'`.  
**curl flags**: `--retry`, `--max-time`, `--connect-timeout`, `-f` fail-fast.

[Back to top](#table-of-contents)
