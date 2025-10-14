# PowerShell Automation Portfolio — SQL Server DBA/DBRE (+ DataOps)

> A practical, production-ready portfolio of PowerShell modules, scripts, tests, CI pipelines, and runbooks focused on SQL Server operations, reliability, and light DataOps automation. Cross-platform with PowerShell 7, secure by default, tested with Pester, and ready for GitHub/GitLab CI.

---

## Table of Contents

- [1. Executive Summary & Value](#1-executive-summary--value)
- [2. Environment & Toolchain](#2-environment--toolchain)
- [3. Repository Structure & Standards](#3-repository-structure--standards)
- [4. Security, Secrets & Governance](#4-security-secrets--governance)
- [5. Error Handling, Logging & Resilience](#5-error-handling-logging--resilience)
- [6. Connectivity, Remoting & Parallelism](#6-connectivity-remoting--parallelism)
- [7. SQL Server Automation Patterns](#7-sql-server-automation-patterns)
  - [7.1 Inventory & Discovery](#71-inventory--discovery)
  - [7.2 Health Checks & Drift](#72-health-checks--drift)
  - [7.3 Backup, Restore & Verification](#73-backup-restore--verification)
  - [7.4 Always On (AOAG) Operations](#74-always-on-aoag-operations)
  - [7.5 Index & Statistics Maintenance](#75-index--statistics-maintenance)
  - [7.6 TempDB & Instance Configuration](#76-tempdb--instance-configuration)
  - [7.7 Patching & Compliance](#77-patching--compliance)
  - [7.8 Capacity, Performance & Baselining](#78-capacity-performance--baselining)
  - [7.9 DR Drills (RTO/RPO Evidence)](#79-dr-drills-rtorpo-evidence)
- [8. Reference Module: SqlOps.Automation](#8-reference-module-sqlopsautomation)
  - [8.1 Manifest & Layout](#81-manifest--layout)
  - [8.2 Sample Advanced Function](#82-sample-advanced-function)
  - [8.3 Pester Tests](#83-pester-tests)
- [9. CI/CD: GitHub Actions & GitLab CI](#9-cicd-github-actions--gitlab-ci)
- [10. Light DataOps Automations](#10-light-dataops-automations)
  - [10.1 Ingestion (S3/Blob → Staging)](#101-ingestion-s3blob--staging)
  - [10.2 Validations & DQ Checks](#102-validations--dq-checks)
  - [10.3 Orchestrating dbt/ADF/Airflow](#103-orchestrating-dbtadfairflow)
- [11. Observability & Alerts](#11-observability--alerts)
- [12. DSC & JEA for Safe Ops](#12-dsc--jea-for-safe-ops)
- [13. Runbooks: On-Call & Triage](#13-runbooks-oncall--triage)
- [14. Templates & Snippet Library](#14-templates--snippet-library)
- [15. Roadmap](#15-roadmap)
- [16. Checklists](#16-checklists)

---

## 1. Executive Summary & Value

PowerShell is a first-class automation language for DBA/DBRE work on Windows and Linux. It integrates natively with SQL Server via the `SqlServer` SMO API, and with community-standard operations modules like `dbatools`. This portfolio demonstrates:

- **Reliability:** Tested runbooks (Pester), repeatable outcomes, evidence artifacts (CSV/JSON/HTML).
- **Speed:** Parallel execution for fleet-wide maintenance, standardized functions/modules.
- **Security:** Code signing, JEA, least-privilege endpoints, secret vault integration.
- **Auditability:** Structured logs, immutable evidence packs for change/DR drills.
- **Cross-Platform:** PowerShell 7 on Windows/Linux with SSH or WinRM.

**Example KPI Improvements**

| KPI                         | Before         | After (Target)   |
|----------------------------|----------------|------------------|
| Mean Change Lead Time      | days           | hours            |
| MTTR (Failover/Restore)    | hours          | < 30–45 minutes  |
| Change Failure Rate        | > 20%          | < 5%             |
| Backup Verification Gap    | ad-hoc         | daily evidence   |
| Health Check Coverage      | partial        | 100% fleet       |

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 2. Environment & Toolchain

- **PowerShell 7 (pwsh)** preferred; Windows PowerShell 5.1 supported when needed.
- **Core modules**
  - `dbatools` (SQL Server automation), `SqlServer` (SMO/Invoke-Sqlcmd)
  - `Pester` (testing), `PSScriptAnalyzer` (linting), `PSReadLine` (dev UX)
  - `Microsoft.PowerShell.SecretManagement` (+ vault extension(s))
- **Editors**: VS Code + PowerShell extension (format on save, code lens, debug).
- **Runners**: GitHub Actions, GitLab CI, Azure DevOps agents (Windows/Linux).
- **Packaging**: `PSResourceGet` for publish/install (private NuGet feed optional).

```powershell
# Install toolchain (run as Admin if needed)
pwsh -NoProfile -Command {
  Set-PSRepository -Name "PSGallery" -InstallationPolicy Trusted
  Install-PSResource dbatools, SqlServer, Pester, PSScriptAnalyzer, PSReadLine, Microsoft.PowerShell.SecretManagement -Scope AllUsers
}
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 3. Repository Structure & Standards

```
/ps-sqlops-portfolio
├── src/
│   ├── SqlOps.Automation/          # Reusable module (functions/.psm1 + manifest)
│   ├── Runbooks/                   # Task-oriented scripts (operational playbooks)
│   └── Tools/                      # Helper scripts (packaging, code signing, etc.)
├── tests/
│   └── SqlOps.Automation.Tests/    # Pester specs per function
├── docs/                           # ADRs, runbook docs, evidence schema
├── examples/                       # Minimal runnable examples per scenario
├── .github/workflows/              # CI: lint, test, publish
└── .psd1/.psm1/.editorconfig/PSRules.psd1
```

**Standards**

- Advanced functions with `CmdletBinding()`, SupportsShouldProcess, `-WhatIf`.
- Comment-based help, parameter validation, **idempotence** where feasible.
- Semantic versioning, conventional commits, CHANGELOG.
- Linting: PSScriptAnalyzer with strict ruleset.

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 4. Security, Secrets & Governance

- **Execution Policy**: All scripts/modules **signed**; CI injects signing cert.
- **SecretManagement**: Store connection strings, tokens, and creds in vaults.
- **JEA** endpoints for task-scoped permissions; avoid blanket admin.
- **Supply Chain**: Pin module versions; maintain internal mirror for critical deps.

```powershell
# Secret retrieval pattern
$SqlCred = Get-Secret -Name 'prod-sql-credential' -AsPlainText
$SecureSqlCred = ConvertTo-SecureString $SqlCred -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential('prod\sqlsvc', $SecureSqlCred)
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 5. Error Handling, Logging & Resilience

- `$ErrorActionPreference = 'Stop'` inside functions; **try/catch/finally** with structured output.
- **Retry/backoff** helpers for transient errors.
- **Correlation IDs** per run; logs emit JSON lines for easy ingestion.

```powershell
function Invoke-WithRetry {
  param([scriptblock]$Script, [int]$Max=5, [int]$DelaySec=3)
  for($i=1; $i -le $Max; $i++){
    try { return & $Script }
    catch {
      if($i -eq $Max){ throw }
      Start-Sleep -Seconds ($DelaySec * $i)
    }
  }
}
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 6. Connectivity, Remoting & Parallelism

- **WinRM/PowerShell remoting** on Windows; **SSH remoting** cross-platform.
- **ForEach-Object -Parallel** (PowerShell 7), **jobs** for fan-out tasks.
- **SMO** for rich SQL interactions; `Invoke-Sqlcmd` for T-SQL execution.

```powershell
$Servers = Get-Content ./docs/server-inventory.txt
$Results = $Servers | ForEach-Object -Parallel {
  Import-Module dbatools
  Test-DbaConnection -SqlInstance $_ -WarningAction SilentlyContinue
} -ThrottleLimit 16
$Results | Where-Object {$_.ConnectSuccess -eq $true} | Export-Csv out/connectivity-ok.csv -NoTypeInformation
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 7. SQL Server Automation Patterns

### 7.1 Inventory & Discovery

- Collect server/instance/database metadata, editions, patch levels, features.
- Tag servers (tier, environment, business owner).

```powershell
$inv = Get-DbaBuildReference -SqlInstance $Servers -EnableException:$false
$inv | Export-Csv out/build-reference.csv -NoTypeInformation
```

### 7.2 Health Checks & Drift

- Check max memory, MAXDOP, cost threshold, backup policies, DB options.
- Compare against **policy files** (JSON/YAML) → emit deviations.

```powershell
$policy = Get-Content .\docs\policies\instance-baseline.json | ConvertFrom-Json
$cfg = Get-DbaMaxDop -SqlInstance $Server
if($cfg.MaxDop -ne $policy.Instance.MaxDop){
  [pscustomobject]@{ Server=$Server; Setting='MaxDOP'; Current=$cfg.MaxDop; Expected=$policy.Instance.MaxDop } |
  Export-Csv out/drift.csv -Append -NoTypeInformation
}
```

### 7.3 Backup, Restore & Verification

- Policy-driven **full/diff/log** backups, encryption, compression.
- **Automated restore verification** to a sandbox instance; checksum/page verify.

```powershell
# Full backup policy example
$targets = @('sql01','sql02')
foreach($t in $targets){
  Backup-DbaDatabase -SqlInstance $t -Database 'ImportantDB' `
    -Type Full -Checksum -CompressBackup -CopyOnly `
    -Verify -BackupDirectory '\\backup\sql' -ErrorAction Stop
}
```

Restore verify:

```powershell
Restore-DbaDatabase -SqlInstance 'sql-verify' -Path '\\backup\sql\ImportantDB\FULL\*.bak' -WithReplace
Invoke-DbaDbccCheck -SqlInstance 'sql-verify' -Database 'ImportantDB' -PhysicalOnly | Tee-Object out\checkdb.txt
```

### 7.4 Always On (AOAG) Operations

- Health checks, failover simulations in maintenance windows, seeding automation.
- Preferred replica & synchronous roles check; listener validation.

```powershell
Get-DbaAgReplica -SqlInstance 'pri-sql' | Select-Object SqlInstance, AvailabilityGroup, Role, AvailabilityMode
# Planned failover (synchronous, healthy, pre-checks passed)
Switch-DbaAgReplica -Primary 'pri-sql' -Secondary 'sec-sql' -WhatIf
```

### 7.5 Index & Statistics Maintenance

- Windowed, **impact-aware** maintenance (fragmentation & size thresholds).
- Respect business hours; throttle per I/O/CPU signals.

```powershell
Invoke-DbaDbIndexOptimize -SqlInstance $Servers -Database 'ImportantDB' `
  -FragmentationLow  <20 -FragmentationMedium 20-40 -FragmentationHigh >40 `
  -TimeLimit 01:00:00 -UpdateStatistics
```

### 7.6 TempDB & Instance Configuration

- Ensure tempdb files = logical core count (cap), equal size, TF recommendations.
- Filegrowth policies (MB, not %), Instant File Initialization check.

```powershell
Set-DbaTempDbConfig -SqlInstance $Server -DataFileCount 8 -AutoGrowth 512MB -WhatIf
```

### 7.7 Patching & Compliance

- Detect **KB** levels vs build reference; orchestrate agent maintenance plans or SCCM hooks.
- Evidence: before/after build CSV + installed updates list.

```powershell
$ref = Get-DbaBuildReference -SqlInstance $Server
$ref | Export-Csv out/build-$Server.csv -NoTypeInformation
```

### 7.8 Capacity, Performance & Baselining

- DMV snapshots + perf counters; store time-series (CSV/Parquet).
- Baselining: 95th percentile wait stats, file I/O, query store top waiters.

```powershell
$ts = Get-Date -Format s
$ws = Invoke-Sqlcmd -ServerInstance $Server -Database master -Query "
SELECT TOP 20 wait_type, wait_time_ms, signal_wait_time_ms
FROM sys.dm_os_wait_stats ORDER BY wait_time_ms DESC"
$ws | Select-Object @{n='Server';e={$Server}},* | Export-Csv out\waitstats-$ts.csv -NoTypeInformation
```

### 7.9 DR Drills (RTO/RPO Evidence)

- Scheduled DR drills: restore last full+logs to DR host; measure timings.
- Produce signed evidence pack (hash + summary JSON).

```powershell
$sw = [Diagnostics.Stopwatch]::StartNew()
# ... restore steps ...
$sw.Stop()
[pscustomobject]@{ RunId=[guid]::NewGuid(); RTO="$($sw.Elapsed.TotalMinutes)"; Source='sql01'; Target='dr-restore' } |
  ConvertTo-Json | Set-Content out\dr-evidence.json
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 8. Reference Module: SqlOps.Automation

### 8.1 Manifest & Layout

```
src/SqlOps.Automation/
├── SqlOps.Automation.psd1  # Module manifest (version, required modules)
├── SqlOps.Automation.psm1  # Functions imported here
└── Public/
    ├── Test-SqlConnectivity.ps1
    ├── Invoke-BackupPolicy.ps1
    ├── Invoke-RestoreVerify.ps1
    └── Measure-InstanceHealth.ps1
```

**Manifest excerpt**:

```powershell
@{
  RootModule        = 'SqlOps.Automation.psm1'
  ModuleVersion     = '0.5.0'
  GUID              = '00000000-0000-4000-8000-000000000001'
  Author            = 'Your Name'
  CompanyName       = 'YourOrg'
  CompatiblePSEditions = @('Core','Desktop')
  RequiredModules   = @(@{ModuleName='dbatools'; ModuleVersion='1.2.0'},
                        @{ModuleName='SqlServer'; ModuleVersion='22.0.0'})
  FunctionsToExport = @('Test-SqlConnectivity','Invoke-BackupPolicy','Invoke-RestoreVerify','Measure-InstanceHealth')
  PowerShellVersion = '7.2'
  PrivateData = @{
    PSData = @{
      Tags = @('SQLServer','DBA','DBRE','Automation')
      ProjectUri = 'https://github.com/your/repo'
    }
  }
}
```

### 8.2 Sample Advanced Function

```powershell
function Test-SqlConnectivity {
  [CmdletBinding(SupportsShouldProcess=$false)]
  param(
    [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName)]
    [string[]]$SqlInstance,
    [int]$TimeoutSec = 5
  )

  begin {
    $results = @()
  }
  process {
    foreach($s in $SqlInstance){
      try {
        $ok = Test-DbaConnection -SqlInstance $s -WarningAction SilentlyContinue -SqlCredential (Get-Secret -Name 'prod-sql-cred' -AsCredential)
        $results += [pscustomobject]@{
          Server = $s
          ConnectSuccess = $ok.ConnectSuccess
          Ping = $ok.Ping
          InstanceName = $ok.InstanceName
          Time = (Get-Date)
        }
      }
      catch {
        $results += [pscustomobject]@{
          Server = $s; ConnectSuccess=$false; Ping=$false; InstanceName=$null; Time=(Get-Date); Error=$_.Exception.Message
        }
      }
    }
  }
  end {
    $results
  }
}
```

### 8.3 Pester Tests

```powershell
Describe 'Test-SqlConnectivity' {
  It 'returns objects with expected properties' {
    $out = Test-SqlConnectivity -SqlInstance 'localhost'
    $out | Should -Not -BeNullOrEmpty
    $out | Get-Member -Name 'Server','ConnectSuccess','Time' | Should -Not -BeNullOrEmpty
  }
}
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 9. CI/CD: GitHub Actions & GitLab CI

**GitHub Actions** (lint, test, pack, publish pre-release):

```yaml
name: ps-sqlops-ci
on: [push, pull_request]
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install PowerShell
        uses: PowerShell/PowerShell-For-GitHub-Actions@v1
      - name: Install toolchain
        shell: pwsh
        run: |
          Install-PSResource Pester, PSScriptAnalyzer, dbatools, SqlServer
      - name: Lint
        shell: pwsh
        run: Invoke-ScriptAnalyzer -Path src -Recurse -Settings ./.config/PSRules.psd1 -Severity Error
      - name: Test
        shell: pwsh
        run: Invoke-Pester -Output Detailed -CI
      - name: Package module
        shell: pwsh
        run: ./Tools/Pack-Module.ps1
```

**GitLab CI** minimal:

```yaml
stages: [lint, test, package]
lint:
  image: mcr.microsoft.com/powershell:7.4-alpine-3.19
  stage: lint
  script:
    - pwsh -NoLogo -Command "Install-PSResource PSScriptAnalyzer; Invoke-ScriptAnalyzer -Path src -Recurse -Severity Error"

test:
  image: mcr.microsoft.com/powershell:7.4-alpine-3.19
  stage: test
  script:
    - pwsh -NoLogo -Command "Install-PSResource Pester; Invoke-Pester -CI"
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 10. Light DataOps Automations

### 10.1 Ingestion (S3/Blob → Staging)

- Pull CSV/JSON from object storage, validate schema, bulk-load to staging DB.
- Partitioned file handling, idempotent loads.

```powershell
param([string]$Bucket='s3://landing/csv', [string]$StageDb='staging')

$files = Get-ChildItem /mnt/s3/landing/csv/*.csv
foreach($f in $files){
  $tbl = "stg_" + ($f.BaseName -replace '[^\w]','_')
  Invoke-Sqlcmd -ServerInstance 'sql-ingest' -Database $StageDb -Query @"
BULK INSERT [$tbl] FROM '$($f.FullName)'
WITH (FIRSTROW=2, FIELDTERMINATOR=',', ROWTERMINATOR='\n', TABLOCK, BATCHSIZE=50000);
"@
}
```

### 10.2 Validations & DQ Checks

- Row counts, null ratios, primary key uniqueness; emit a **DQ report**.

```powershell
$checks = @(
  "SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM staging.dbo.orders;",
  "SELECT 'orders' AS table_name, SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_id FROM staging.dbo.orders;"
)
$report = foreach($q in $checks){ Invoke-Sqlcmd -ServerInstance 'sql-ingest' -Query $q }
$report | Export-Csv out/dq-report.csv -NoTypeInformation
```

### 10.3 Orchestrating dbt/ADF/Airflow

- Kick off dbt models or trigger ADF pipelines with REST; wait/poll for completion.

```powershell
$resp = Invoke-RestMethod -Method Post -Uri $env:ADF_PIPELINE_URL -Headers @{Authorization="Bearer $env:ADF_TOKEN"} -Body (@{param1="daily"} | ConvertTo-Json)
Write-Host "Triggered ADF: $($resp.runId)"
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 11. Observability & Alerts

- Emit key metrics (backup age, last CHECKDB, AOAG role, DB free space).
- Push events to Teams/Slack; publish metrics to a gateway or log store.

```powershell
$metric = [pscustomobject]@{ server='sql01'; metric='backup_age_min'; value=17; ts=(Get-Date).ToUniversalTime().ToString('o') }
$payload = $metric | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri $env:TEAMS_WEBHOOK_URL -Body $payload -ContentType 'application/json'
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 12. DSC & JEA for Safe Ops

- DSC to converge instance/OS settings (firewall, services, packages).
- JEA **role capability**: only expose specific commands/parameters for operators.

```powershell
# JEA session configuration (excerpt)
New-PSSessionConfigurationFile -Path .\jea\SqlOpsJEA.pssc -SessionType RestrictedRemoteServer `
  -TranscriptDirectory 'C:\JEA\Transcripts' -RunAsVirtualAccount -RoleDefinitions @{
    'YOURDOMAIN\SqlOpsOperators' = @{ RoleCapabilities = @('SqlOpsRole') }
}
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 13. Runbooks: On-Call & Triage

- **Connectivity incident**: validate listener, DNS, port, AOAG primary, failover decision tree.
- **Space pressure**: file growth policy, largest free extent, shrink **avoidance**, targeted reclaim.
- **High waits**: top waits, blocked processes, top consuming queries, capture evidence.

```powershell
# Quick triage pack
.\Runbooks\Get-QuickTriage.ps1 -SqlInstance 'prod-listener' -OutDir "evidence\$(Get-Date -f yyyyMMdd-HHmmss)"
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 14. Templates & Snippet Library

**Function header**

```powershell
function Verb-Noun {
  [CmdletBinding(SupportsShouldProcess)]
  param(
    [Parameter(Mandatory)][string]$Name,
    [switch]$Force
  )
  begin { $cid = [guid]::NewGuid(); Write-Verbose "CorrelationId: $cid" }
  process {
    if($PSCmdlet.ShouldProcess($Name, 'DoSomething')){
      try {
        # core
      } catch {
        Write-Error ("[$cid] " + $_.Exception.Message)
        throw
      }
    }
  }
}
```

**Retry wrapper usage**

```powershell
Invoke-WithRetry -Script { Invoke-Sqlcmd -ServerInstance $s -Query "SELECT 1" }
```

**Evidence writer**

```powershell
function Write-Evidence {
  param([object]$Data, [string]$Path)
  $Data | ConvertTo-Json -Depth 5 | Set-Content $Path
}
```

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 15. Roadmap

- Add **OpenTelemetry** exporter for structured tracing.
- Expand **DR drill harness** to multiple apps/DBs with dependency graph.
- Introduce **policy packs** (JSON) for instance/db baselines (lint + fix).
- Publish **containerized runners** (Linux pwsh + SqlClient tools) for CI.

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## 16. Checklists

### 16.1 Release Readiness (Module)

- [ ] Functions have comment-based help & examples.
- [ ] PSScriptAnalyzer clean (no Error/Warning).
- [ ] Pester suite green; coverage ≥ 80% for public functions.
- [ ] Manifest pinned `RequiredModules` versions.
- [ ] Module packaged; signature applied in CI.

### 16.2 SQL Backup & Verify

- [ ] Full/Diff/Log schedules defined; encryption+compression enabled.
- [ ] **Restore verify** jobs succeed daily; CHECKDB run on restore.
- [ ] Evidence artifacts uploaded (JSON/CSV + checksum).
- [ ] Backup age monitors/alerts configured.

### 16.3 AOAG Operations

- [ ] Preferred primary configured; synchronous pairs validated.
- [ ] Listener tested; read-only routing validated.
- [ ] Failover **simulation** performed in maintenance windows; timings recorded.

### 16.4 Baseline & Drift

- [ ] Instance baseline JSON updated quarterly.
- [ ] Drift report produced weekly; deltas triaged.
- [ ] DMV+perf counters baseline captured daily; trends reviewed.

[Back to top](#powershell-automation-portfolio--sql-server-dbadbre--dataops)

---

## Appendix: Example Runbooks (mini)

**Runbook: Verify Backups (Fleet)**

```powershell
$servers = Get-Content .\docs\server-inventory.txt
foreach($s in $servers){
  try {
    $age = (Get-DbaDbBackupInformation -SqlInstance $s -Database 'ImportantDB' -Last).LastBackup
    [pscustomobject]@{ server=$s; minutes=(New-TimeSpan $age (Get-Date)).TotalMinutes } |
      Export-Csv out\backup-age.csv -Append -NoTypeInformation
  } catch {
    Write-Error "$s: $($_.Exception.Message)"
  }
}
```

**Runbook: Space Pressure Alert**

```powershell
Invoke-Sqlcmd -ServerInstance 'prod-listener' -Query "
SELECT
  DB_NAME(mf.database_id) AS db_name,
  mf.name AS file_name,
  size/128.0 AS size_mb,
  FILEPROPERTY(mf.name, 'SpaceUsed')/128.0 AS used_mb
FROM sys.master_files mf
" | Export-Csv out\space-report.csv -NoTypeInformation
```

**Runbook: Blocked Session Snapshot**

```powershell
Invoke-Sqlcmd -ServerInstance 'prod-listener' -Query "
SELECT
  r.session_id, r.status, r.blocking_session_id, r.wait_type, r.wait_time, t.text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.blocking_session_id <> 0;"
```

---

### License & Attribution

- Scripts are examples; review and adapt to your org’s policies.
- `dbatools` (community project) used under its license; pin versions in production.

---
