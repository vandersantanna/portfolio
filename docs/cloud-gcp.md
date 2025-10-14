```markdown
# Google Cloud Platform (GCP) — Data Platform & DBRE Portfolio

**Vander Sant Anna — Senior DBA / DBRE — Remote — US/Canada/EU/Latin America time zones**  
Email: [vandersantanna@gmail.com](mailto:vandersantanna@gmail.com) • LinkedIn: [linkedin.com/in/vandersantanna](https://linkedin.com/in/vandersantanna) • GitHub: [github.com/vandersantanna](https://github.com/vandersantanna)

> Last updated: October 14, 2025

## Table of Contents
- [Executive Summary](#executive-summary)
- [Services & Capabilities](#services--capabilities)
- [Architecture Principles](#architecture-principles)
- [Reference Architectures](#reference-architectures)
  - [High Availability (In-Region)](#high-availability-in-region)
  - [Disaster Recovery (Cross-Region)](#disaster-recovery-cross-region)
  - [Zero-Downtime Deployments](#zero-downtime-deployments)
- [Core Services Map](#core-services-map)
- [Infrastructure as Code (IaC) & CI/CD](#infrastructure-as-code-iac--cicd)
- [Security & Compliance Baseline](#security--compliance-baseline)
- [Database HA/DR Patterns](#database-hadr-patterns)
- [Observability](#observability)
- [FinOps & Cost Controls](#finops--cost-controls)
- [Runbooks & Playbooks](#runbooks--playbooks)
- [Sample Case Studies](#sample-case-studies)
- [Checklists](#checklists)
- [Links](#links)
- [Contact](#contact)
## Executive Summary
    Enterprise-grade delivery for mission-critical data platforms on Google Cloud Platform. Focus on **HA/DR**, **security**, **performance**, and **cost-efficiency** via **automation (IaC + GitOps)** and actionable **observability**.

    ## Services & Capabilities
    - **Design & Implementation:** secure landing zone, network, identity, encryption, database services, data integration.
    - **Reliability Engineering:** HA/DR topologies, failover automation, SLOs/SLA tracking, chaos & DR drills.
    - **Performance & Scaling:** workload profiling, indexing/IO, storage tiers, caching, connection resiliency.
    - **Security & Governance:** least privilege IAM, key management, secrets rotation, policy guardrails, audit trails.
    - **FinOps:** rightsizing, reservation/commitment strategies, lifecycle & archival, showback/tagging.
    - **Automation:** Terraform modules, GitOps pipelines, blue/green and zero-downtime deploys.
    - **Operations:** backup/recovery, patching, capacity planning, runbooks, on-call enablement.

    ## Architecture Principles
    - **Secure-by-Default:** private endpoints, no public DB exposure, envelope encryption with managed keys.
    - **Resilient-by-Design:** multi-AZ/AD and cross-region DR with proven RTO/RPO targets.
    - **Automated & Observable:** IaC everywhere, change is reviewed/tested; golden dashboards/alerts-as-code.
    - **Cost-Aware:** scale-to-zero where possible, right storage classes, commitments/discounts.

    ## Reference Architectures

    ### High Availability (In-Region)
    - Zonal failure isolation, multi-AZ/AD deployments for control and data plane.
    - Synchronous replication where supported; async replicas for reads and rapid promotion.
    - Health-based routing and connection retries/backoff at clients.

    ### Disaster Recovery (Cross-Region)
    - Async replication to secondary region; regular **failover drills** with documented runbooks.
    - **Immutable backups** in object storage with lifecycle & replication; **RPO/RTO** objectives tracked on dashboards.

    ### Zero-Downtime Deployments
    - Blue/Green or Rolling with connection draining and feature flags.
    - Schema migrations with expand/contract pattern and **backward compatibility** windows.

    ## Core Services Map
    - **Networking:** VPC (global), Subnets, Firewall Rules, Cloud NAT, Load Balancing, Cloud DNS
- **Identity:** IAM, Workforce/Workload Identity Federation, Organization Policies
- **Encryption:** Cloud KMS, Secret Manager
- **Storage:** Cloud Storage (Standard/Nearline/Coldline/Archive), Persistent Disks, Filestore
- **Observability:** Cloud Logging/Monitoring/Trace, Error Reporting, Profiler
- **Databases:** Cloud SQL (PostgreSQL/MySQL/SQL Server), **AlloyDB**, BigQuery, Datastream
- **Data Platform:** Dataflow (Apache Beam), Dataproc, Pub/Sub, Data Fusion, Composer (Airflow)

    ## Infrastructure as Code (IaC) & CI/CD

    ### Terraform — Provider & Baseline
    ```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_network" "vpc" {
  name = "dbre-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "db" {
  name          = "db-subnet"
  ip_cidr_range = "10.40.1.0/24"
  network       = google_compute_network.vpc.id
  region        = var.region
}

