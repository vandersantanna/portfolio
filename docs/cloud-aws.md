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
  - [4.4 Amazon ElastiCache (Redis/Memcached)](#44-amazon-elasticache-redismemcached)
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
  - [10.4 Oracle (oracledb/cx_Oracle, TCPS, wallets)](#104-oracle-oracledbcxoracle-tcps-wallets)
  - [10.5 SQL Server (pyodbc, Linux ODBC drivers)](#105-sql-server-pyodbc-linux-odbc-drivers)
  - [10.6 Cross-DB Abstraction (SQLAlchemy)](#106-cross-db-abstraction-sqlalchemy)
  - [10.7 Safety (dry-run, schema diffs, migration gating)](#107-safety-dry-run-schema-diffs-migration-gating)
  - [10.8 Throughput & Batching Patterns](#108-throughput--batching-patterns)
- [11. Infrastructure as Code & GitOps](#11-infrastructure-as-code--gitops)
  - [11.1 Terraform (Modules, Workspaces, Remote State)](#111-terraform-modules-workspaces-remote-state)
  - [11.2 AWS CDK & CloudFormation (Stacks, StackSets)](#112-aws-cdk--cloudformation-stacks-stacksets)
  - [11.3 Policy as Code (SCPs, IAM, Config Rules)](#113-policy-as-code-scps-iam-config-rules)
  - [11.4 CI/CD (GitHub Actions/GitLab CI/CodePipeline)](#114-cicd-github-actionsgitlab-cicodepipeline)
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
  - [14.2 RPO/RTO Objectives & Testing Cadence](#142-rporto-objectives--testing-cadence)
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
  - [28.2 Further Reading (AWS Docs, Whitepapers, Blogs)](#282-further-reading-aws-docs-whitepapers-blogs)

---

## 1. Executive Summary



### 1.1 Purpose & Audience






### 1.2 What “DBRE on AWS” Means






### 1.3 Portfolio Highlights & Outcomes






### 1.4 How to Navigate this Document






---

## 2. Architecture Overview



### 2.1 Reference Architectures (Single-Region, Multi-AZ, Multi-Region)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 2.2 Data Plane vs. Control Plane (AWS Services Map)






### 2.3 Workload Taxonomy (OLTP, Analytics, Streaming, Caching)






### 2.4 Reliability, Security, Cost as First-Class Concerns




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 3. AWS Foundations



### 3.1 Multi-Account Strategy (Organizations, SCPs, Guardrails)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 3.2 Networking (VPC, Subnets, TGW, PrivateLink, DX/VPN, IPv6)






### 3.3 Identity & Access (IAM Roles, SSO, Break-Glass)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 3.4 Encryption & Key Management (KMS, MRKs, Key Rotation)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 3.5 Secrets & Parameters (Secrets Manager, Parameter Store)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


---

## 4. Data Platform Services on AWS



### 4.1 Amazon Aurora (MySQL/PostgreSQL)






### 4.2 Amazon RDS (PostgreSQL, MySQL, SQL Server, Oracle)






### 4.3 Amazon DynamoDB (On-Demand, GSIs, DAX)






### 4.4 Amazon ElastiCache (Redis/Memcached)






### 4.5 Amazon OpenSearch Service






### 4.6 Amazon Redshift & Lakehouse Adjacent (Glue, Athena, Lake Formation)






### 4.7 Document & Graph (DocumentDB, Neptune)






### 4.8 Self-Managed on EC2/EKS (when & why)






---

## 5. Reliability Engineering (SLIs/SLOs & Operations)



### 5.1 SLIs & SLOs per Service (Latency, Availability, Durability)






### 5.2 Error Budgets & Release Policies






### 5.3 Incident Management (On-Call, Tiers, Escalations)






### 5.4 Postmortems & Continuous Improvement






---

## 6. Observability



### 6.1 Metrics, Logs, Traces (CloudWatch, X-Ray, OTEL)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.2 Dashboards & Alarms (CW Dashboards, AMG/Grafana)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.3 Query Performance Telemetry (Aurora/RDS Performance Insights)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.4 Synthetics & Probes (CloudWatch Synthetics)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 6.5 Log Shipping & Search (OpenSearch, S3 + Athena)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 7. Automation Frameworks (Python-First)



### 7.1 Boto3 SDK Foundations (Auth, Pagination, Retries)






### 7.2 Idempotent Operations & Safe Rollbacks






### 7.3 Event-Driven Ops (EventBridge, Step Functions, Lambda)






### 7.4 SSM Automation (Run Command, Documents, State Manager)






### 7.5 Reusable Libraries (Provisioning, Backups, Failover, Compliance)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


---

## 8. Python Integration for Automation (Foundations)



### 8.1 Packaging & Environments (pip/poetry, venv, Docker)






### 8.2 Configuration Management (env vars, Pydantic, SSM/Secrets)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 8.3 Retries, Backoff, Idempotency Keys




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 8.4 Structured Logging & Correlation IDs






### 8.5 Testing Strategy (unit/integration), CI Hooks






### 8.6 Distribution (Lambda layers, containers, wheels)






---

## 9. API Integrations in Python (AWS & Third-Party)



### 9.1 REST (requests/httpx), Auth (SigV4, OAuth2)






### 9.2 GraphQL (client patterns, pagination)






### 9.3 Webhooks & EventBridge Pipes






### 9.4 Rate Limiting, Circuit Breakers, Retries






### 9.5 Schema Validation (pydantic), Error Handling






### 9.6 Examples: ServiceNow/Jira/Slack, GitHub/GitLab, AWS Health API






---

## 10. Python Database Connectivity for Automation



### 10.1 Common Patterns (pools, secrets, transactions, retries)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 10.2 PostgreSQL (psycopg 3: async, COPY, examples)






### 10.3 MySQL (mysql-connector-python/PyMySQL)






### 10.4 Oracle (oracledb/cx_Oracle, TCPS, wallets)






### 10.5 SQL Server (pyodbc, Linux ODBC drivers)






### 10.6 Cross-DB Abstraction (SQLAlchemy)






### 10.7 Safety (dry-run, schema diffs, migration gating)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 10.8 Throughput & Batching Patterns






---

## 11. Infrastructure as Code & GitOps



### 11.1 Terraform (Modules, Workspaces, Remote State)






### 11.2 AWS CDK & CloudFormation (Stacks, StackSets)






### 11.3 Policy as Code (SCPs, IAM, Config Rules)






### 11.4 CI/CD (GitHub Actions/GitLab CI/CodePipeline)






### 11.5 Drift Detection & Remediation






---

## 12. Database Provisioning & Lifecycle



### 12.1 Golden Patterns (Parameter Groups, Option Groups)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 12.2 Secure Bootstrapping (Networking, KMS, Secrets)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 12.3 User/Role Model & Least Privilege






### 12.4 Upgrades, Patching, Blue/Green (RDS Blue/Green)






### 12.5 Decommissioning & Data Wipe Procedures






---

## 13. Performance Engineering



### 13.1 Workload Characterization & Benchmarks




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: explain plan for a critical report (ensure stats up to date)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: plan with buffers for a 7-day report
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# MySQL: EXPLAIN format=JSON for latency investigation
import mysql.connector as mysql, os, json
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: estimated plan XML for analysis (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 13.2 Aurora/RDS Tuning (Connections, Memory, IOPS, Storage Types)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: explain plan for a critical report (ensure stats up to date)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: plan with buffers for a 7-day report
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# MySQL: EXPLAIN format=JSON for latency investigation
import mysql.connector as mysql, os, json
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: estimated plan XML for analysis (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 13.3 RDS Proxy & Connection Pooling




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: active sessions and limits
import oracledb, os
conn = oracledb.connect(user="mon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT status, COUNT(*) FROM V$SESSION GROUP BY status")
print(cur.fetchall())
cur.execute("SELECT name, value FROM V$PARAMETER WHERE name IN ('sessions','processes')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: connection count vs max_connections
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM pg_stat_activity")
    used = cur.fetchone()[0]
    cur.execute("SHOW max_connections")
    maxc = cur.fetchone()[0]
    print({"used": used, "max": maxc})
```

*MySQL*

```python
# MySQL: threads connected vs max_connections
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW STATUS LIKE 'Threads_connected'"); used = cur.fetchone()[1]
cur.execute("SHOW VARIABLES LIKE 'max_connections'"); maxc = cur.fetchone()[1]
print({"used": used, "max": maxc})
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: current sessions and worker counts
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1")
print(("user_sessions", cur.fetchone()[0]))
cur.execute("SELECT * FROM sys.configurations WHERE name IN ('max worker threads')")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 13.4 Read Scaling (Read Replicas, Global Database for Aurora)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 13.5 Caching Strategies (ElastiCache, Application Patterns)






### 13.6 Query Tuning Playbook (Postgres/MySQL/SQL Server/Oracle)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: explain plan for a critical report (ensure stats up to date)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: plan with buffers for a 7-day report
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# MySQL: EXPLAIN format=JSON for latency investigation
import mysql.connector as mysql, os, json
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: estimated plan XML for analysis (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


---

## 14. High Availability & Disaster Recovery



### 14.1 Multi-AZ vs. Multi-Region Trade-offs




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 14.2 RPO/RTO Objectives & Testing Cadence






### 14.3 Aurora Global Database & Cross-Region Replication




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 14.4 DynamoDB Global Tables & DAX HA






### 14.5 Backup Strategy (AWS Backup, Snapshots, PITR)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: recent RMAN jobs (self-managed/EC2). On RDS, snapshot/PITR is API-driven.
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.ec2.internal/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: archiver health (useful for PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL: binlog status (PITR precondition); snapshots are AWS-managed
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS")
print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS")
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: latest native backups (EC2 or RDS native backup to S3 scenario)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.ec2.internal;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 14.6 DR Runbooks & Automated Failover




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


---

## 15. Migrations & Modernization



### 15.1 Discovery & Assessment (SCT, Workload Traces)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 15.2 Online Migrations (DMS, CDC, Dual-Write Caution)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 15.3 Replatform vs. Refactor (Aurora, DynamoDB, Serverless)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 15.4 Data Validation & Cutover Plans




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 15.5 Post-Migration Hardening & Observability




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 16. Security & Compliance



### 16.1 Shared Responsibility Model (DBRE Lens)






### 16.2 Network Segmentation, Private Access, Egress Controls




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 16.3 Encryption In-Transit/At-Rest (TLS, KMS, TDE)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 16.4 Vulnerability Management & Patch Strategy






### 16.5 Auditability (CloudTrail, Config, Detective Controls)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 16.6 Compliance Tooling (Security Hub, GuardDuty, Macie, Artifact)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 17. Cost Optimization



### 17.1 Cost Allocation (Tags, Accounts, CUR)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (capacity/cost visibility)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: top databases by size
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 17.2 Rightsizing (Instance Families, Graviton, Storage Classes)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (capacity/cost visibility)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: top databases by size
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 17.3 Savings Plans & RIs (Where It Fits Databases)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (capacity/cost visibility)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: top databases by size
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 17.4 S3 Lifecycle & Glacier for Backups/Logs




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


### 17.5 Performance vs. Cost Trade-off Patterns




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: explain plan for a critical report (ensure stats up to date)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: plan with buffers for a 7-day report
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# MySQL: EXPLAIN format=JSON for latency investigation
import mysql.connector as mysql, os, json
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: estimated plan XML for analysis (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


---

## 18. Continuous Delivery for Database Changes



### 18.1 Declarative Change Management (Liquibase/Flyway)






### 18.2 Schema Migration Pipelines (CI/CD with Approvals)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 18.3 Automated Tests (Unit, Integration, Migration Smoke)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 18.4 Feature Flags & Backward-Compatible Releases






### 18.5 Rollback & Hotfix Strategies






---

## 19. GameDays, Chaos & Validation



### 19.1 Fault Injection (FIS) & Failure Modes






### 19.2 DR Drills & SLO Verification




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 19.3 Load & Soak Testing (Distributed Load Testing, Locust)






### 19.4 Runbook Rehearsals & Time-to-Mitigate Metrics




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top wait events (system-level) for observability dashboards
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT event, total_waits, time_waited_micro FROM V$SYSTEM_EVENT ORDER BY time_waited_micro DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: database-level activity and (if enabled) pg_stat_statements top total_time
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, numbackends, xact_commit, blks_read, blks_hit FROM pg_stat_database ORDER BY (blks_read+blks_hit) DESC LIMIT 5")
    print(cur.fetchall())
    # Requires extension pg_stat_statements
    cur.execute("SELECT queryid, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10")
    print(cur.fetchall()[:3])
```

*MySQL*

```python
# MySQL: top statements by total latency (performance_schema)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("""SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: top cumulative CPU queries for dashboards
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
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
""")
print(cur.fetchall()[:1])
cur.close(); cnx.close()
```


---

## 20. Case Studies & Patterns



### 20.1 Zero-Downtime Migration to Aurora




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: pre/post cutover rowcount parity for critical tables
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="target.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ORDERS WHERE CREATED_AT >= SYSDATE - 7")
print(cur.fetchone())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: Flyway/Liquibase history check (schema drift guard)
import psycopg2, os
conn = psycopg2.connect("host=target.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: drift check via Liquibase DATABASECHANGELOG
import mysql.connector as mysql, os
cnx = mysql.connect(host="target.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"), database="app")
cur = cnx.cursor()
cur.execute("SELECT id, author, filename, dateexecuted FROM DATABASECHANGELOG ORDER BY dateexecuted DESC LIMIT 10")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: parity check for key tables during migration dry-run
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=target.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.Orders WHERE CreatedAt >= DATEADD(day,-7,SYSUTCDATETIME())")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 20.2 Cross-Region Read Replica Strategy for Analytics




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 20.3 DynamoDB Hot-Partition Remediation






### 20.4 Redis Latency Spike Investigation






### 20.5 Cost Downshift without SLO Regression




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (capacity/cost visibility)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: top databases by size
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 21. Operational Runbooks & Playbooks



### 21.1 Backup/Restore (RDS/Aurora/DynamoDB/ElastiCache)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: recent RMAN jobs (self-managed/EC2). On RDS, snapshot/PITR is API-driven.
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.ec2.internal/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: archiver health (useful for PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL: binlog status (PITR precondition); snapshots are AWS-managed
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS")
print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS")
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: latest native backups (EC2 or RDS native backup to S3 scenario)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.ec2.internal;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 21.2 Failover/Failback (Aurora Global, Route 53, App Changes)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 21.3 Performance Firefighting (DB-Specific)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: explain plan for a critical report (ensure stats up to date)
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("EXPLAIN PLAN FOR SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM ORDERS WHERE CREATED_AT >= SYSDATE-7 AND STATUS = 'OPEN'")
cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY())")
print("\n".join(r[0] for r in cur.fetchall()))
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: plan with buffers for a 7-day report
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) SELECT id, created_at FROM orders WHERE created_at >= now() - interval '7 days' AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
    print("\n".join(r[0] for r in cur.fetchall()))
```

*MySQL*

```python
# MySQL: EXPLAIN format=JSON for latency investigation
import mysql.connector as mysql, os, json
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("EXPLAIN FORMAT=JSON SELECT id, created_at FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY AND status = %s ORDER BY created_at DESC LIMIT 500", ("OPEN",))
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: estimated plan XML for analysis (avoid running heavy query)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=app;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SET SHOWPLAN_XML ON; SELECT id, created_at FROM dbo.Orders WHERE created_at >= DATEADD(day,-7, SYSUTCDATETIME()) AND status = 'OPEN' ORDER BY created_at DESC; SET SHOWPLAN_XML OFF;")
print(cur.fetchone())
cur.close(); cnx.close()
```


### 21.4 Security Incidents (Key Compromise, Secret Rotation)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 21.5 Capacity Emergencies (Burst Credit, Storage Auto-Scale)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: active sessions and limits
import oracledb, os
conn = oracledb.connect(user="mon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT status, COUNT(*) FROM V$SESSION GROUP BY status")
print(cur.fetchall())
cur.execute("SELECT name, value FROM V$PARAMETER WHERE name IN ('sessions','processes')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: connection count vs max_connections
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM pg_stat_activity")
    used = cur.fetchone()[0]
    cur.execute("SHOW max_connections")
    maxc = cur.fetchone()[0]
    print({"used": used, "max": maxc})
```

*MySQL*

```python
# MySQL: threads connected vs max_connections
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW STATUS LIKE 'Threads_connected'"); used = cur.fetchone()[1]
cur.execute("SHOW VARIABLES LIKE 'max_connections'"); maxc = cur.fetchone()[1]
print({"used": used, "max": maxc})
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: current sessions and worker counts
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1")
print(("user_sessions", cur.fetchone()[0]))
cur.execute("SELECT * FROM sys.configurations WHERE name IN ('max worker threads')")
print(cur.fetchall())
cur.close(); cnx.close()
```


---

## 22. Checklists



### 22.1 Production Readiness






### 22.2 Launch/Go-Live






### 22.3 Compliance & Audit Prep




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 22.4 Cost Review (Monthly/Quarterly)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: top tablespaces by size (capacity/cost visibility)
import oracledb, os
conn = oracledb.connect(user="capmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT tablespace_name, ROUND(SUM(bytes)/1024/1024/1024,2) AS GB FROM dba_segments GROUP BY tablespace_name ORDER BY GB DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: top databases by size
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC LIMIT 10")
    print(cur.fetchall())
```

*MySQL*

```python
# MySQL: schema size breakdown
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024/1024,2) AS GB FROM information_schema.tables GROUP BY table_schema ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: database sizes (GB)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=capmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT DB_NAME(database_id) AS db, CAST(SUM(size)*8.0/1024/1024 AS DECIMAL(10,2)) AS GB FROM sys.master_files GROUP BY database_id ORDER BY GB DESC")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 22.5 DR Readiness (Quarterly)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


---

## 23. Appendix A — Python (boto3) Automation Library



### 23.1 RDS/Aurora Provisioning & Parameterization




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: verify TDE wallet and network encryption (RDS Oracle/Oracle 19c)
import oracledb, os
conn = oracledb.connect(user="admin", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
# In-transit (TCPS) cipher details for current session
cur.execute("SELECT NETWORK_SERVICE_BANNER FROM V$SESSION_CONNECT_INFO WHERE SID = SYS_CONTEXT('USERENV','SID')")
print([r[0] for r in cur.fetchall()][:1])
# At-rest: encrypted tablespaces & wallet status
cur.execute("SELECT tablespace_name, encrypted FROM V$ENCRYPTED_TABLESPACES")
print(cur.fetchall())
cur.execute("SELECT WRL_TYPE, WRL_PARAMETER, STATUS FROM V$ENCRYPTION_WALLET")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL (RDS/Aurora PG): verify SSL for session; at-rest is KMS-managed (not queryable from SQL)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=app user=app_user password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SHOW ssl")
    print("ssl:", cur.fetchone()[0])
    cur.execute("SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
    print(cur.fetchone())
# Note: At-rest encryption status is controlled by AWS KMS at the instance/cluster level.
```

*MySQL*

```python
# MySQL (RDS/Aurora MySQL): verify TLS in-transit; at-rest uses AWS-managed KMS
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="app_user", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
print(cur.fetchall())
cur.execute("SHOW VARIABLES LIKE 'ssl_%'")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server (RDS/EC2): verify TLS and TDE state
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=app_user;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
# In-transit TLS
cur.execute("SELECT encrypt_option, protocol_version FROM sys.dm_exec_connections WHERE session_id = @@SPID")
print(cur.fetchone())
# At-rest TDE
cur.execute("SELECT DB_NAME(database_id) AS db, encryption_state FROM sys.dm_database_encryption_keys")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 23.2 Automated Snapshots & PITR Restore




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: recent RMAN jobs (self-managed/EC2). On RDS, snapshot/PITR is API-driven.
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.ec2.internal/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: archiver health (useful for PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL: binlog status (PITR precondition); snapshots are AWS-managed
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS")
print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS")
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: latest native backups (EC2 or RDS native backup to S3 scenario)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.ec2.internal;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 23.3 Cross-Account, Cross-Region Backup Copy




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: recent RMAN jobs (self-managed/EC2). On RDS, snapshot/PITR is API-driven.
import oracledb, os
conn = oracledb.connect(user="rmanmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.ec2.internal/ORCL", ssl_server_dn_match=False)
cur = conn.cursor()
cur.execute("SELECT start_time, end_time, input_type, status FROM V$RMAN_BACKUP_JOB_DETAILS ORDER BY start_time DESC FETCH FIRST 10 ROWS ONLY")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: archiver health (useful for PITR readiness)
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT archived_count, last_archived_time, failed_count, last_failed_time FROM pg_stat_archiver")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL: binlog status (PITR precondition); snapshots are AWS-managed
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW BINARY LOGS")
print(cur.fetchall()[:3])
cur.execute("SHOW MASTER STATUS")
print(cur.fetchone())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: latest native backups (EC2 or RDS native backup to S3 scenario)
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.ec2.internal;DATABASE=msdb;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=yes")
cur = cnx.cursor()
cur.execute("""SELECT TOP 10 database_name, backup_start_date, backup_finish_date, type AS backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC
""")
print(cur.fetchall())
cur.close(); cnx.close()
```


### 23.4 Read Replica & Global DB Management




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle Data Guard: transport/apply lag and role
import oracledb, os
conn = oracledb.connect(user="app_user", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT open_mode, database_role FROM V$DATABASE")
print(cur.fetchall())
cur.execute("SELECT NAME, VALUE FROM V$DATAGUARD_STATS WHERE NAME IN ('transport lag','apply lag')")
print(cur.fetchall())
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: replica lag (primary perspective)
import psycopg2, os
conn = psycopg2.connect("host=primary.rds.amazonaws.com dbname=app user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("""SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication
""")
    print(cur.fetchall())

```

*MySQL*

```python
# MySQL 8: replica status via performance_schema (Aurora/RDS compatible)
import mysql.connector as mysql, os
cnx = mysql.connect(host="replica.rds.amazonaws.com", user="monitor", password=os.getenv("MYSQL_PASS","***"),
                    database="app", ssl_disabled=False)
cur = cnx.cursor()
cur.execute("SELECT CHANNEL_NAME, SERVICE_STATE, RECEIVED_TRANSACTION_SET FROM performance_schema.replication_connection_status")
print(cur.fetchall())
cur.execute("SELECT CHANNEL_NAME, COUNT_TRANSACTIONS_RETRIES, APPLYING_TRANSACTION_TIMESTAMP FROM performance_schema.replication_applier_status_by_worker")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: AG health and queues
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=primary.rds.amazonaws.com;DATABASE=master;"
                     "UID=monitor;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("""SELECT ag.name, ar.replica_server_name, drs.synchronization_state_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
""")
print(cur.fetchall()[:3])
cur.close(); cnx.close()
```


### 23.5 DynamoDB Table Ops & Global Tables






### 23.6 ElastiCache Cluster Operations






---

## 24. Appendix B — Terraform/CDK Modules



### 24.1 Module Layout & Standards






### 24.2 Example: Aurora PostgreSQL Production Module






### 24.3 Example: DynamoDB Global Tables Module






### 24.4 Example: Observability Baseline (CW, Alarms, Dashboards)






---

## 25. Appendix C — IAM & Security Artifacts



### 25.1 Least-Privilege Policies for DBRE Automation




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


### 25.2 Break-Glass Role with Session Controls






### 25.3 SCP Examples for Database Guardrails




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 26. Appendix D — CI/CD Pipelines



### 26.1 GitHub Actions Templates (Terraform/Liquibase)






### 26.2 GitLab CI & AWS CodePipeline Variants






### 26.3 Policy Checkers & Security Scanners (OPA, tfsec, cfn-nag)




**Context-specific Python DB examples:**

*Oracle*

```python
# Oracle: users and locked/expired accounts review
import oracledb, os
conn = oracledb.connect(user="secmon", password=os.getenv("ORACLE_PASS","***"),
                        dsn="db.rds.amazonaws.com/ORCL", ssl_server_dn_match=True)
cur = conn.cursor()
cur.execute("SELECT username, account_status, profile FROM dba_users ORDER BY account_status DESC")
print(cur.fetchall()[:10])
cur.close(); conn.close()
```

*PostgreSQL*

```python
# PostgreSQL: roles and replication privileges
import psycopg2, os
conn = psycopg2.connect("host=db.rds.amazonaws.com dbname=postgres user=monitor password=" + os.getenv("PG_PASS","***") + " sslmode=require")
with conn, conn.cursor() as cur:
    cur.execute("SELECT rolname, rolsuper, rolreplication, rolcreaterole FROM pg_roles ORDER BY rolsuper DESC, rolname")
    print(cur.fetchall()[:10])
```

*MySQL*

```python
# MySQL: grants for a specific user (requires appropriate privileges)
import mysql.connector as mysql, os
cnx = mysql.connect(host="db.rds.amazonaws.com", user="admin", password=os.getenv("MYSQL_PASS","***"))
cur = cnx.cursor()
cur.execute("SHOW GRANTS FOR 'app_user'@'%'")
print(cur.fetchall())
cur.close(); cnx.close()
```

*SQL Server*

```python
# SQL Server: server principals and disabled logins
import pyodbc, os
cnx = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=db.rds.amazonaws.com;DATABASE=master;"
                     "UID=secmon;PWD=" + os.getenv("MSSQL_PASS","***") + ";Encrypt=yes;TrustServerCertificate=no")
cur = cnx.cursor()
cur.execute("SELECT name, type_desc, is_disabled FROM sys.sql_logins ORDER BY is_disabled DESC, name")
print(cur.fetchall()[:10])
cur.close(); cnx.close()
```


---

## 27. Appendix E — Templates & Records



### 27.1 Postmortem Template






### 27.2 DR Plan Template






### 27.3 Architecture Decision Record (ADR)






### 27.4 Risk Register & SLO Catalog






---

## 28. Glossary & References



### 28.1 Terms & Acronyms






### 28.2 Further Reading (AWS Docs, Whitepapers, Blogs)




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



