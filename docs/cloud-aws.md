# Amazon Web Services (AWS) — Data Platform & DBRE Portfolio

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
    Enterprise-grade delivery for mission-critical data platforms on Amazon Web Services. Focus on **HA/DR**, **security**, **performance**, and **cost-efficiency** via **automation (IaC + GitOps)** and actionable **observability**.

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
    - **Networking:** VPC, Private Subnets, NAT, Transit Gateway, PrivateLink, ALB/NLB, Route 53
- **Identity:** IAM, Organizations/SCPs, IAM Roles Anywhere, AWS SSO
- **Encryption:** KMS (CMKs), Secrets Manager, Parameter Store
- **Storage:** S3 (Standard/IA/Glacier), EBS, EFS, FSx
- **Observability:** CloudWatch (metrics/logs/alarms), CloudTrail, Config, X-Ray
- **Databases:** RDS (Oracle, SQL Server, PostgreSQL, MySQL), **Aurora**, DynamoDB, DMS
- **Data Analytics:** Glue, Lake Formation, EMR, Redshift, MSK/Kinesis

    ## Infrastructure as Code (IaC) & CI/CD

    ### Terraform — Provider & Baseline
    ```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "dbre-vpc"
  cidr   = "10.20.0.0/16"
  azs    = ["${var.region}a","${var.region}b"]
  private_subnets = ["10.20.1.0/24","10.20.2.0/24"]
  enable_nat_gateway = true
}

module "aurora_pg" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  name    = "aurora-pg"
  engine  = "aurora-postgresql"
  subnets = module.vpc.private_subnets
  vpc_id  = module.vpc.vpc_id
  create_db_subnet_group = true
  storage_encrypted = true
  kms_key_id = aws_kms_key.this.arn
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
# Assume role with SSO/OIDC (example placeholder)
aws sts get-caller-identity

# RDS snapshots
aws rds describe-db-snapshots --db-instance-identifier prod-sql

# CloudWatch metric example (average CPU)
aws cloudwatch get-metric-statistics   --namespace AWS/RDS --metric-name CPUUtilization   --dimensions Name=DBInstanceIdentifier,Value=prod-sql   --statistics Average --period 300   --start-time $(date -u -d '-1 hour' +%FT%TZ)   --end-time $(date -u +%FT%TZ)
```

    ## Security & Compliance Baseline
    - **Identity:** least privilege, workload identities, JIT/PIM for admins; periodic access reviews.
    - **Encryption:** KMS-managed keys (at-rest) + TLS in-transit; **TDE** for databases where applicable.
    - **Secrets:** managed secret stores; short-lived tokens; rotation pipelines.
    - **Network:** private endpoints, service endpoints/peering, **no inbound public DB**; WAF, DDoS/base controls.
    - **Policy:** guardrails (CIS, custom), IaC policy-as-code checks in CI; drift detection and remediation.
    - **Audit:** centralized logs/metrics/traces; immutable storage and retention with least-privilege access.

    ## Database HA/DR Patterns
    - **Aurora PostgreSQL/MySQL:** Multi-AZ with reader endpoints; cross-region replicas for DR; automated failover.
- **RDS Oracle/SQL Server:** Multi-AZ with synchronous standby; cross-region read replicas or DMS for DR.
- **DynamoDB:** Global tables for multi-region active-active (where applicable).

    ## Observability
    - **Metrics:** CPU/Memory/IOPS, buffer/cache hit ratio, replication lag, deadlocks.
- **Logs:** RDS/Aurora error logs to CloudWatch Logs; VPC Flow Logs for network diagnostics.
- **Dashboards:** SLOs with error budgets, storage growth, top slow queries; anomaly detection alarms.

    ## FinOps & Cost Controls
    - **Savings Plans/Reserved Instances** for steady workloads; right-size instances/storage.
- S3 lifecycle to Glacier/Deep Archive; **CUDOS/Cost Explorer** dashboards; tag-based cost allocation.

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