resource "google_sql_database_instance" "pg" {
  name             = "cloudsql-pg"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-custom-2-7680"
    ip_configuration { 
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
    availability_type = "REGIONAL"
  }
}
```

    ### CI/CD with GitHub Actions (OIDC)
    ```yaml
    name: ci-iac
    on:
      push:
        branches: [ main ]
    jobs:
      plan-and-apply:
        runs-on: ubuntu-latest
        permissions:
          id-token: write
          contents: read
        steps:
          - uses: actions/checkout@v4
          - name: Setup Terraform
            uses: hashicorp/setup-terraform@v3
          - name: Auth to Cloud (OIDC)
            run: |
              echo "Authenticate using OIDC token to assume role / workload identity"
          - name: Terraform Init/Plan/Apply
            run: |
              terraform init
              terraform validate
              terraform plan -out tf.plan
              terraform apply -auto-approve tf.plan
    ```

    ### CLI Essentials
    ```bash
# Auth (Workload Identity/ADC)
gcloud auth list

# Cloud SQL instances
gcloud sql instances list

# BigQuery quick check
bq ls --format=prettyjson
```

    ## Security & Compliance Baseline
    - **Identity:** least privilege, workload identities, JIT/PIM for admins; periodic access reviews.
    - **Encryption:** KMS-managed keys (at-rest) + TLS in-transit; **TDE** for databases where applicable.
    - **Secrets:** managed secret stores; short-lived tokens; rotation pipelines.
    - **Network:** private endpoints, service endpoints/peering, **no inbound public DB**; WAF, DDoS/base controls.
    - **Policy:** guardrails (CIS, custom), IaC policy-as-code checks in CI; drift detection and remediation.
    - **Audit:** centralized logs/metrics/traces; immutable storage and retention with least-privilege access.

    ## Database HA/DR Patterns
    - **Cloud SQL (PostgreSQL/MySQL/SQL Server):** Regional HA; cross-region read replicas for DR; PITR backups.
- **AlloyDB:** Primary + read pool with rapid failover; cross-region DR with replicas.
- **BigQuery:** Multi-region datasets with object lifecycle; DR via dataset copies and exports.

    ## Observability
    - **Metrics:** CPU/Memory/Connection/Replication lag; query latency histograms.
- **Logs:** Cloud SQL logs, VPC flow, audit logs; aggregated to Log Buckets with retention.
- **Dashboards:** Uptime checks; SLO/error budget views; Data Studio/Looker Studio for cost + perf.

    ## FinOps & Cost Controls
    - **Committed Use Discounts** and **Sustained Use Discounts**; storage lifecycle (Nearline/Coldline/Archive).
- Budget alerts and cost anomaly detection; labels for showback/chargeback.

    ## Runbooks & Playbooks

    ### Backup & Restore (Generic)
    1. Validate RPO (last successful backup age) and RTO (estimated restore time).
    2. Verify encryption keys and permissions to backup storage.
    3. Restore to **isolated** environment; run consistency checks; compare checksums/row counts.
    4. Document timings; update dashboards and lessons learned.

    ### DR Drill (Generic)
    1. Freeze writes (if needed), force checkpoint/snapshot.
    2. Promote replica or restore from point-in-time.
    3. Redirect traffic (DNS or connection string switch) with retry policies.
    4. Validate SLOs; rollback criteria ready; postmortem & improvements.

    ### Patching (Generic)
    - Stage → Canary → Broad rollout with health gates and automatic rollback on SLO breach.

    ## Sample Case Studies
    - **Cost Down:** Saved ~30% on database TCO combining reservations/commitments, storage class tuning, and query/index improvements.
    - **Resilience Up:** Achieved RTO ≤ 15 min / RPO ≤ 30 sec with cross-region DR and automated failover testing.
    - **Performance Boost:** 40–60% latency reduction via caching, connection pooling, and IO layout tuning.

    ## Checklists

    ### Go-Live
    - [ ] Runbooks ready; on-call rotation set
    - [ ] SLOs, dashboards, and alerts configured
    - [ ] Backups tested; restore time known
    - [ ] Security review passed; secrets rotated
    - [ ] Cost budgets/alerts enabled; tagging policy enforced

    ### Quarterly
    - [ ] DR drill executed and documented
    - [ ] Access recertification completed
    - [ ] Cost/right-sizing review; storage lifecycle tuning
    - [ ] Patch baseline updated; known CVEs reviewed
## Links

- **Multi-Cloud Landing:** `/portfolio-cloud/cloud-portfolio.md`
- **Other Clouds:**  
  - OCI → `/portfolio-cloud/cloud/oci.md`  
  - AWS → `/portfolio-cloud/cloud/aws.md`  
  - Azure → `/portfolio-cloud/cloud/azure.md`  
  - GCP → `/portfolio-cloud/cloud/gcp.md`  

## Contact
Available for remote consulting, migrations, HA/DR readiness reviews, performance tuning, cost optimization, and reliability audits.  
Email: [vandersantanna@gmail.com](mailto:vandersantanna@gmail.com)

```
