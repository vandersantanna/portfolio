<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Multi-Cloud Reliability Engineering for Databases — AWS • Azure • GCP • OCI
*From landing zones and observability to cross-region DR—secure, automatable, measured.*

## Table of Contents
- [1. Executive Summary](#1-executive-summary)
- [2. Scope & Value Proposition (Multi-Cloud)](#2-scope--value-proposition-multi-cloud)
- [3. Skills Matrix](#3-skills-matrix)
  - [3.1 Core DBRE Competencies](#31-core-dbre-competencies)
  - [3.2 Cloud Provider Expertise](#32-cloud-provider-expertise)
  - [3.3 Platform & Tooling](#33-platform--tooling)
- [4. Reference Architectures & Landing Zones](#4-reference-architectures--landing-zones)
  - [4.1 Networking Foundations (per cloud)](#41-networking-foundations-per-cloud)
  - [4.2 Managed Database Building Blocks (per cloud)](#42-managed-database-building-blocks-per-cloud)
- [5. Reliability Fundamentals](#5-reliability-fundamentals)
  - [5.1 SLOs & Error Budgets](#51-slos--error-budgets)
  - [5.2 Synthetics & Health Probes (per cloud)](#52-synthetics--health-probes-per-cloud)
- [6. Observability & Monitoring](#6-observability--monitoring)
  - [6.1 Metrics/Logs Pipelines (per cloud)](#61-metricslogs-pipelines-per-cloud)
  - [6.2 Alerting Examples (per cloud)](#62-alerting-examples-per-cloud)
- [7. Performance & Capacity Engineering](#7-performance--capacity-engineering)
  - [7.1 Storage/IOPS Tuning (per cloud)](#71-storageiops-tuning-per-cloud)
  - [7.2 Connection Pooling & Proxies (per cloud)](#72-connection-pooling--proxies-per-cloud)
- [8. High Availability & Disaster Recovery](#8-high-availability--disaster-recovery)
  - [8.1 Intra-Region/Multi-AZ Patterns (per cloud)](#81-intra-regionmulti-az-patterns-per-cloud)
  - [8.2 Cross-Region DR (per cloud)](#82-cross-region-dr-per-cloud)
  - [8.3 Backups & PITR (per cloud)](#83-backups--pitr-per-cloud)
- [9. Security, Compliance & Governance](#9-security-compliance--governance)
  - [9.1 Identity & Access (per cloud)](#91-identity--access-per-cloud)
  - [9.2 Encryption & Secrets (per cloud)](#92-encryption--secrets-per-cloud)
  - [9.3 Audit/Policy Guardrails (per cloud)](#93-auditpolicy-guardrails-per-cloud)
- [10. Change Management & Release Engineering](#10-change-management--release-engineering)
  - [10.1 GitOps/IaC](#101-gitopsiac)
  - [10.2 Database CI/CD (multi-cloud matrix)](#102-database-cicd-multi-cloud-matrix)
- [11. Automation & Runbooks](#11-automation--runbooks)
  - [11.1 Daily/Weekly Health Checks](#111-dailyweekly-health-checks)
  - [11.2 Operational Playbooks (per cloud)](#112-operational-playbooks-per-cloud)
- [12. Integration & Streaming](#12-integration--streaming)
  - [12.1 CDC & Migrations (per cloud)](#121-cdc--migrations-per-cloud)
- [13. Cost & FinOps](#13-cost--finops)
  - [13.1 Budgets & Alerts (per cloud)](#131-budgets--alerts-per-cloud)
  - [13.2 Cost Optimization Playbook](#132-cost-optimization-playbook)
- [14. Multi-Cloud Governance](#14-multi-cloud-governance)
- [15. Reliability Case Studies](#15-reliability-case-studies)
- [16. KPIs & Executive Reporting](#16-kpis--executive-reporting)
- [17. Standards & Conventions](#17-standards--conventions)
- [18. Roadmap & Continuous Improvement](#18-roadmap--continuous-improvement)
- [19. Diagrams (Mermaid)](#19-diagrams-mermaid)

---

## 1. Executive Summary
I build and operate **reliable, secure, performant, and cost-efficient** database platforms across **AWS, Azure, GCP, and OCI**. My DBRE approach translates business outcomes into **SLOs** backed by **deep observability**, **safe change delivery**, and **provable HA/DR** with **PITR**.

## 2. Scope & Value Proposition (Multi-Cloud)
- **Scope:** Managed relational (Aurora/RDS, Azure SQL/PG Flexible, Cloud SQL/AlloyDB, Autonomous/HeatWave), NoSQL/streaming, and data warehouses.
- **Value:** Unified SLOs, repeatable IaC/CI, zero-surprise failovers/DR drills, and cost controls—**without vendor lock-in**.

---

## 3. Skills Matrix

### 3.1 Core DBRE Competencies
- SLI/SLO/SLA design • Error budgets • Incident response & postmortems • DR/chaos drills  
- Observability (metrics/logs/traces) • Performance & capacity modeling • Change safety (CFR↓) • FinOps

### 3.2 Cloud Provider Expertise
- **AWS:** RDS/Aurora, DynamoDB, Redshift, MSK; VPC/PrivateLink; CloudWatch/CloudTrail; KMS, Secrets Manager; DMS  
- **Azure:** Azure SQL/Managed Instance, PostgreSQL/MySQL Flexible, Cosmos DB; VNet/Private Endpoint; Monitor; Key Vault; DMS/ADF  
- **GCP:** Cloud SQL, AlloyDB, Spanner/Bigtable/BigQuery; VPC/PSC; Cloud Monitoring/Logging; Cloud KMS/Secret Manager; DMS/Dataflow  
- **OCI:** Autonomous (ATP/ADW), MySQL HeatWave, Exadata; VCN/Service Gateway; OCI Monitoring/Logging; Vault/Keys; GoldenGate

### 3.3 Platform & Tooling
Terraform • Bicep/ARM • Google DM • OCI RM • Ansible • Helm/Kustomize • GitHub Actions/Azure DevOps/GitLab CI  
Prometheus/Grafana • OpenTelemetry • Loki/ELK • pgBouncer/ProxySQL/RDS Proxy

---

## 4. Reference Architectures & Landing Zones

### 4.1 Networking Foundations (per cloud)
~~~hcl
# AWS — VPC with private subnets + interface endpoints (Terraform)
resource "aws_vpc" "db" { cidr_block = "10.10.0.0/16" }
resource "aws_subnet" "priv_a" { vpc_id = aws_vpc.db.id cidr_block = "10.10.1.0/24" availability_zone = "us-east-1a" }
resource "aws_subnet" "priv_b" { vpc_id = aws_vpc.db.id cidr_block = "10.10.2.0/24" availability_zone = "us-east-1b" }
resource "aws_vpc_endpoint" "secrets" { vpc_id = aws_vpc.db.id service_name = "com.amazonaws.us-east-1.secretsmanager" vpc_endpoint_type = "Interface" subnet_ids = [aws_subnet.priv_a.id, aws_subnet.priv_b.id] }
~~~

~~~bicep
// Azure — VNet + subnets + Private Endpoint for DB
resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
  name: 'vnet-db'
  location: resourceGroup().location
  properties: {
    addressSpace: { addressPrefixes: ['10.20.0.0/16'] }
    subnets: [
      { name: 'db', properties: { addressPrefix: '10.20.1.0/24' } }
      { name: 'app', properties: { addressPrefix: '10.20.2.0/24' } }
    ]
  }
}
resource pe 'Microsoft.Network/privateEndpoints@2023-04-01' = {
  name: 'pe-pg'
  location: resourceGroup().location
  properties: {
    subnet: { id: vnet.properties.subnets[0].id }
    privateLinkServiceConnections: [{
      name: 'pg-link'
      properties: { privateLinkServiceId: resourceId('Microsoft.DBforPostgreSQL/flexibleServers','pg-app') }
    }]
  }
}
~~~

~~~hcl
# GCP — VPC + Private Service Connect for Cloud SQL (Terraform)
resource "google_compute_network" "vpc" { name = "vpc-db" auto_create_subnetworks = false }
resource "google_compute_subnetwork" "db" { name = "subnet-db" ip_cidr_range = "10.30.1.0/24" region = "us-central1" network = google_compute_network.vpc.id }
# Cloud SQL uses Private IP via PSC automatically when private_network is set on the instance.
~~~

~~~hcl
# OCI — VCN + private subnet + Service Gateway (Terraform)
resource "oci_core_vcn" "vcn" { cidr_block = "10.40.0.0/16" compartment_id = var.compartment_id display_name = "vcn-db" }
resource "oci_core_subnet" "db" { cidr_block = "10.40.1.0/24" vcn_id = oci_core_vcn.vcn.id prohibit_public_ip_on_vnic = true display_name = "subnet-db" }
resource "oci_core_service_gateway" "sgw" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.vcn.id
  services       = [data.oci_core_services.all_services.services[0].id] # Object Storage access w/o internet
}
~~~

### 4.2 Managed Database Building Blocks (per cloud)
~~~hcl
# AWS — Aurora PostgreSQL (Multi-AZ writer + readers)
resource "aws_kms_key" "db" { description = "RDS KMS" }
resource "aws_rds_cluster" "aurora" {
  engine = "aurora-postgresql" engine_version = "15.4"
  database_name = "app" master_username = "dbadmin" master_password = var.db_password
  storage_encrypted = true kms_key_id = aws_kms_key.db.arn
  backup_retention_period = 7 deletion_protection = true
}
resource "aws_rds_cluster_instance" "writer" { cluster_identifier = aws_rds_cluster.aurora.id instance_class = "db.r6g.large" }
resource "aws_rds_cluster_instance" "reader" { count = 2 cluster_identifier = aws_rds_cluster.aurora.id instance_class = "db.r6g.large" }
~~~

~~~bicep
// Azure — PostgreSQL Flexible Server (Zone-Redundant)
resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: 'pg-app'
  location: resourceGroup().location
  sku: { name: 'GP_Standard_D4s_v3' }
  properties: {
    version: '16'
    backup: { backupRetentionDays: 7, geoRedundantBackup: 'Enabled' }
    network: { publicNetworkAccess: 'Disabled' }
    highAvailability: { mode: 'ZoneRedundant', standbyAvailabilityZone: '2' }
    storage: { storageSizeGB: 256 }
    authentication: { activeDirectoryAuth: 'Disabled' }
  }
}
~~~

~~~hcl
# GCP — Cloud SQL for PostgreSQL (Regional HA + PITR)
resource "google_sql_database_instance" "pg" {
  name = "pg-app" database_version = "POSTGRES_16" region = "us-central1"
  settings {
    tier = "db-custom-4-16384"
    availability_type = "REGIONAL"
    ip_configuration { ipv4_enabled = false, private_network = google_compute_network.vpc.self_link }
    backup_configuration { enabled = true, point_in_time_recovery_enabled = true, transaction_log_retention_days = 7 }
  }
}
resource "google_sql_user" "app" { instance = google_sql_database_instance.pg.name name = "app" password = var.app_password }
~~~

~~~hcl
# OCI — Autonomous Transaction Processing (ATP) with Data Guard
resource "oci_database_autonomous_database" "atp" {
  compartment_id = var.compartment_id db_name = "APPDB" display_name = "atp-app" db_workload = "OLTP"
  cpu_core_count = 2 data_storage_size_in_tbs = 1 is_auto_scaling_enabled = true is_data_guard_enabled = true protection_mode = "MAXIMUM_AVAILABILITY"
}
~~~

---

## 5. Reliability Fundamentals

### 5.1 SLOs & Error Budgets
~~~yaml
# SLOs-as-code (applies across clouds)
service: orders-db
slos:
  - name: p99_read_latency_ms   ; target: "< 40" ; window: 30d
  - name: p99_commit_latency_ms ; target: "< 120"; window: 30d
  - name: replica_lag_seconds   ; target: "<= 5" ; window: 30d
  - name: restore_time_minutes  ; target: "<= 20"; window: 30d
burn_policies:
  - if_burn_rate: "> 2.0x"
    action: "freeze risky changes; open reliability epic; schedule DR drill"
~~~

### 5.2 Synthetics & Health Probes (per cloud)
~~~hcl
# AWS — CloudWatch Synthetics Canary (Terraform, simple HTTPS check)
resource "aws_synthetics_canary" "db_rw" {
  name = "rw-endpoint-health"
  artifact_s3_location = "s3://synthetics-artifacts/"
  runtime_version = "syn-nodejs-puppeteer-3.8"
  handler = "page.handler"
  code { handler = "exports.handler = async () => { return 'ok' }" }
  schedule { expression = "rate(1 minute)" }
}
~~~

~~~bicep
// Azure — Application Insights availability test (classic ping)
resource ai 'Microsoft.Insights/components@2020-02-02' = { name: 'appinsights-db'; location: resourceGroup().location kind: 'web' properties: { Application_Type: 'web' } }
resource test 'Microsoft.Insights/webtests@2015-05-01' = {
  name: 'db-rw-check'
  location: 'global'
  properties: {
    SyntheticMonitorId: 'db-rw-check'
    Name: 'db-rw-check'
    Kind: 'ping'
    Enabled: true
    Frequency: 60
    Locations: [{ Id: 'us-fl-mia-azr' }]
    Configuration: { WebTest: '<WebTest ... />' }
  }
}
~~~

~~~yaml
# GCP — Uptime Check (YAML for gcloud monitoring)
uptimeCheckConfig:
  displayName: "db-rw-check"
  monitoredResource: { type: "uptime_url", labels: { host: "rw.internal.example" } }
  httpCheck: { useSsl: true, path: "/", port: 443 }
  timeout: "10s"
  period: "60s"
~~~

~~~hcl
# OCI — Health Checks HTTP monitor (Terraform)
resource "oci_health_checks_http_monitor" "db_rw" {
  compartment_id = var.compartment_id
  display_name   = "db-rw-check"
  interval_in_seconds = 60
  targets = ["rw.internal.example"]
  protocol = "HTTPS"
  method = "GET"
  path = "/"
}
~~~

---

## 6. Observability & Monitoring

### 6.1 Metrics/Logs Pipelines (per cloud)
~~~hcl
# AWS — Enable RDS Enhanced Monitoring & log exports (Terraform)
resource "aws_db_parameter_group" "pg" { name = "pg-params" family = "aurora-postgresql15" }
resource "aws_rds_cluster" "aurora" { # (see earlier) enable_cloudwatch_logs_exports = ["postgresql","upgrade"] }
~~~

~~~bicep
// Azure — Diagnostic Settings to Log Analytics
resource la 'Microsoft.OperationalInsights/workspaces@2021-12-01-preview' = { name: 'law-db'; location: resourceGroup().location properties: {} }
resource ds 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-pg'
  scope: resourceId('Microsoft.DBforPostgreSQL/flexibleServers','pg-app')
  properties: {
    workspaceId: la.id
    logs: [ { category: 'PostgreSQLLogs', enabled: true } ]
    metrics: [ { category: 'AllMetrics', enabled: true } ]
  }
}
~~~

~~~hcl
# GCP — Route Cloud SQL logs to Logging sink (Terraform)
resource "google_logging_project_sink" "sql_sink" {
  name = "cloudsql-logs-to-bucket"
  destination = "storage.googleapis.com/${google_storage_bucket.logs.name}"
  filter = "resource.type=cloudsql_database"
}
resource "google_storage_bucket" "logs" { name = "gcp-sql-logs-${var.project_id}" location = "US" uniform_bucket_level_access = true }
~~~

~~~hcl
# OCI — Stream Autonomous DB logs to Logging group (Terraform)
resource "oci_logging_log_group" "lg" { compartment_id = var.compartment_id display_name = "db-logs" }
resource "oci_logging_log" "adb" {
  display_name = "autonomous-db-logs"
  log_group_id = oci_logging_log_group.lg.id
  log_type = "SERVICE"
  configuration { source { category = "autonomousdatabase" resource = oci_database_autonomous_database.atp.id service = "database" } }
  is_enabled = true
}
~~~

### 6.2 Alerting Examples (per cloud)
~~~hcl
# AWS — CloudWatch Alarm (Aurora ReplicaLag)
resource "aws_cloudwatch_metric_alarm" "replica_lag" {
  alarm_name = "AuroraReplicaLagHigh"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods = 3 period = 60 threshold = 5
  metric_name = "ReplicaLag"
  namespace = "AWS/RDS"
  dimensions = { DBClusterIdentifier = aws_rds_cluster.aurora.id }
  statistic = "Average"
}
~~~

~~~bicep
// Azure — Metric Alert (CPU for Flexible Server)
resource alert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'pg-cpu-high'
  location: 'global'
  properties: {
    description: 'CPU > 80% for 10m'
    severity: 2 enabled: true scopes: [resourceId('Microsoft.DBforPostgreSQL/flexibleServers','pg-app')]
    evaluationFrequency: 'PT1M' windowSize: 'PT10M'
    criteria: {
      allOf: [{
        name: 'cpu'
        metricName: 'cpu_percent'
        operator: 'GreaterThan' threshold: 80 timeAggregation: 'Average'
        metricNamespace: 'Microsoft.DBforPostgreSQL/flexibleServers'
      }]
    }
  }
}
~~~

~~~yaml
# GCP — Alert Policy (Cloud SQL CPU utilization)
displayName: "CloudSQL CPU High"
combiner: "OR"
conditions:
- displayName: "CPU > 80% 10m"
  conditionThreshold:
    filter: 'metric.type="cloudsql.googleapis.com/database/cpu/utilization" resource.type="cloudsql_database"'
    comparison: "COMPARISON_GT"
    thresholdValue: 0.8
    duration: "600s"
notificationChannels: []
~~~

~~~hcl
# OCI — Monitoring Alarm (Autonomous DB CPU)
resource "oci_monitoring_alarm" "adb_cpu" {
  compartment_id = var.compartment_id
  display_name = "ADB CPU High"
  query = "oci_autonomous_database, CpuUtilization[1m]{resourceId = \""${oci_database_autonomous_database.atp.id}\""}.mean() > 80"
  severity = "CRITICAL"
  is_enabled = true
  destinations = [var.ons_topic_ocid]
}
~~~

---

## 7. Performance & Capacity Engineering

### 7.1 Storage/IOPS Tuning (per cloud)
~~~hcl
# AWS — RDS storage gp3 with provisioned IOPS/throughput
resource "aws_db_instance" "pg" {
  allocated_storage = 500 storage_type = "gp3" iops = 12000 throughput = 500
  engine = "postgres" engine_version = "16" instance_class = "db.m6i.large"
  username = "postgres" password = var.password skip_final_snapshot = true
}
~~~

~~~bicep
// Azure — Flexible Server storage & autogrow
resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' existing = { name: 'pg-app' }
resource upd 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: pg.name
  properties: { storage: { storageSizeGB: 512, autoGrow: 'Enabled' } }
}
~~~

~~~hcl
# GCP — Cloud SQL PD_SSD + disk autoresize
resource "google_sql_database_instance" "pg" {
  name = "pg-app"
  database_version = "POSTGRES_16"
  region = "us-central1"
  settings {
    tier = "db-custom-8-30720"
    availability_type = "REGIONAL"
    disk_type = "PD_SSD"
    disk_autoresize = true
  }
}
~~~

~~~hcl
# OCI — ATP auto-scaling for compute/storage (already enabled above)
# Example: scale up cores via Terraform variable change
resource "oci_database_autonomous_database" "atp" {
  # ...
  cpu_core_count = 4   # increase when cpu-utilization SLOs at risk
  data_storage_size_in_tbs = 2
}
~~~

### 7.2 Connection Pooling & Proxies (per cloud)
~~~hcl
# AWS — RDS Proxy for Postgres
resource "aws_db_proxy" "pg" {
  name = "pg-proxy" engine_family = "POSTGRESQL"
  auth { auth_scheme = "SECRETS" secret_arn = aws_secretsmanager_secret.db.arn iam_auth = "DISABLED" }
  role_arn = aws_iam_role.rds_proxy.arn
  vpc_subnet_ids = [aws_subnet.priv_a.id, aws_subnet.priv_b.id]
}
~~~

~~~bicep
// Azure — PgBouncer as container in AKS (helm release stub)
resource helm 'helm.sh/release/v2@2020-01-01-preview' = {
  name: 'pgbouncer'
  properties: {
    chart: { repository: 'https://charts.example.com', name: 'pgbouncer', version: '1.0.0' }
    values: { dbHost: 'pg-app.postgres.database.azure.com', poolMode: 'transaction' }
  }
}
~~~

~~~yaml
# GCP — Cloud SQL Auth Proxy as sidecar (Deployment excerpt)
containers:
- name: app
  image: gcr.io/myproj/app:latest
- name: cloud-sql-proxy
  image: gcr.io/cloudsql-docker/gce-proxy:1.37.1
  args: ["-instances=$(PROJECT):us-central1:pg-app=tcp:5432", "-enable_iam_login"]
~~~

~~~hcl
# OCI — MySQL HeatWave has built-in pooling; for ATP use app-side poolers (e.g., HikariCP).
# Example shows a compute instance running PgBouncer behind a private LB (sketch).
# (Infra omitted for brevity; use OCI LB + Instance Pool modules.)
~~~

---

## 8. High Availability & Disaster Recovery

### 8.1 Intra-Region/Multi-AZ Patterns (per cloud)
~~~hcl
# AWS — Aurora: writer + read replicas across AZs (see Section 4.2). Failover managed by service.
~~~

~~~bicep
// Azure — Flexible Server Zone-Redundant HA (already configured); read replicas in-zone
resource rr 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: 'pg-app-rep1'
  location: resourceGroup().location
  properties: { createMode: 'Replica', sourceServerResourceId: resourceId('Microsoft.DBforPostgreSQL/flexibleServers','pg-app') }
}
~~~

~~~hcl
# GCP — Cloud SQL REGIONAL (zonal control handled by service). Add read replica in-region:
resource "google_sql_database_instance" "replica_in_region" {
  name = "pg-app-replica-a"
  database_version = "POSTGRES_16" region = "us-central1"
  master_instance_name = google_sql_database_instance.pg.name
}
~~~

~~~hcl
# OCI — ATP has standby in same region when Data Guard enabled (fast-start failover supported).
# (Properties enabled in Section 4.2)
~~~

### 8.2 Cross-Region DR (per cloud)
~~~hcl
# AWS — Aurora Global Database (Terraform)
resource "aws_rds_global_cluster" "global" { global_cluster_identifier = "aurora-global" engine = "aurora-postgresql" engine_version = "15.4" }
resource "aws_rds_cluster" "primary" { # region A; global_cluster_identifier = aws_rds_global_cluster.global.id ... }
resource "aws_rds_cluster" "secondary" { # region B; global_cluster_identifier = aws_rds_global_cluster.global.id ... }
~~~

~~~bash
# Azure — Create cross-region read replica (CLI)
az postgres flexible-server replica create \
  --name pg-app-replica-euw \
  --source-server pg-app \
  --resource-group rg-db \
  --location westeurope
~~~

~~~hcl
# GCP — Cross-region replica (Terraform)
resource "google_sql_database_instance" "replica_xr" {
  name = "pg-app-replica-eu"
  database_version = "POSTGRES_16"
  region = "europe-west1"
  master_instance_name = google_sql_database_instance.pg.name
}
~~~

~~~hcl
# OCI — Autonomous Data Guard association (Terraform)
resource "oci_database_autonomous_database_dataguard_association" "adg" {
  autonomous_database_id = oci_database_autonomous_database.atp.id
  creation_type           = "ExistingRemote" # or "New"
  peer_autonomous_database_id = oci_database_autonomous_database.adb_peer.id
  protection_mode         = "MAXIMUM_AVAILABILITY"
}
~~~

### 8.3 Backups & PITR (per cloud)
~~~hcl
# AWS — RDS snapshot + PITR enabled (see Section 4.2). Example on-demand snapshot:
resource "aws_db_snapshot" "snap" { db_instance_identifier = aws_db_instance.pg.id db_snapshot_identifier = "manual-snap-01" }
~~~

~~~bicep
// Azure — Geo-redundant backups already enabled. Point-in-time restore via CLI:
@description('PITR example')
output pitrCommand string = 'az postgres flexible-server restore --name pg-restore --resource-group rg-db --source-server pg-app --restore-time "2025-10-08T12:20:00Z"'
~~~

~~~bash
# GCP — PITR restore (gcloud)
gcloud sql backups list --instance=pg-app
gcloud sql instances clone pg-restore --source=pg-app --point-in-time="2025-10-08T12:20:00Z"
~~~

~~~bash
# OCI — ATP PITR (oci CLI)
oci db autonomous-database restore --autonomous-database-id $ADB_OCID --timestamp "2025-10-08T12:20:00Z"
~~~

---

## 9. Security, Compliance & Governance

### 9.1 Identity & Access (per cloud)
~~~hcl
# AWS — IAM policy allowing read of Secrets Manager for DB creds
data "aws_iam_policy_document" "sm_read" {
  statement { actions = ["secretsmanager:GetSecretValue"] resources = [aws_secretsmanager_secret.db.arn] }
}
resource "aws_iam_role_policy" "attach" { role = aws_iam_role.app.name policy = data.aws_iam_policy_document.sm_read.json }
~~~

~~~bicep
// Azure — Key Vault access policy for app SP
resource kv 'Microsoft.KeyVault/vaults@2022-07-01' = { name: 'kv-db'; location: resourceGroup().location properties: { tenantId: subscription().tenantId sku: { name: 'standard', family: 'A' } } }
resource pol 'Microsoft.KeyVault/vaults/accessPolicies@2022-07-01' = {
  name: '${kv.name}/add'
  properties: {
    accessPolicies: [{ tenantId: subscription().tenantId, objectId: '<app-sp-objectid>', permissions: { secrets: ['get','list'] } }]
  }
}
~~~

~~~hcl
# GCP — Secret Manager + IAM binding
resource "google_secret_manager_secret" "db" { secret_id = "db-password" replication { automatic = true } }
resource "google_secret_manager_secret_version" "dbv" { secret = google_secret_manager_secret.db.id secret_data = var.db_password }
resource "google_secret_manager_secret_iam_member" "allow" { secret_id = google_secret_manager_secret.db.id role = "roles/secretmanager.secretAccessor" member = "serviceAccount:${var.app_sa}" }
~~~

~~~hcl
# OCI — Vault secret (password) and policy
resource "oci_kms_vault" "vault" { compartment_id = var.compartment_id display_name = "vault-db" vault_type = "DEFAULT" }
resource "oci_vault_secret" "db" {
  compartment_id = var.compartment_id
  vault_id       = oci_kms_vault.vault.id
  secret_name    = "db-password"
  secret_content { content_type = "BASE64" content = base64encode(var.db_password) }
}
~~~

### 9.2 Encryption & Secrets (per cloud)
~~~hcl
# AWS — CMEK via KMS on Aurora (already used); enforce TLS at parameter group
resource "aws_db_parameter_group" "tls" { name = "pg-require-ssl" family = "aurora-postgresql15" parameter { name = "rds.force_ssl" value = "1" } }
~~~

~~~bicep
// Azure — Enforce TLS and minimal TLS version
resource conf 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2023-03-01-preview' = {
  name: 'pg-app/min_tls_version'
  parent: pg
  properties: { value: 'TLS1_2', source: 'user-override' }
}
~~~

~~~hcl
# GCP — Cloud SQL CMEK (KMS) and require SSL
resource "google_kms_key_ring" "db" { name = "db-keys" location = "us" }
resource "google_kms_crypto_key" "cmek" { name = "sql-cmek" key_ring = google_kms_key_ring.db.id }
resource "google_sql_database_instance" "pg" {
  # ...
  disk_encryption_configuration { kms_key_name = google_kms_crypto_key.cmek.id }
  settings { ip_configuration { require_ssl = true } }
}
~~~

~~~hcl
# OCI — ATP always encrypted at rest; enforce TLS for clients via wallet (client-side).
# (Wallet/TCPS used in JDBC URLs for Autonomous.)
~~~

### 9.3 Audit/Policy Guardrails (per cloud)
~~~hcl
# AWS — SCP to deny public RDS (Organizations)
data "aws_iam_policy_document" "deny_public_rds" {
  statement {
    effect = "Deny"
    actions = ["rds:ModifyDBInstance","rds:CreateDBInstance"]
    resources = ["*"]
    condition { test = "StringEquals" variable = "rds:PubliclyAccessible" values = ["true"] }
  }
}
# Attach this SCP JSON at the OU level via aws_organizations_policy.
~~~

~~~bicep
// Azure — Policy: PostgreSQL Flexible must disable public network access
resource polDef 'Microsoft.Authorization/policyDefinitions@2021-06-01' = {
  name: 'deny-public-pg-flex'
  properties: {
    policyType: 'Custom'
    mode: 'All'
    displayName: 'Deny public access for PostgreSQL Flexible'
    policyRule: {
      if: { allOf: [
        { field: 'type', equals: 'Microsoft.DBforPostgreSQL/flexibleServers' },
        { field: 'Microsoft.DBforPostgreSQL/flexibleServers/publicNetworkAccess', equals: 'Enabled' }
      ] }
      then: { effect: 'deny' }
    }
  }
}
~~~

~~~yaml
# GCP — Org Policy (restrict public IP on Cloud SQL)
# (Apply via gcloud org-policies set)
constraint: constraints/sql.restrictPublicIp
listPolicy:
  deniedValues: ["INCLUDE_PUBLIC_IP"]
~~~

~~~hcl
# OCI — Network guardrail: Security List denies ingress from 0.0.0.0/0 to DB ports
resource "oci_core_security_list" "db" {
  vcn_id = oci_core_vcn.vcn.id
  display_name = "db-sec"
  ingress_security_rules = [{
    source = "10.0.0.0/8" protocol = "6" tcp_options = { destination_port_range = { min = 1521, max = 1522 } }
  }]
}
~~~

---

## 10. Change Management & Release Engineering

### 10.1 GitOps/IaC
- **Pattern:** Terraform modules per cloud, versioned; policy-as-code gates; drift detection; PR environments.
- **State & Secrets:** Remote state backends (S3+DynamoDB / Azure Storage / GCS / OCI Object Storage) + OIDC/OAuth for ephemeral creds.

### 10.2 Database CI/CD (multi-cloud matrix)
~~~yaml
# GitHub Actions — Run Flyway/Liquibase migrations across clouds via matrix
name: db-migrations
on: { push: { paths: ["db/migrations/**"] } }
jobs:
  migrate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        cloud: [aws, azure, gcp, oci]
    steps:
      - uses: actions/checkout@v4
      - name: Setup Flyway
        run: |
          curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.0.0/flyway-commandline-10.0.0-linux-x64.tar.gz | tar xz
          sudo ln -s $PWD/flyway-10.0.0/flyway /usr/local/bin/flyway

      # AWS
      - if: matrix.cloud == 'aws'
        name: Migrate on Aurora (JDBC)
        env: { DB_URL: "jdbc:postgresql://aurora-writer.cluster-xxxxx.us-east-1.rds.amazonaws.com:5432/app", DB_USER: "appmigrator", DB_PASS: "${{ secrets.AWS_DB_PASS }}" }
        run: flyway -url=$DB_URL -user=$DB_USER -password=$DB_PASS -locations=filesystem:db/migrations migrate

      # Azure
      - if: matrix.cloud == 'azure'
        name: Migrate on Azure PG Flexible
        env: { DB_URL: "jdbc:postgresql://pg-app.postgres.database.azure.com:5432/app?sslmode=require", DB_USER: "appmigrator@pg-app", DB_PASS: "${{ secrets.AZ_DB_PASS }}" }
        run: flyway -url="$DB_URL" -user="$DB_USER" -password="$DB_PASS" -locations=filesystem:db/migrations migrate

      # GCP
      - if: matrix.cloud == 'gcp'
        name: Migrate on Cloud SQL via Auth Proxy
        env: { INSTANCE: "${{ secrets.GCP_INSTANCE }}" }
        run: |
          wget https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.11.3/cloud-sql-proxy.linux.amd64 -O cloud-sql-proxy && chmod +x cloud-sql-proxy
          ./cloud-sql-proxy $INSTANCE & sleep 2
          flyway -url="jdbc:postgresql://127.0.0.1:5432/app?sslmode=disable" -user="${{ secrets.GCP_DB_USER }}" -password="${{ secrets.GCP_DB_PASS }}" -locations=filesystem:db/migrations migrate

      # OCI
      - if: matrix.cloud == 'oci'
        name: Migrate on Autonomous (Wallet/TCPS)
        run: |
          unzip wallet.zip -d wallet
          flyway -url="jdbc:oracle:thin:@app_high?TNS_ADMIN=wallet" -user="${{ secrets.OCI_DB_USER }}" -password="${{ secrets.OCI_DB_PASS }}" -locations=filesystem:db/migrations/oracle migrate
~~~

---

## 11. Automation & Runbooks

### 11.1 Daily/Weekly Health Checks
- Backups successful & recent; restore test cadence met; replica/stream lag within SLO; CPU/IO/locks ok; error budget burn under thresholds.

~~~bash
# Cross-cloud generic read/write probe (psql)
psql "$DB_URL" -c "select 1;" && echo "RW probe OK"
~~~

### 11.2 Operational Playbooks (per cloud)
~~~markdown
**AWS — Planned Aurora failover**
1) Confirm RPO/RTO readiness; backups OK.  
2) `aws rds failover-db-cluster --db-cluster-identifier <id>`  
3) Validate app traffic via writer endpoint; check ReplicaLag & connections.  
4) Post-steps: tag new writer; update dashboards.
~~~
---
**Azure — Promote PG Flexible replica**
1) Drain writes; ensure replica lag < SLO.  
2) `az postgres flexible-server replica promote --name pg-app-replica-euw --resource-group rg-db`  
3) Update DNS/pgbouncer; validate queries; reconfigure former primary as replica.  

~~~markdown
**GCP — Promote Cloud SQL cross-region replica**
1) Pause risky changes; confirm read-only state.  
2) `gcloud sql instances promote-replica pg-app-replica-eu`  
3) Flip traffic (DNS/service mesh); validate; recreate replica the other way.
~~~

~~~markdown
**OCI — Switchover Autonomous Data Guard**
1) Ensure lag zero and protection mode healthy.  
2) `oci db autonomous-database switchover --autonomous-database-id $PRIMARY`  
3) Validate application & wallets if endpoints changed.  
~~~

---

## 12. Integration & Streaming

### 12.1 CDC & Migrations (per cloud)

- AWS — DMS Task (excerpt)

~~~json
{
  "MigrationType": "cdc",
  "SourceEndpointArn": "arn:aws:dms:...:source",
  "TargetEndpointArn": "arn:aws:dms:...:target",
  "TableMappings": { "rules": [ { "rule-type":"selection","rule-id":"1","rule-name":"1","object-locator":{"schema-name":"public","table-name":"orders"},"rule-action":"include"} ] }
}
~~~

- Azure — ADF copy activity (excerpt)
~~~json
{
  "name": "CopyOrders",
  "type": "Copy",
  "typeProperties": {
    "source": { "type": "AzurePostgreSqlSource", "query": "select * from public.orders" },
    "sink":   { "type": "AzureSqlSink" }
  }
}
~~~

~~~yaml
# GCP — DMS connection profile (YAML excerpt)
postgresqlConnectionProfile:
  cloudSqlId: "pg-app"
displayName: "pg-cdc"
~~~

- OCI — GoldenGate deployment (very high-level placeholder)
~~~json
{
  "deploymentType": "OGG",
  "cpuCoreCount": 2,
  "licenseModel": "BRING_YOUR_OWN_LICENSE",
  "displayName": "gg-deploy-app"
}
~~~

# 13. Cost & FinOps

## 13.1 Budgets & Alerts (per cloud)

~~~hcl
# AWS — Budgets (Terraform)
resource "aws_budgets_budget" "monthly" {
  name = "db-monthly"
  budget_type = "COST" limit_amount = "2000" limit_unit = "USD" time_unit = "MONTHLY"
  cost_filters = { TagKeyValue = ["env$prod"] }
  notification { comparison_operator = "GREATER_THAN" threshold = 80 threshold_type = "PERCENTAGE" notification_type = "ACTUAL" subscriber_email_addresses = [var.email] }
}
~~~

~~~bicep
// Azure — Consumption budget
resource budget 'Microsoft.Consumption/budgets@2021-10-01' = {
  name: 'db-monthly'
  scope: subscription().id
  properties: {
    amount: 2000
    timeGrain: 'Monthly'
    timePeriod: { startDate: '2025-10-01T00:00:00Z', endDate: '2026-10-01T00:00:00Z' }
    category: 'Cost'
    notifications: {
      actual80: { enabled: true, threshold: 80, operator: 'GreaterThan', contactEmails: [ 'finops@example.com' ] }
    }
  }
}
~~~

~~~hcl
# GCP — Billing budget (Terraform)
resource "google_billing_budget" "monthly" {
  billing_account = var.billing_account
  display_name = "db-monthly"
  amount { specified_amount { currency_code = "USD" units = 2000 } }
  budget_filter { labels = { "env" = "prod" } }
  threshold_rules { threshold_percent = 0.8 }
}
~~~

~~~hcl
# OCI — Budget (Terraform)
resource "oci_budget_budget" "monthly" {
  compartment_id = var.compartment_id
  target_compartment_id = var.compartment_id
  amount = 2000 reset_period = "MONTHLY" description = "DB spend"
  targets = [var.compartment_id]
}
resource "oci_budget_alert_rule" "warn80" {
  budget_id = oci_budget_budget.monthly.id
  threshold_type = "PERCENTAGE" threshold = 80 message = "DB spend over 80%"
  recipients = var.email
}
~~~

## 13.2 Cost Optimization Playbook

- Right-size instances and storage tiers; enable auto-scaling judiciously; use serverless/read pools where bursty.
- Prefer private networking (egress reduction); cold storage for old backups; Savings Plans/Reservations/CUDs/OCPUs where steady.
- Enforce tagging/labels; monthly cost SLOs (e.g., “<$X/month per workload”).

# 14. Multi-Cloud Governance

- Service catalog & guardrails: approved DB services & versions, data residency rules, encryption posture, private networking only.
- Change controls: CI/CD gates on SLO burn and DR readiness.
- Data strategy: classification, retention, lineage, lawful basis (GDPR/LGPD), and access reviews.

# 15. Reliability Case Studies

- A: Aurora Global + DR drills → RTO 45s, RPO < 30s.
- B: Azure PG Flexible zone-redundant + PgBouncer → p99 −35%.
- C: Cloud SQL REGIONAL + Uptime checks → availability 99.97%/6 months.
- D: OCI ATP with ADG + PITR rehearsals → CFR −50%.

# 16. KPIs & Executive Reporting

~~~markdown
**Monthly DB Reliability Summary (Template)**
- Availability: 99.97% (SLO: 99.95%) ✅
- Error budget burn: 24% (policy < 50%)
- Incidents: Sev-1:0, Sev-2:1, Sev-3:2 (MTTR: 19m)
- Changes: 48 deploys, CFR: 2.7%
- DR: 1 drill passed, RTO 12m (target ≤ 20m), RPO 60s
- Cost: $18.7k (budget $20k) — top drivers: storage snapshots, cross-region egress
~~~

# 17. Standards & Conventions

- Naming: db-{cloud}-{env}-{service}, tagging/labels for owner, cost center, data class.
- Docs: ADRs, runbook templates, SQL style guide, change IDs linked to SLOs.
- Git: trunk-based or GitFlow; semantic versioning; CODEOWNERS; mandatory reviews.

# 18. Roadmap & Continuous Improvement

- Q1: 100% SLO coverage on tier-1; weekly automated restore tests.
- Q2: Global DR runbooks; policy-as-code guardrails; drift detection.
- Q3: OTel tracing to DB; per-table hot-spot partitioning.
- Q4: FinOps phase-2; zero-touch patching; deprecate legacy paths.

# 19. Diagrams (Mermaid)

~~~mermaid

flowchart LR
  subgraph AWS
    AUR[(Aurora PG)]:::a
  end
  subgraph Azure
    AZPG[(Azure PG Flexible)]:::z
  end
  subgraph GCP
    CSQL[(Cloud SQL PG)]:::g
  end
  subgraph OCI
    ATP[(Autonomous TP)]:::o
  end
  AUR --- AZPG --- CSQL --- ATP
  classDef a fill:#eef,stroke:#66f,stroke-width:2px;
  classDef z fill:#efe,stroke:#090,stroke-width:2px;
  classDef g fill:#ffe,stroke:#aa0,stroke-width:2px;
  classDef o fill:#fee,stroke:#c33,stroke-width:2px;
~~~
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

