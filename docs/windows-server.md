markdown
# Windows Server Guide for SQL Server: DBA / DBRE / DataOps (2025 Edition)

**Version:** 2025-10-13  
**Applies to:** Windows Server 2016/2019/2022/2025 (LTSC), Datacenter / Standard / Datacenter: Azure Edition; SQL Server 2016/2017/2019/2022

> **Purpose**  
> Practical, production-ready guidance to configure Windows Server for **SQL Server** workloads with a focus on **DBA**, **DBRE**, and **DataOps** roles: installation baselines, security hardening, storage & networking for performance, clustering & HA/DR, automation with PowerShell/DSC, observability, patching strategies (including **Hotpatch**), and CI/CD for database changes.

---

## Table of Contents

- [1. Scope & Audience](#1-scope--audience)
- [2. What’s New (Windows Server 2025) & Support Lifecycle](#2-whats-new-windows-server-2025--support-lifecycle)
- [3. Licensing & Editions (OS view for SQL workloads)](#3-licensing--editions-os-view-for-sql-workloads)
- [4. Hardware Sizing & Platform](#4-hardware-sizing--platform)
- [5. Installation & Baseline Build](#5-installation--baseline-build)
- [6. Security Baseline (Hardening)](#6-security-baseline-hardening)
- [7. Accounts & Identity (gMSA, SPNs, Kerberos)](#7-accounts--identity-gmsa-spns-kerberos)
- [8. Storage for SQL Server](#8-storage-for-sql-server)
- [9. Networking for Data Workloads](#9-networking-for-data-workloads)
- [10. Patching & Availability](#10-patching--availability)
- [11. Failover Clustering (WSFC) Fundamentals](#11-failover-clustering-wsfc-fundamentals)
- [12. SQL Server HA on Windows (FCI / AG)](#12-sql-server-ha-on-windows-fci--ag)
- [13. Storage Spaces Direct (S2D) — Optional](#13-storage-spaces-direct-s2d--optional)
- [14. Virtualization & Cloud](#14-virtualization--cloud)
- [15. OS Backups, VSS & Recovery](#15-os-backups-vss--recovery)
- [16. Observability & Telemetry](#16-observability--telemetry)
- [17. Automation (PowerShell, DSC, GPO, IaC)](#17-automation-powershell-dsc-gpo-iac)
- [18. DataOps on Windows for SQL Server](#18-dataops-on-windows-for-sql-server)
- [19. App Connectivity & Resilience](#19-app-connectivity--resilience)
- [20. OS Performance Tuning](#20-os-performance-tuning)
- [21. Advanced Troubleshooting](#21-advanced-troubleshooting)
- [22. BC/DR & Multi-Site](#22-bcdr--multi-site)
- [23. Compliance & Auditing](#23-compliance--auditing)
- [24. Checklists & Runbooks](#24-checklists--runbooks)
- [25. Version-Specific Notes (Windows & SQL Server)](#25-version-specific-notes-windows--sql-server)
- [26. References](#26-references)

---

## 1. Scope & Audience

**Audience:**  
- **DBA/DBRE** operating SQL Server on Windows Server (physical/VM/cloud).  
- **DataOps** engineers automating database delivery and environment drift control.

**Environments:** on-premises, virtualized (Hyper-V/VMware), and cloud (Azure, AWS, GCP).

**Not in scope:** deep app design patterns; Linux-specific SQL guidance.

---

## 2. What’s New (Windows Server 2025) & Support Lifecycle

- **Windows Server 2025 (LTSC)** is the current release (GA **Nov 2024**).  
  - **Lifecycle:** Mainstream support **until Nov 13, 2029**; Extended support **until Nov 14, 2034**.
- **Hotpatch** (Windows Server 2025, Azure Edition + Azure Arc) lets you apply many security updates **without reboot**, reducing maintenance windows for SQL clusters/AGs.
- **Rolling OS Cluster Upgrade** improvements and updated tooling simplify in-place upgrades for WSFC nodes with minimal downtime.
- Updated security baseline, TLS defaults, SMB improvements, and hybrid management via **Windows Admin Center** and **Azure Arc**.

> **Upgrade reality check:** 2012 R2 is **end-of-support**; plan to evacuate workloads. Keep 2016/2019 patched and review mitigations and microcode updates that may affect throughput on older CPUs.

---

## 3. Licensing & Editions (OS view for SQL workloads)

- **Standard vs Datacenter**  
  - **Datacenter**: includes **Storage Spaces Direct (S2D)**, **Shielded VMs**, unlimited virtualization rights per host.  
  - **Standard**: adequate for smaller clusters or standalone SQL nodes.
- **Datacenter: Azure Edition** (on Azure Stack HCI/Azure): enables **Hotpatch** and some hybrid-only features.
- **Licensing model:** per-core + CALs. Align virtualization rights with your SQL Server licensing plan (per-core SQL licensing is typical).

---

## 4. Hardware Sizing & Platform

- **CPU & NUMA**: prefer fewer, faster cores; align SQL Server `MAXDOP` and memory per NUMA node; avoid spanning vNUMA improperly.  
- **Power plan**: **High performance** for SQL workloads.  
  ```powershell
  # Force High performance
  powercfg /L
  powercfg /S SCHEME_MIN
  ```
- **Memory**: plan headroom for OS + agent tooling + backup engines. Enable **LPIM** for SQL service account.  
- **Storage**: NVMe / SSD preferred for data & log; 64K allocation unit size; avoid write-caching surprises.  
  ```powershell
  # Example: format with 64K allocation for SQL volumes
  Initialize-Disk -Number 2 -PartitionStyle GPT
  New-Partition -DiskNumber 2 -UseMaximumSize -DriveLetter F
  Format-Volume -DriveLetter F -FileSystem NTFS -NewFileSystemLabel "SQLDATA" -AllocationUnitSize 65536 -Confirm:$false
  ```
- **Networking**: 10/25/40GbE, consider **RDMA** (RoCEv2 or iWARP) for SMB Direct (backups/ingest/AG seeding).

---

## 5. Installation & Baseline Build

- **Server Core** recommended for SQL nodes (reduced patch surface). Use Desktop Experience only if tooling demands it.  
- **Unattended build**: answer file + `sconfig` for hostname, domain join, NTP.  
- **Tools**: Windows Admin Center (WAC), RSAT, SQL Server Management Tools as needed.  
- **Feature install (common)**:  
  ```powershell
  # Core failover clustering & admin tools (run as admin)
  Install-WindowsFeature Failover-Clustering, RSAT-Clustering-Mgmt, RSAT-Clustering-PowerShell, FS-iSCSI-Target-Server -IncludeManagementTools
  ```
- **Package baseline** (optional): winget/choco for standard utilities (Sysinternals, Wireshark, 7zip, Git).

---

## 6. Security Baseline (Hardening)

- Apply **Microsoft Security Baselines** and review **CIS** recommendations before go-live.
- **TLS**: disable SSL 2.0/3.0, TLS 1.0/1.1; enforce TLS 1.2+ (validate SQL Native Client / drivers).  
- **Disable legacy protocols** (SMBv1, NTLMv1) unless strictly required.  
- **Credential protection**: LSA Protection, Credential Guard when compatible with SQL agents; harden **RDP** (NLA, restricted access).  
- **Firewall**: allow-list only needed ports (SQL, WSFC, WMI/WinRM for admin).  
- **WDAC/AppLocker**: consider for jump servers; use allow-listing carefully on SQL boxes.

---

## 7. Accounts & Identity (gMSA, SPNs, Kerberos)

- Use **gMSA** for SQL services when possible for automatic password rotation.  
  ```powershell
  # Example: create and use gMSA for SQL Server service
  # 1) Create KDS root key (once per domain; wait for replication in production)
  Add-KdsRootKey -EffectiveTime ((Get-Date).AddHours(-10))

  # 2) Create gMSA with SPN pre-auth
  New-ADServiceAccount -Name "svc-sql-gmsa" -DNSHostName "sqlnode01.contoso.local" -PrincipalsAllowedToRetrieveManagedPassword "CN=SQL Nodes,OU=Servers,DC=contoso,DC=local"

  # 3) On SQL node
  Install-ADServiceAccount -Identity "svc-sql-gmsa"
  Test-ADServiceAccount -Identity "svc-sql-gmsa"
  ```
- **SPNs** for Kerberos:  
  ```powershell
  # Typical SPNs
  setspn -S MSSQLSvc/sqlnode01.contoso.local:1433 CONTOSO\svc-sql-gmsa$
  setspn -S MSSQLSvc/sqllistener.contoso.local:1433 CONTOSO\svc-sql-gmsa$
  ```
- If using **constrained delegation** (e.g., SQL → another service), configure allowed services on the account and validate tickets.

- **User rights** for SQL service account: **Lock pages in memory (LPIM)** and **Perform volume maintenance tasks (IFI)**.  
  - Configure via GPO: `Computer Configuration → Windows Settings → Security Settings → Local Policies → User Rights Assignment`.

---

## 8. Storage for SQL Server

- **NTFS vs ReFS**  
  - **NTFS**: default for data/log/tempdb.  
  - **ReFS** (newer versions): attractive for **backup volumes** (fast block cloning) and integrity streams; validate vendor support.
- **Allocation unit**: 64K for SQL volumes.  
- **Write-caching**: enable only if protected by battery-backed cache; verify with storage vendor.  
- **MPIO & iSCSI**: use vendor DSM; set appropriate load balance policy.  
- **Dedupe/Compression**: avoid on live DB volumes; allowed on **backup** targets after validation.

---

## 9. Networking for Data Workloads

- **Teaming** for redundancy; validate RSS/VMQ settings on 10GbE+.  
- **Jumbo frames** (MTU 9000) when **end-to-end** supported; measure benefit.  
  ```powershell
  Get-NetAdapterAdvancedProperty -Name "Ethernet*"
  Set-NetAdapterAdvancedProperty -Name "Ethernet1" -DisplayName "Jumbo Packet" -DisplayValue "9014 Bytes"
  ```
- **SMB Multichannel & SMB Direct (RDMA)** for backup/ingest paths:  
  ```powershell
  Get-SmbClientConfiguration
  Get-SmbMultichannelConnection
  ```
- **DNS & SPNs**: set low TTL for AG listeners; ensure reverse lookup zones.

---

## 10. Patching & Availability

- **Order**: OS first, then SQL, then agents/tools.  
- **Maintenance windows**: automate with **WSUS/WUfB** or patching tools.  
- **Cluster-Aware Updating (CAU)** minimizes downtime on WSFC:  
  ```powershell
  # Add CAU clustered role
  Add-CauClusterRole -ClusterName "SQL-CL01" -MaxFailedNodes 0 -RequireAllNodesOnline $true -CauPluginName "Microsoft.WindowsUpdatePlugin"

  # Trigger an updating run
  Invoke-CauRun -ClusterName "SQL-CL01" -CauPluginName "Microsoft.WindowsUpdatePlugin" -RequireAllNodesOnline $true
  ```
- **Hotpatch (2025)**: if using **Azure Edition** or **Azure Arc** connected machines, enable Hotpatch to reduce reboots for monthly security updates. Validate SQL cumulative updates separately.

---

## 11. Failover Clustering (WSFC) Fundamentals

- **Validation** before cluster creation:  
  ```powershell
  Test-Cluster -Node sqlnode01,sqlnode02 -Include "Storage","Inventory","Network","System Configuration"
  ```
- **Create cluster** and quorum:  
  ```powershell
  New-Cluster -Name SQL-CL01 -Node sqlnode01,sqlnode02 -StaticAddress 10.10.10.100 -NoStorage
  Set-ClusterQuorum -NodeMajority
  # or File Share Witness / Cloud Witness for multi-site
  ```
- **Quorum**: prefer **Cloud/File Witness** for 2-node clusters; avoid dynamic vote surprises by planning witness placement.
- **DTC**: configure if distributed transactions are used by apps.

---

## 12. SQL Server HA on Windows (FCI / AG)

### 12.1 Failover Cluster Instance (FCI)
- Shared storage (SAN / SMB). Great for **instance-level** HA; single copy of DB files.  
- For SMB, use **continuous availability** shares on Scale-Out File Server; ensure network resilience.

### 12.2 Availability Groups (AG)
- **Database-level** HA/DR (multiple replicas). Listener, synchronous/asynchronous modes.  
- **Multi-subnet** AGs: configure client-side **`MultiSubnetFailover=True`**; adjust DNS TTL; test failover.  
- **Seeding**: automatic or manual; validate throughput on backup network.

**Example: create WSFC + enable AG features (SQL 2019/2022)**  
```powershell
# Enable Always On availability groups at the instance level (requires restart)
Import-Module SqlServer
Enable-SqlAlwaysOn -ServerInstance "sqlnode01\MSSQLSERVER" -Force
Enable-SqlAlwaysOn -ServerInstance "sqlnode02\MSSQLSERVER" -Force
```

**T-SQL: create AG**
```sql
-- On primary
CREATE AVAILABILITY GROUP AG_Orders
  WITH (AUTOMATED_BACKUP_PREFERENCE = SECONDARY)
  FOR DATABASE [OrdersDB]
  REPLICA ON 
    N'sqlnode01' WITH (ENDPOINT_URL = 'TCP://sqlnode01.contoso.local:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC),
    N'sqlnode02' WITH (ENDPOINT_URL = 'TCP://sqlnode02.contoso.local:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC);
GO
-- Create listener
ALTER AVAILABILITY GROUP AG_Orders ADD LISTENER 'AGORDERS-LSN' (WITH IP ((N'10.10.10.200', N'255.255.255.0')), PORT=1433);
```

---

## 13. Storage Spaces Direct (S2D) — Optional

- **When**: hyperconverged clusters; simplifies storage but adds an abstraction layer.  
- **Considerations**: cache drives, NVMe, RDMA, resiliency (3-way mirror), CSVFS ReFS for VMs/backups. Validate performance for heavy OLTP.

---

## 14. Virtualization & Cloud

- **Hyper-V/VMware**:  
  - Avoid **Dynamic Memory** for SQL; set static and reserve.  
  - Align **vNUMA** with physical NUMA boundaries; no CPU overcommit on Tier-1 DBs.  
- **Azure IaaS**:  
  - Use marketplace images for SQL on Windows or build hardened images (Packer).  
  - Storage: **Premium/Ultra Disks** for logs; spread tempdb across multiple files.  
  - Consider **Azure Hybrid Benefit** and **Azure Backup** application-consistent policies.

---

## 15. OS Backups, VSS & Recovery

- **VSS**: ensure SQL VSS Writer healthy; coordinate with backup vendor for app-consistent snaps.  
- **Bare Metal Recovery**: keep build **runbooks** (Packer/Ansible/DSC) to **rebuild over restore** when time allows.  
- **Off-host snapshots**: test recovery for consistency; prefer AG/FCI-aware backups.

---

## 16. Observability & Telemetry

- **PerfMon**: build Data Collector Sets for OS + SQL. Example counters:
  - CPU: `% Processor Time`, `Processor Queue Length`
  - Memory: `Available MBytes`, `Pages/sec`
  - Disk: `Avg. Disk sec/Read`, `Avg. Disk sec/Write`, `Disk Transfers/sec`
  - Network: `Bytes Total/sec`, `Output Queue Length`
- **ETW/WPR/WPA** for deep traces; **PAL** tool to parse logs.  
- **Windows Event Forwarding (WEF)** to SIEM; **Azure Monitor / Log Analytics**; exporters for Prometheus if needed.

---

## 17. Automation (PowerShell, DSC, GPO, IaC)

- **PowerShell** as the default automation surface.  
- **DSC** to enforce server state (features, registry, rights):  
  ```powershell
  configuration SqlWindowsBaseline
  {
    Import-DscResource -ModuleName PSDesiredStateConfiguration
    Node $AllNodes.NodeName
    {
      WindowsFeature FailoverClustering { Name = "Failover-Clustering"; Ensure = "Present" }
      Registry DisableSMB1 { Key = "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters"; ValueName = "SMB1"; ValueType = "Dword"; ValueData = "0"; Ensure = "Present" }
    }
  }
  SqlWindowsBaseline -OutputPath C:\DSC\SqlBaseline
  Start-DscConfiguration -Path C:\DSC\SqlBaseline -Wait -Verbose -Force
  ```
- **GPO** for user rights (LPIM/IFI), TLS ciphers, firewall baselines.  
- **IaC**: Packer (golden images), Ansible (Windows via WinRM), Terraform (IaaS infra provisioning).

---

## 18. DataOps on Windows for SQL Server

- **Artifacts**: DACPAC (SqlPackage/DacFx) and **Flyway** migrations.  
- **Build agents** on Windows with required SDKs/drivers.  
- **Secrets**: Windows Cert Store / DPAPI / Azure Key Vault.  
- **Promotion**: Dev → Test → PreProd → Prod with approvals.  
- **Rollback**: versioned schema + data-safe rollbacks (idempotent Flyway, blue/green DBs).

**Example: DACPAC deploy (PowerShell)**  
```powershell
$SqlPackage = "C:\Program Files\Microsoft SQL Server\160\DAC\bin\SqlPackage.exe"
& $SqlPackage /Action:Publish /SourceFile:"build\app.dacpac" /TargetServerName:"AGORDERS-LSN" /TargetDatabaseName:"OrdersDB" /p:BlockOnPossibleDataLoss=false /p:CommandTimeout=1200
```

**Example: Flyway (PowerShell)**  
```powershell
$env:FLYWAY_URL="jdbc:sqlserver://AGORDERS-LSN:1433;databaseName=OrdersDB;encrypt=true;trustServerCertificate=true"
$env:FLYWAY_USER="CONTOSO\svc-sql-gmsa$"
$env:FLYWAY_PASSWORD=""  # Using Integrated Security or Secret retrieval
flyway -locations=filesystem:sql -baselineOnMigrate=true migrate
```

---

## 19. App Connectivity & Resilience

- **Connection strings**: enable encryption/TLS; prefer **AAD** (Entra ID) auth where possible.  
- **Retry** with exponential backoff; detect AG failover using `MultiSubnetFailover=True`.  
- **Certificates**: monitor expiry; automate renewal and binding.

---

## 20. OS Performance Tuning

- **CPU scheduling**: pin noisy neighbors; consider disabling unnecessary mitigations only after risk review.  
- **File system**: 64K clusters; monitor disk latencies; ensure queue depths align with device limits.  
- **Network**: validate RSS, interrupt moderation, offloads; measure before enabling **Jumbo frames**.

---

## 21. Advanced Troubleshooting

- **Crash dumps**: enable kernel dumps; analyze with WinDbg (`!analyze -v`).  
- **Network**: `pktmon`, `netsh trace`, Wireshark.  
- **Storage**: `DiskSpd` to isolate device vs stack issues.  
- **Perf**: WPR/WPA session templates for CPU, Disk I/O, and Networking.  
- **Playbooks**: incident runbooks for timeouts, high wait stats, AG failover loops, patching regressions.

---

## 22. BC/DR & Multi-Site

- **Dependencies**: AD/DNS/DHCP, Certificate Services redundancy.  
- **Quorum**: **Cloud/File Witness** in third site for 2-node stretched clusters.  
- **Runbooks**: plan/test failovers regularly; document network/DNS/cert changes.

---

## 23. Compliance & Auditing

- **Audit policies**: Object Access, Policy Change, Logon/Logoff; forward to SIEM.  
- **Crypto**: TLS 1.2+, FIPS mode when mandated; BitLocker on at-rest volumes; SMB signing as required.  
- **Evidence**: keep DSC/GPO exports, patch reports, and PerfMon baselines per release.

---

## 24. Checklists & Runbooks

### 24.1 Golden Image Build (per OS version)
- [ ] LTSC media verified (hash) and current cumulative update integrated.  
- [ ] Features: Failover-Clustering, RSAT-Clustering-*, iSCSI tools (if needed).  
- [ ] Power plan = High performance; pagefile policy set.  
- [ ] TLS baseline, disable SMBv1; firewall profiles configured.  
- [ ] Tools: WAC, Sysinternals, DiskSpd, SQL tools.  
- [ ] DSC/GPO applied; local policies for LPIM/IFI prepared.

### 24.2 Cluster Readiness
- [ ] Firmware/driver matrix validated (HBA/NIC).  
- [ ] Shared storage or SMB CA shares (FCI) or dedicated networks for AG.  
- [ ] `Test-Cluster` clean; quorum/witness planned.  
- [ ] DTC configured if needed; listener DNS records & TTL verified.  
- [ ] Backup/monitoring agents installed and whitelisted.

### 24.3 Patching Day (WSFC)
- [ ] Freeze app releases; notify stakeholders.  
- [ ] Backups healthy; AG failover tested.  
- [ ] CAU/Hotpatch plan executed; verify node health after each cycle.  
- [ ] Post-patch validation: SQL services, AG sync, perf counters, event logs.

---

## 25. Version-Specific Notes (Windows & SQL Server)

### Windows Server
- **2016**: stable baseline; older SMB/TLS defaults → harden aggressively.  
- **2019**: improved ReFS/SMB; good for SQL 2017/2019; watch TLS defaults.  
- **2022**: security updates, SMB compression improvements, longer runway for 2019/2022 SQL.  
- **2025 (LTSC)**: **Hotpatch** (Azure Edition / Azure Arc), latest kernel/network/storage stack, release-health channel; plan new greenfield here.

### SQL Server
- **2016/2017**: legacy but widely deployed; review support timelines; patch to latest CU.  
- **2019**: mainstream support ended **Feb 28, 2025**; now in **Extended Support** → security updates only.  
- **2022**: current GA release; prefer for new builds; many engine improvements (intelligent query processing v2, etc.).

> **Coexistence tips:** Run mixed-version AGs only for migration windows; align client drivers with server version; verify TLS and cipher suites per driver.

---

## 26. References

- Windows Server **2025 lifecycle** (dates, LTSC): https://learn.microsoft.com/en-us/lifecycle/products/windows-server-2025  
- Windows Server **release health / GA**: https://learn.microsoft.com/en-us/windows/release-health/status-windows-server-2025  
- **What’s new** in Windows Server 2025: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025  
- **Hotpatch** overview (Azure Arc/Azure Edition): https://learn.microsoft.com/en-us/windows-server/get-started/hotpatch  
- **Cluster-Aware Updating (CAU)**: https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-aware-updating  
- **Rolling OS cluster upgrade**: https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-operating-system-rolling-upgrade  
- gMSA overview: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview  
- Register **SPN** for SQL Server Kerberos: https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/register-a-service-principal-name-for-kerberos-connections

---

### Appendix: Useful Tools

- **Sysinternals**: Process Explorer, RAMMap, Procmon.  
- **DiskSpd**: synthetic I/O load generation for storage validation.  
- **Windows Admin Center**: unified admin portal; extensions for clustering.  
- **PAL**: Performance Analysis of Logs (PerfMon).

---

*End of document.*
