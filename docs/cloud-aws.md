<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# AWS Database Reliability Engineering (DBRE) 
*DBRE on AWS: automate, observe, and ship without downtime.*

## 📚 Table of Contents

- [1. Executive Summary](#1-executive-summary)  
  - [1.1 Purpose & Audience](#11-purpose--audience)  
  - [1.2 What “DBRE on AWS” Means](#12-what-dbre-on-aws-means)  
  - [1.3 Portfolio Highlights & Outcomes](#13-portfolio-highlights--outcomes)  
  - [1.4 How to Navigate this Document](#14-how-to-navigate-this-document)
- [2. Architecture Overview](#2-architecture-overview)  
  - [2.1 Reference Architectures (Single-Region, Multi-AZ, Multi-Region)](#21-reference-architectures-single-region-multi-az-multi-region)  
  - [2.2 Data Plane vs. Control Plane (AWS Services Map)](#22-data-plane-vs-control-plane-aws-services-map)  
  - [2.3 Workload Taxonomy (OLTP, Analytics, Streaming, Caching)](#23-workload-taxonomy-oltp-analytics-streaming-caching)  
  - [2.4 Reliability, Security, Cost as First-Class Concerns](#24-reliability-security-cost-as-first-class-concerns)
- [3. AWS Foundations](#3-aws-foundations)  
  - [3.1 Multi-Account Strategy (Organizations, SCPs, Guardrails)](#31-multi-account-strategy-organizations-scps-guardrails)  
  - [3.2 Networking (VPC, Subnets, TGW, PrivateLink, DX/VPN, IPv6)](#32-networking-vpc-subnets-tgw-privatelink-dxvpn-ipv6)  
  - [3.3 Identity & Access (IAM Roles, SSO, Break-Glass)](#33-identity--access-iam-roles-sso-break-glass)  
  - [3.4 Encryption & Key Management (KMS, MRKs, Key Rotation)](#34-encryption--key-management-kms-mrks-key-rotation)  
  - [3.5 Secrets & Parameters (Secrets Manager, Parameter Store)](#35-secrets--parameters-secrets-manager-parameter-store)
- [4. Data Platform Services on AWS](#4-data-platform-services-on-aws)  
  - [4.1 Amazon Aurora (MySQL/PostgreSQL)](#41-amazon-aurora-mysqlpostgresql)  
  - [4.2 Amazon RDS (PostgreSQL, MySQL, SQL Server, Oracle)](#42-amazon-rds-postgresql-mysql-sql-server-oracle)  
  - [4.3 Amazon DynamoDB (On-Demand, GSIs, DAX)](#43-amazon-dynamodb-on-demand-gsis-dax)  
  - [4.4 Amazon ElastiCache (Redis/Memcached)](#44-amazon-elasticache-redis-memcached)  
  - [4.5 Amazon OpenSearch Service](#45-amazon-opensearch-service)  
  - [4.6 Amazon Redshift & Lakehouse Adjacent (Glue, Athena, Lake Formation)](#46-amazon-redshift--lakehouse-adjacent-glue-athena-lake-formation)  
  - [4.7 Document & Graph (DocumentDB, Neptune)](#47-document--graph-documentdb-neptune)  
  - [4.8 Self-Managed on EC2/EKS (when & why)](#48-self-managed-on-ec2eks-when--why)
- [5. Reliability Engineering (SLIs/SLOs & Operations)](#5-reliability-engineering-slisslos--operations)  
  - [5.1 SLIs & SLOs per Service (Latency, Availability, Durability)](#51-slis--slos-per-service-latency-availability-durability)  
  - [5.2 Error Budgets & Release Policies](#52-error-budgets--release-policies)  
  - [5.3 Incident Management (On-Call, Tiers, Escalations)](#53-incident-management-on-call-tiers-escalations)  
  - [5.4 Postmortems & Continuous Improvement](#54-postmortems--continuous-improvement)
- [6. Observability](#6-observability)  
  - [6.1 Metrics, Logs, Traces (CloudWatch, X-Ray, OTEL)](#61-metrics-logs-traces-cloudwatch-x-ray-otel)  
  - [6.2 Dashboards & Alarms (CW Dashboards, AMG/Grafana)](#62-dashboards--alarms-cw-dashboards-amggrafana)  
  - [6.3 Query Performance Telemetry (Aurora/RDS Performance Insights)](#63-query-performance-telemetry-aurorards-performance-insights)  
  - [6.4 Synthetics & Probes (CloudWatch Synthetics)](#64-synthetics--probes-cloudwatch-synthetics)  
  - [6.5 Log Shipping & Search (OpenSearch, S3 + Athena)](#65-log-shipping--search-opensearch-s3--athena)
- [7. Automation Frameworks (Python-First)](#7-automation-frameworks-python-first)  
  - [7.1 Boto3 SDK Foundations (Auth, Pagination, Retries)](#71-boto3-sdk-foundations-auth-pagination-retries)  
  - [7.2 Idempotent Operations & Safe Rollbacks](#72-idempotent-operations--safe-rollbacks)  
  - [7.3 Event-Driven Ops (EventBridge, Step Functions, Lambda)](#73-event-driven-ops-eventbridge-step-functions-lambda)  
  - [7.4 SSM Automation (Run Command, Documents, State Manager)](#74-ssm-automation-run-command-documents-state-manager)  
  - [7.5 Reusable Libraries (Provisioning, Backups, Failover, Compliance)](#75-reusable-libraries-provisioning-backups-failover-compliance)
- [8. Python Integration for Automation (Foundations)](#8-python-integration-for-automation-foundations)  
  - [8.1 Packaging & Environments (pip/poetry, venv, Docker)](#81-packaging--environments-pippoetry-venv-docker)  
  - [8.2 Configuration Management (env vars, Pydantic, SSM/Secrets)](#82-configuration-management-env-vars-pydantic-ssmsecrets)  
  - [8.3 Retries, Backoff, Idempotency Keys](#83-retries-backoff-idempotency-keys)  
  - [8.4 Structured Logging & Correlation IDs](#84-structured-logging--correlation-ids)  
  - [8.5 Testing Strategy (unit/integration), CI Hooks](#85-testing-strategy-unitintegration-ci-hooks)  
  - [8.6 Distribution (Lambda layers, containers, wheels)](#86-distribution-lambda-layers-containers-wheels)
- [9. API Integrations in Python (AWS & Third-Party)](#9-api-integrations-in-python-aws--third-party)  
  - [9.1 REST (requests/httpx), Auth (SigV4, OAuth2)](#91-rest-requestshttpx-auth-sigv4-oauth2)  
  - [9.2 GraphQL (client patterns, pagination)](#92-graphql-client-patterns-pagination)  
  - [9.3 Webhooks & EventBridge Pipes](#93-webhooks--eventbridge-pipes)  
  - [9.4 Rate Limiting, Circuit Breakers, Retries](#94-rate-limiting-circuit-breakers-retries)  
  - [9.5 Schema Validation (pydantic), Error Handling](#95-schema-validation-pydantic-error-handling)  
  - [9.6 Examples: ServiceNow/Jira/Slack, GitHub/GitLab, AWS Health API](#96-examples-servicenowjiraslack-githubgitlab-aws-health-api)
- [10. Python Database Connectivity for Automation](#10-python-database-connectivity-for-automation)  
  - [10.1 Common Patterns (pools, secrets, transactions, retries)](#101-common-patterns-pools-secrets-transactions-retries)  
  - [10.2 PostgreSQL (psycopg 3: async, COPY, examples)](#102-postgresql-psycopg-3-async-copy-examples)  
  - [10.3 MySQL (mysql-connector-python/PyMySQL)](#103-mysql-mysql-connector-pythonpymysql)  
  - [10.4 Oracle (oracledb/cx_Oracle, TCPS, wallets)](#104-oracle-oracledbcx_oracle-tcps-wallets)  
  - [10.5 SQL Server (pyodbc, Linux ODBC drivers)](#105-sql-server-pyodbc-linux-odbc-drivers)  
  - [10.6 Cross-DB Abstraction (SQLAlchemy)](#106-cross-db-abstraction-sqlalchemy)  
  - [10.7 Safety (dry-run, schema diffs, migration gating)](#107-safety-dry-run-schema-diffs-migration-gating)  
  - [10.8 Throughput & Batching Patterns](#108-throughput--batching-patterns)
- [11. Infrastructure as Code & GitOps](#11-infrastructure-as-code--gitops)  
  - [11.1 Terraform (Modules, Workspaces, Remote State)](#111-terraform-modules-workspaces-remote-state)  
  - [11.2 AWS CDK & CloudFormation (Stacks, StackSets)](#112-aws-cdk--cloudformation-stacks-stacksets)  
  - [11.3 Policy as Code (SCPs, IAM, Config Rules)](#113-policy-as-code-scps-iam-config-rules)  
  - [11.4 CI/CD (GitHub Actions/GitLab CI/CodePipeline)](#114-cicd-github-actionsgitlab-ci-codepipeline)  
  - [11.5 Drift Detection & Remediation](#115-drift-detection--remediation)
- [12. Database Provisioning & Lifecycle](#12-database-provisioning--lifecycle)  
  - [12.1 Golden Patterns (Parameter Groups, Option Groups)](#121-golden-patterns-parameter-groups-option-groups)  
  - [12.2 Secure Bootstrapping (Networking, KMS, Secrets)](#122-secure-bootstrapping-networking-kms-secrets)  
  - [12.3 User/Role Model & Least Privilege](#123-userrole-model--least-privilege)  
  - [12.4 Upgrades, Patching, Blue/Green (RDS Blue/Green)](#124-upgrades-patching-bluegreen-rds-bluegreen)  
  - [12.5 Decommissioning & Data Wipe Procedures](#125-decommissioning--data-wipe-procedures)
- [13. Performance Engineering](#13-performance-engineering)  
  - [13.1 Workload Characterization & Benchmarks](#131-workload-characterization--benchmarks)  
  - [13.2 Aurora/RDS Tuning (Connections, Memory, IOPS, Storage Types)](#132-aurorards-tuning-connections-memory-iops-storage-types)  
  - [13.3 RDS Proxy & Connection Pooling](#133-rds-proxy--connection-pooling)  
  - [13.4 Read Scaling (Read Replicas, Global Database for Aurora)](#134-read-scaling-read-replicas-global-database-for-aurora)  
  - [13.5 Caching Strategies (ElastiCache, Application Patterns)](#135-caching-strategies-elasticache-application-patterns)  
  - [13.6 Query Tuning Playbook (Postgres/MySQL/SQL Server/Oracle)](#136-query-tuning-playbook-postgresmysqlsql-serveroracle)
- [14. High Availability & Disaster Recovery](#14-high-availability--disaster-recovery)  
  - [14.1 Multi-AZ vs. Multi-Region Trade-offs](#141-multi-az-vs-multi-region-trade-offs)  
  - [14.2 RPO/RTO Objectives & Testing Cadence](#142-rporpo-objectives--testing-cadence)  
  - [14.3 Aurora Global Database & Cross-Region Replication](#143-aurora-global-database--cross-region-replication)  
  - [14.4 DynamoDB Global Tables & DAX HA](#144-dynamodb-global-tables--dax-ha)  
  - [14.5 Backup Strategy (AWS Backup, Snapshots, PITR)](#145-backup-strategy-aws-backup-snapshots-pitr)  
  - [14.6 DR Runbooks & Automated Failover](#146-dr-runbooks--automated-failover)
- [15. Migrations & Modernization](#15-migrations--modernization)  
  - [15.1 Discovery & Assessment (SCT, Workload Traces)](#151-discovery--assessment-sct-workload-traces)  
  - [15.2 Online Migrations (DMS, CDC, Dual-Write Caution)](#152-online-migrations-dms-cdc-dual-write-caution)  
  - [15.3 Replatform vs. Refactor (Aurora, DynamoDB, Serverless)](#153-replatform-vs-refactor-aurora-dynamodb-serverless)  
  - [15.4 Data Validation & Cutover Plans](#154-data-validation--cutover-plans)  
  - [15.5 Post-Migration Hardening & Observability](#155-post-migration-hardening--observability)
- [16. Security & Compliance](#16-security--compliance)  
  - [16.1 Shared Responsibility Model (DBRE Lens)](#161-shared-responsibility-model-dbre-lens)  
  - [16.2 Network Segmentation, Private Access, Egress Controls](#162-network-segmentation-private-access-egress-controls)  
  - [16.3 Encryption In-Transit/At-Rest (TLS, KMS, TDE)](#163-encryption-in-transitat-rest-tls-kms-tde)  
  - [16.4 Vulnerability Management & Patch Strategy](#164-vulnerability-management--patch-strategy)  
  - [16.5 Auditability (CloudTrail, Config, Detective Controls)](#165-auditability-cloudtrail-config-detective-controls)  
  - [16.6 Compliance Tooling (Security Hub, GuardDuty, Macie, Artifact)](#166-compliance-tooling-security-hub-guardduty-macie-artifact)
- [17. Cost Optimization](#17-cost-optimization)  
  - [17.1 Cost Allocation (Tags, Accounts, CUR)](#171-cost-allocation-tags-accounts-cur)  
  - [17.2 Rightsizing (Instance Families, Graviton, Storage Classes)](#172-rightsizing-instance-families-graviton-storage-classes)  
  - [17.3 Savings Plans & RIs (Where It Fits Databases)](#173-savings-plans--ris-where-it-fits-databases)  
  - [17.4 S3 Lifecycle & Glacier for Backups/Logs](#174-s3-lifecycle--glacier-for-backupslogs)  
  - [17.5 Performance vs. Cost Trade-off Patterns](#175-performance-vs-cost-trade-off-patterns)
- [18. Continuous Delivery for Database Changes](#18-continuous-delivery-for-database-changes)  
  - [18.1 Declarative Change Management (Liquibase/Flyway)](#181-declarative-change-management-liquibaseflyway)  
  - [18.2 Schema Migration Pipelines (CI/CD with Approvals)](#182-schema-migration-pipelines-cicd-with-approvals)  
  - [18.3 Automated Tests (Unit, Integration, Migration Smoke)](#183-automated-tests-unit-integration-migration-smoke)  
  - [18.4 Feature Flags & Backward-Compatible Releases](#184-feature-flags--backward-compatible-releases)  
  - [18.5 Rollback & Hotfix Strategies](#185-rollback--hotfix-strategies)
- [19. GameDays, Chaos & Validation](#19-gamedays-chaos--validation)  
  - [19.1 Fault Injection (FIS) & Failure Modes](#191-fault-injection-fis--failure-modes)  
  - [19.2 DR Drills & SLO Verification](#192-dr-drills--slo-verification)  
  - [19.3 Load & Soak Testing (Distributed Load Testing, Locust)](#193-load--soak-testing-distributed-load-testing-locust)  
  - [19.4 Runbook Rehearsals & Time-to-Mitigate Metrics](#194-runbook-rehearsals--time-to-mitigate-metrics)
- [20. Case Studies & Patterns](#20-case-studies--patterns)  
  - [20.1 Zero-Downtime Migration to Aurora](#201-zero-downtime-migration-to-aurora)  
  - [20.2 Cross-Region Read Replica Strategy for Analytics](#202-cross-region-read-replica-strategy-for-analytics)  
  - [20.3 DynamoDB Hot-Partition Remediation](#203-dynamodb-hot-partition-remediation)  
  - [20.4 Redis Latency Spike Investigation](#204-redis-latency-spike-investigation)  
  - [20.5 Cost Downshift without SLO Regression](#205-cost-downshift-without-slo-regression)
- [21. Operational Runbooks & Playbooks](#21-operational-runbooks--playbooks)  
  - [21.1 Backup/Restore (RDS/Aurora/DynamoDB/ElastiCache)](#211-backuprestore-rdsauroradynamodbelasticache)  
  - [21.2 Failover/Failback (Aurora Global, Route 53, App Changes)](#212-failoverfailback-aurora-global-route-53-app-changes)  
  - [21.3 Performance Firefighting (DB-Specific)](#213-performance-firefighting-db-specific)  
  - [21.4 Security Incidents (Key Compromise, Secret Rotation)](#214-security-incidents-key-compromise-secret-rotation)  
  - [21.5 Capacity Emergencies (Burst Credit, Storage Auto-Scale)](#215-capacity-emergencies-burst-credit-storage-auto-scale)
- [22. Checklists](#22-checklists)  
  - [22.1 Production Readiness](#221-production-readiness)  
  - [22.2 Launch/Go-Live](#222-launchgo-live)  
  - [22.3 Compliance & Audit Prep](#223-compliance--audit-prep)  
  - [22.4 Cost Review (Monthly/Quarterly)](#224-cost-review-monthlyquarterly)  
  - [22.5 DR Readiness (Quarterly)](#225-dr-readiness-quarterly)
- [23. Appendix A — Python (boto3) Automation Library](#23-appendix-a--python-boto3-automation-library)  
  - [23.1 RDS/Aurora Provisioning & Parameterization](#231-rdsaurora-provisioning--parameterization)  
  - [23.2 Automated Snapshots & PITR Restore](#232-automated-snapshots--pitr-restore)  
  - [23.3 Cross-Account, Cross-Region Backup Copy](#233-cross-account-cross-region-backup-copy)  
  - [23.4 Read Replica & Global DB Management](#234-read-replica--global-db-management)  
  - [23.5 DynamoDB Table Ops & Global Tables](#235-dynamodb-table-ops--global-tables)  
  - [23.6 ElastiCache Cluster Operations](#236-elasticache-cluster-operations)
- [24. Appendix B — Terraform/CDK Modules](#24-appendix-b--terraformcdk-modules)  
  - [24.1 Module Layout & Standards](#241-module-layout--standards)  
  - [24.2 Example: Aurora PostgreSQL Production Module](#242-example-aurora-postgresql-production-module)  
  - [24.3 Example: DynamoDB Global Tables Module](#243-example-dynamodb-global-tables-module)  
  - [24.4 Example: Observability Baseline (CW, Alarms, Dashboards)](#244-example-observability-baseline-cw-alarms-dashboards)
- [25. Appendix C — IAM & Security Artifacts](#25-appendix-c--iam--security-artifacts)  
  - [25.1 Least-Privilege Policies for DBRE Automation](#251-least-privilege-policies-for-dbre-automation)  
  - [25.2 Break-Glass Role with Session Controls](#252-break-glass-role-with-session-controls)  
  - [25.3 SCP Examples for Database Guardrails](#253-scp-examples-for-database-guardrails)
- [26. Appendix D — CI/CD Pipelines](#26-appendix-d--cicd-pipelines)  
  - [26.1 GitHub Actions Templates (Terraform/Liquibase)](#261-github-actions-templates-terraformliquibase)  
  - [26.2 GitLab CI & AWS CodePipeline Variants](#262-gitlab-ci--aws-codepipeline-variants)  
  - [26.3 Policy Checkers & Security Scanners (OPA, tfsec, cfn-nag)](#263-policy-checkers--security-scanners-opa-tfsec-cfn-nag)
- [27. Appendix E — Templates & Records](#27-appendix-e--templates--records)  
  - [27.1 Postmortem Template](#271-postmortem-template)  
  - [27.2 DR Plan Template](#272-dr-plan-template)  
  - [27.3 Architecture Decision Record (ADR)](#273-architecture-decision-record-adr)  
  - [27.4 Risk Register & SLO Catalog](#274-risk-register--slo-catalog)
- [28. Glossary & References](#28-glossary--references)  
  - [28.1 Terms & Acronyms](#281-terms--acronyms)  
  - [28.2 Further Reading](#282-further-reading-aws-docs-whitepapers-blogs)

---

## 1. Executive Summary

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 1.1 Purpose & Audience

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 1.2 What “DBRE on AWS” Means

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 1.3 Portfolio Highlights & Outcomes

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 1.4 How to Navigate this Document

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 2. Architecture Overview

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 2.1 Reference Architectures (Single-Region, Multi-AZ, Multi-Region)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 2.2 Data Plane vs. Control Plane (AWS Services Map)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 2.3 Workload Taxonomy (OLTP, Analytics, Streaming, Caching)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 2.4 Reliability, Security, Cost as First-Class Concerns

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 3. AWS Foundations

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 3.1 Multi-Account Strategy (Organizations, SCPs, Guardrails)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 3.2 Networking (VPC, Subnets, TGW, PrivateLink, DX/VPN, IPv6)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 3.3 Identity & Access (IAM Roles, SSO, Break-Glass)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 3.4 Encryption & Key Management (KMS, MRKs, Key Rotation)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 3.5 Secrets & Parameters (Secrets Manager, Parameter Store)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 4. Data Platform Services on AWS

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 4.1 Amazon Aurora (MySQL/PostgreSQL)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.2 Amazon RDS (PostgreSQL, MySQL, SQL Server, Oracle)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.3 Amazon DynamoDB (On-Demand, GSIs, DAX)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.4 Amazon ElastiCache (Redis/Memcached)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.5 Amazon OpenSearch Service

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.6 Amazon Redshift & Lakehouse Adjacent (Glue, Athena, Lake Formation)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.7 Document & Graph (DocumentDB, Neptune)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 4.8 Self-Managed on EC2/EKS (when & why)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 5. Reliability Engineering (SLIs/SLOs & Operations)

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 5.1 SLIs & SLOs per Service (Latency, Availability, Durability)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 5.2 Error Budgets & Release Policies

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 5.3 Incident Management (On-Call, Tiers, Escalations)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 5.4 Postmortems & Continuous Improvement

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 6. Observability

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 6.1 Metrics, Logs, Traces (CloudWatch, X-Ray, OTEL)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 6.2 Dashboards & Alarms (CW Dashboards, AMG/Grafana)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 6.3 Query Performance Telemetry (Aurora/RDS Performance Insights)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 6.4 Synthetics & Probes (CloudWatch Synthetics)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 6.5 Log Shipping & Search (OpenSearch, S3 + Athena)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 7. Automation Frameworks (Python-First)

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 7.1 Boto3 SDK Foundations (Auth, Pagination, Retries)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 7.2 Idempotent Operations & Safe Rollbacks

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 7.3 Event-Driven Ops (EventBridge, Step Functions, Lambda)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 7.4 SSM Automation (Run Command, Documents, State Manager)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 7.5 Reusable Libraries (Provisioning, Backups, Failover, Compliance)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 8. Python Integration for Automation (Foundations)

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 8.1 Packaging & Environments (pip/poetry, venv, Docker)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 8.2 Configuration Management (env vars, Pydantic, SSM/Secrets)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 8.3 Retries, Backoff, Idempotency Keys

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 8.4 Structured Logging & Correlation IDs

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 8.5 Testing Strategy (unit/integration), CI Hooks

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 8.6 Distribution (Lambda layers, containers, wheels)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 9. API Integrations in Python (AWS & Third-Party)

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 9.1 REST (requests/httpx), Auth (SigV4, OAuth2)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 9.2 GraphQL (client patterns, pagination)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 9.3 Webhooks & EventBridge Pipes

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 9.4 Rate Limiting, Circuit Breakers, Retries

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 9.5 Schema Validation (pydantic), Error Handling

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 9.6 Examples: ServiceNow/Jira/Slack, GitHub/GitLab, AWS Health API

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 10. Python Database Connectivity for Automation

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 10.1 Common Patterns (pools, secrets, transactions, retries)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.2 PostgreSQL (psycopg 3: async, COPY, examples)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.3 MySQL (mysql-connector-python/PyMySQL)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.4 Oracle (oracledb/cx_Oracle, TCPS, wallets)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.5 SQL Server (pyodbc, Linux ODBC drivers)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.6 Cross-DB Abstraction (SQLAlchemy)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.7 Safety (dry-run, schema diffs, migration gating)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 10.8 Throughput & Batching Patterns

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 11. Infrastructure as Code & GitOps

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 11.1 Terraform (Modules, Workspaces, Remote State)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 11.2 AWS CDK & CloudFormation (Stacks, StackSets)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 11.3 Policy as Code (SCPs, IAM, Config Rules)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 11.4 CI/CD (GitHub Actions/GitLab CI/CodePipeline)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 11.5 Drift Detection & Remediation

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 12. Database Provisioning & Lifecycle

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 12.1 Golden Patterns (Parameter Groups, Option Groups)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 12.2 Secure Bootstrapping (Networking, KMS, Secrets)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 12.3 User/Role Model & Least Privilege

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 12.4 Upgrades, Patching, Blue/Green (RDS Blue/Green)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 12.5 Decommissioning & Data Wipe Procedures

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 13. Performance Engineering

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 13.1 Workload Characterization & Benchmarks

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 13.2 Aurora/RDS Tuning (Connections, Memory, IOPS, Storage Types)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 13.3 RDS Proxy & Connection Pooling

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 13.4 Read Scaling (Read Replicas, Global Database for Aurora)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 13.5 Caching Strategies (ElastiCache, Application Patterns)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 13.6 Query Tuning Playbook (Postgres/MySQL/SQL Server/Oracle)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 14. High Availability & Disaster Recovery

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 14.1 Multi-AZ vs. Multi-Region Trade-offs

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 14.2 RPO/RTO Objectives & Testing Cadence

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 14.3 Aurora Global Database & Cross-Region Replication

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 14.4 DynamoDB Global Tables & DAX HA

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 14.5 Backup Strategy (AWS Backup, Snapshots, PITR)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 14.6 DR Runbooks & Automated Failover

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 15. Migrations & Modernization

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 15.1 Discovery & Assessment (SCT, Workload Traces)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 15.2 Online Migrations (DMS, CDC, Dual-Write Caution)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 15.3 Replatform vs. Refactor (Aurora, DynamoDB, Serverless)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 15.4 Data Validation & Cutover Plans

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 15.5 Post-Migration Hardening & Observability

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 16. Security & Compliance

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 16.1 Shared Responsibility Model (DBRE Lens)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 16.2 Network Segmentation, Private Access, Egress Controls

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 16.3 Encryption In-Transit/At-Rest (TLS, KMS, TDE)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 16.4 Vulnerability Management & Patch Strategy

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 16.5 Auditability (CloudTrail, Config, Detective Controls)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 16.6 Compliance Tooling (Security Hub, GuardDuty, Macie, Artifact)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 17. Cost Optimization

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 17.1 Cost Allocation (Tags, Accounts, CUR)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 17.2 Rightsizing (Instance Families, Graviton, Storage Classes)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 17.3 Savings Plans & RIs (Where It Fits Databases)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 17.4 S3 Lifecycle & Glacier for Backups/Logs

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 17.5 Performance vs. Cost Trade-off Patterns

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 18. Continuous Delivery for Database Changes

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 18.1 Declarative Change Management (Liquibase/Flyway)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 18.2 Schema Migration Pipelines (CI/CD with Approvals)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 18.3 Automated Tests (Unit, Integration, Migration Smoke)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 18.4 Feature Flags & Backward-Compatible Releases

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 18.5 Rollback & Hotfix Strategies

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 19. GameDays, Chaos & Validation

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 19.1 Fault Injection (FIS) & Failure Modes

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 19.2 DR Drills & SLO Verification

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 19.3 Load & Soak Testing (Distributed Load Testing, Locust)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 19.4 Runbook Rehearsals & Time-to-Mitigate Metrics

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 20. Case Studies & Patterns

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 20.1 Zero-Downtime Migration to Aurora

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 20.2 Cross-Region Read Replica Strategy for Analytics

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 20.3 DynamoDB Hot-Partition Remediation

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 20.4 Redis Latency Spike Investigation

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 20.5 Cost Downshift without SLO Regression

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 21. Operational Runbooks & Playbooks

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 21.1 Backup/Restore (RDS/Aurora/DynamoDB/ElastiCache)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 21.2 Failover/Failback (Aurora Global, Route 53, App Changes)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 21.3 Performance Firefighting (DB-Specific)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 21.4 Security Incidents (Key Compromise, Secret Rotation)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 21.5 Capacity Emergencies (Burst Credit, Storage Auto-Scale)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 22. Checklists

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 22.1 Production Readiness

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 22.2 Launch/Go-Live

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 22.3 Compliance & Audit Prep

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 22.4 Cost Review (Monthly/Quarterly)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 22.5 DR Readiness (Quarterly)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 23. Appendix A — Python (boto3) Automation Library

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 23.1 RDS/Aurora Provisioning & Parameterization

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 23.2 Automated Snapshots & PITR Restore

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 23.3 Cross-Account, Cross-Region Backup Copy

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 23.4 Read Replica & Global DB Management

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 23.5 DynamoDB Table Ops & Global Tables

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 23.6 ElastiCache Cluster Operations

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 24. Appendix B — Terraform/CDK Modules

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 24.1 Module Layout & Standards

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 24.2 Example: Aurora PostgreSQL Production Module

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 24.3 Example: DynamoDB Global Tables Module

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 24.4 Example: Observability Baseline (CW, Alarms, Dashboards)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 25. Appendix C — IAM & Security Artifacts

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 25.1 Least-Privilege Policies for DBRE Automation

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 25.2 Break-Glass Role with Session Controls

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 25.3 SCP Examples for Database Guardrails

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 26. Appendix D — CI/CD Pipelines

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 26.1 GitHub Actions Templates (Terraform/Liquibase)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 26.2 GitLab CI & AWS CodePipeline Variants

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 26.3 Policy Checkers & Security Scanners (OPA, tfsec, cfn-nag)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 27. Appendix E — Templates & Records

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 27.1 Postmortem Template

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 27.2 DR Plan Template

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 27.3 Architecture Decision Record (ADR)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 27.4 Risk Register & SLO Catalog

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

---

## 28. Glossary & References

This section keeps the same narrative as before: decisions anchored on SLOs and error budgets,
guided by observability and reversibility. The emphasis remains on encoding guardrails into
automation so changes are safe, auditable, and repeatable.

We preserve the original content and add RDBMS‑specific code **only** at the subtopic level per
your request. Each subtopic now contains Oracle, PostgreSQL, MySQL, and SQL Server Python
connection examples, using TLS and parameterized statements.

### 28.1 Terms & Acronyms

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```

### 28.2 Further Reading (AWS Docs, Whitepapers, Blogs)

As before, the design intent here is to make failures cheap to detect and recover from. Document
assumptions, expected behaviors under fault, and the exact signals that define success/failure.
Prefer patterns that minimize manual steps and bound the blast radius.

Consistency across environments reduces incident entropy: identical naming, tagging, secret
handling, and retry/timeouts are essential. All operations should be idempotent, leave a
verifiable trace, and be gated by change approvals when risk is non‑trivial.

```python
# Oracle (oracledb): TCPS connection with named binds
import oracledb, os
conn = oracledb.connect(
    user="app_user", password=os.getenv("ORACLE_PASS","***"),
    dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True
)
cur = conn.cursor()
cur.execute("SELECT username, account_status FROM dba_users WHERE account_status=:st FETCH FIRST 3 ROWS ONLY",
            st="OPEN")
print(cur.fetchall())
cur.close(); conn.close()
```

```python
# PostgreSQL: parameterized SELECT with TLS
import psycopg2, os
conn = psycopg2.connect(
    "host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require"
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE status = %s ORDER BY id DESC LIMIT %s", ("ACTIVE", 50))
    print(cur.fetchall()[:5])
conn.close()
```

```python
# MySQL: safe UPDATE with parameters
import mysql.connector as mysql, os
cnx = mysql.connect(
    host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
    database="app", ssl_disabled=False
)
cur = cnx.cursor()
cur.execute("UPDATE orders SET status=%s, processed_at=NOW() WHERE id=%s", ("SHIPPED", 1234))
cnx.commit()
cur.close(); cnx.close()
```

```python
# SQL Server (pyodbc): stored procedure with parameter binding
import pyodbc, os
cnx = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
    "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no"
)
cur = cnx.cursor()
cur.execute("EXEC dbo.rotate_api_key @user_id = ?", 42)
cnx.commit()
cur.close(); cnx.close()
```
---
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


