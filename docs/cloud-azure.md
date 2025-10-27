<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Azure Database Reliability Engineering Guide
*Practical patterns for Microsoft Azure—HA/DR, Terraform + OIDC, observability, and SLOs.*

## 📚 Table of Contents

- [1. Executive Summary](#1-executive-summary)
  - [1.1 Purpose & Audience](#11-purpose--audience)
  - [1.2 What “DBRE on Azure” Means](#12-what-dbre-on-azure-means)
  - [1.3 Portfolio Highlights & Outcomes](#13-portfolio-highlights--outcomes)
  - [1.4 How to Navigate this Document](#14-how-to-navigate-this-document)
- [2. Architecture Overview](#2-architecture-overview)
  - [2.1 Reference Architectures (Single-Region, AZ-Zone Redundant, Multi-Region)](#21-reference-architectures-single-region-az-zone-redundant-multi-region)
  - [2.2 Data Plane vs. Control Plane (Azure Services Map)](#22-data-plane-vs-control-plane-azure-services-map)
  - [2.3 Workload Taxonomy (OLTP, Analytics, Streaming, Caching)](#23-workload-taxonomy-oltp-analytics-streaming-caching)
  - [2.4 Reliability, Security, Cost as First-Class Concerns](#24-reliability-security-cost-as-first-class-concerns)
- [3. Azure Foundations](#3-azure-foundations)
  - [3.1 Management Groups, Subscriptions, Azure Policy (Guardrails)](#31-management-groups-subscriptions-azure-policy-guardrails)
  - [3.2 Networking (VNet, Subnets, Peering, Private Link, ExpressRoute/VPN, IPv6)](#32-networking-vnet-subnets-peering-private-link-expressroutevpn-ipv6)
  - [3.3 Identity & Access (Microsoft Entra ID, PIM, Break-Glass)](#33-identity--access-microsoft-entra-id-pim-break-glass)
  - [3.4 Encryption & Key Management (Key Vault, Managed HSM, CMK Rotation)](#34-encryption--key-management-key-vault-managed-hsm-cmk-rotation)
  - [3.5 Secrets & App Configuration (Key Vault, App Config)](#35-secrets--app-configuration-key-vault-app-config)
- [4. Data Platform Services on Azure](#4-data-platform-services-on-azure)
  - [4.1 Azure SQL Database & SQL Managed Instance](#41-azure-sql-database--sql-managed-instance)
  - [4.2 Azure Database for PostgreSQL (Flexible Server)](#42-azure-database-for-postgresql-flexible-server)
  - [4.3 Azure Database for MySQL (Flexible Server)](#43-azure-database-for-mysql-flexible-server)
  - [4.4 Azure Cosmos DB (NoSQL, Cassandra, Gremlin)](#44-azure-cosmos-db-nosql-cassandra-gremlin)
  - [4.5 Azure Cache for Redis](#45-azure-cache-for-redis)
  - [4.6 Azure Synapse Analytics / Microsoft Fabric](#46-azure-synapse-analytics--microsoft-fabric)
  - [4.7 Azure Cognitive Search / Elastic on Azure](#47-azure-cognitive-search--elastic-on-azure)
  - [4.8 Self-Managed on VMs/AKS (incl. Oracle on Azure)](#48-self-managed-on-vmsaks-incl-oracle-on-azure)
- [5. Reliability Engineering (SLIs/SLOs & Operations)](#5-reliability-engineering-slisslos--operations)
  - [5.1 SLIs & SLOs per Service (Latency, Availability, Durability)](#51-slis--slos-per-service-latency-availability-durability)
  - [5.2 Error Budgets & Release Policies](#52-error-budgets--release-policies)
  - [5.3 Incident Management (On-Call, Tiers, Escalations)](#53-incident-management-on-call-tiers-escalations)
  - [5.4 Postmortems & Continuous Improvement](#54-postmortems--continuous-improvement)
- [6. Observability](#6-observability)
  - [6.1 Metrics, Logs, Traces (Azure Monitor, App Insights, OTEL)](#61-metrics-logs-traces-azure-monitor-app-insights-otel)
  - [6.2 Workbooks & Alerts (Azure Monitor, Managed Grafana)](#62-workbooks--alerts-azure-monitor-managed-grafana)
  - [6.3 Query Performance Telemetry (Query Store/pg_stat_statements)](#63-query-performance-telemetry-query-storepgstatstatements)
  - [6.4 Availability Tests & Synthetic Probes](#64-availability-tests--synthetic-probes)
  - [6.5 Log Shipping & Search (Log Analytics/Kusto, ADX)](#65-log-shipping--search-log-analyticskusto-adx)
- [7. Automation Frameworks (Python-First)](#7-automation-frameworks-python-first)
  - [7.1 Azure SDK for Python (azure-identity, management SDKs)](#71-azure-sdk-for-python-azure-identity-management-sdks)
  - [7.2 Idempotent Operations & Safe Rollbacks](#72-idempotent-operations--safe-rollbacks)
  - [7.3 Event-Driven Ops (Event Grid, Functions, Durable Functions)](#73-event-driven-ops-event-grid-functions-durable-functions)
  - [7.4 Azure Automation (Runbooks, Update Manager)](#74-azure-automation-runbooks-update-manager)
  - [7.5 Reusable Libraries (Provisioning, Backups, Failover, Compliance)](#75-reusable-libraries-provisioning-backups-failover-compliance)
- [8. Python Integration for Automation (Foundations)](#8-python-integration-for-automation-foundations)
  - [8.1 Packaging & Environments (pip/poetry, venv, Docker)](#81-packaging--environments-pippoetry-venv-docker)
  - [8.2 Configuration Management (env vars, Pydantic, Key Vault)](#82-configuration-management-env-vars-pydantic-key-vault)
  - [8.3 Retries, Backoff, Idempotency Keys](#83-retries-backoff-idempotency-keys)
  - [8.4 Structured Logging & Correlation IDs](#84-structured-logging--correlation-ids)
  - [8.5 Testing Strategy (unit/integration), CI Hooks](#85-testing-strategy-unitintegration-ci-hooks)
  - [8.6 Distribution (Functions, containers, wheels)](#86-distribution-functions-containers-wheels)
- [9. API Integrations in Python (Azure & Third-Party)](#9-api-integrations-in-python-azure--third-party)
  - [9.1 REST (requests/httpx), Auth (Entra OAuth2/Client Credentials)](#91-rest-requestshttpx-auth-entra-oauth2client-credentials)
  - [9.2 GraphQL (client patterns, pagination)](#92-graphql-client-patterns-pagination)
  - [9.3 Webhooks & Event Grid/Service Hooks](#93-webhooks--event-gridservice-hooks)
  - [9.4 Rate Limiting, Circuit Breakers, Retries](#94-rate-limiting-circuit-breakers-retries)
  - [9.5 Schema Validation (pydantic), Error Handling](#95-schema-validation-pydantic-error-handling)
  - [9.6 Examples: ServiceNow/Jira/Slack, GitHub/GitLab, Azure Service Health](#96-examples-servicenowjiraslack-githubgitlab-azure-service-health)
- [10. Python Database Connectivity for Automation](#10-python-database-connectivity-for-automation)
  - [10.1 Common Patterns (pools, secrets, transactions, retries)](#101-common-patterns-pools-secrets-transactions-retries)
  - [10.2 PostgreSQL (psycopg 3: async, COPY, examples)](#102-postgresql-psycopg-3-async-copy-examples)
  - [10.3 MySQL (mysql-connector-python/PyMySQL)](#103-mysql-mysql-connector-pythonpymysql)
  - [10.4 Oracle (oracledb/cx_Oracle, TCPS, wallets)](#104-oracle-oracledbcxoracle-tcps-wallets)
  - [10.5 SQL Server (pyodbc, Azure SQL)](#105-sql-server-pyodbc-azure-sql)
  - [10.6 Cross-DB Abstraction (SQLAlchemy)](#106-cross-db-abstraction-sqlalchemy)
  - [10.7 Safety (dry-run, schema diffs, migration gating)](#107-safety-dry-run-schema-diffs-migration-gating)
  - [10.8 Throughput & Batching Patterns](#108-throughput--batching-patterns)
- [11. Infrastructure as Code & GitOps](#11-infrastructure-as-code--gitops)
  - [11.1 Terraform (azurerm), Bicep/ARM](#111-terraform-azurerm-biceparm)
  - [11.2 Azure DevOps Pipelines & GitHub Actions](#112-azure-devops-pipelines--github-actions)
  - [11.3 Policy as Code (Azure Policy, OPA/Conftest)](#113-policy-as-code-azure-policy-opaconftest)
  - [11.4 CI/CD (Actions/Azure Pipelines/CodePipeline-equivalents)](#114-cicd-actionsazure-pipelinescodepipeline-equivalents)
  - [11.5 Drift Detection & Remediation](#115-drift-detection--remediation)
- [12. Database Provisioning & Lifecycle](#12-database-provisioning--lifecycle)
  - [12.1 Golden Patterns (Server Parameters, Maintenance Windows)](#121-golden-patterns-server-parameters-maintenance-windows)
  - [12.2 Secure Bootstrapping (Networking, Key Vault, Private Link)](#122-secure-bootstrapping-networking-key-vault-private-link)
  - [12.3 User/Role Model & Least Privilege](#123-userrole-model--least-privilege)
  - [12.4 Upgrades, Patching, Blue/Green/Slot Strategies](#124-upgrades-patching-bluegreenslot-strategies)
  - [12.5 Decommissioning & Data Wipe Procedures](#125-decommissioning--data-wipe-procedures)
- [13. Performance Engineering](#13-performance-engineering)
  - [13.1 Workload Characterization & Benchmarks](#131-workload-characterization--benchmarks)
  - [13.2 Engine Tuning (Connections, Memory, IOPS/Storage)](#132-engine-tuning-connections-memory-iopsstorage)
  - [13.3 Connection Pooling (eg., Azure SQL/pgbouncer)](#133-connection-pooling-eg-azure-sqlpgbouncer)
  - [13.4 Read Scaling (Read Replicas, Geo-Replicas)](#134-read-scaling-read-replicas-geo-replicas)
  - [13.5 Caching Strategies (Azure Cache, App Patterns)](#135-caching-strategies-azure-cache-app-patterns)
  - [13.6 Query Tuning Playbook (Postgres/MySQL/SQL Server/Oracle)](#136-query-tuning-playbook-postgresmysqlsql-serveroracle)
- [14. High Availability & Disaster Recovery](#14-high-availability--disaster-recovery)
  - [14.1 Zone Redundancy vs. Multi-Region Trade-offs](#141-zone-redundancy-vs-multi-region-trade-offs)
  - [14.2 RPO/RTO Objectives & Testing Cadence](#142-rporto-objectives--testing-cadence)
  - [14.3 Azure SQL Geo-Replication & Auto-Failover Groups](#143-azure-sql-geo-replication--auto-failover-groups)
  - [14.4 PostgreSQL/MySQL Replication & HA](#144-postgresqlmysql-replication--ha)
  - [14.5 Backup Strategy (LTR, Snapshots, PITR)](#145-backup-strategy-ltr-snapshots-pitr)
  - [14.6 DR Runbooks & Automated Failover](#146-dr-runbooks--automated-failover)
- [15. Migrations & Modernization](#15-migrations--modernization)
  - [15.1 Discovery & Assessment (DMA, DMS, Workload Traces)](#151-discovery--assessment-dma-dms-workload-traces)
  - [15.2 Online Migrations (DMS, CDC, Dual-Write Caution)](#152-online-migrations-dms-cdc-dual-write-caution)
  - [15.3 Replatform vs. Refactor (MI, Serverless, PaaS)](#153-replatform-vs-refactor-mi-serverless-paas)
  - [15.4 Data Validation & Cutover Plans](#154-data-validation--cutover-plans)
  - [15.5 Post-Migration Hardening & Observability](#155-post-migration-hardening--observability)
- [16. Security & Compliance](#16-security--compliance)
  - [16.1 Shared Responsibility Model (DBRE Lens)](#161-shared-responsibility-model-dbre-lens)
  - [16.2 Network Segmentation, Private Access, Egress Controls](#162-network-segmentation-private-access-egress-controls)
  - [16.3 Encryption In-Transit/At-Rest (TLS, Key Vault, TDE)](#163-encryption-in-transitat-rest-tls-key-vault-tde)
  - [16.4 Vulnerability Management & Patch Strategy](#164-vulnerability-management--patch-strategy)
  - [16.5 Auditability (Activity Logs, Diagnostic Settings)](#165-auditability-activity-logs-diagnostic-settings)
  - [16.6 Compliance Tooling (Defender for Cloud, Purview, Sentinel)](#166-compliance-tooling-defender-for-cloud-purview-sentinel)
- [17. Cost Optimization](#17-cost-optimization)
  - [17.1 Cost Allocation (Tags, Subscriptions, EA/PayG)](#171-cost-allocation-tags-subscriptions-eapayg)
  - [17.2 Rightsizing (SKU, vCore/DTU, Storage Classes)](#172-rightsizing-sku-vcoredtu-storage-classes)
  - [17.3 Reservations & Savings Plans](#173-reservations--savings-plans)
  - [17.4 Lifecycle Policies for Backups/Logs (Cool/Archive)](#174-lifecycle-policies-for-backupslogs-coolarchive)
  - [17.5 Performance vs. Cost Trade-off Patterns](#175-performance-vs-cost-trade-off-patterns)
- [18. Continuous Delivery for Database Changes](#18-continuous-delivery-for-database-changes)
  - [18.1 Declarative Change Management (Liquibase/Flyway)](#181-declarative-change-management-liquibaseflyway)
  - [18.2 Schema Migration Pipelines (CI/CD with Approvals)](#182-schema-migration-pipelines-cicd-with-approvals)
  - [18.3 Automated Tests (Unit, Integration, Migration Smoke)](#183-automated-tests-unit-integration-migration-smoke)
  - [18.4 Feature Flags & Backward-Compatible Releases](#184-feature-flags--backward-compatible-releases)
  - [18.5 Rollback & Hotfix Strategies](#185-rollback--hotfix-strategies)
- [19. GameDays, Chaos & Validation](#19-gamedays-chaos--validation)
  - [19.1 Azure Chaos Studio & Failure Modes](#191-azure-chaos-studio--failure-modes)
  - [19.2 DR Drills & SLO Verification](#192-dr-drills--slo-verification)
  - [19.3 Load & Soak Testing (Load Testing service, Locust)](#193-load--soak-testing-load-testing-service-locust)
  - [19.4 Runbook Rehearsals & Time-to-Mitigate Metrics](#194-runbook-rehearsals--time-to-mitigate-metrics)
- [20. Case Studies & Patterns](#20-case-studies--patterns)
  - [20.1 Zero-Downtime Migration to MI/PostgreSQL](#201-zero-downtime-migration-to-mipostgresql)
  - [20.2 Cross-Region Read Replica Strategy for Analytics](#202-cross-region-read-replica-strategy-for-analytics)
  - [20.3 Cosmos DB Hot-Partition Remediation](#203-cosmos-db-hot-partition-remediation)
  - [20.4 Redis Latency Spike Investigation](#204-redis-latency-spike-investigation)
  - [20.5 Cost Downshift without SLO Regression](#205-cost-downshift-without-slo-regression)
- [21. Operational Runbooks & Playbooks](#21-operational-runbooks--playbooks)
  - [21.1 Backup/Restore (SQL/PG/MySQL/Redis/Cosmos patterns)](#211-backuprestore-sqlpgmysqlrediscosmos-patterns)
  - [21.2 Failover/Failback (Auto-Failover Groups, DNS, App Changes)](#212-failoverfailback-auto-failover-groups-dns-app-changes)
  - [21.3 Performance Firefighting (DB-Specific)](#213-performance-firefighting-db-specific)
  - [21.4 Security Incidents (Key Compromise, Secret Rotation)](#214-security-incidents-key-compromise-secret-rotation)
  - [21.5 Capacity Emergencies (Burst, Storage Auto-Scale)](#215-capacity-emergencies-burst-storage-auto-scale)
- [22. Checklists](#22-checklists)
  - [22.1 Production Readiness](#221-production-readiness)
  - [22.2 Launch/Go-Live](#222-launchgo-live)
  - [22.3 Compliance & Audit Prep](#223-compliance--audit-prep)
  - [22.4 Cost Review (Monthly/Quarterly)](#224-cost-review-monthlyquarterly)
  - [22.5 DR Readiness (Quarterly)](#225-dr-readiness-quarterly)
- [23. Appendix A — Python (Azure SDK) Automation Library](#23-appendix-a--python-azure-sdk-automation-library)
  - [23.1 SQL/PG/MySQL Provisioning & Parameterization](#231-sqlpgmysql-provisioning--parameterization)
  - [23.2 Automated Snapshots & PITR Restore (where applicable)](#232-automated-snapshots--pitr-restore-where-applicable)
  - [23.3 Cross-Subscription, Cross-Region Backup Copy](#233-cross-subscription-cross-region-backup-copy)
  - [23.4 Replica/Geo-Replica Management](#234-replicageo-replica-management)
  - [23.5 Cosmos DB/Redis Operations](#235-cosmos-dbredis-operations)
  - [23.6 Monitor Query Examples (Metrics/Logs)](#236-monitor-query-examples-metricslogs)
- [24. Appendix B — IaC Modules (Terraform/Bicep)](#24-appendix-b--iac-modules-terraformbicep)
  - [24.1 Module Layout & Standards](#241-module-layout--standards)
  - [24.2 Example: Azure SQL MI Production Module](#242-example-azure-sql-mi-production-module)
  - [24.3 Example: Azure PostgreSQL Flexible Server Module](#243-example-azure-postgresql-flexible-server-module)
  - [24.4 Example: Observability Baseline (Alerts, Workbooks)](#244-example-observability-baseline-alerts-workbooks)
- [25. Appendix C — IAM & Security Artifacts](#25-appendix-c--iam--security-artifacts)
  - [25.1 Least-Privilege Roles for DBRE Automation](#251-least-privilege-roles-for-dbre-automation)
  - [25.2 Break-Glass with PIM & Session Controls](#252-break-glass-with-pim--session-controls)
  - [25.3 Policy Examples for Database Guardrails](#253-policy-examples-for-database-guardrails)
- [26. Appendix D — CI/CD Pipelines](#26-appendix-d--cicd-pipelines)
  - [26.1 GitHub Actions Templates (Terraform/Liquibase)](#261-github-actions-templates-terraformliquibase)
  - [26.2 Azure Pipelines Variants](#262-azure-pipelines-variants)
  - [26.3 Policy Checkers & Security Scanners (Checkov, tfsec)](#263-policy-checkers--security-scanners-checkov-tfsec)
- [27. Appendix E — Templates & Records](#27-appendix-e--templates--records)
  - [27.1 Postmortem Template](#271-postmortem-template)
  - [27.2 DR Plan Template](#272-dr-plan-template)
  - [27.3 Architecture Decision Record (ADR)](#273-architecture-decision-record-adr)
  - [27.4 Risk Register & SLO Catalog](#274-risk-register--slo-catalog)
- [28. Glossary & References](#28-glossary--references)
  - [28.1 Terms & Acronyms](#281-terms--acronyms)
  - [28.2 Further Reading (Azure Docs, Whitepapers, Blogs)](#282-further-reading-azure-docs-whitepapers-blogs)

---

## 1. Executive Summary

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 1.1 Purpose & Audience

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 1.2 What “DBRE on Azure” Means

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 1.3 Portfolio Highlights & Outcomes

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 1.4 How to Navigate this Document

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 2. Architecture Overview

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 2.1 Reference Architectures (Single-Region, AZ-Zone Redundant, Multi-Region)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 2.2 Data Plane vs. Control Plane (Azure Services Map)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 2.3 Workload Taxonomy (OLTP, Analytics, Streaming, Caching)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 2.4 Reliability, Security, Cost as First-Class Concerns

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 3. Azure Foundations

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 3.1 Management Groups, Subscriptions, Azure Policy (Guardrails)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 3.2 Networking (VNet, Subnets, Peering, Private Link, ExpressRoute/VPN, IPv6)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 3.3 Identity & Access (Microsoft Entra ID, PIM, Break-Glass)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 3.4 Encryption & Key Management (Key Vault, Managed HSM, CMK Rotation)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 3.5 Secrets & App Configuration (Key Vault, App Config)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


---

## 4. Data Platform Services on Azure

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 4.1 Azure SQL Database & SQL Managed Instance

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.2 Azure Database for PostgreSQL (Flexible Server)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.3 Azure Database for MySQL (Flexible Server)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.4 Azure Cosmos DB (NoSQL, Cassandra, Gremlin)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.5 Azure Cache for Redis

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.6 Azure Synapse Analytics / Microsoft Fabric

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.7 Azure Cognitive Search / Elastic on Azure

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 4.8 Self-Managed on VMs/AKS (incl. Oracle on Azure)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 5. Reliability Engineering (SLIs/SLOs & Operations)

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 5.1 SLIs & SLOs per Service (Latency, Availability, Durability)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 5.2 Error Budgets & Release Policies

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 5.3 Incident Management (On-Call, Tiers, Escalations)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 5.4 Postmortems & Continuous Improvement

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 6. Observability

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 6.1 Metrics, Logs, Traces (Azure Monitor, App Insights, OTEL)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.2 Workbooks & Alerts (Azure Monitor, Managed Grafana)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.3 Query Performance Telemetry (Query Store/pg_stat_statements)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.4 Availability Tests & Synthetic Probes

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 6.5 Log Shipping & Search (Log Analytics/Kusto, ADX)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 7. Automation Frameworks (Python-First)

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 7.1 Azure SDK for Python (azure-identity, management SDKs)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 7.2 Idempotent Operations & Safe Rollbacks

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 7.3 Event-Driven Ops (Event Grid, Functions, Durable Functions)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 7.4 Azure Automation (Runbooks, Update Manager)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 7.5 Reusable Libraries (Provisioning, Backups, Failover, Compliance)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


---

## 8. Python Integration for Automation (Foundations)

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 8.1 Packaging & Environments (pip/poetry, venv, Docker)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 8.2 Configuration Management (env vars, Pydantic, Key Vault)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 8.3 Retries, Backoff, Idempotency Keys

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 8.4 Structured Logging & Correlation IDs

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 8.5 Testing Strategy (unit/integration), CI Hooks

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 8.6 Distribution (Functions, containers, wheels)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 9. API Integrations in Python (Azure & Third-Party)

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 9.1 REST (requests/httpx), Auth (Entra OAuth2/Client Credentials)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 9.2 GraphQL (client patterns, pagination)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 9.3 Webhooks & Event Grid/Service Hooks

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 9.4 Rate Limiting, Circuit Breakers, Retries

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 9.5 Schema Validation (pydantic), Error Handling

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 9.6 Examples: ServiceNow/Jira/Slack, GitHub/GitLab, Azure Service Health

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 10. Python Database Connectivity for Automation

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 10.1 Common Patterns (pools, secrets, transactions, retries)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 10.2 PostgreSQL (psycopg 3: async, COPY, examples)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 10.3 MySQL (mysql-connector-python/PyMySQL)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 10.4 Oracle (oracledb/cx_Oracle, TCPS, wallets)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 10.5 SQL Server (pyodbc, Azure SQL)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 10.6 Cross-DB Abstraction (SQLAlchemy)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 10.7 Safety (dry-run, schema diffs, migration gating)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 10.8 Throughput & Batching Patterns

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 11. Infrastructure as Code & GitOps

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 11.1 Terraform (azurerm), Bicep/ARM

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 11.2 Azure DevOps Pipelines & GitHub Actions

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 11.3 Policy as Code (Azure Policy, OPA/Conftest)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 11.4 CI/CD (Actions/Azure Pipelines/CodePipeline-equivalents)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 11.5 Drift Detection & Remediation

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 12. Database Provisioning & Lifecycle

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 12.1 Golden Patterns (Server Parameters, Maintenance Windows)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 12.2 Secure Bootstrapping (Networking, Key Vault, Private Link)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 12.3 User/Role Model & Least Privilege

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 12.4 Upgrades, Patching, Blue/Green/Slot Strategies

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 12.5 Decommissioning & Data Wipe Procedures

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 13. Performance Engineering

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 13.1 Workload Characterization & Benchmarks

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: EXPLAIN PLAN for a weekly report (pair with AWR/ASH in Azure VM/Oracle@Azure)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: EXPLAIN ANALYZE with buffers for a 7-day query (tie to Query Performance Insight)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# Azure MySQL: EXPLAIN JSON for latency analysis (connect with Azure Monitor)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: estimated plan (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 13.2 Engine Tuning (Connections, Memory, IOPS/Storage)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: EXPLAIN PLAN for a weekly report (pair with AWR/ASH in Azure VM/Oracle@Azure)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: EXPLAIN ANALYZE with buffers for a 7-day query (tie to Query Performance Insight)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# Azure MySQL: EXPLAIN JSON for latency analysis (connect with Azure Monitor)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: estimated plan (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 13.3 Connection Pooling (eg., Azure SQL/pgbouncer)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: sessions and limits on Azure VM/Oracle@Azure
import oracledb, os
conn = oracledb.connect(user="mon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT status, COUNT(*) FROM V$SESSION GROUP BY status"); print(cur.fetchall())
cur.execute("SELECT name, value FROM V$PARAMETER WHERE name IN ('sessions','processes')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: connection count vs max_connections
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM pg_stat_activity"); used = cur.fetchone()[0]
    cur.execute("SHOW max_connections"); maxc = cur.fetchone()[0]
    print({"used": used, "max": maxc})
```

*MySQL*

```python
# Azure MySQL: threads connected vs max_connections
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW STATUS LIKE 'Threads_connected'"); used = cur.fetchone()[1]
cur.execute("SHOW VARIABLES LIKE 'max_connections'"); maxc = cur.fetchone()[1]
print({"used": used, "max": maxc})
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: user sessions and workers
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1"); print(("user_sessions", cur.fetchone()[0]))
cur.execute("SELECT * FROM sys.configurations WHERE name IN ('max worker threads')"); print(cur.fetchall())
cur.close(); cnx.close()
```


### 13.4 Read Scaling (Read Replicas, Geo-Replicas)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 13.5 Caching Strategies (Azure Cache, App Patterns)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 13.6 Query Tuning Playbook (Postgres/MySQL/SQL Server/Oracle)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: EXPLAIN PLAN for a weekly report (pair with AWR/ASH in Azure VM/Oracle@Azure)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: EXPLAIN ANALYZE with buffers for a 7-day query (tie to Query Performance Insight)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# Azure MySQL: EXPLAIN JSON for latency analysis (connect with Azure Monitor)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: estimated plan (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


---

## 14. High Availability & Disaster Recovery

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 14.1 Zone Redundancy vs. Multi-Region Trade-offs

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 14.2 RPO/RTO Objectives & Testing Cadence

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 14.3 Azure SQL Geo-Replication & Auto-Failover Groups

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 14.4 PostgreSQL/MySQL Replication & HA

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 14.5 Backup Strategy (LTR, Snapshots, PITR)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle RMAN on Azure VM: recent backup jobs (for managed PaaS, use platform policies)
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclevm.privatelink.azure/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: archiver stats (PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: binlog status to confirm PITR prerequisites
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS"); print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI / SQL on VM: latest native backups from msdb
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""");
print(cur.fetchall())
cur.close(); cnx.close()
```


### 14.6 DR Runbooks & Automated Failover

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


---

## 15. Migrations & Modernization

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 15.1 Discovery & Assessment (DMA, DMS, Workload Traces)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 15.2 Online Migrations (DMS, CDC, Dual-Write Caution)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 15.3 Replatform vs. Refactor (MI, Serverless, PaaS)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 15.4 Data Validation & Cutover Plans

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 15.5 Post-Migration Hardening & Observability

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 16. Security & Compliance

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 16.1 Shared Responsibility Model (DBRE Lens)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 16.2 Network Segmentation, Private Access, Egress Controls

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 16.3 Encryption In-Transit/At-Rest (TLS, Key Vault, TDE)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 16.4 Vulnerability Management & Patch Strategy

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 16.5 Auditability (Activity Logs, Diagnostic Settings)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 16.6 Compliance Tooling (Defender for Cloud, Purview, Sentinel)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 17. Cost Optimization

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 17.1 Cost Allocation (Tags, Subscriptions, EA/PayG)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (feed into Azure Cost Management tagging model)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: database sizes
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 17.2 Rightsizing (SKU, vCore/DTU, Storage Classes)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (feed into Azure Cost Management tagging model)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: database sizes
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 17.3 Reservations & Savings Plans

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (feed into Azure Cost Management tagging model)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: database sizes
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 17.4 Lifecycle Policies for Backups/Logs (Cool/Archive)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 17.5 Performance vs. Cost Trade-off Patterns

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: EXPLAIN PLAN for a weekly report (pair with AWR/ASH in Azure VM/Oracle@Azure)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: EXPLAIN ANALYZE with buffers for a 7-day query (tie to Query Performance Insight)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# Azure MySQL: EXPLAIN JSON for latency analysis (connect with Azure Monitor)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: estimated plan (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


---

## 18. Continuous Delivery for Database Changes

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 18.1 Declarative Change Management (Liquibase/Flyway)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 18.2 Schema Migration Pipelines (CI/CD with Approvals)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 18.3 Automated Tests (Unit, Integration, Migration Smoke)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 18.4 Feature Flags & Backward-Compatible Releases

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 18.5 Rollback & Hotfix Strategies

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 19. GameDays, Chaos & Validation

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 19.1 Azure Chaos Studio & Failure Modes

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 19.2 DR Drills & SLO Verification

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 19.3 Load & Soak Testing (Load Testing service, Locust)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 19.4 Runbook Rehearsals & Time-to-Mitigate Metrics

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 20. Case Studies & Patterns

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 20.1 Zero-Downtime Migration to MI/PostgreSQL

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: cutover parity (rowcount) after Azure DMS migration
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclemi.privatelink.azure/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7"); print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: Flyway history validation
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: Liquibase changelog validation
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: parity check during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())"); print(cur.fetchone())
cur.close(); cnx.close()
```


### 20.2 Cross-Region Read Replica Strategy for Analytics

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 20.3 Cosmos DB Hot-Partition Remediation

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 20.4 Redis Latency Spike Investigation

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 20.5 Cost Downshift without SLO Regression

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (feed into Azure Cost Management tagging model)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: database sizes
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 21. Operational Runbooks & Playbooks

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 21.1 Backup/Restore (SQL/PG/MySQL/Redis/Cosmos patterns)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle RMAN on Azure VM: recent backup jobs (for managed PaaS, use platform policies)
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclevm.privatelink.azure/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: archiver stats (PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: binlog status to confirm PITR prerequisites
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS"); print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI / SQL on VM: latest native backups from msdb
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""");
print(cur.fetchall())
cur.close(); cnx.close()
```


### 21.2 Failover/Failback (Auto-Failover Groups, DNS, App Changes)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 21.3 Performance Firefighting (DB-Specific)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: EXPLAIN PLAN for a weekly report (pair with AWR/ASH in Azure VM/Oracle@Azure)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: EXPLAIN ANALYZE with buffers for a 7-day query (tie to Query Performance Insight)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# Azure MySQL: EXPLAIN JSON for latency analysis (connect with Azure Monitor)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: estimated plan (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 21.4 Security Incidents (Key Compromise, Secret Rotation)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 21.5 Capacity Emergencies (Burst, Storage Auto-Scale)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: sessions and limits on Azure VM/Oracle@Azure
import oracledb, os
conn = oracledb.connect(user="mon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT status, COUNT(*) FROM V$SESSION GROUP BY status"); print(cur.fetchall())
cur.execute("SELECT name, value FROM V$PARAMETER WHERE name IN ('sessions','processes')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: connection count vs max_connections
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM pg_stat_activity"); used = cur.fetchone()[0]
    cur.execute("SHOW max_connections"); maxc = cur.fetchone()[0]
    print({"used": used, "max": maxc})
```

*MySQL*

```python
# Azure MySQL: threads connected vs max_connections
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW STATUS LIKE 'Threads_connected'"); used = cur.fetchone()[1]
cur.execute("SHOW VARIABLES LIKE 'max_connections'"); maxc = cur.fetchone()[1]
print({"used": used, "max": maxc})
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: user sessions and workers
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1"); print(("user_sessions", cur.fetchone()[0]))
cur.execute("SELECT * FROM sys.configurations WHERE name IN ('max worker threads')"); print(cur.fetchall())
cur.close(); cnx.close()
```


---

## 22. Checklists

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 22.1 Production Readiness

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 22.2 Launch/Go-Live

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 22.3 Compliance & Audit Prep

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 22.4 Cost Review (Monthly/Quarterly)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (feed into Azure Cost Management tagging model)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: database sizes
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 22.5 DR Readiness (Quarterly)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 23. Appendix A — Python (Azure SDK) Automation Library

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 23.1 SQL/PG/MySQL Provisioning & Parameterization

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure (Oracle Database@Azure or VM): verify TDE wallet and TCPS session
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit: negotiated cipher for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: TDE wallet/tablespace state
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL - Flexible Server: verify SSL on session
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption is Azure-managed/KMS-backed and not queryable via SQL.
```

*MySQL*

```python
# Azure Database for MySQL - Flexible Server: verify TLS session
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'"); print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'"); print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL Managed Instance / SQL on Azure VM: check TLS and TDE
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 23.2 Automated Snapshots & PITR Restore (where applicable)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle RMAN on Azure VM: recent backup jobs (for managed PaaS, use platform policies)
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclevm.privatelink.azure/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: archiver stats (PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: binlog status to confirm PITR prerequisites
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS"); print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI / SQL on VM: latest native backups from msdb
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""");
print(cur.fetchall())
cur.close(); cnx.close()
```


### 23.3 Cross-Subscription, Cross-Region Backup Copy

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle RMAN on Azure VM: recent backup jobs (for managed PaaS, use platform policies)
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oraclevm.privatelink.azure/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: archiver stats (PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL: binlog status to confirm PITR prerequisites
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS"); print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI / SQL on VM: latest native backups from msdb
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""");
print(cur.fetchall())
cur.close(); cnx.close()
```


### 23.4 Replica/Geo-Replica Management

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard on Azure VM/Oracle@Azure: role and lag
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE"); print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')"); print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL Flexible Server: replication status (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""");
    print(cur.fetchall())
```

*MySQL*

```python
# Azure MySQL Flexible Server: replication worker status
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW REPLICA STATUS"); print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: AG health (auto-failover groups on Azure SQL DB use different views)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 23.5 Cosmos DB/Redis Operations

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 23.6 Monitor Query Examples (Metrics/Logs)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle on Azure: top wait events for Azure Monitor/Log Analytics dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure Database for PostgreSQL: activity + pg_stat_statements (if enabled) for Workbooks
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# Azure Database for MySQL: top statements (performance_schema) for Azure Monitor
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""");
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: top CPU queries for Azure Monitor workbook
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10
  total_worker_time/1000 AS total_cpu_ms,
  execution_count,
  total_elapsed_time/1000 AS total_elapsed_ms,
  SUBSTRING(qt.text,(qs.statement_start_offset/2)+1,
            ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY total_worker_time DESC
""");
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 24. Appendix B — IaC Modules (Terraform/Bicep)

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 24.1 Module Layout & Standards

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 24.2 Example: Azure SQL MI Production Module

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 24.3 Example: Azure PostgreSQL Flexible Server Module

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 24.4 Example: Observability Baseline (Alerts, Workbooks)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 25. Appendix C — IAM & Security Artifacts

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 25.1 Least-Privilege Roles for DBRE Automation

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 25.2 Break-Glass with PIM & Session Controls

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 25.3 Policy Examples for Database Guardrails

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 26. Appendix D — CI/CD Pipelines

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 26.1 GitHub Actions Templates (Terraform/Liquibase)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 26.2 Azure Pipelines Variants

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 26.3 Policy Checkers & Security Scanners (Checkov, tfsec)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: account posture review (pair with Entra ID/Key Vault for access flows)
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="oracle.db.azurecloud/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# Azure PostgreSQL: roles and replication privs (align with Azure AD auth if enabled)
import psycopg2, os
conn = psycopg2.connect("host=pg-flex.postgres.database.azure.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# Azure MySQL: user grants (coordinate with Azure AD auth where applicable)
import mysql.connector as mysql, os
cnx = mysql.connect(host="mysql-flex.mysql.database.azure.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'"); print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# Azure SQL MI: principals posture (pair with Entra ID, PIM, conditional access)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=mi.privatelink.database.windows.net;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 27. Appendix E — Templates & Records

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 27.1 Postmortem Template

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 27.2 DR Plan Template

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 27.3 Architecture Decision Record (ADR)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 27.4 Risk Register & SLO Catalog

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

---

## 28. Glossary & References

This section presents Azure-aligned DBRE practices with an emphasis on SLO-driven decision-making,
safe rollouts, and measurable outcomes. Designs favor clear ownership boundaries, deterministic
failure modes, and built-in observation points so that rollback paths are immediate and auditable.

Compared to other clouds, Azure offers first-class constructs for identity (Entra ID), policy
(Azure Policy), networking (Private Link), and observability (Azure Monitor, Log Analytics). We
leverage those to make changes reversible and low-risk, codifying guardrails into automation and
peer-reviewed runbooks.

### 28.1 Terms & Acronyms

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

> _No code sample for this subtopic (conceptual/policy focus)._

### 28.2 Further Reading (Azure Docs, Whitepapers, Blogs)

The focus here is to reduce operational uncertainty: isolate blast radius, standardize patterns
across environments, and ensure every operation leaves a verifiable trace. We connect the
conceptual intent to queryable evidence—only where evidence belongs in the database layer.

When code is omitted, it's deliberate: the subtopic is policy/process oriented and should be
validated via Azure control-plane signals (Policy, Activity Logs, Diagnostics) rather than SQL.
Where code appears, each example targets the subtopic's intent.

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
