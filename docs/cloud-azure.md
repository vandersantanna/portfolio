# Microsoft Azure — Data Platform & DBRE Portfolio

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
    Enterprise-grade delivery for mission-critical data platforms on Microsoft Azure. Focus on **HA/DR**, **security**, **performance**, and **cost-efficiency** via **automation (IaC + GitOps)** and actionable **observability**.

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
    - **Networking:** VNet, Subnets, NSG, Private Endpoints, Application Gateway, Azure DNS
- **Identity:** Azure AD (Entra ID), PIM/JIT, RBAC, Managed Identity
- **Encryption:** Key Vault (keys/secrets/certs), TDE by default for SQL
- **Storage:** Blob (Hot/Cool/Archive), Premium Disks, Files, Backup
- **Observability:** Azure Monitor, Log Analytics, Application Insights, Activity Logs
- **Databases:** Azure SQL (DB/MI), SQL Server on Azure VM, PostgreSQL/MySQL Flexible Server, Cosmos DB
- **Data Platform:** Data Factory, Synapse, Event Hubs, Purview

    ## Infrastructure as Code (IaC) & CI/CD

    ### Terraform — Provider & Baseline
    ```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-cloud-portfolio"
  location = var.location
}

module "vnet" {
  source              = "Azure/vnet/azurerm"
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.30.0.0/16"]
  subnet_prefixes     = ["10.30.1.0/24"]
  subnet_names        = ["db-subnet"]
}

module "sql_mi" {
  source              = "Azure/managed-sql/azurerm"
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = module.vnet.vnet_subnets[0]
  administrator_login = "sqladmin"
  license_type        = "BasePrice"
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
    ```powershell
# Login (OIDC/Device code)
az account show

# List SQL MI
az sql mi list -g rg-cloud-portfolio --output table

# Create a Key Vault secret (example)
az keyvault secret set --vault-name kv-portfolio --name "db-password" --value "REDACTED"
```

    ## Security & Compliance Baseline
    - **Identity:** least privilege, workload identities, JIT/PIM for admins; periodic access reviews.
    - **Encryption:** KMS-managed keys (at-rest) + TLS in-transit; **TDE** for databases where applicable.
    - **Secrets:** managed secret stores; short-lived tokens; rotation pipelines.
    - **Network:** private endpoints, service endpoints/peering, **no inbound public DB**; WAF, DDoS/base controls.
    - **Policy:** guardrails (CIS, custom), IaC policy-as-code checks in CI; drift detection and remediation.
    - **Audit:** centralized logs/metrics/traces; immutable storage and retention with least-privilege access.

    ## Database HA/DR Patterns
    - **Azure SQL MI:** Zone-redundant deployments; auto-failover groups for DR; private endpoints.
- **SQL Server on VM:** Always On AG across zones; Azure Backup; SRM for DR where needed.
- **PostgreSQL/MySQL Flexible Server:** HA zone-redundant; PITR backups; read replicas for scale.

    ## Observability
    - **Metrics/Logs:** Azure Monitor + Log Analytics queries (KQL) for DTU/vCore, waits, deadlocks, IO latency.
- **Dashboards:** Workbooks for RTO/RPO indicators, backup freshness, error budgets.
- **Alerts:** Action Groups to Teams/Email/Webhooks; autoscale and budget alerts.

    ## FinOps & Cost Controls
    - **Reservations** for vCores/MI; Azure Hybrid Benefit; storage tiering and auto-pause where applicable.
- Azure Cost Management & budgets; tagging strategy (env, app, owner, cost-center).

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
