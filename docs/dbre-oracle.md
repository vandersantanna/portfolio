# Oracle DBRE Portfolio — Complete README

A professional, single-file **Oracle Database Reliability Engineering (DBRE)** portfolio you can paste directly into GitHub as `README.md`. It demonstrates strategy, architecture, operations, and deep technical execution with examples (SQL/PLSQL, Bash, Ansible, Terraform, GitHub Actions, DGMGRL/RMAN, etc.). All code blocks use `~~~` fences to avoid breaking this single-file export.

---

## Table of Contents
- [1. Executive Summary](#1-executive-summary)
- [2. Role Scope & Value Proposition](#2-role-scope--value-proposition)
- [3. Skills Matrix](#3-skills-matrix)
  - [3.1 Core DBRE Competencies](#31-core-dbre-competencies)
  - [3.2 Oracle Database Stack](#32-oracle-database-stack)
  - [3.3 Platform & Tooling](#33-platform--tooling)
- [4. Reference Architecture & Environments](#4-reference-architecture--environments)
  - [4.1 Topologies](#41-topologies)
  - [4.2 Cloud & Hybrid](#42-cloud--hybrid)
  - [4.3 Data Flows](#43-data-flows)
- [5. Reliability Engineering Fundamentals](#5-reliability-engineering-fundamentals)
  - [5.1 SLOs, SLIs, SLAs](#51-slos-slis-slas)
  - [5.2 Error Budgets & Risk](#52-error-budgets--risk)
  - [5.3 Incident Lifecycle & Postmortems](#53-incident-lifecycle--postmortems)
- [6. Observability & Monitoring](#6-observability--monitoring)
  - [6.1 Metrics & Dashboards](#61-metrics--dashboards)
  - [6.2 Tracing & Profiling](#62-tracing--profiling)
  - [6.3 Logging & Alerting](#63-logging--alerting)
- [7. Capacity Planning & Performance Engineering](#7-capacity-planning--performance-engineering)
  - [7.1 Baselines & Benchmarking](#71-baselines--benchmarking)
  - [7.2 SQL & Schema Tuning](#72-sql--schema-tuning)
  - [7.3 Resource & Storage Optimization](#73-resource--storage-optimization)
- [8. High Availability & Disaster Recovery](#8-high-availability--disaster-recovery)
  - [8.1 Data Guard & Active Data Guard](#81-data-guard--active-data-guard)
  - [8.2 Real Application Clusters (RAC)](#82-real-application-clusters-rac)
  - [8.3 Backup, Recovery & DR Testing](#83-backup-recovery--dr-testing)
- [9. Security, Compliance & Governance](#9-security-compliance--governance)
  - [9.1 Identity & Access](#91-identity--access)
  - [9.2 Encryption, Keys & Secrets](#92-encryption-keys--secrets)
  - [9.3 Auditing, Masking & Data Privacy](#93-auditing-masking--data-privacy)
- [10. Change Management & Release Engineering](#10-change-management--release-engineering)
  - [10.1 GitOps & IaC](#101-gitops--iac)
  - [10.2 CI/CD for Databases](#102-cicd-for-databases)
  - [10.3 Safe Deployment Patterns](#103-safe-deployment-patterns)
- [11. Automation & Runbooks](#11-automation--runbooks)
  - [11.1 Provisioning & Patching](#111-provisioning--patching)
  - [11.2 Health Checks & Self-Healing](#112-health-checks--self-healing)
  - [11.3 Operational Playbooks](#113-operational-playbooks)
- [12. Data Integration & Replication](#12-data-integration--replication)
  - [12.1 Oracle GoldenGate & CDC](#121-oracle-goldengate--cdc)
  - [12.2 Streaming Pipelines](#122-streaming-pipelines)
  - [12.3 Cross-DB & Heterogeneous Replication](#123-cross-db--heterogeneous-replication)
- [13. Cost & Efficiency Engineering](#13-cost--efficiency-engineering)
  - [13.1 Licensing & Editions](#131-licensing--editions)
  - [13.2 Right-Sizing & Scaling](#132-right-sizing--scaling)
  - [13.3 Storage & Networking Economics](#133-storage--networking-economics)
- [14. Reliability Case Studies](#14-reliability-case-studies)
- [15. KPIs, Dashboards & Reporting](#15-kpis-dashboards--reporting)
- [16. Standards & Conventions](#16-standards--conventions)
- [17. Roadmap & Continuous Improvement](#17-roadmap--continuous-improvement)
- [18. Appendices & Templates](#18-appendices--templates)
  - [A. Scripts & Snippets](#a-scripts--snippets)
  - [B. Terraform & Ansible (OCI/Azure)](#b-terraform--ansible-ociazure)
  - [C. CI/CD Pipelines (GitHub Actions/Azure DevOps)](#c-cicd-pipelines-github-actionsazure-devops)
  - [D. Runbook Templates](#d-runbook-templates)
  - [E. Checklists](#e-checklists)
  - [F. Diagrams (Mermaid)](#f-diagrams-mermaid)
  - [G. Acronyms & Glossary](#g-acronyms--glossary)

---

## 1. Executive Summary
I design and operate highly available, secure, and cost-efficient Oracle data platforms. My DBRE approach translates business objectives into measurable **SLOs**, enforced by automation, observability, tested **HA/DR**, and safe change delivery. Outcomes: fewer incidents, faster recovery, predictable performance, and auditable compliance across on-prem, OCI, and hybrid estates.

## 2. Role Scope & Value Proposition
- **Scope:** Oracle DB reliability across greenfield/brownfield; OLTP/Analytical; single-instance, RAC, Exadata, ADG; on-prem, OCI, Azure Interconnect.
- **Interfaces:** App teams, SRE/Platform, SecOps, Data Engineering, Architecture, and Leadership.
- **Value:** Align SLOs to user experience; codify architecture as **IaC**; automate operations; implement **observability-first** culture; continuously reduce toil and risk.

## 3. Skills Matrix

### 3.1 Core DBRE Competencies
- SLI/SLO/SLA design, error budgets, risk registers, change failure rate reduction
- Incident response, postmortems, chaos/DR drills, operational excellence
- Observability at depth (metrics/logs/traces), performance modeling, capacity planning
- Automation-first: GitOps, pipelines, Ansible/Terraform, policy-as-code

### 3.2 Oracle Database Stack
- **Versions & Features:** 19c/21c, Multitenant (CDB/PDB), RAC, ASM/ACFS, Exadata
- **HA/DR:** Data Guard / Active Data Guard, Far Sync, Snapshot Standby
- **Performance:** AWR/ASH/ADDM, SQL Plan Baselines, Partitioning, Compression
- **Ops:** RMAN, ZDLRA, OEM/EM13c, Fleet Maintenance, Data Pump, SQLcl

### 3.3 Platform & Tooling
- **OS:** RHEL 8/9 tuning (HugePages, NUMA, I/O schedulers), systemd, cgroups
- **IaC/Automation:** Terraform (OCI/Azure), Ansible, Packer, Bash, Python
- **Pipelines:** GitHub Actions, Azure DevOps; DB migrations with Flyway/Liquibase
- **Observability:** Prometheus exporters, Grafana, Alertmanager, Loki/ELK
- **Security/Secrets:** Vault, OCI Vault, Azure Key Vault; TLS/TDE/PKI
- **Containers/Orchestration:** Podman/Docker; K8s StatefulSets (operator-aware)

---

## 4. Reference Architecture & Environments

### 4.1 Topologies
- **Single-Instance**: resilient infra + ADG for DR, suitable for many OLTP workloads
- **RAC**: scale-out with service-based failover and rolling patching
- **Exadata**: smart scan/offload, storage cell balancing, consolidated multitenant

### 4.2 Cloud & Hybrid
- **OCI**: OCPU sizing, Block Volumes (multi-attach for RAC), FSS for ACFS, Bastion
- **Azure Interconnect**: low-latency private peering to OCI, identity boundary care
- **Hybrid**: routing/DNS, private link, end-to-end TLS, unified audit domains

### 4.3 Data Flows
OLTP ingestion → CDC (GoldenGate) → Stream → Lake/Warehouse; read offload on ADG; governed retention & archival.

---

## 5. Reliability Engineering Fundamentals

### 5.1 SLOs, SLIs, SLAs
- **SLIs** (examples): p99 read latency < 40 ms; commit latency < 120 ms; error rate < 0.1%; ADG lag < 5 s
- **SLOs**: 99.95% monthly availability for checkout service DB; 99.9% for reporting DB
- **Practice**: rolling windows (28/30d), burn-rate policies, SLO review cadence

~~~yaml
# Example SLO (YAML for docs/policy-as-code)
service: orders-db
slos:
  - name: p99_read_latency
    target: "p99 < 40ms"
    window: 30d
  - name: adg_lag_seconds
    target: "<= 5s"
    window: 30d
burn_policies:
  - if_burn_rate: "> 2.0x"
    action: "freeze nonessential changes; raise reliability epic"
~~~

### 5.2 Error Budgets & Risk
- Track budget consumption; restrict risky changes during burn
- Risk register per system: probability × impact; mitigation backlog

### 5.3 Incident Lifecycle & Postmortems
- **Flow:** Detect → Triage → Mitigate → Recover → Review
- Blameless postmortems with action ownership & due dates; link to runbooks

---

## 6. Observability & Monitoring

### 6.1 Metrics & Dashboards
- **Layers:** OS, ASM, Instance, PDB, RAC, DG, App queries
- **Dashboards:** SLO compliance, capacity headroom, top waits, ADG lag

~~~sql
-- AWR/ASH Snapshot: Top Wait Events (last hour)
SELECT wait_class, event, ROUND( (time_waited / 100) ,2) AS seconds
FROM   v$system_event
WHERE  event NOT LIKE 'rdbms ipc message%'
AND    event NOT LIKE 'class slave wait%'
ORDER  BY time_waited DESC
FETCH FIRST 10 ROWS ONLY;
~~~

~~~ini
# Prometheus: oracledb_exporter scrape job (example)
scrape_configs:
  - job_name: 'oracle-db'
    static_configs:
      - targets: ['db-prim:9161','db-standby:9161']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
~~~

### 6.2 Tracing & Profiling
- Session tracing, ASH/SQL Monitor; capture bind-aware history; SPM baselines

~~~sql
-- Enable 10046 trace for a session (diagnostic example)
ALTER SESSION SET sql_trace=true;
ALTER SESSION SET events '10046 trace name context forever, level 12';
-- ... run workload ...
ALTER SESSION SET sql_trace=false;
~~~

### 6.3 Logging & Alerting
- Structured logs (Loki/ELK), correlation IDs, deduplicated alerts, runbook links

~~~yaml
# Alertmanager: ADG replication lag alert (example)
groups:
- name: oracle
  rules:
  - alert: ADGReplicationLagHigh
    expr: adg_apply_lag_seconds > 5
    for: 5m
    labels: { severity: page }
    annotations:
      summary: "ADG lag high on {{ $labels.instance }}"
      runbook: "runbooks/dr/adg-lag.md"
~~~

---

## 7. Capacity Planning & Performance Engineering

### 7.1 Baselines & Benchmarking
- Tools: Swingbench / SLOB / HammerDB; per-workload KPIs; seasonality detection
- Capacity models: CPU/IOPS/Memory/Redo/Temp; 30–90d projections with buffers

~~~bash
# Swingbench (charbench) baseline example
export ORACLE_SID=ORCL
charbench -cs //db-prim:1521/ORCLPDB1 -u soe -p soe -r -min 8 -max 64 -intermin 30 -intermax 180 \
  -rt 900 -v users,tpm,tps,errors -a results/baseline.csv
~~~

### 7.2 SQL & Schema Tuning
- Indexing strategy, histograms, partitioning (range/hash/list), compression
- SQL Plan Management for stability; avoid hinting unless proven necessary

~~~sql
-- Create SPM baseline for a high-value query
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => '8a1z3h9k2svwq', plan_hash_value => NULL, fixed => 'YES');
  DBMS_OUTPUT.PUT_LINE('Baselines loaded: '||l_plans);
END;
/
~~~

### 7.3 Resource & Storage Optimization
- ASM diskgroup layout (DATA/RECO/REDO), redo sizing, TEMP spill control
- XFS mount options, multipathing, NVMe; network latency budgets for RAC/DG

---

## 8. High Availability & Disaster Recovery

### 8.1 Data Guard & Active Data Guard
- Protection modes (MAX PROT/AVAIL/PERF), Far Sync for WAN resilience
- Read offloading on ADG; snapshot standby for patch tests

~~~bash
# DGMGRL: switchover example
dgmgrl sys@prim "show configuration"
dgmgrl sys@prim "switchover to 'STBY1'"
dgmgrl sys@stby1 "show configuration"
~~~

~~~sql
-- Monitor apply lag (seconds)
SELECT name, (EXTRACT(DAY FROM (SYSDATE-NEXT_TIME))*86400
             + EXTRACT(HOUR FROM (SYSDATE-NEXT_TIME))*3600
             + EXTRACT(MINUTE FROM (SYSDATE-NEXT_TIME))*60
             + EXTRACT(SECOND FROM (SYSDATE-NEXT_TIME))) AS apply_lag_s
FROM   v$archived_log
WHERE  applied = 'YES'
ORDER  BY NEXT_TIME DESC FETCH FIRST 1 ROW ONLY;
~~~

### 8.2 Real Application Clusters (RAC)
- Services with preferred/available instances; SCAN listeners; GNS/DNS HA
- Interconnect tuning (MTU/Jumbo frames, UDP/RDMA); GC wait minimization

~~~bash
# SRVCTL: define a service with preferred/available instances
srvctl add service -d ORCL -s OLTP_SVC -r "ORCL1,ORCL2" -a "ORCL3" -P BASIC -B SERVICE_TIME -e SELECT
srvctl start service -d ORCL -s OLTP_SVC
srvctl status service -d ORCL -s OLTP_SVC
~~~

### 8.3 Backup, Recovery & DR Testing
- RMAN incremental merge, block change tracking, ZDLRA integration
- Quarterly restore validations; PITR drills; documented RPO/RTO

~~~bash
# RMAN: Full + Archivelog with validation
rman target /
RUN {
  CONFIGURE CONTROLFILE AUTOBACKUP ON;
  BACKUP AS COMPRESSED BACKUPSET INCREMENTAL LEVEL 0 DATABASE PLUS ARCHIVELOG;
  VALIDATE DATABASE;
}
# Restore test (sandbox)
rman AUXILIARY /
DUPLICATE DATABASE TO TESTDB FROM ACTIVE DATABASE NOFILENAMECHECK;
~~~

---

## 9. Security, Compliance & Governance

### 9.1 Identity & Access
- Roles/profiles, least privilege; break-glass accounts with MFA; session timeouts

~~~sql
-- Least-privilege role for read-only analysts
CREATE ROLE ro_analytics;
GRANT CREATE SESSION TO ro_analytics;
GRANT SELECT ANY TABLE TO ro_analytics;
ALTER USER analyst PROFILE app_profile;
GRANT ro_analytics TO analyst;
~~~

### 9.2 Encryption, Keys & Secrets
- TDE (tablespace/column), TLS in transit, KMS/HSM (OCI Vault/Azure Key Vault)
- Rotation policies, key escrow, certificate renewal pipelines

~~~sql
-- TDE: create keystore and set master key (demonstration)
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/u01/app/wallet' IDENTIFIED BY "StrongPass!";
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "StrongPass!" WITH BACKUP;
ALTER SYSTEM SET ENCRYPTION WALLET OPEN IDENTIFIED BY "StrongPass!";
~~~

### 9.3 Auditing, Masking & Data Privacy
- Unified Auditing/FGA; retention to WORM storage; masking/subsetting for lower envs

~~~sql
-- Unified Auditing policy for privileged operations
CREATE AUDIT POLICY admin_actions
  ACTIONS ALL PRIVILEGES
  WHEN 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') <> ''SYS''' EVALUATE PER STATEMENT;
AUDIT POLICY admin_actions;
~~~

---

## 10. Change Management & Release Engineering

### 10.1 GitOps & IaC
- All infra as code (Terraform/Ansible); peer-review; drift detection; policy gates

### 10.2 CI/CD for Databases
- Versioned migrations (**Flyway/Liquibase**), pre-deploy checks, smoke tests
- Canary/blue-green schemas for risk reduction; automatic rollback on failure

~~~properties
# Flyway example (conf)
flyway.url=jdbc:oracle:thin:@//db-prim:1521/ORCLPDB1
flyway.user=app_migrator
flyway.password=${APP_MIGRATOR_PWD}
flyway.locations=filesystem:./db/migrations
flyway.baselineOnMigrate=true
flyway.outOfOrder=false
~~~

~~~sql
-- V1__create_orders_table.sql (example)
CREATE TABLE orders (
  id            NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  customer_id   NUMBER NOT NULL,
  status        VARCHAR2(30) NOT NULL,
  created_at    TIMESTAMP DEFAULT SYSTIMESTAMP
);
CREATE INDEX ix_orders_status ON orders(status);
~~~

### 10.3 Safe Deployment Patterns
- Shadow writes + compare, feature flags, progressive rollout, hold if SLO risk increases

---

## 11. Automation & Runbooks

### 11.1 Provisioning & Patching
- Golden images with Packer; Fleet Maintenance/OPatch orchestration; rolling patch for RAC/ADG

~~~yaml
# Ansible: ensure HugePages and kernel params
- hosts: db
  become: true
  tasks:
    - name: Configure sysctl for Oracle
      ansible.posix.sysctl:
        name: "{{ item.name }}"
        value: "{{ item.value }}"
        state: present
      loop:
        - { name: vm.nr_hugepages, value: 4096 }
        - { name: fs.aio-max-nr,   value: 1048576 }
        - { name: kernel.shmmax,   value: 68719476736 }
        - { name: kernel.sem,      value: "250 32000 100 128" }
~~~

### 11.2 Health Checks & Self-Healing
- Daily health scripts; restart stuck apply; auto expand TEMP/REDO with guardrails

~~~bash
# Bash: lightweight ADG lag watchdog
LAG=$(sqlplus -s / as sysdba <<'SQL'
SET HEADING OFF FEEDBACK OFF
SELECT NVL((SELECT apply_lag FROM v$dataguard_stats WHERE name='apply lag'), INTERVAL '0' SECOND) FROM dual;
SQL
)
echo "Lag: $LAG"
# if > 00:00:05 then page (example hook)
~~~

### 11.3 Operational Playbooks
- Start/Stop, Switchover/Failover, Backup Validate, Restore Dry-run, Capacity Expansion
- All steps numbered, pre-checks, success criteria, rollback instructions

---

## 12. Data Integration & Replication

### 12.1 Oracle GoldenGate & CDC
- Topologies: uni/bi-directional with conflict detection; heartbeat monitoring; DDL replication policies

~~~ini
-- Extract parameter (excerpt)
EXTRACT E_SALES
USERIDALIAS ogg_admin
EXTTRAIL ./dirdat/sa
TRANLOGOPTIONS ENABLE_INSTANTIATION_FILTERING
TABLE SALES.ORDERS;
~~~

### 12.2 Streaming Pipelines
- CDC → Kafka → consumers; idempotent writes; ordering keys; replay strategy

### 12.3 Cross-DB & Heterogeneous Replication
- Oracle ↔ PostgreSQL/MySQL/Snowflake; datatype mapping; end-to-end consistency checks

---

## 13. Cost & Efficiency Engineering

### 13.1 Licensing & Editions
- EE vs SE2; options (Partitioning, RAC, ADG, Compression); BYOL in cloud; license audits

### 13.2 Right-Sizing & Scaling
- OCPU/CPU, memory, IOPS targets; autoscale envelopes; consolidation vs isolation trade-offs

### 13.3 Storage & Networking Economics
- Tiering snapshots/archival, backup retention economics, egress budgets, interconnect utilization

---

## 14. Reliability Case Studies
**Case Study A — SLO Rollout for Checkout DB**
- **Problem:** inconsistent p99 latency; no SLOs; noisy alerts  
- **Action:** SLOs for read/commit; dashboards; burn policy; SQL baselines  
- **Result:** p99 read latency down 38%; change failure rate −45%; MTTR −30%

**Case Study B — ADG Lag Elimination Across Regions**
- **Problem:** 25–60s ADG lag causing stale reads  
- **Action:** redo bandwidth increase, Far Sync, log buffer/redo tuning, ASM IOPS uplift  
- **Result:** sustained lag < 3s; RPO confidence improved; read-only offload unlocked

**Case Study C — RAC Replatform with Zero Downtime**
- **Problem:** aging hardware; licensing pressure  
- **Action:** move to OCI, RAC 2-node, services-based failover, rolling patching  
- **Result:** 99.98% 6-month availability; 23% cost reduction; faster patch windows

---

## 15. KPIs, Dashboards & Reporting
- **Availability:** per service & aggregate; error budget burn  
- **Latency:** p50/p90/p99 for key transactions  
- **Change:** deployment frequency, lead time, change failure rate  
- **Ops:** MTTR/MTTD, toil hours, backup success, DR drill pass rate  
- **Capacity:** CPU/IOPS headroom, growth forecasts

~~~markdown
**Monthly Executive Summary (template)**
- Availability: 99.96% (SLO: 99.95%) ✅
- Error budget burn: 32% (policy: <50%)
- Incidents: Sev-1:0, Sev-2:2, Sev-3:5 (MTTR: 28m)
- Changes: 62 deploys, CFR: 3.2% (↘︎ 0.8 pp)
- DR: 1 drill passed, RTO 14m (target ≤ 20m)
- Risks: RAC interconnect saturation (Q4 remediation)
~~~

---

## 16. Standards & Conventions
- **Naming/Tagging:** `db-{env}-{service}-{role}`, PDBs `pdb_{team}_{purpose}`, services `svc_{tier}_{rw}`  
- **Docs:** ADR/runbook format, decision records (ADRs), code style (SQL/PLSQL/Bash/Python)  
- **Git:** trunk-based or GitFlow; semantic versioning; signed commits; CODEOWNERS

---

## 17. Roadmap & Continuous Improvement
- **Q1:** 100% SLO coverage for tier-1 DBs; DR drill pass rate ≥ 90%  
- **Q2:** Migrate backups to ZDLRA/immutable storage; automate restore tests weekly  
- **Q3:** RAC interconnect revamp; observability rev-2 (traces)  
- **Q4:** Cost optimization phase-2; operator-driven patching; deprecate legacy runbooks

---

## 18. Appendices & Templates

### A. Scripts & Snippets

~~~sql
-- AWR delta for top SQL by elapsed time (last snapshot)
SELECT * FROM (
  SELECT sql_id, plan_hash_value, elapsed_time_delta/1e6 AS sec, executions_delta,
         (elapsed_time_delta/DECODE(executions_delta,0,1,executions_delta))/1e6 AS sec_per_exec
  FROM   dba_hist_sqlstat
  WHERE  snap_id = (SELECT MAX(snap_id) FROM dba_hist_snapshot)
  ORDER BY elapsed_time_delta DESC
) WHERE ROWNUM <= 20;
~~~

~~~plsql
-- Health check: invalid objects report
SET SERVEROUTPUT ON
DECLARE
  v_cnt NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_cnt FROM dba_objects WHERE status='INVALID';
  DBMS_OUTPUT.PUT_LINE('Invalid objects: '||v_cnt);
END;
/
~~~

~~~bash
# Quick listener health + port check
lsnrctl status LISTENER | grep -E "STATUS|Port"
nc -zv db-prim 1521
~~~

~~~python
# Minimal Prometheus exporter (illustrative)
from prometheus_client import start_http_server, Gauge
import cx_Oracle, time
g = Gauge('adg_apply_lag_seconds','ADG apply lag')
def loop():
    while True:
        with cx_Oracle.connect("metrics/****@db-standby/ORCLPDB1") as con:
            cur = con.cursor()
            cur.execute("""SELECT EXTRACT(SECOND FROM apply_lag)+60*EXTRACT(MINUTE FROM apply_lag)
                           FROM v$dataguard_stats WHERE name='apply lag'""")
            lag = cur.fetchone()[0] or 0
            g.set(lag)
        time.sleep(15)
if __name__ == "__main__":
    start_http_server(9161)
    loop()
~~~

### B. Terraform & Ansible (OCI/Azure)

~~~hcl
# Terraform (OCI) - Simplified DB VM + Block Volumes (illustrative)
variable "compartment_ocid" {}
provider "oci" {}

resource "oci_core_instance" "db_prim" {
  availability_domain = "Uocm:SA-SAOPAULO-1-AD-1"
  compartment_id      = var.compartment_ocid
  shape               = "VM.Standard3.Flex"
  shape_config { ocpus = 8, memory_in_gbs = 64 }
  display_name        = "db-prim"
  create_vnic_details { subnet_id = oci_core_subnet.app_subnet.id }
  metadata = { ssh_authorized_keys = file("~/.ssh/id_rsa.pub") }
}
resource "oci_core_volume" "data" { size_in_gbs = 512  compartment_id = var.compartment_ocid }
resource "oci_core_volume_attachment" "data_attach" {
  instance_id = oci_core_instance.db_prim.id
  volume_id   = oci_core_volume.data.id
  attachment_type = "iscsi"
}
~~~

~~~yaml
# Ansible — Oracle install prerequisites (excerpt)
- hosts: db
  become: true
  vars:
    oracle_groups:
      - { name: oinstall, gid: 54321 }
      - { name: dba,      gid: 54322 }
  tasks:
    - group: { name: "{{ item.name }}", gid: "{{ item.gid }}", state: present }
      loop: "{{ oracle_groups }}"
    - user:
        name: oracle
        uid: 54321
        groups: "oinstall,dba"
        shell: /bin/bash
        create_home: yes
~~~

### C. CI/CD Pipelines (GitHub Actions/Azure DevOps)

~~~yaml
# GitHub Actions: Oracle DB migrations with Flyway + OIDC secretless auth to Vault (illustrative)
name: db-migrate
on:
  push: { paths: ["db/migrations/**"] }
jobs:
  migrate:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Auth to Vault (OIDC)
        run: |
          echo "Exchange JWT for short-lived DB creds"
      - name: Flyway Migrate
        run: |
          curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.0.0/flyway-commandline-10.0.0-linux-x64.tar.gz \
            | tar xz && sudo ln -s $PWD/flyway-10.0.0/flyway /usr/local/bin/flyway
          flyway -configFiles=db/flyway.conf migrate
~~~

~~~yaml
# Azure DevOps: Multistage DB pipeline (excerpt)
stages:
- stage: Validate
  jobs:
  - job: Lint
    steps:
    - script: echo "Validate SQL formatting, run unit checks"
- stage: Migrate
  dependsOn: Validate
  jobs:
  - deployment: Flyway
    environment: prod
    strategy:
      runOnce:
        deploy:
          steps:
          - script: flyway -configFiles=db/flyway.conf migrate
~~~

### D. Runbook Templates

~~~markdown
# Runbook: ADG Switchover

## Preconditions
- Both databases `READY` in DGMGRL; apply lag < 5s
- Backups healthy (last 24h)

## Steps
1. Freeze risky changes; notify stakeholders
2. `dgmgrl "show configuration"`
3. `dgmgrl "switchover to 'STBY1'"`
4. Validate: services running, read/write health, SLO probes
5. Update DNS/connection strings if needed

## Rollback
- `dgmgrl "switchover to 'PRIM'"` if validation fails

## Post-actions
- Update runbook log; file postmortem items if any
~~~

### E. Checklists

~~~markdown
## Patch Day Checklist
- [ ] Backups complete and validated
- [ ] Change ticket approved; maintenance window confirmed
- [ ] Rolling patch plan for RAC/ADG
- [ ] Health baseline captured (AWR, dashboards)
- [ ] Post-patch validation (AWR delta, SLO probes)
~~~

### F. Diagrams (Mermaid)

~~~mermaid
flowchart LR
  subgraph Primary[Primary - OLTP]
    A[App] -->|JDBC| DB[(Oracle CDB/PDB)]
  end
  DB -->|Redo| DG>Data Guard Transport]
  subgraph Standby[Standby - ADG]
    DG --> STB[(Standby DB)]
    STB -->|Read-Only| Analytics[(Analytics/Reports)]
  end
  classDef strong fill:#eef,stroke:#66f,stroke-width:2px;
  class DB,STB strong;
~~~

### G. Acronyms & Glossary
- **DBRE** — Database Reliability Engineering  
- **SLA/SLO/SLI** — Agreement/Objectives/Indicators  
- **MTTR/MTTD** — Mean Time to Recover/Detect  
- **ADG** — Active Data Guard; **DG** — Data Guard  
- **RAC** — Real Application Clusters  
- **ASM/ACFS** — Automatic Storage Management / Cluster File System  
- **SPM** — SQL Plan Management  
- **ZDLRA** — Zero Data Loss Recovery Appliance

---

## How to Use & Customize
1. Replace examples with your environments (hostnames, OCIDs, tenancy details).  
2. Expand **Case Studies** with before/after KPIs and architecture diagrams.  
3. Link deeper docs from each section (e.g., `/runbooks`, `/pipelines`, `/terraform`).  
4. Keep SLOs living documents; revisit burn policies quarterly.  
5. Automate **restore tests** and **DR drills**; publish results in **KPIs**.

> **Note:** All code blocks are fenced with `~~~` on purpose so this entire README can be copied in one go from chat. Once pasted into GitHub, the `~~~` fences render normally with syntax highlighting.
