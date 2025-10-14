```markdown
# Oracle Cloud Infrastructure (OCI) — Data Platform & DBRE Portfolio

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
    Enterprise-grade delivery for mission-critical data platforms on Oracle Cloud Infrastructure. Focus on **HA/DR**, **security**, **performance**, and **cost-efficiency** via **automation (IaC + GitOps)** and actionable **observability**.

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
    - **Networking:** VCN, Subnets (Private), NSG, DRG, Service Gateway, Load Balancer
- **Identity:** IAM (Compartments/Policies/Dynamic Groups), Cloud Guard, Security Zones
- **Encryption:** OCI Vault (Keys/Secrets), TDE for DBs
- **Storage:** Object Storage (Standard/IA/Archive), Block Volumes, File Storage (NFS)
- **Observability:** OCI Monitoring/Logging/Events/Alarms, Logging Analytics
- **Databases:** Oracle Autonomous (ATP/ADW), Exadata Cloud Service, DB Systems (19c), MySQL HeatWave, OKE (for apps)
- **Data Integration:** GoldenGate on OCI, Data Integration, Data Flow (Spark), Streaming

    ## Infrastructure as Code (IaC) & CI/CD

    ### Terraform — Provider & Baseline
    ```hcl
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 6.0"
    }
  }
}

provider "oci" {
  auth = "InstancePrincipal" # or API keys / OIDC via workload identity
  region = var.region
}

module "network" {
  source = "github.com/org/oci-network-module"
  compartment_ocid = var.compartment_ocid
  vcn_cidr = "10.10.0.0/16"
  subnets = { private_db = "10.10.10.0/24" }
}

module "db_19c" {
  source = "github.com/org/oci-db19c-module"
  compartment_ocid = var.compartment_ocid
  subnet_id        = module.network.subnets["private_db"].id
  shape            = "VM.Standard3.Flex"
  storage_gb       = 1024
  tde_enabled      = true
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
# Authenticate (instance principal or config)
oci iam compartment list

# List DB Systems
oci db system list --compartment-id $COMP_OCID

# Create alarm example
oci monitoring alarm create --compartment-id $COMP_OCID   --display-name "High CPU DB" --query-text "CpuUtilization[1m]{resourceId = 'ocid1.dbnode..*'}.mean() > 80"   --severity CRITICAL --is-enabled true
```

    ## Security & Compliance Baseline
    - **Identity:** least privilege, workload identities, JIT/PIM for admins; periodic access reviews.
    - **Encryption:** KMS-managed keys (at-rest) + TLS in-transit; **TDE** for databases where applicable.
    - **Secrets:** managed secret stores; short-lived tokens; rotation pipelines.
    - **Network:** private endpoints, service endpoints/peering, **no inbound public DB**; WAF, DDoS/base controls.
    - **Policy:** guardrails (CIS, custom), IaC policy-as-code checks in CI; drift detection and remediation.
    - **Audit:** centralized logs/metrics/traces; immutable storage and retention with least-privilege access.

    ## Database HA/DR Patterns
    - **Oracle 19c on Exadata/DB Systems:** Primary in AD1 with **Data Guard** to AD2/region; **FSFO** for automatic failover.
- **Autonomous (ATP/ADW):** Cross-region **ADG** for DR; Data Safe for security; APEX/ORDS private access.
- **MySQL HeatWave:** Multi-AZ HA; backups to Object Storage; promotion runbooks.

    ## Observability
    - **Metrics:** CPU, IOPS, session count, wait events; **DB time** and **redo generation** for Oracle.
- **Logs:** DB alert logs, listener logs, OS syslog; route to Logging Analytics with saved searches.
- **Dashboards:** RTO/RPO gauges (derived from replication lag + restore tests), error budgets, cost per env.

    ## FinOps & Cost Controls
    - Use **Flex shapes** for right-sizing; monitor storage growth and tier cold backups to **Archive**.
- **Commitment contracts** for sustained usage; enforce **tagging** for showback; alarms on spend anomalies.

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
