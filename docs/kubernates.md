# DBRE/DBA/DataOps on Kubernetes — **EXTENDED** Portfolio

![Kubernetes](https://img.shields.io/badge/Kubernetes-1.x-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-Chart-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![Kustomize](https://img.shields.io/badge/Kustomize-Overlays-2E7D32?style=for-the-badge)
![Argo%20CD](https://img.shields.io/badge/Argo%20CD-GitOps-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![Flux](https://img.shields.io/badge/Flux-GitOps-2C3E50?style=for-the-badge&logo=flux&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Registry-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQL%20Server](https://img.shields.io/badge/SQL%20Server-2022-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.x-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.x-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-3.x-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Loki](https://img.shields.io/badge/Loki-Logs-4C8BF5?style=for-the-badge)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Traces-000000?style=for-the-badge&logo=opentelemetry&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EKS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-AKS-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-GKE-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![OCI](https://img.shields.io/badge/OCI-OKE-F80000?style=for-the-badge&logo=oracle&logoColor=white)

---

## Table of Contents

- [1. Badge Strip (Summary)](#1-badge-strip-summary)
- [2. Purpose & Audience](#2-purpose--audience)
- [3. When (Not) to Run Databases on Kubernetes](#3-when-not-to-run-databases-on-kubernetes)
- [4. Cluster Architecture for Stateful Workloads](#4-cluster-architecture-for-stateful-workloads)
- [5. Node Classes, Taints/Tolerations & Topology](#5-node-classes-taintstolerations--topology)
- [6. StatefulSets vs. Deployments for Databases](#6-statefulsets-vs-deployments-for-databases)
- [7. Storage Strategy: CSI, PV/PVC & Access Modes](#7-storage-strategy-csi-pvpvc--access-modes)
- [8. Storage Performance & Media Selection](#8-storage-performance--media-selection)
- [9. Database Operators vs. Helm/Kustomize](#9-database-operators-vs-helmkustomize)
- [10. Networking & Service Exposure for Databases](#10-networking--service-exposure-for-databases)
- [11. Service Mesh Considerations (mTLS, Sidecars)](#11-service-mesh-considerations-mtls-sidecars)
- [12. Security Baseline: RBAC, Pod Security, Seccomp](#12-security-baseline-rbac-pod-security-seccomp)
- [13. Secrets & Key Management (Vault/KMS)](#13-secrets--key-management-vaultkms)
- [14. Encryption: At Rest & In Transit (incl. TDE)](#14-encryption-at-rest--in-transit-incl-tde)
- [15. Resource Management: Requests, Limits & QoS](#15-resource-management-requests-limits--qos)
- [16. Scheduling for Performance & Resilience](#16-scheduling-for-performance--resilience)
- [17. High Availability & Failover Patterns](#17-high-availability--failover-patterns)
- [18. Disaster Recovery & Cross-Cluster Designs](#18-disaster-recovery--cross-cluster-designs)
- [19. Backups & Restores: Engine-Native vs. Platform](#19-backups--restores-engine-native-vs-platform)
- [20. Observability: Metrics, Logs, Traces](#20-observability-metrics-logs-traces)
- [21. Query-Level Exporters & DB Health Probes](#21-query-level-exporters--db-health-probes)
- [22. SLOs/SLIs/Error Budgets for Data Platforms](#22-slossliserror-budgets-for-data-platforms)
- [23. CI/CD & GitOps for DB Workloads](#23-cicd--gitops-for-db-workloads)
- [24. Schema Migrations (Flyway/Liquibase) at Scale](#24-schema-migrations-flywayliquibase-at-scale)
- [25. Release Safety: PDBs, Drains & Disruption Budgets](#25-release-safety-pdbs-drains--disruption-budgets)
- [26. DataOps Pipelines around Kubernetes](#26-dataops-pipelines-around-kubernetes)
- [27. Test Data, Ephemeral Environments & Masking](#27-test-data-ephemeral-environments--masking)
- [28. Cost & Capacity Management](#28-cost--capacity-management)
- [29. Compliance, Auditing & Governance](#29-compliance-auditing--governance)
- [30. Incident Response & Runbooks](#30-incident-response--runbooks)
- [31. Chaos & Resilience Testing](#31-chaos--resilience-testing)
- [32. Multi-Tenancy & Namespace Strategy](#32-multi-tenancy--namespace-strategy)
- [33. Cloud-Specific Notes (EKS/AKS/GKE/OKE)](#33-cloud-specific-notes-eksaksgkeoke)
- [34. Migration Paths to Kubernetes](#34-migration-paths-to-kubernetes)
- [35. Common Anti-Patterns to Avoid](#35-common-anti-patterns-to-avoid)
- [36. Reference Architectures (Per Engine)](#36-reference-architectures-per-engine)
- [37. Repository Templates & Conventions](#37-repository-templates--conventions)
- [38. Appendix: Glossary, Labs & Further Reading](#38-appendix-glossary-labs--further-reading)

---

> **How to use this portfolio**: Each topic includes (1) a dense paragraph, (2) an actionable checklist, and (3) 3–5 concrete examples (commands, YAML, or patterns). All examples are production-leaning and designed for copy/paste adaptation.

---

## 1. Badge Strip (Summary)
A compact badge strip communicates the portfolio’s scope at a glance: orchestrators, packaging, IaC, observability, core databases, and target clouds. Limit badges to your standard toolset to reinforce consistency and reduce cognitive load for reviewers and teammates.

**Checklist**
- Show only technologies you actively support in production.
- Keep versions realistic and periodically update badges.
- Link each badge to an internal runbook or standard (optional).

**Examples**
- Orchestration/Packaging: Kubernetes, Helm, Kustomize, Argo CD/Flux.
- Databases/Messaging: PostgreSQL, MySQL, SQL Server, MongoDB, Redis, Kafka.
- Observability/IaC: Prometheus, Grafana, Loki, OpenTelemetry, Terraform, Ansible.

---

## 2. Purpose & Audience
This portfolio targets senior DBAs/DBREs/DataOps practitioners responsible for designing, deploying, and operating stateful data platforms on Kubernetes with security, auditability, and repeatability. It emphasizes GitOps, runbooks, SLOs, and disciplined release management to balance speed with reliability.

**Checklist**
- Define responsibilities (DBA vs. Platform vs. App teams).
- Document SLOs and DR targets (RPO/RTO) per service.
- Align standards with compliance frameworks (LGPD/GDPR/PCI/HIPAA).
- Maintain operator support matrices and upgrade calendars.

**Examples**
- Roles: DBRE, DBA, SRE, Platform Engineer, Data Engineer (infra-facing).
- Artifacts: Git repos (manifests/migrations), runbooks, dashboards, alerts.
- Outcomes: measurable reliability, lower MTTR, reproducible deployments, audit trails.

---

## 3. When (Not) to Run Databases on Kubernetes
Running databases on Kubernetes is powerful but conditional. Evaluate IO patterns, latency sensitivity, operator maturity, staffing, and alternatives like DBaaS. Start with replicas, non-critical workloads, or read-heavy services before promoting primaries.

**Checklist**
- Benchmark storage (fio) and workload (pgbench/sysbench) before cutover.
- Confirm operator support for required features (PITR, TLS, TDE, major upgrades).
- Ensure dedicated node pools with NVMe for hot primaries.
- Validate failover, backups, restores, and client retry logic under load.

**Examples**
- Prefer DBaaS for ultra-high availability and tight compliance with limited ops staff.
- Use K8s when you need portability, custom extensions, or uniform GitOps.
- Avoid K8s for ultra-low-latency OLTP without NVMe/local PV + strict node isolation.
- Hybrid: managed primary + K8s replicas for read scaling and DR rehearsal.

---

## 4. Cluster Architecture for Stateful Workloads
Design the cluster around failure domains: separate control-plane and workers, multi-zone worker pools, and standard add-ons (CNI, CSI, metrics, logging, ingress, DNS). Keep versions within supported windows and run rehearsed upgrade playbooks.

**Checklist**
- CNI (Calico/Cilium), metrics-server, CoreDNS + NodeLocal DNSCache.
- CSI driver with snapshots and expansion; ingress/gateway as needed.
- Version skew policy: N-1 for K8s and operators; documented cadence.
- Blue/green or surge upgrades with PDB awareness and runbooks.

**Examples**
- Gateway API for stable north-south; limit ingress to DB-adjacent proxies only.
- Node images hardened and aligned to CIS Benchmarks.
- Cluster-autoscaler paused for DB nodes during maintenance windows.

---

## 5. Node Classes, Taints/Tolerations & Topology
Use dedicated node pools for DB workloads (memory- and IO-optimized). Taint/tolerate to pin DB pods; add affinities and topology-spread to keep replicas in separate zones. Prefer NVMe for WAL/redo-intensive primaries.

**Checklist**
- Dedicated node pool labels (e.g., `workload=db`, `storage=nvme`).
- Taints on DB nodes; tolerations on DB pods.
- Topology spread constraints across zones for replicas.
- PriorityClasses to protect DB pods from preemption.

**Examples**
- Taint pool:
  ```bash
  kubectl taint nodes pool=db db=yes:NoSchedule
  ```
- Pod spec:
  ```yaml
  nodeSelector: { workload: "db", storage: "nvme" }
  tolerations: [{ key: "db", operator: "Equal", value: "yes", effect: "NoSchedule" }]
  ```
- Spread:
  ```yaml
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
      labelSelector: { matchLabels: { app: "postgres" } }
  ```

---

## 6. StatefulSets vs. Deployments for Databases
StatefulSets maintain stable identities, ordered rollouts, and persistent volumes—essential for replication and backups. Deployments are for stateless sidecars (exporters, proxies). Use headless Services for deterministic DNS per replica.

**Checklist**
- Use StatefulSets for DB engines and consensus clusters.
- Headless Service with `clusterIP: None`.
- Ordered updates; `podManagementPolicy: OrderedReady` when needed.
- Versioned images; immutable tags; signed containers.

**Examples**
- Minimal StatefulSet + headless Service for PostgreSQL (3 replicas).
- Proxy/connection pooler (PgBouncer/ProxySQL) as Deployment with HPA.
- Partitioned rollouts for minor upgrades; blue/green for major versions.

---

## 7. Storage Strategy: CSI, PV/PVC & Access Modes
Match access modes and volume types to the engine. Prefer RWO for primaries; use RWX only for tooling (backups, logs). Enable expansion and snapshots. Choose filesystem vs. block according to engine recommendations.

**Checklist**
- Enable `allowVolumeExpansion: true` in StorageClass.
- `WaitForFirstConsumer` to bind volume in correct zone.
- Define VolumeSnapshotClass with `Retain` for safety.
- Pre-provision separate PVCs for WAL/redo when beneficial.

**Examples**
- StorageClass (gp3 on EKS) with baseline IOPS/throughput.
- PVC per replica (RWO, 1Ti); WAL PVC (100–200Gi) on higher-IOPS class.
- SnapshotClass for crash-consistent snapshots; immutable backup path.

---

## 8. Storage Performance & Media Selection
Storage is the most common bottleneck. Use NVMe/local PVs or high-IOPS SSDs, separate hot logs, tune filesystems (XFS). Benchmark with fio and validate DB-specific throughput and latency targets.

**Checklist**
- Benchmark (fio) sequential and random IO; record baselines.
- Mount options: `noatime`, queue depth alignment; check scheduler.
- Isolate WAL/redo and temp from data when it helps.
- Monitor disk saturation and fs errors; alert on latency p95/p99.

**Examples**
- fio baseline:
  ```bash
  fio --name=randrw --filename=/nvme/test --ioengine=libaio --direct=1 \
      --rw=randrw --bs=4k --rwmixread=70 --size=20G --iodepth=64 --runtime=120 --numjobs=4
  ```
- XFS mount:
  ```bash
  mount -o noatime,nodiratime /dev/nvme0n1 /var/lib/postgresql
  ```
- Dedicated PVC for WAL mounted to `/var/lib/postgresql/wal`.

---

## 9. Database Operators vs. Helm/Kustomize
Operators (CloudNativePG, Percona Operators, MongoDB Operator) encode day‑2 ops: initialization, scaling, upgrades, backups, failover. Helm/Kustomize compose and parametrize deployments and policies. Combine both: operator for core lifecycle; Helm/Kustomize for exporters, secrets integration, network policy, and GitOps overlays.

**Checklist**
- Track operator support matrix and CRD versions.
- GitOps CRs with environment overlays (dev/stg/prod).
- Backups defined in CRs; scheduled and monitored.
- Rollout policies and resource defaults baked into Helm values.

**Examples**
- CloudNativePG `Cluster` CR (3 replicas, 1Ti PVC, TLS, monitoring enabled).
- Percona MySQL `InnoDBCluster` with router and XtraBackup configuration.
- MongoDB Community Operator ReplicaSet with TLS/KMIP and PodMonitors.

---

## 10. Networking & Service Exposure for Databases
Prefer east‑west via ClusterIP/headless Services. Use LoadBalancer only when external clients need it; restrict by firewall/allowlist and enforce TLS. Consider session affinity for clients lacking retries; reduce DNS latency with NodeLocal DNSCache.

**Checklist**
- Separate RW and RO Services; health‑checked backends for poolers.
- Enforce mTLS or TLS for client connections.
- Avoid gratuitous ingress in front of DBs.
- NodeLocal DNSCache for large clusters/heavy DNS usage.

**Examples**
- RW/RO Services:
  ```yaml
  kind: Service
  metadata: { name: pg-rw }
  spec: { selector: { app: pg, role: primary }, ports: [{ port: 5432 }] }
  ---
  kind: Service
  metadata: { name: pg-ro }
  spec: { selector: { app: pg, role: replica }, ports: [{ port: 5432 }] }
  ```
- `sessionAffinity: ClientIP` where clients lack retry/rr logic.
- NodeLocal DNSCache DaemonSet installed via Helm.

---

## 11. Service Mesh Considerations (mTLS, Sidecars)
Meshes add mTLS, policy, and observability—at the cost of latency and complexity. For DB traffic, prefer direct TLS at client libraries or selective/ambient mesh modes. Never inject sidecars blindly into DB pods.

**Checklist**
- If mesh is mandatory, exclude DB pods from sidecar injection.
- Enforce mTLS on app namespaces; measure latency impact.
- Prefer end‑to‑end TLS with cert-manager/Vault for DB connections.
- Keep retry/backoff at client poolers (PgBouncer/ProxySQL).

**Examples**
- Namespace label `istio-injection=disabled` for DB namespaces.
- PeerAuthentication enforcing mTLS only for app→app.
- Client TLS: JDBC/psql with mounted secrets from cert-manager (Vault issuer).

---

## 12. Security Baseline: RBAC, Pod Security, Seccomp
Apply least‑privilege RBAC, Pod Security Admission (`restricted`), and seccomp/AppArmor. Require signed images and disallow root. Scan images and SBOMs; block pulls on policy violations.

**Checklist**
- Pod securityContext: non‑root, read‑only FS, `RuntimeDefault` seccomp.
- RBAC: split duties (DBA vs. Platform vs. Security auditors).
- Image policy: Cosign signatures + Kyverno/Gatekeeper rules.
- Secrets from central store; avoid literals in manifests.

**Examples**
- Pod `securityContext` hardening.
- Role/RoleBinding grant read‑only access for auditor group.
- Kyverno policy requiring signatures for `ghcr.io/org/*` images.

---

## 13. Secrets & Key Management (Vault/KMS)
Manage secrets centrally (Vault/KMS). Sync to Kubernetes via External Secrets Operator, rotate regularly, and keep TTLs short. Automate TLS issuance with cert-manager backed by Vault or cloud KMS.

**Checklist**
- ESO configured with ClusterSecretStore; per‑namespace ExternalSecrets.
- Rotate passwords/keys; annotate secrets with rotation dates.
- Separate RBAC for secret readers vs. writers.
- Audit all secret accesses; restrict kubectl exec on DB pods.

**Examples**
- ExternalSecret mapping `prod/db/password` to `DB_PASSWORD`.
- Vault Agent Injector writing creds to tmpfs and signaling app reload.
- cert‑manager Issuer pointing to Vault PKI for DB TLS lifecycle.

---

## 14. Encryption: At Rest & In Transit (incl. TDE)
Use multi‑layer encryption: storage‑level (CSI/cloud disk), engine‑native TDE, and TLS in transit. Validate cipher suites; rotate certs; test cold restores with encrypted backups and track key provenance.

**Checklist**
- Storage encryption enabled by default for PVCs/disks.
- DB TDE where supported (SQL Server, Oracle, some Postgres plugins).
- Client TLS 1.2+; deprecate weak ciphers.
- Backup encryption with separate KMS keys and access policies.

**Examples**
- Postgres TLS: `ssl=on`, `ssl_min_protocol_version=TLSv1.2` with mounted certs.
- SQL Server TDE: master key → certificate → `ALTER DATABASE ... SET ENCRYPTION ON`.
- MongoDB TLS + KMIP with rotation coordinated through maintenance windows.

---

## 15. Resource Management: Requests, Limits & QoS
Right‑size CPU/memory; avoid CPU throttling on primaries by omitting CPU limits and reserving memory. Consider hugepages/shared memory; minimize sidecars. Guarantee QoS by matching memory requests=limits on critical DB pods.

**Checklist**
- Reserve headroom on DB nodes; avoid bin‑packing primaries.
- Memory limits = requests for predictability; watch OOM risks.
- HugePages for engines benefiting from large pages.
- Keep sidecars minimal (exporter/log agent only if needed).

**Examples**
- Primary resources (8 vCPU, 64Gi RAM; memory‑guaranteed, no CPU limit).
- HugePages limit for shared buffers/SGA‑like memory.
- PodPriority to avoid eviction under pressure.

---

## 16. Scheduling for Performance & Resilience
Use affinities and topology constraints to distribute replicas. Coordinate PDBs, rollout surge, and node drains to preserve quorum. Pin primaries to NVMe nodes; keep read replicas on cheaper classes if acceptable.

**Checklist**
- Anti‑affinity for replicas across zones.
- `maxUnavailable: 0` for primary StatefulSets.
- PriorityClasses for DB workloads.
- Surge/partitioned rollouts for safer upgrades.

**Examples**
- Anti‑affinity using `requiredDuringSchedulingIgnoredDuringExecution`.
- StatefulSet rolling update with partition to control promotions.
- Node drain playbook integrating PDB checks and Argo pause. 

---

## 17. High Availability & Failover Patterns
Choose replication style (sync/async, quorum‑based). Automate leader election and fencing; ensure app clients handle retries and idempotency. Test failover under realistic load; measure promotion times and replication catch‑up.

**Checklist**
- Document topology and quorum rules.
- Health checks for replication lag and write availability.
- Client‑side retry policies with backoff/jitter.
- Split‑brain prevention and fencing actions documented.

**Examples**
- Patroni on Postgres with K8s DCS.
- MySQL Orchestrator with semi‑sync and promotion policies.
- Redis Operator + Sentinel; AOF rewrite configuration.
- HAProxy/PgBouncer with health‑checked backends and RW/RO routing.

---

## 18. Disaster Recovery & Cross-Cluster Designs
Design for region outage: async replication to secondary cluster, immutable backups, and scripted cutover/return. Rotate secrets in DR; practice restores and DNS flips. Track RPO/RTO and document exceptions.

**Checklist**
- Secondary cluster ready with operators and secrets synced.
- WAL/binlog/object backups replicated cross‑region.
- Failover runbook with checklists and rollback.
- DR game days with success criteria and evidence capture.

**Examples**
- WAL‑G to S3/OCI/GCS; restore to promote replica in DR cluster.
- MySQL delayed replica protecting against accidental drops.
- DNS switch via traffic manager; readiness verified by synthetic checks.
- Backfill catch‑up before returning to primary region.

---

## 19. Backups & Restores: Engine-Native vs. Platform
Engine‑native backups enable PITR; platform snapshots accelerate crash‑consistent restores. Use both. Validate restores regularly, measure RTO, and keep immutable retention with lifecycle policies.

**Checklist**
- Scheduled full/incremental + archival (WAL/binlog/log backups).
- Immutable object storage (WORM) and versioning.
- Restore rehearsals into isolated namespaces with masked data.
- Monitoring for backup success/lag and storage costs.

**Examples**
- pgBackRest full+incr + PITR to object storage; periodic `restore --delta` drills.
- XtraBackup with binlog‑based PITR; GTID continuity checks.
- SQL Server FULL/DIFF/LOG; `WITH NORECOVERY` and tail‑log captures.
- Velero+CSI snapshots for fast lab restores (not a PITR replacement).

---

## 20. Observability: Metrics, Logs, Traces
Unify DB + K8s metrics; build dashboards aligned to SLOs; centralize logs; trace critical data paths. Alert on burn rate, saturation, and error/freshness SLIs to reduce noise and improve MTTR.

**Checklist**
- Prometheus scrape configs for engines and poolers.
- Grafana dashboards: availability, latency, saturation, errors.
- Loki/ELK with structured labels for fast filtering.
- OTel Collector exporting traces to Tempo/Jaeger.

**Examples**
- PrometheusRule for replica lag and disk saturation.
- Grafana dashboard panels combining DB and node IO latency.
- Loki labels `{namespace,app,role,instance}`; exemplars linking to traces.
- Trace sampling for heavy jobs; full trace for critical endpoints.

---

## 21. Query-Level Exporters & DB Health Probes
Tune readiness/liveness/startup probes to DB reality; leverage exporters with custom queries for slow queries, locks, and cache stats. Monitor poolers and connection saturation.

**Checklist**
- Generous `initialDelaySeconds` for recovery/warmup.
- Exporters with curated query collectors per engine.
- Pooler metrics (PgBouncer/ProxySQL) in Prometheus.
- Probe commands using engine‑native tools (pg_isready, mysqladmin ping).

**Examples**
- Postgres readiness probe with 60s initial delay and failure threshold 6.
- mysqld_exporter with custom collector for buffer pool hit ratio.
- mssql_exporter for waits/blocks; redis_exporter for evictions/latency.
- Pooler dashboard for active/idle clients and max servers. 

---

## 22. SLOs/SLIs/Error Budgets for Data Platforms
Define SLIs (availability, latency, freshness) per service; set SLOs and error budget policies. Use multi‑window burn‑rate alerts and connect them to release gating and maintenance freezes.

**Checklist**
- SLIs documented with formulas and data sources.
- SLO targets agreed with product/engineering.
- Burn‑rate alerts (2h/24h) to capture fast/slow incidents.
- Error budget policy documented and enforced.

**Examples**
- Availability SLI: `successful_connections / total_connections` over 30d.
- Freshness SLI: `% of partitions updated within 15m window`.
- Burn‑rate alert gating schema migrations when exceeded.
- Weekly SLO review with actionable improvements.

---

## 23. CI/CD & GitOps for DB Workloads
Everything in Git: manifests, policies, migrations, dashboards, runbooks. Use Argo CD/Flux for reconciling, with policy checks and image signatures. Promote via overlays (dev→stg→prod) and require approvals for risky changes.

**Checklist**
- Pre‑merge: schema linters, `kubeconform`, `helm lint`, policy tests.
- Cosign signature verification; provenance attestations.
- Automated sync with limited windows for DB tiers.
- Drift detection and self‑healing except during maintenance.

**Examples**
- Argo CD Application with automated prune/self‑heal and sync options.
- GitHub Action checking policies + building SBOM; Cosign signing.
- Kustomize overlays separating per‑env values (storage, resources, secrets refs).

---

## 24. Schema Migrations (Flyway/Liquibase) at Scale
Build forward‑only, backward‑compatible migrations. Separate deploy from release with feature flags; batch backfills; define roll‑forward plans. Gate heavy DDL with performance windows and lock‑avoidance tactics.

**Checklist**
- Versioned migrations; immutable artifacts tied to app releases.
- Statement/lock timeouts; `EXPLAIN` plans and safety checks.
- Online DDL strategies and backfill jobs with throttling.
- Roll‑forward procedures and emergency rollback scripts.

**Examples**
- Flyway CLI step in CI with JDBC URL to RW Service.
- Liquibase changelog with `preConditions` + rollback.
- Online DDL sequence: add nullable → backfill → switch code → drop old.
- Backfill with `LIMIT/OFFSET` or key‑range in batches; track progress table.

---

## 25. Release Safety: PDBs, Drains & Disruption Budgets
Protect quorum with PDBs; coordinate node drains and autoscaling. Set `maxUnavailable: 0` for primaries; test rollouts in staging. Log disruptive actions and correlate with SLO changes.

**Checklist**
- PDB per engine/role; check before drains.
- Maintenance window playbook; autoscaler coordination.
- `kubectl cordon/drain` scripts with guardrails.
- Rollback plan and success criteria defined per change.

**Examples**
- PDB with `minAvailable: 2` for 3‑replica clusters.
- Drain script invoking cluster checks and pausing Argo sync.
- Rolling update partitioned to keep a replica set writable. 

---

## 26. DataOps Pipelines around Kubernetes
Integrate ingestion, transformations, quality, and lineage with K8s‑hosted DBs. Coordinate windows around replication lag and backups; enforce data contracts to protect downstream reliability.

**Checklist**
- Orchestrator (Airflow/Argo Workflows) integrated with SLO checks.
- dbt tests and Great Expectations gates.
- Lineage capture and metadata push (OpenLineage, Amundsen, DataHub).
- Snapshots, checksums, and artifact promotion metadata.

**Examples**
- Airflow DAG calling dbt + GE checkpoint; halts on failed SLO probe.
- Argo Workflow step snapshotting PVC then verifying checksums.
- dbt incremental materializations with partition pruning.

---

## 27. Test Data, Ephemeral Environments & Masking
On every PR, create ephemeral namespaces with masked data. Use snapshots/clones for speed. Destroy envs automatically; enforce quotas and TTLs to control costs.

**Checklist**
- VolumeSnapshot cloning for test DBs.
- Masking pipeline preserving referential integrity and distributions.
- TTL after inactivity; auto‑cleanup on merge.
- PR‑tagged images and isolated RW/RO Services.

**Examples**
- Kustomize sets image tag to `$(git rev-parse --short HEAD)`.
- Snapshot → clone PVC into `ns-pr-1234`; seed masked dump.
- Deterministic masking of PII with tokenization tables.

---

## 28. Cost & Capacity Management
Make costs observable and predictable. Right‑size nodes and storage; minimize over‑provisioned IOPS; consolidate read replicas; label for chargeback/showback. Reserve/commit for steady loads; keep burst headroom.

**Checklist**
- Kubecost or provider cost data labeled by namespace/team.
- Storage tiers aligned to IO profile; WAL/redo on faster class.
- Capacity models per service; scaling guardrails.
- Regular rightsizing reviews tied to SLOs.

**Examples**
- Kubecost allocation dashboard by `owner.team=dbre`.
- gp3 baseline for data; io2/NVMe for WAL/redo.
- Read pool size matches p95 read concurrency; drop unused replicas.

---

## 29. Compliance, Auditing & Governance
Enforce CIS/Kubernetes Benchmarks, separation of duties, immutable backups, and audit trails. Default deny network policies; least‑privilege RBAC. Keep evidence for audits and produce attestation reports for changes.

**Checklist**
- Signed images; SBOMs stored; policy checks in CI.
- Audit sinks for API and DB changes; retention policies.
- NetworkPolicy default deny with explicit allows.
- Evidence capture on DR/restore drills and failovers.

**Examples**
- Cosign verification Kyverno policy; block unsigned images.
- Audit logs shipped to central WORM storage.
- NetworkPolicy permitting only app namespaces to DB ports.

---

## 30. Incident Response & Runbooks
Codify detection → diagnosis → mitigation → learning. Keep “first 5 minutes” actions, golden queries, rollback steps, and escalation matrices. Review incidents and fix classes of problems (not just symptoms).

**Checklist**
- Golden dashboards and queries per engine.
- Paging thresholds and runbook links on alerts.
- On‑call rotations; handover template with current risks.
- PIR template with actions/time‑to‑fix and prevention items.

**Examples**
- Runbook: storage pressure → throttle jobs → expand PVC → reindex if needed.
- Runbook: replica lag → identify writer hotspots → fix WAL/Binlog IOPS.
- Mitigation: raise pool limits temporarily with rollback timer.

---

## 31. Chaos & Resilience Testing
Run failure drills: pod/node/zone loss, network partitions, IOPS throttling, backup corruption, and slow disks. Validate alerting and RTO/RPO. Track resilience scores and improvements.

**Checklist**
- Chaos experiments scheduled and tagged to services.
- Synthetic traffic during chaos to emulate production.
- Evidence captured: timings, alerts, dashboards, logs.
- Follow‑up issues created automatically.

**Examples**
- Litmus workflow deleting DB pod; measure failover and client impact.
- `tc qdisc` injecting 100ms latency between app and RO Service.
- FIO limiting IOPS to simulate noisy neighbor.
- Restore drill from last immutable backup into clean namespace.

---

## 32. Multi-Tenancy & Namespace Strategy
Isolate by namespace or cluster depending on compliance and blast radius. Apply ResourceQuotas/LimitRanges; NetworkPolicy default deny; Gatekeeper/Kyverno enforcing labels, owners, and quotas.

**Checklist**
- Per‑tenant quotas for CPU/memory/PVC GiB.
- Owner labels; cost center annotations.
- Default deny NetworkPolicy; explicit allows per app→DB.
- Admission policies for naming and security contexts.

**Examples**
- ResourceQuota limiting PVC total GiB per tenant.
- NetworkPolicy allowing select namespaces to DB Services only.
- Gatekeeper policy requiring `owner.team` and `cost.center` labels.

---

## 33. Cloud-Specific Notes (EKS/AKS/GKE/OKE)
Managed K8s differ in storage, networks, and IAM. Align operator support and verify snapshot semantics, IOPS, and quotas. Document cloud‑specific runbooks for incidents and upgrades.

**Checklist**
- Storage class mapping per cloud with IOPS/throughput guidance.
- IAM integration for ESO/cert-manager and controllers.
- Quota checks for snapshots/PVs/LBs.
- Node image/OS hardening and patch calendars.

**Examples**
- **EKS**: gp3 + IRSA; ALB for app ingress only; EBS snapshots for PVCs.
- **AKS**: Premium/Ultra Disks; workload identity; Azure Files for RWX (careful).
- **GKE**: Balanced/Premium PDs; Filestore for RWX; fleet for multi‑cluster.
- **OKE**: OCI Block Volumes; CSI/IAM policies documented.

---

## 34. Migration Paths to Kubernetes
Migrate incrementally to de‑risk. Start with replicas or non‑critical services; wrap VMs with GitOps for consistency; adopt operators later. Maintain rollback to DBaaS/VM while SLIs stabilize.

**Checklist**
- Phase plan: Read replicas → secondary workloads → primaries.
- Success criteria: SLO stability, chaos pass, DR drill pass.
- Rollback plan and data synchronization strategy.
- Communication plan with downstream teams.

**Examples**
- Lift read replicas first; validate operations; promote during freeze.
- Hybrid: DBaaS primary + K8s replicas for reads and DR practice.
- Sidecar backups/observability on VMs to unify ops before migration.

---

## 35. Common Anti-Patterns to Avoid
Avoid RWX for primary write paths, missing PDBs, CPU limits on primaries, sidecar sprawl, and skipping restore drills. Prevent mixed storage across replicas unless intentional and documented.

**Checklist**
- No mesh sidecars on DB pods unless justified.
- Keep CPU limits off primaries; control via node sizing.
- Test restores regularly; document evidence.
- Don’t skip WAL/binlog isolation for hot workloads.

**Examples**
- Node drain without PDB → quorum loss.
- CPU throttling from strict limits → tail latency spikes.
- RWX PVC for primary data → corruption risk under failover.
- No PITR test in 90 days → audit finding.

---

## 36. Reference Architectures (Per Engine)
Blueprints accelerate consistent deployments. Each includes storage, HA, backups, observability, and security. Treat these as golden paths reviewed quarterly.

**Checklist**
- Postgres: CloudNativePG, WAL on NVMe, pgBackRest, TLS, exporter.
- MySQL: Percona Operator InnoDBCluster, XtraBackup, ProxySQL.
- SQL Server: Single writer + readable replicas, TDE, FULL/DIFF/LOG, exporter.
- MongoDB: Operator ReplicaSet, TLS+KMIP, PITR, exporter.
- Redis: Operator/Sentinel, AOF, redis_exporter.

**Examples**
- **PostgreSQL** (snippet):
  ```yaml
  apiVersion: postgresql.cnpg.io/v1
  kind: Cluster
  metadata: { name: pg-prod, namespace: db }
  spec:
    instances: 3
    storage: { size: 1Ti, storageClass: gp3 }
    walStorage: { size: 200Gi, storageClass: gp3-io }
    superuserSecret: { name: pg-superuser }
    monitoring: { enablePodMonitor: true }
  ```
- **MySQL** (snippet): Percona InnoDBCluster with 3 members + router.
- **SQL Server** (snippet): StatefulSet with PVC RWO, TLS, exporter sidecar.

---

## 37. Repository Templates & Conventions
Standardize repos for speed and safety. Include manifests, charts, policies, migrations, runbooks, and CI. Enforce linters and policy tests; require signed images and CODEOWNERS approvals.

**Checklist**
- Layout with `/k8s/base`, `/k8s/overlays/{dev,stg,prod}`, `/helm`, `/policies`, `/runbooks`, `/migrations`.
- CI: `kubeconform`, `helm lint`, `yamllint`, `kyverno apply`, `cosign verify`.
- Conventional commits and PR templates.
- README with quick start and support matrix.

**Examples**
- Repo tree:
  ```
  /k8s
    /base
    /overlays/{dev,stg,prod}
  /helm/{charts}
  /migrations/{flyway,liquibase}
  /policies/{kyverno}
  /runbooks
  README.md
  ```
- PR template requiring risk assessment and rollback plan.

---

## 38. Appendix: Glossary, Labs & Further Reading
A shared glossary improves collaboration; labs turn theory into operational muscle memory. Keep reading lists short and official. Tie labs to SLOs, DR, and resilience outcomes.

**Checklist**
- Glossary maintained with links to runbooks.
- Labs: storage benchmarks, failover, PITR restore, DR cutover/return.
- Evidence template capturing timings and outcomes.
- Curated reading: official operators, CSI snapshots, GitOps, O11y.

**Examples**
- Glossary: StatefulSet, headless Service, PDB, RWX/RWO, PVC, CSI, WAL, PITR, SLO/SLI.
- Lab 1: fio baseline; record IOPS/latency; compare gp3 vs. NVMe.
- Lab 2: failover under load; measure promotion and client impact.
- Lab 3: PITR into clean namespace; validate data integrity.

---

### Quick Start Snippets (Appendix)

- **Helm install with overlay values:**
  ```bash
  helm upgrade --install pg oci://ghcr.io/cloudnative-pg/charts/cluster \
    -n db --create-namespace -f overlays/prod/values.yaml
  ```

- **Argo CD Application (GitOps):**
  ```yaml
  apiVersion: argoproj.io/v1alpha1
  kind: Application
  metadata: { name: db-platform, namespace: argocd }
  spec:
    project: default
    source: { repoURL: "https://github.com/org/platform", path: "k8s/overlays/prod", targetRevision: main }
    destination: { server: https://kubernetes.default.svc, namespace: db }
    syncPolicy: { automated: { prune: true, selfHeal: true }, syncOptions: ["Validate=true","CreateNamespace=true"] }
  ```

- **PodDisruptionBudget:**
  ```yaml
  apiVersion: policy/v1
  kind: PodDisruptionBudget
  metadata: { name: pg-pdb, namespace: db }
  spec:
    minAvailable: 2
    selector: { matchLabels: { app: pg } }
  ```

- **ExternalSecret (Vault/KMS):**
  ```yaml
  apiVersion: external-secrets.io/v1beta1
  kind: ExternalSecret
  metadata: { name: db-credentials, namespace: db }
  spec:
    secretStoreRef: { kind: ClusterSecretStore, name: vault-prod }
    target: { name: db-secret }
    data:
      - secretKey: DB_PASSWORD
        remoteRef: { key: prod/db/password }
  ```

- **Read/Write split Services:**
  ```yaml
  kind: Service
  apiVersion: v1
  metadata: { name: pg-rw, namespace: db }
  spec:
    selector: { app: pg, role: primary }
    ports: [{ name: postgres, port: 5432, targetPort: 5432 }]
  ---
  kind: Service
  apiVersion: v1
  metadata: { name: pg-ro, namespace: db }
  spec:
    selector: { app: pg, role: replica }
    ports: [{ name: postgres, port: 5432, targetPort: 5432 }]
  ```
