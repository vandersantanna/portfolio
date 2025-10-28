<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>


# Azure SQL – Professional Portfolio Guide

> Objective: Demonstrate end-to-end, production-grade mastery of Azure SQL (Azure SQL Database, Azure SQL Managed Instance, and SQL Server on Azure VMs) with architecture, security, reliability (DBRE/SRE), automation, and CI/CD artifacts you can copy into real environments.

---

## Table of Contents

- [1. Executive Summary & Positioning](#1-executive-summary--positioning)
- [2. Azure SQL Overview & Decision Guide](#2-azure-sql-overview--decision-guide)
- [3. Reference Architecture (Landing Zone First)](#3-reference-architecture-landing-zone-first)
- [4. Networking & Connectivity](#4-networking--connectivity)
- [5. Security & Data Protection](#5-security--data-protection)
- [6. Business Continuity (HA/DR) & Backup Strategy](#6-business-continuity-hadr--backup-strategy)
- [7. Performance, Scalability & Capacity Planning](#7-performance-scalability--capacity-planning)
- [8. Observability & Operations (DBRE/SRE)](#8-observability--operations-dbresre)
- [9. Cost Management & FinOps](#9-cost-management--finops)
- [10. Data Lifecycle & Migration](#10-data-lifecycle--migration)
- [11. Schema, Change & Release Management](#11-schema-change--release-management)
- [12. Developer Experience & Local Productivity](#12-developer-experience--local-productivity)
- [13. Infrastructure as Code (IaC)](#13-infrastructure-as-code-iac)
- [14. Automation & Platform Engineering](#14-automation--platform-engineering)
- [15. Compliance, Governance & Audit Readiness](#15-compliance-governance--audit-readiness)
- [16. Repo Structure, Artifacts & Documentation](#16-repo-structure-artifacts--documentation)
- [17. Patterns, Anti-Patterns & Reference Use Cases](#17-patterns-anti-patterns--reference-use-cases)
- [18. Troubleshooting Playbooks](#18-troubleshooting-playbooks)
- [19. SQL Server on Azure Virtual Machines (IaaS Focus)](#19-sql-server-on-azure-virtual-machines-iaas-focus)
- [20. CI/CD Pipelines](#20-cicd-pipelines)
  - [20.1 GitHub Actions (OIDC, Bicep, Terraform)](#201-github-actions-oidc-bicep-terraform)
  - [20.2 Azure DevOps (Multi-Stage)](#202-azure-devops-multi-stage)
  - [20.3 Database Migrations: DACPAC & Flyway](#203-database-migrations-dacpac--flyway)
- [21. Application Connectivity & Resilience](#21-application-connectivity--resilience)
  - [21.1 Connection Strings & AAD](#211-connection-strings--aad)
  - [21.2 Robust Retry Patterns](#212-robust-retry-patterns)
  - [21.3 Sample Snippets (.NET, Python, Node.js, Java)](#213-sample-snippets-net-python-nodejs-java)
- [22. Performance Labs & Benchmarks](#22-performance-labs--benchmarks)
- [23. Roadmap & Continuous Improvement](#23-roadmap--continuous-improvement)
- [24. Appendices](#24-appendices)
  - [A. Azure CLI & PowerShell Cheat Sheet](#a-azure-cli--powershell-cheat-sheet)
  - [B. KQL Query Library](#b-kql-query-library)
  - [C. Naming Conventions, Tags & Labels](#c-naming-conventions-tags--labels)
  - [D. Operational Checklists](#d-operational-checklists)
  - [E. SLA/SLO Mapping & Calculator](#e-slaslo-mapping--calculator)
  - [F. Glossary & Acronyms](#f-glossary--acronyms)

---

## 1. Executive Summary & Positioning

This guide is a portfolio-ready blueprint showing how to plan, build, secure, operate, and continuously improve Azure SQL platforms. It includes repeatable IaC modules (Bicep/Terraform), CI/CD pipelines (GitHub Actions/Azure DevOps), security baselines, SRE playbooks, cost controls, and code samples for application connectivity and resilience.

Target audience: DBAs/DBREs, Platform/SRE teams, Cloud Architects, and hiring managers seeking hands-on aptitude and operational rigor.

Deliverables:
- Ready-to-run IaC modules and pipelines.
- Operational playbooks and KQL libraries.
- Security/BCDR baselines.
- App connectivity patterns with AAD, MI, Private Endpoints.
- Reusable checklists and documentation templates.

---

## 2. Azure SQL Overview & Decision Guide

Choices:
- Azure SQL Database (PaaS): Single/Elastic Pool/Hyperscale; minimal ops, fast provisioning, serverless options.
- Azure SQL Managed Instance (PaaS): High compatibility, SQL Agent, cross-db queries, linked servers.
- SQL Server on Azure VM (IaaS): Full control; required for niche features/OS; higher ops burden.

Workload fit (summary):
- Rapid modernization with minimal admin → SQL DB (or Hyperscale if very large).
- “Lift-but-modernize” with SQL Agent/compat needs → Managed Instance.
- Complex HADR topologies, 3rd-party agents, OS-level deps → SQL on Azure VM.

Environments: Dev/Test/Stage/Prod split by subscription or resource group, with isolated networking and policy guardrails.

---

## 3. Reference Architecture (Landing Zone First)

Landing zone components: Management Groups, Policies/Initiatives, RBAC, Azure Monitor/Defender, Key Vault, centralized networking (Hub-and-Spoke), private DNS, and CI/CD identity setup.

ASCII view:

    [Mgmt Group & Policies] --> [LZ Subscriptions]
           |                          |
           v                          v
       [Monitor]                  [Key Vault]
              \                    /
               \                  /
                [Hub VNet]----[Spoke VNet-App]
                     |         [Spoke VNet-Data]
                     |                 |
                     v                 v
                  [PE: SQL/KV/Storage][Azure SQL (DB/MI)]

---

## 4. Networking & Connectivity

- Private Endpoints for SQL Database/MI + Private DNS Zones.
- VNet injection for MI; NSGs/UDRs to segment traffic; Azure Firewall or NVA.
- Hybrid: ExpressRoute/VPN with DNS forwarders. Avoid public endpoints in Prod.

Azure CLI – Private Endpoint (SQL DB):

    az network private-endpoint create \
      -g rg-data-prod -n pe-sqldb-prod \
      --vnet-name vnet-data --subnet snet-data \
      --private-connection-resource-id "/subscriptions/<sub>/resourceGroups/rg-data-prod/providers/Microsoft.Sql/servers/sql-svr-prod" \
      --group-id sqlServer \
      --connection-name pe-sql-conn

    az network private-dns record-set a add-record \
      -g rg-data-prod -z "privatelink.database.windows.net" -n sql-svr-prod \
      -a 10.0.20.5

---

## 5. Security & Data Protection

- Encryption: TDE everywhere; Customer-Managed Keys (CMK) in Key Vault for sovereignty.
- Access: Microsoft Entra ID, least privilege RBAC; prefer AAD-only auth where possible.
- Data security: Always Encrypted, Dynamic Data Masking, Row-Level Security (RLS).
- Monitoring: SQL Auditing to Log Analytics/Storage; Microsoft Defender for SQL.

T-SQL – Row-Level Security (RLS):

    CREATE SCHEMA sec;
    GO
    CREATE FUNCTION sec.fnTenantPredicate(@TenantId AS INT)
    RETURNS TABLE
    WITH SCHEMABINDING
    AS
    RETURN SELECT 1 AS fn_result
    WHERE @TenantId = CAST(SESSION_CONTEXT(N'TenantId') AS INT);
    GO

    CREATE SECURITY POLICY sec.TenantPolicy
    ADD FILTER PREDICATE sec.fnTenantPredicate(TenantId) ON dbo.Orders
    WITH (STATE = ON);
    GO

    EXEC sys.sp_set_session_context @key=N'TenantId', @value=42;
    SELECT TOP 5 * FROM dbo.Orders;

T-SQL – Dynamic Data Masking:

    ALTER TABLE dbo.Customers
    ALTER COLUMN Email ADD MASKED WITH (FUNCTION='email()');

Notes:
- TDE is ON by default for new Azure SQL DBs; enforce CMK at server level.
- Rotate keys; restrict KV access to CI/CD and break-glass only.

---

## 6. Business Continuity (HA/DR) & Backup Strategy

- HA: Zone redundancy; Auto-Failover Groups (readers in secondary); align to SLA.
- DR: Geo-replication to paired region; DR runbooks with periodic failover drills.
- Backups: PITR/LTR validation; restore tests into sandbox; document RTO/RPO.

CLI – Failover Group (SQL DB):

    az sql failover-group create \
      -g rg-data-prod --name fog-sql-prod \
      --server sql-svr-prod --partner-server sql-svr-dr \
      --add-db dbapp1 dbapp2 --failover-policy Automatic

---

## 7. Performance, Scalability & Capacity Planning

- Service model: vCore vs DTU; provisioned vs serverless; Hyperscale for very large OLTP.
- Elastic pools for multi-tenant cost efficiency.
- Query Store required for baselines and regression triage. Automatic Tuning judiciously.
- Benchmarking: Use HammerDB/k6; track baselines and headroom.

T-SQL – Query Store + Automatic Tuning:

    ALTER DATABASE dbapp1 SET QUERY_STORE = ON;
    ALTER DATABASE dbapp1 SET QUERY_STORE (INTERVAL_LENGTH_MINUTES = 10, MAX_STORAGE_SIZE_MB = 1024);
    ALTER DATABASE dbapp1 SET AUTOMATIC_TUNING (FORCE_LAST_GOOD_PLAN = ON);

---

## 8. Observability & Operations (DBRE/SRE)

- Centralize metrics/logs in Log Analytics; alert on SLO-aligned indicators.
- Build Workbooks for performance and security posture.
- Blameless post-incident reviews; track action items.

KQL – DTU/CPU Hot Databases:

    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.SQL"
    | where Category == "SQLInsights"
    | summarize avgCpu=avg(avg_cpu_percent) by Resource, bin(TimeGenerated, 5m)
    | top 10 by avgCpu desc

KQL – Potential Locks/Blocking Signal:

    AzureDiagnostics
    | where Category in ("SQLSecurityAuditEvents","SQLInsights")
    | where wait_type_s has "LCK_" or additional_information_s has "deadlock"
    | summarize count() by Resource, bin(TimeGenerated, 5m)

---

## 9. Cost Management & FinOps

- Levers: Reservations, Savings Plans, Azure Hybrid Benefit; right-sizing tiers.
- Serverless auto-pause (where applicable) and elastic pools to control idle cost.
- Budgets/alerts; monthly cost reviews with owners; tag rigor for showback/chargeback.

---

## 10. Data Lifecycle & Migration

- Assess compatibility; plan cutover (big-bang vs phased).
- Use DMS (online where possible), BACPAC/DACPAC, or backup/restore for MI/VM.
- Validate data integrity and performance post-cutover.

SqlPackage – Extract/Publish:

    sqlpackage /Action:Extract /SourceConnectionString:"Server=src;Database=dbapp1;User Id=...;Password=..." /TargetFile:dbapp1.dacpac
    sqlpackage /Action:Publish /TargetConnectionString:"Server=tcp:sql-svr-prod.database.windows.net,1433;Database=dbapp1;Authentication=ActiveDirectoryIntegrated" /SourceFile:dbapp1.dacpac /p:BlockOnPossibleDataLoss=false

---

## 11. Schema, Change & Release Management

- Version database with DACPAC (state-based) or Flyway (migration-based).
- Backward-compatible changes; feature flags in app layer.
- Change windows + approval gates in pipelines.

Flyway – flyway.conf (snippet):

    flyway.url=jdbc:sqlserver://sql-svr-prod.database.windows.net:1433;databaseName=dbapp1;encrypt=true;trustServerCertificate=false
    flyway.user=${FLYWAY_USER}
    flyway.password=${FLYWAY_PASSWORD}
    flyway.locations=filesystem:./db/migrations
    flyway.baselineOnMigrate=true

Flyway – V1__init.sql (example):

    CREATE TABLE dbo.Customers(
      CustomerId INT IDENTITY PRIMARY KEY,
      Name NVARCHAR(200) NOT NULL,
      Email NVARCHAR(320) NOT NULL UNIQUE,
      TenantId INT NOT NULL
    );
    CREATE INDEX IX_Customers_TenantId ON dbo.Customers(TenantId);

---

## 12. Developer Experience & Local Productivity

- Tools: SSMS, Azure Data Studio, VS Code SQL extensions, SqlPackage, SqlCmd.
- Dev containers seeded with synthetic/masked data; repeatable local env via docker-compose.

docker-compose (local dev with SQL Server):

    version: "3.9"
    services:
      mssql:
        image: mcr.microsoft.com/mssql/server:2022-latest
        environment:
          - ACCEPT_EULA=Y
          - SA_PASSWORD=YourStrong!Passw0rd
        ports:
          - "1433:1433"
        volumes:
          - mssql_data:/var/opt/mssql
    volumes:
      mssql_data: {}

---

## 13. Infrastructure as Code (IaC)

### 13.1 Bicep – Azure SQL Database + Private Endpoint (simplified)

    param location string = resourceGroup().location
    param sqlServerName string
    param sqlAdminLogin string
    @secure()
    param sqlAdminPassword string
    param dbName string = 'dbapp1'
    param subnetId string

    resource sqlServer 'Microsoft.Sql/servers@2022-05-01-preview' = {
      name: sqlServerName
      location: location
      properties: {
        administratorLogin: sqlAdminLogin
        administratorLoginPassword: sqlAdminPassword
        minimalTlsVersion: '1.2'
        publicNetworkAccess: 'Disabled'
      }
    }

    resource database 'Microsoft.Sql/servers/databases@2022-02-01-preview' = {
      name: '${sqlServer.name}/${dbName}'
      properties: {
        collation: 'SQL_Latin1_General_CP1_CI_AS'
        requestedServiceObjectiveName: 'GP_Gen5_2'
      }
    }

    resource pe 'Microsoft.Network/privateEndpoints@2022-09-01' = {
      name: 'pe-sql-${sqlServer.name}'
      location: location
      properties: {
        subnet: { id: subnetId }
        privateLinkServiceConnections: [
          {
            name: 'pls-sql'
            properties: {
              privateLinkServiceId: sqlServer.id
              groupIds: [ 'sqlServer' ]
            }
          }
        ]
      }
    }

### 13.2 Terraform – Azure SQL Server + DB + Private Endpoint (simplified)

    terraform {
      required_version = ">= 1.6"
      required_providers {
        azurerm = { source = "hashicorp/azurerm", version = ">= 3.80.0" }
      }
    }

    provider "azurerm" { features {} }

    variable "rg_name" {}
    variable "location" { default = "brazilsouth" }
    variable "sql_server_name" {}
    variable "admin_login" {}
    variable "admin_password" { sensitive = true }
    variable "subnet_id" {}
    variable "db_name" { default = "dbapp1" }

    resource "azurerm_mssql_server" "this" {
      name                          = var.sql_server_name
      resource_group_name           = var.rg_name
      location                      = var.location
      version                       = "12.0"
      administrator_login           = var.admin_login
      administrator_login_password  = var.admin_password
      public_network_access_enabled = false
      minimum_tls_version           = "1.2"
    }

    resource "azurerm_mssql_database" "db" {
      name           = var.db_name
      server_id      = azurerm_mssql_server.this.id
      sku_name       = "GP_Gen5_2"
      collation      = "SQL_Latin1_General_CP1_CI_AS"
      zone_redundant = true
    }

    resource "azurerm_private_endpoint" "pe" {
      name                = "pe-${var.sql_server_name}"
      location            = var.location
      resource_group_name = var.rg_name
      subnet_id           = var.subnet_id

      private_service_connection {
        name                           = "psc-sql"
        private_connection_resource_id = azurerm_mssql_server.this.id
        is_manual_connection           = false
        subresource_names              = ["sqlServer"]
      }
    }

---

## 14. Automation & Platform Engineering

- Day-2: statistics/index maintenance, job orchestration (Azure Automation, Functions).
- Golden blueprints: consistent modules + policies enforced via pipelines.

PowerShell – Rotate SQL Server Admin Password (Key Vault secret):

    $secret = Get-AzKeyVaultSecret -VaultName "kv-prod" -Name "sql-admin-pass"
    $plain  = [System.Text.Encoding]::UTF8.GetString($secret.SecretValue)
    Set-AzSqlServer -ResourceGroupName "rg-data-prod" -ServerName "sql-svr-prod" `
      -SqlAdministratorPassword (ConvertTo-SecureString $plain -AsPlainText -Force)

Azure Function (Timer) – Stats Update (T-SQL):

    UPDATE STATISTICS dbo.Customers WITH FULLSCAN;

---

## 15. Compliance, Governance & Audit Readiness

- Map controls (ISO/SOC/HIPAA/GDPR) to platform capabilities.
- Evidence packs: policies, screenshots, KQL exports, audit logs, pipeline histories.
- Data retention & eDiscovery with legal hold.

---

## 16. Repo Structure, Artifacts & Documentation

Recommended structure:

    /azure-sql-portfolio
      /iac
        /bicep
        /terraform
      /pipelines
        /github-actions
        /azure-devops
      /db
        /dacpac
        /flyway
          /migrations
      /ops
        /runbooks
        /kql
      /docs
        architecture.md
        sre-playbooks.md
        security-baseline.md
      CODEOWNERS
      CONTRIBUTING.md
      ADRs/

Notes:
- Use ADRs for key decisions; CODEOWNERS for critical folders; CONTRIBUTING.md with conventions and commit policy.

---

## 17. Patterns, Anti-Patterns & Reference Use Cases

Patterns:
- Multi-tenant SaaS → Elastic Pools + RLS per tenant + per-tenant workload caps.
- Read-intensive → Auto-Failover Groups with read-only listener for analytics jobs.
- High-growth → Hyperscale with tier upgrades via pipelines.

Anti-patterns:
- Cross-db dependencies on SQL DB; over-indexing; hot partition keys; public endpoints in Prod.

---

## 18. Troubleshooting Playbooks

Connectivity:
- Verify DNS resolution to privatelink FQDN from app subnets; confirm PE NIC/IP.
- Check NSGs/UDRs; ensure no asymmetrical routing; inspect firewall logs.

Performance regression:
- Query Store compare; force last good plan; update stats; verify parameter sniffing patterns.

Blocking/deadlocks:
- Capture with Extended Events (MI/VM) or telemetry; fix access patterns and indexing; consider RCSI when appropriate.

Failover issues:
- Validate secondary readiness; login/users/permissions parity (MI/VM); test app retry logic.

T-SQL – Read Regressed Queries (example):

    SELECT TOP 10 qsrs.runtime_stats_id, qsq.query_sql_text, rs.avg_duration
    FROM sys.query_store_runtime_stats rs
    JOIN sys.query_store_plan qsp ON rs.plan_id = qsp.plan_id
    JOIN sys.query_store_query qsq ON qsp.query_id = qsq.query_id
    JOIN sys.query_store_runtime_stats_interval qsrs ON rs.runtime_stats_interval_id = qsrs.runtime_stats_interval_id
    ORDER BY rs.avg_duration DESC;

---

## 19. SQL Server on Azure Virtual Machines (IaaS Focus)

When:
- OS dependencies, legacy features, 3rd-party agents, custom HADR.

HADR:
- Always On AGs or FCI; proper storage layout; Accelerated Networking; Azure Load Balancer considerations.

Ops:
- Patching cadence, Defender integration, Backup to URL, Azure Monitor agent.

Storage layout (guideline):
- Separate disks for data, log, tempdb; premium SSD; enable read cache on data, none on log.

---

## 20. CI/CD Pipelines

### 20.1 GitHub Actions (OIDC, Bicep, Terraform)

    name: deploy-azure-sql
    on:
      push:
        branches: [ "main" ]
      workflow_dispatch:
    permissions:
      id-token: write
      contents: read

    jobs:
      iac:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Azure Login (OIDC)
            uses: azure/login@v2
            with:
              client-id: ${{ secrets.AZURE_CLIENT_ID }}
              tenant-id: ${{ secrets.AZURE_TENANT_ID }}
              subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

          - name: Deploy Bicep (group)
            run: |
              az deployment group create \
                -g rg-data-prod \
                -f iac/bicep/sql.bicep \
                -p sqlServerName=sql-svr-prod sqlAdminLogin=sqladmin sqlAdminPassword=${{ secrets.SQL_ADMIN_PASS }}

          - name: Terraform Init/Plan/Apply
            working-directory: iac/terraform
            run: |
              terraform init -upgrade
              terraform plan -out=tfplan
              terraform apply -auto-approve tfplan

### 20.2 Azure DevOps (Multi-Stage)

    trigger:
    - main

    stages:
    - stage: Build
      jobs:
      - job: BuildDacpac
        pool: { vmImage: 'windows-latest' }
        steps:
        - task: VSBuild@1
          inputs:
            solution: 'db/dacpac/DbProj.sln'
        - publish: db/dacpac/bin/Release/DbProj.dacpac
          artifact: dacpac

    - stage: Deploy
      dependsOn: Build
      jobs:
      - deployment: DeployToProd
        environment: prod
        strategy:
          runOnce:
            deploy:
              steps:
              - download: current
                artifact: dacpac
              - task: SqlAzureDacpacDeployment@1
                inputs:
                  azureSubscription: 'spn-oidc'
                  AuthenticationType: 'servicePrincipal'
                  ServerName: 'sql-svr-prod.database.windows.net'
                  DatabaseName: 'dbapp1'
                  DeployType: 'DacpacTask'
                  DacpacFile: '$(Pipeline.Workspace)/dacpac/DbProj.dacpac'
                  AdditionalArguments: '/p:BlockOnPossibleDataLoss=false'

### 20.3 Database Migrations: DACPAC & Flyway

GitHub Actions – Flyway Migrate:

    name: flyway-migrate
    on: { workflow_dispatch: {} }
    jobs:
      migrate:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Flyway CLI
            run: |
              curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.18.0/flyway-commandline-10.18.0-linux-x64.tar.gz | tar xz
              sudo ln -s $PWD/flyway-10.18.0/flyway /usr/local/bin/flyway
          - name: Migrate
            env:
              FLYWAY_USER: ${{ secrets.DB_USER }}
              FLYWAY_PASSWORD: ${{ secrets.DB_PASS }}
            run: |
              flyway -configFiles=db/flyway/flyway.conf migrate

---

## 21. Application Connectivity & Resilience

### 21.1 Connection Strings & AAD

- Prefer AAD tokens (Managed Identity/Workload Identity) over SQL logins.
- Enforce Encrypt=True; validate server certificates.

### 21.2 Robust Retry Patterns

- Exponential backoff + jitter for transient errors (throttling, failovers).
- Keep connections short-lived where appropriate; pool with health checks.

### 21.3 Sample Snippets (.NET, Python, Node.js, Java)

.NET (C#) – AAD Token with DefaultAzureCredential:

    using Azure.Identity;
    using Microsoft.Data.SqlClient;
    var conn = new SqlConnection("Server=tcp:sql-svr-prod.database.windows.net,1433;Database=dbapp1;Encrypt=True;TrustServerCertificate=False;");
    var credential = new DefaultAzureCredential();
    var token = credential.GetToken(new Azure.Core.TokenRequestContext(new[] { "https://database.windows.net/.default" }));
    conn.AccessToken = token.Token;
    await conn.OpenAsync();
    // Execute queries...

Python – AAD Token with azure-identity + pyodbc:

    import struct, pyodbc
    from azure.identity import DefaultAzureCredential

    cred = DefaultAzureCredential()
    scope = "https://database.windows.net/.default"
    token = cred.get_token(scope).token
    exptoken = b"%s" % token.encode("utf-16-le")
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

    conn = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};Server=tcp:sql-svr-prod.database.windows.net,1433;Database=dbapp1;Encrypt=yes;TrustServerCertificate=no;",
        attrs_before = { 1256: tokenstruct } # SQL_COPT_SS_ACCESS_TOKEN
    )
    cur = conn.cursor()
    cur.execute("SELECT TOP 1 @@VERSION")
    print(cur.fetchone())

Node.js – mssql with AAD access token:

    const sql = require('mssql');
    const { DefaultAzureCredential } = require('@azure/identity');

    const credential = new DefaultAzureCredential();
    async function getToken() {
      const { token } = await credential.getToken('https://database.windows.net/.default');
      return token;
    }

    (async () => {
      const accessToken = await getToken();
      const pool = await sql.connect({
        server: 'sql-svr-prod.database.windows.net',
        database: 'dbapp1',
        options: { encrypt: true, trustServerCertificate: false },
        authentication: {
          type: 'azure-active-directory-access-token',
          options: { token: accessToken }
        }
      });
      const result = await pool.request().query('SELECT TOP 1 GETUTCDATE() AS now');
      console.log(result.recordset[0]);
    })();

Java – JDBC with Managed Identity (connection string):

    jdbc:sqlserver://sql-svr-prod.database.windows.net:1433;database=dbapp1;encrypt=true;authentication=ActiveDirectoryManagedIdentity

---

## 22. Performance Labs & Benchmarks

- Define scenarios (read/write mix), target SLOs, and saturation thresholds.
- Tools: HammerDB, k6 (via API gateway against data-access layer).
- Store results (CSV/JSON) + graphs in Workbooks/Power BI; compare against baselines.

---

## 23. Roadmap & Continuous Improvement

- Quarterly reviews: architecture fitness, SLOs, security posture, cost.
- Backlog themes: security hardening, observability depth, cost optimizations, automated DR drills.
- Retire tech debt; document decisions via ADRs.

---

## 24. Appendices

### A. Azure CLI & PowerShell Cheat Sheet

Azure CLI:

    az login
    az account set --subscription "<SUB_ID>"
    az group create -n rg-data-prod -l brazilsouth
    az sql server create -g rg-data-prod -n sql-svr-prod -l brazilsouth -u sqladmin -p 'Str0ngP@ss' --public-network-access Disabled
    az sql db create -g rg-data-prod -s sql-svr-prod -n dbapp1 --service-objective GP_Gen5_2

PowerShell:

    Connect-AzAccount
    Set-AzContext -Subscription "<SUB_ID>"
    Set-AzKeyVaultSecret -VaultName kv-prod -Name "sql-admin-pass" -SecretValue (ConvertTo-SecureString "Str0ngP@ss" -AsPlainText -Force)
    Set-AzSecurityPricing -Name SqlServers -PricingTier Standard

### B. KQL Query Library

Top queries by duration:

    AzureDiagnostics
    | where Category == "SQLInsights"
    | summarize avgDur=avg(duration_s), p95Dur=percentile(duration_s,95) by statement_s, bin(TimeGenerated, 15m)
    | top 20 by p95Dur desc

Deadlocks (sample pattern):

    AzureDiagnostics
    | where Category == "SQLSecurityAuditEvents"
    | where action_id_s == "DL" or additional_information_s has "deadlock"
    | summarize cnt=count() by bin(TimeGenerated, 15m), Resource

Logins failed:

    AzureDiagnostics
    | where Category in ("SQLSecurityAuditEvents","SQLSecurityAuditEventsV2")
    | where action_id_s in ("LGIF","LGIF_EXT")
    | summarize fails=count() by bin(TimeGenerated, 15m), client_ip_s

### C. Naming Conventions, Tags & Labels

Naming examples:
- Resource Group: rg-<domain>-<env> → rg-data-prod
- SQL Server: sql-<role>-<env> → sql-svr-prod
- Managed Instance: sql-mi-<env> → sql-mi-prod
- Private Endpoint: pe-<service>-<env> → pe-sql-prod

Tags:

    owner=platform-team
    env=prod
    costCenter=FIN-001
    dataClass=confidential
    app=dbapp

### D. Operational Checklists

Go-Live (excerpt):
- [ ] Private Endpoints/DNS validated from app subnets
- [ ] AAD-only auth enforced (where supported)
- [ ] TDE + CMK verified; Defender enabled
- [ ] Baselines captured; alerts configured on SLOs
- [ ] DR tested; RTO/RPO documented

DR Drill (excerpt):
- [ ] Initiate failover (FOG/Geo-rep) during window
- [ ] Validate app connectivity and performance
- [ ] Switch back; capture metrics deltas
- [ ] Document findings and actions

### E. SLA/SLO Mapping & Calculator

Example SLOs:
- Availability (monthly): ≥ 99.95%
- P95 Query Latency: ≤ 200 ms
- RPO: ≤ 5 min (critical), ≤ 15 min (standard)
- RTO: ≤ 15 min (critical), ≤ 60 min (standard)

Error budget (monthly):

    error_budget_minutes = minutes_in_month * (1 - availability_target)

### F. Glossary & Acronyms

- AAD: Microsoft Entra ID (Azure AD)
- AG: Availability Group
- CMK: Customer-Managed Key
- DTU/vCore: Purchasing models for Azure SQL
- FOG: Failover Group
- IaC: Infrastructure as Code
- KQL: Kusto Query Language
- MI: Managed Instance
- PE: Private Endpoint
- RLS/DDM: Row-Level Security / Dynamic Data Masking
- RPO/RTO: Recovery Point/Time Objective
- SLA/SLO/SLI: Agreement/Objective/Indicator
- SRE/DBRE: (Database) Site Reliability Engineering

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
