

# Running Databases on Kubernetes — Engineering Playbook
*Stateful done right: storage, scheduling, security, and operators—without the foot-guns, storage you can trust, failovers you can rehearse, operations you can automate.*

---

## Table of Contents

- [1. Purpose & Audience](#1-purpose--audience)
- [2. When (Not) to Run Databases on Kubernetes](#2-when-not-to-run-databases-on-kubernetes)
- [3. Cluster Architecture for Stateful Workloads](#3-cluster-architecture-for-stateful-workloads)
- [4. Node Classes, Taints/Tolerations & Topology](#4-node-classes-taintstolerations--topology)
- [5. StatefulSets vs. Deployments for Databases](#5-statefulsets-vs-deployments-for-databases)
- [6. Storage Strategy: CSI, PV/PVC & Access Modes](#6-storage-strategy-csi-pvpvc--access-modes)
- [7. Storage Performance & Media Selection](#7-storage-performance--media-selection)
- [8. Database Operators vs. Helm/Kustomize](#8-database-operators-vs-helmkustomize)
- [9. Networking & Service Exposure for Databases](#9-networking--service-exposure-for-databases)
- [10. Service Mesh Considerations (mTLS, Sidecars)](#10-service-mesh-considerations-mtls-sidecars)
- [11. Security Baseline: RBAC, Pod Security, Seccomp](#11-security-baseline-rbac-pod-security-seccomp)
- [12. Secrets & Key Management (Vault/KMS)](#12-secrets--key-management-vaultkms)
- [13. Encryption: At Rest & In Transit (incl. TDE)](#13-encryption-at-rest--in-transit-incl-tde)
- [14. Resource Management: Requests, Limits & QoS](#14-resource-management-requests-limits--qos)
- [15. Scheduling for Performance & Resilience](#15-scheduling-for-performance--resilience)
- [16. High Availability & Failover Patterns](#16-high-availability--failover-patterns)
- [17. Disaster Recovery & Cross-Cluster Designs](#17-disaster-recovery--cross-cluster-designs)
- [18. Backups & Restores: Engine-Native vs. Platform](#18-backups--restores-engine-native-vs-platform)
- [19. Observability: Metrics, Logs, Traces](#19-observability-metrics-logs-traces)
- [20. Query-Level Exporters & DB Health Probes](#20-query-level-exporters--db-health-probes)
- [21. SLOs/SLIs/Error Budgets for Data Platforms](#21-slossliserror-budgets-for-data-platforms)
- [22. CI/CD & GitOps for DB Workloads](#22-cicd--gitops-for-db-workloads)
- [23. Schema Migrations (Flyway/Liquibase) at Scale](#23-schema-migrations-flywayliquibase-at-scale)
- [24. Release Safety: PDBs, Drains & Disruption Budgets](#24-release-safety-pdbs-drains--disruption-budgets)
- [25. DataOps Pipelines around Kubernetes](#25-dataops-pipelines-around-kubernetes)
- [26. Test Data, Ephemeral Environments & Masking](#26-test-data-ephemeral-environments--masking)
- [27. Cost & Capacity Management](#27-cost--capacity-management)
- [28. Compliance, Auditing & Governance](#28-compliance-auditing--governance)
- [29. Incident Response & Runbooks](#29-incident-response--runbooks)
- [30. Chaos & Resilience Testing](#30-chaos--resilience-testing)
- [31. Multi-Tenancy & Namespace Strategy](#31-multi-tenancy--namespace-strategy)
- [32. Cloud-Specific Notes (EKS/AKS/GKE/OKE)](#32-cloud-specific-notes-eksaksgkeoke)
- [33. Migration Paths to Kubernetes](#33-migration-paths-to-kubernetes)
- [34. Common Anti-Patterns to Avoid](#34-common-anti-patterns-to-avoid)
- [35. Reference Architectures (Per Engine)](#35-reference-architectures-per-engine)
- [36. Repository Templates & Conventions](#36-repository-templates--conventions)
- [37. Appendix: Glossary, Labs & Further Reading](#37-appendix-glossary-labs--further-reading)

---

## 1. Purpose & Audience

> **Next steps**: plug these modules into Airflow/Prefect jobs, wrap with CI (pytest), and enable secrets via your target cloud. Extend with migrations (Alembic/Flyway), metrics exporters, and SLO dashboards.

This portfolio targets senior Database Engineers, DBAs, DBREs and DataOps tasked with designing, deploying, and operating databases and data services on Kubernetes. It emphasizes GitOps, security, observability, SLO discipline, and audited automation across environments (on‑prem, hybrid, and multi‑cloud).

**Checklist**
- Clarify ownership (DBA vs. Platform vs. Security).
- Publish SLOs, DR targets, and support matrix.
- Maintain operator/support version calendars.

**Code Examples**
- **YAML — SLO document (Sloth-like):**
  ```yaml
  apiVersion: sloth.slok.dev/v1
  kind: PrometheusServiceLevel
  metadata: { name: db-availability, namespace: db }
  spec:
    service: "postgres-primary"
    slos:
      - name: "availability"
        objective: 99.95
        sli: { events: { errorQuery: "1 - (sum(rate(tcp_connections_accepted_total{job='pg',status='success'}[5m])) / sum(rate(tcp_connections_accepted_total{job='pg'}[5m])))", totalQuery: "1" } }
        alerting: { name: "SLOAvailability", burnRate: [ {window: "2h", threshold: 14}, {window: "24h", threshold: 7} ] }
  ```
- **YAML — Support matrix (fragment):**
  ```yaml
  postgres:
    operator: cloudnativepg>=1.23
    k8s: "1.29"
    storageClass: gp3
    backups: pgBackRest+S3
  ```

---

## 2. When (Not) to Run Databases on Kubernetes
Running DBs on Kubernetes is powerful but conditional. Evaluate IO profile, replication topology, operator maturity, team expertise, and whether DBaaS better serves SLAs and compliance. Start with replicas/non‑critical workloads, prove operations, then cut over primaries.

**Checklist**
- fio/pgbench/sysbench baselines.
- Operator feature parity (PITR, TLS/TDE, upgrades).
- Dedicated DB nodes (NVMe for hot primaries).
- Proved failover/backup/restore under load.

**Code Examples**
- **pgbench baseline:**
  ```bash
  pgbench -i -s 50 "host=pg-rw dbname=bench user=pgbench sslmode=require"
  pgbench -c 64 -j 8 -T 600 "host=pg-rw dbname=bench user=pgbench sslmode=require"
  ```
- **fio random RW:**
  ```bash
  fio --name=randrw --filename=/nvme/test --ioengine=libaio --direct=1 \
      --rw=randrw --bs=4k --rwmixread=70 --size=20G --iodepth=64 --runtime=120 --numjobs=4
  ```

---

## 3. Cluster Architecture for Stateful Workloads
Separate control plane and workers; use multi‑zone pools; standardize add‑ons (CNI, CSI, metrics, logging, DNS). Keep versions within supported windows; run rehearsed upgrade playbooks with maintenance windows and disruption controls.

**Checklist**
- CNI (Calico/Cilium), CoreDNS + NodeLocal DNSCache.
- CSI with snapshots/expansion; metrics-server.
- Version skew policy (N‑1) for K8s/operators.

**Code Examples**
- **Install NodeLocal DNSCache (Helm):**
  ```bash
  helm repo add deliveryhero https://charts.deliveryhero.io/
  helm upgrade --install nodelocaldns deliveryhero/node-local-dns --namespace kube-system
  ```
- **metrics-server (Helm):**
  ```bash
  helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
  helm upgrade --install metrics-server metrics-server/metrics-server -n kube-system
  ```

---

## 4. Node Classes, Taints/Tolerations & Topology
Use dedicated node pools for DBs. Pin pods via taints/tolerations and affinities. Spread replicas across zones using topology constraints. Prefer memory‑rich, NVMe‑backed nodes for primaries.

**Checklist**
- Labels (e.g., `workload=db`, `storage=nvme`).
- Taints on DB nodes; tolerations on DB pods.
- Topology spread across zones.

**Code Examples**
- **Taint/labels:**
  ```bash
  kubectl label nodes ip-10-0-1-10 workload=db storage=nvme
  kubectl taint nodes ip-10-0-1-10 db=yes:NoSchedule
  ```
- **Topology spread:**
  ```yaml
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
      labelSelector: { matchLabels: { app: "postgres" } }
  ```

---

## 5. StatefulSets vs. Deployments for Databases
StatefulSets provide stable identities, PVs, and ordered rollouts; headless Services give deterministic DNS per replica. Use Deployments for stateless adjacents (exporters, poolers).

**Checklist**
- StatefulSets for engines/quorum systems.
- Headless Services (`clusterIP: None`).
- Ordered rollouts.

**Code Examples**
- **Postgres StatefulSet (fragment):**
  ```yaml
  apiVersion: apps/v1
  kind: StatefulSet
  metadata: { name: pg }
  spec:
    serviceName: "pg"
    replicas: 3
    selector: { matchLabels: { app: pg } }
    template:
      metadata: { labels: { app: pg } }
      spec:
        containers:
        - name: postgres
          image: ghcr.io/cloudnative-pg/postgresql:16
          volumeMounts: [{ name: data, mountPath: /var/lib/postgresql/data }]
    volumeClaimTemplates:
    - metadata: { name: data }
      spec:
        accessModes: ["ReadWriteOnce"]
        resources: { requests: { storage: 1Ti } }
  ```
- **Headless Service:**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata: { name: pg }
  spec: { clusterIP: None, selector: { app: pg }, ports: [{ name: pg, port: 5432 }] }
  ```

---

## 6. Storage Strategy: CSI, PV/PVC & Access Modes
Map engine IO to storage classes; prefer RWO for primaries; use RWX carefully for tooling. Enable volume expansion and snapshots. Choose filesystem vs. block per engine guidance.

**Checklist**
- StorageClass with `allowVolumeExpansion`.
- `WaitForFirstConsumer` binding.
- VolumeSnapshotClass `Retain` policy.

**Code Examples**
- **StorageClass (EKS gp3):**
  ```yaml
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata: { name: gp3 }
  provisioner: ebs.csi.aws.com
  volumeBindingMode: WaitForFirstConsumer
  allowVolumeExpansion: true
  parameters: { type: "gp3", iops: "6000", throughput: "250" }
  ```
- **SnapshotClass:**
  ```yaml
  apiVersion: snapshot.storage.k8s.io/v1
  kind: VolumeSnapshotClass
  metadata: { name: csi-snap }
  driver: ebs.csi.aws.com
  deletionPolicy: Retain
  ```

---

## 7. Storage Performance & Media Selection
Storage is commonly the bottleneck. Use NVMe/local PVs or high‑IOPS SSDs; separate hot logs; tune filesystem; benchmark with fio; monitor saturation and latency percentiles.

**Checklist**
- fio baselines; mount options (noatime).
- Separate WAL/redo and temp where useful.
- Alert on disk latency p95/p99.

**Code Examples**
- **Mount XFS with noatime:**
  ```bash
  mount -o noatime,nodiratime /dev/nvme0n1 /var/lib/postgresql
  ```
- **Dedicated WAL PVC (fragment):**
  ```yaml
  volumeMounts:
    - { name: wal, mountPath: /var/lib/postgresql/wal }
  ```

---

## 8. Database Operators vs. Helm/Kustomize
Operators encode day‑2 ops; Helm/Kustomize compose policies and overlays. Combine both: operator CRs for lifecycle; Helm for surrounding services and policy bundles.

**Checklist**
- Track operator/e2e features.
- CRs committed via GitOps.
- Backups and monitoring in CRs.

**Code Examples**
- **CloudNativePG Cluster:**
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
- **Kustomize overlay (values patch):**
  ```yaml
  apiVersion: kustomize.config.k8s.io/v1beta1
  kind: Kustomization
  resources: ["../../base"]
  patches:
    - target: { kind: Cluster, name: pg-prod }
      patch: |-
        - op: replace
          path: /spec/storage/size
          value: 2Ti
  ```

---

## 9. Networking & Service Exposure for Databases
Prefer east‑west ClusterIP/headless. Use LoadBalancer only when external access is required; restrict via firewall/allowlist and enforce TLS. Consider session affinity for legacy clients; deploy NodeLocal DNSCache to reduce latency spikes.

**Checklist**
- RW/RO Services; health‑checked poolers.
- TLS end‑to‑end.
- Avoid ingress in front of DBs.

**Code Examples**
- **RW/RO Services:**
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
- **Session affinity:**
  ```yaml
  spec:
    sessionAffinity: ClientIP
  ```

---

## 10. Service Mesh Considerations (mTLS, Sidecars)
Meshes provide mTLS/policy but add latency. Prefer client‑side TLS or selective/ambient mesh modes; exclude DB pods from sidecars unless mandated and tested.

**Checklist**
- Exclude DB pods from injection.
- Enforce mTLS in app tiers.
- Measure latency impact.

**Code Examples**
- **Disable injection for DB namespace:**
  ```bash
  kubectl label ns db istio-injection=disabled --overwrite
  ```
- **Istio PeerAuthentication (STRICT mTLS for apps):**
  ```yaml
  apiVersion: security.istio.io/v1beta1
  kind: PeerAuthentication
  metadata: { name: app-mtls, namespace: app }
  spec: { mtls: { mode: STRICT } }
  ```

---

## 11. Security Baseline: RBAC, Pod Security, Seccomp
Apply least‑privilege RBAC and Pod Security Admission (`restricted`); require signed images; use seccomp/AppArmor and read‑only root FS; avoid root users.

**Checklist**
- Non‑root pods; `RuntimeDefault` seccomp.
- Split duties in RBAC.
- Image signature verification.

**Code Examples**
- **Pod securityContext:**
  ```yaml
  securityContext:
    runAsUser: 999
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
    seccompProfile: { type: RuntimeDefault }
  ```
- **Kyverno policy — require Cosign signatures:**
  ```yaml
  apiVersion: kyverno.io/v1
  kind: ClusterPolicy
  metadata: { name: require-signed-images }
  spec:
    rules:
      - name: verify-image
        match: { resources: { kinds: ["Pod"] } }
        verifyImages:
          - image: "ghcr.io/*"
            key: "cosign.pub"
  ```

---

## 12. Secrets & Key Management (Vault/KMS)
Centralize secrets in Vault/KMS and sync via External Secrets Operator; rotate keys; automate TLS via cert‑manager. Audit access and avoid literals in manifests.

**Checklist**
- ESO + ClusterSecretStore.
- Rotation schedules; short TTLs.
- Access audit and separation of duties.

**Code Examples**
- **ExternalSecret:**
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
- **cert-manager Issuer (Vault):**
  ```yaml
  apiVersion: cert-manager.io/v1
  kind: ClusterIssuer
  metadata: { name: vault-issuer }
  spec:
    vault:
      server: https://vault.example.com
      path: pki/sign/cluster
      auth:
        kubernetes:
          mountPath: /v1/auth/kubernetes
          role: cert-manager
  ```

---

## 13. Encryption: At Rest & In Transit (incl. TDE)
Use layered encryption: storage‑level, engine‑native (TDE), and TLS. Validate cipher suites; rotate certs; test cold restores with encrypted backups and keep key provenance.

**Checklist**
- Storage encryption default on.
- Engine TDE where applicable.
- TLS 1.2+; no legacy ciphers.

**Code Examples**
- **Postgres `postgresql.conf` (fragment):**
  ```conf
  ssl = on
  ssl_min_protocol_version = 'TLSv1.2'
  ssl_ciphers = 'HIGH:!aNULL:!MD5'
  ```
- **SQL Server TDE (T‑SQL):**
  ```sql
  USE master;
  CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongPass!';
  CREATE CERTIFICATE TDECert WITH SUBJECT = 'TDE Certificate';
  USE MyDB;
  CREATE DATABASE ENCRYPTION KEY
    WITH ALGORITHM = AES_256 ENCRYPTION BY SERVER CERTIFICATE TDECert;
  ALTER DATABASE MyDB SET ENCRYPTION ON;
  ```

---

## 14. Resource Management: Requests, Limits & QoS
Right‑size CPU/memory; avoid CPU limits on primaries; guarantee memory; keep sidecars minimal; consider hugepages for engines that benefit.

**Checklist**
- Memory requests=limits for critical DBs.
- No CPU limits on primaries (use node sizing).
- Headroom on DB nodes.

**Code Examples**
- **Guaranteed QoS (fragment):**
  ```yaml
  resources:
    requests: { cpu: "8", memory: "64Gi" }
    limits:   { memory: "64Gi" }
  ```
- **HugePages:**
  ```yaml
  resources: { limits: { hugepages-2Mi: "2Gi" } }
  ```

---

## 15. Scheduling for Performance & Resilience
Distribute replicas across zones; protect with PDBs and PriorityClasses; coordinate node drains with autoscalers and rollouts.

**Checklist**
- Anti‑affinity for replicas.
- `maxUnavailable: 0` for primaries.
- PriorityClasses for DBs.

**Code Examples**
- **Anti‑affinity:**
  ```yaml
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector: { matchLabels: { app: pg } }
        topologyKey: topology.kubernetes.io/zone
  ```
- **PriorityClass:**
  ```yaml
  apiVersion: scheduling.k8s.io/v1
  kind: PriorityClass
  metadata: { name: db-critical }
  value: 100000
  preemptionPolicy: PreemptLowerPriority
  ```

---

## 16. High Availability & Failover Patterns
Pick replication style (sync/async, quorum). Automate elections and fencing; ensure clients retry and are idempotent. Test failovers under realistic load and measure promotion/catch‑up times.

**Checklist**
- Document topology/quorum rules.
- Health checks for lag/write availability.
- Client‑side retries with backoff/jitter.

**Code Examples**
- **Patroni (fragment):**
  ```yaml
  bootstrap:
    dcs:
      postgresql:
        parameters: { wal_level: replica, max_wal_senders: 10 }
      synchronous_mode: true
  ```
- **HAProxy for RW/RO routing:**
  ```cfg
  frontend pg
    bind *:5432
    default_backend pg-backend
  backend pg-backend
    option httpchk GET /health
    server primary pg-0.pg.db.svc.cluster.local:5432 check
    server replica1 pg-1.pg.db.svc.cluster.local:5432 check backup
  ```

---

## 17. Disaster Recovery & Cross-Cluster Designs
Design for regional failure: async replication to DR cluster, immutable backups, scripted cutover/return, and secrets rotation. Practice and record evidence.

**Checklist**
- DR cluster pre‑provisioned and secrets synced.
- Cross‑region backup replication.
- DNS/app cutover runbook.

**Code Examples**
- **WAL‑G env (ConfigMap):**
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata: { name: wal-g-env, namespace: db }
  data:
    WALG_S3_PREFIX: s3://bucket/pg/walg
    AWS_REGION: us-east-1
  ```
- **Restore Job (fragment):**
  ```yaml
  apiVersion: batch/v1
  kind: Job
  metadata: { name: pg-restore }
  spec:
    template:
      spec:
        containers:
        - name: restore
          image: ghcr.io/wal-g/wal-g
          envFrom: [{ configMapRef: { name: wal-g-env } }]
          command: ["wal-g","backup-fetch","/var/lib/postgresql/data","LATEST"]
        restartPolicy: Never
  ```

---

## 18. Backups & Restores: Engine-Native vs. Platform
Use engine‑native for consistency/PITR; platform snapshots for speed. Validate restores and measure RTO; keep immutable retention and alerts for failures/lag.

**Checklist**
- Full/incremental schedules; PITR.
- Immutable object storage (WORM).
- Regular restore drills.

**Code Examples**
- **pgBackRest (fragment):**
  ```bash
  pgbackrest --stanza=pg --type=full backup
  pgbackrest --stanza=pg --type=diff backup
  pgbackrest --stanza=pg restore --type=time "--target=2025-10-10 12:00:00"
  ```
- **Velero CSI snapshot:**
  ```bash
  velero backup create db-snap --include-namespaces db --snapshot-volumes
  ```

---

## 19. Observability: Metrics, Logs, Traces
Expose DB + K8s metrics; centralize logs; trace critical flows. Build SLO‑aligned dashboards and alert on burn rates and saturation, not single spikes.

**Checklist**
- Prometheus scrapes; exporters and poolers.
- Grafana with availability/latency/saturation panels.
- Loki/ELK with structured labels.

**Code Examples**
- **PrometheusRule (replica lag):**
  ```yaml
  groups:
  - name: db.rules
    rules:
    - alert: PostgresReplicaLagHigh
      expr: pg_replication_lag_seconds > 10
      for: 5m
      labels: { severity: critical }
      annotations: { runbook: "runbooks/replica-lag.md" }
  ```
- **Loki labels (example pod annotations):**
  ```yaml
  metadata:
    labels: { app: pg, role: primary }
    annotations: { loki.grafana.com/log-format: "json" }
  ```

---

## 20. Query-Level Exporters & DB Health Probes
Use engine‑specific exporters and calibrated probes; avoid restarts during recovery by setting generous initial delays and thresholds; monitor poolers.

**Checklist**
- Exporters with curated collectors.
- Probes using engine tools (pg_isready/mysqladmin).
- Pooler metrics.

**Code Examples**
- **Readiness probe:**
  ```yaml
  readinessProbe:
    exec: { command: ["bash","-lc","pg_isready -U postgres -h 127.0.0.1"] }
    initialDelaySeconds: 60
    periodSeconds: 10
    failureThreshold: 6
  ```
- **mysqld_exporter (args):**
  ```yaml
  args: ["--collect.info_schema.processlist", "--collect.engine_innodb_status"]
  ```

---

## 21. SLOs/SLIs/Error Budgets for Data Platforms
Define SLIs (availability, latency, freshness) and SLOs; attach burn‑rate alerts; gate risky releases with budget consumption; review weekly.

**Checklist**
- SLIs and formulas documented.
- Burn‑rate alerts (2h/24h).
- Release gating on budget health.

**Code Examples**
- **Sloth SLO (latency):**
  ```yaml
  slos:
    - name: "latency"
      objective: 99.0
      sli:
        raw:
          errorRatioQuery: |
            sum(rate(db_query_latency_bucket{le="0.1"}[5m])) / sum(rate(db_query_latency_count[5m]))
  ```
- **Prometheus burn rate (example):**
  ```yaml
  expr: (increase(error_ratio[2h]) / (2*3600)) > (1 - 0.9995)
  ```

---

## 22. CI/CD & GitOps for DB Workloads
Everything in Git; Argo CD/Flux for reconciling; policy checks; image signatures; overlays and promotion flows; controlled windows for DB tiers.

**Checklist**
- Pre‑merge: kubeconform/helm lint/policy tests.
- Cosign verify; provenance attestation.
- Drift detection/self‑heal with maintenance windows.

**Code Examples**
- **Argo CD Application:**
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
- **GitHub Action (fragment) with cosign:**
  ```yaml
  - name: Verify signatures
    run: cosign verify --key cosign.pub ghcr.io/org/db-image@${{ steps.meta.outputs.digest }}
  ```

---

## 23. Schema Migrations (Flyway/Liquibase) at Scale
Forward‑only, backward‑compatible; feature flags; batch backfills; roll‑forward plans; gate heavy DDL with performance windows and lock‑avoidance tactics.

**Checklist**
- Versioned migrations; immutable artifacts.
- Statement/lock timeout & plan checks.
- Backfill throttling.

**Code Examples**
- **Flyway CLI:**
  ```bash
  flyway -url=jdbc:postgresql://pg-rw/db -user=ci -password=$PASS -locations=filesystem:migrations migrate
  ```
- **Liquibase preConditions:**
  ```yaml
  preConditions:
    - onFail: HALT
      not:
        tableExists: { tableName: "new_table" }
  ```

---

## 24. Release Safety: PDBs, Drains & Disruption Budgets
Keep quorum with PDBs; coordinate drains/autoscaling; set `maxUnavailable: 0` for primaries; test rollouts in staging; log disruptive actions.

**Checklist**
- PDB per role; checks before drains.
- Maintenance windows playbook.
- Autoscaler coordination.

**Code Examples**
- **PDB:**
  ```yaml
  apiVersion: policy/v1
  kind: PodDisruptionBudget
  metadata: { name: pg-pdb, namespace: db }
  spec: { minAvailable: 2, selector: { matchLabels: { app: pg } } }
  ```
- **Drain script (bash fragment):**
  ```bash
  kubectl cordon "$NODE"
  kubectl get pdb -n db
  kubectl drain "$NODE" --ignore-daemonsets --delete-emptydir-data --grace-period=60
  ```

---

## 25. DataOps Pipelines around Kubernetes
Integrate ingestion/transformations/quality/lineage with K8s‑hosted DBs; coordinate with replication lag and backup windows; enforce data contracts for downstream reliability.

**Checklist**
- Orchestrator integrated with SLO checks.
- dbt + Great Expectations gates.
- Lineage capture (OpenLineage).

**Code Examples**
- **Airflow DAG skeleton:**
  ```python
  with DAG("etl_daily", schedule="@daily") as dag:
      start = EmptyOperator(task_id="start")
      ingest = BashOperator(task_id="ingest", bash_command="python src/ingest.py")
      transform = BashOperator(task_id="dbt", bash_command="dbt run --profiles-dir .")
      test = BashOperator(task_id="dq", bash_command="great_expectations checkpoint run dq.yml")
      start >> ingest >> transform >> test
  ```
- **Argo Workflow snapshot step (fragment):**
  ```yaml
  - name: snapshot-db
    container:
      image: bitnami/kubectl
      command: ["kubectl","create","volumesnapshot","pg-data-snap","--source-pvc=pg-data-0"]
  ```

---

## 26. Test Data, Ephemeral Environments & Masking
Create ephemeral namespaces per PR with masked datasets; snapshot/clone PVCs; destroy on merge; enforce TTLs and quotas to control costs.

**Checklist**
- VolumeSnapshot cloning.
- Deterministic masking to preserve joins.
- TTL controller for cleanup.

**Code Examples**
- **Kustomize set image tag:**
  ```bash
  kustomize edit set image repo/app:$(git rev-parse --short HEAD)
  ```
- **VolumeSnapshot + clone (fragment):**
  ```yaml
  apiVersion: snapshot.storage.k8s.io/v1
  kind: VolumeSnapshot
  metadata: { name: pg-snap }
  spec: { source: { persistentVolumeClaimName: pg-data-0 } }
  ```

---

## 27. Cost & Capacity Management
Make costs observable; right‑size nodes/storage; avoid over‑provisioned IOPS; consolidate replicas; use reserved/committed instances for steady loads; keep burst headroom.

**Checklist**
- Kubecost/provider cost mapping by labels.
- Storage tiers by IO profile.
- Periodic rightsizing reviews.

**Code Examples**
- **Cost labels/annotations:**
  ```yaml
  metadata:
    labels: { owner.team: "dbre" }
    annotations: { cost.center: "data-platform" }
  ```
- **Kubecost helm (fragment):**
  ```bash
  helm repo add kubecost https://kubecost.github.io/cost-analyzer/
  helm upgrade --install kubecost kubecost/cost-analyzer -n kubecost --create-namespace
  ```

---

## 28. Compliance, Auditing & Governance
Map to CIS/Kubernetes Benchmarks and data laws (LGPD/GDPR/PCI/HIPAA). Enforce signed images, audit trails, immutable backups, default deny networks, and least‑privilege RBAC.

**Checklist**
- Image signing & SBOMs; policy checks.
- Audit sinks; retention policies.
- NetworkPolicy default deny.

**Code Examples**
- **Kyverno — block unsigned:**
  ```yaml
  apiVersion: kyverno.io/v1
  kind: ClusterPolicy
  metadata: { name: block-unsigned }
  spec:
    validationFailureAction: Enforce
    rules:
      - name: require-signature
        match: { resources: { kinds: ["Pod"] } }
        verifyImages:
          - image: "ghcr.io/*"
            key: "cosign.pub"
  ```
- **NetworkPolicy default deny:**
  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata: { name: default-deny, namespace: db }
  spec: { podSelector: {}, policyTypes: ["Ingress","Egress"] }
  ```

---

## 29. Incident Response & Runbooks
Codify detection→diagnosis→mitigation→learning with runbooks, golden dashboards/queries, rollback steps, and escalation matrices. Practice and iterate.

**Checklist**
- “First 5 minutes” actions.
- Paging thresholds with runbook links.
- PIR template and follow‑ups.

**Code Examples**
- **Runbook template (Markdown):**
  ```markdown
  # Incident: <summary>
  ## First 5 minutes
  - Check alert dashboard link
  - Identify scope and impacted SLO
  ## Mitigation
  - Steps taken (with timestamps)
  ## Root cause & actions
  - Immediate, short-term, long-term
  ```
- **Alert annotation with runbook:**
  ```yaml
  annotations: { runbook: "https://git.example/runbooks/replica-lag.md" }
  ```

---

## 30. Chaos & Resilience Testing
Run controlled failures (pod/node/zone loss, network partitions, IOPS throttling). Validate that alerts fire and SLOs hold; record evidence and improvements.

**Checklist**
- Chaos experiments scheduled.
- Synthetic traffic during tests.
- Evidence capture.

**Code Examples**
- **LitmusChaos experiment (fragment):**
  ```yaml
  apiVersion: litmuschaos.io/v1alpha1
  kind: ChaosEngine
  metadata: { name: db-pod-kill, namespace: db }
  spec:
    appinfo: { appns: db, applabel: "app=pg", appkind: statefulset }
    experiments: [{ name: pod-delete }]
  ```
- **`tc` latency injection:**
  ```bash
  tc qdisc add dev eth0 root netem delay 100ms 20ms distribution normal
  ```

---

## 31. Multi-Tenancy & Namespace Strategy
Isolate by namespace/cluster based on compliance and blast radius. Apply ResourceQuotas/LimitRanges; default deny NetworkPolicies; enforce labels/owners/quotas with Gatekeeper/Kyverno.

**Checklist**
- Per‑tenant quotas and labels.
- Default deny networks.
- Admission policies for security contexts.

**Code Examples**
- **ResourceQuota:**
  ```yaml
  apiVersion: v1
  kind: ResourceQuota
  metadata: { name: tenant-a, namespace: tenant-a }
  spec:
    hard: { requests.cpu: "32", requests.memory: "128Gi", requests.storage: "5Ti" }
  ```
- **Gatekeeper policy (labels required):**
  ```yaml
  apiVersion: constraints.gatekeeper.sh/v1beta1
  kind: K8sRequiredLabels
  metadata: { name: require-owner-team }
  spec:
    match: { kinds: [{ apiGroups: [""], kinds: ["Namespace"] }] }
    parameters: { labels: ["owner.team","cost.center"] }
  ```

---

## 32. Cloud-Specific Notes (EKS/AKS/GKE/OKE)
Managed K8s differ in storage, load balancers, and IAM. Below are reinforced patterns and concrete code per cloud provider for DB workloads.

**Checklist**
- Map StorageClasses to IO profiles.
- Configure workload identities (IRSA/Workload Identity).
- Verify snapshot semantics/quotas per cloud.

**Code Examples**
- **AWS EKS**
  - StorageClass (gp3 with IOPS/throughput):
    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata: { name: gp3 }
    provisioner: ebs.csi.aws.com
    allowVolumeExpansion: true
    volumeBindingMode: WaitForFirstConsumer
    parameters: { type: "gp3", iops: "9000", throughput: "500" }
    ```
  - IRSA (ServiceAccount with IAM role):
    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: db-eso
      namespace: db
      annotations:
        eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/eso-s3-role
    ```
  - `eksctl` nodegroup (NVMe optimized):
    ```bash
    eksctl create nodegroup --cluster my-eks --name db-nvme --instance-types c6id.4xlarge \
      --nodes 3 --nodes-min 3 --nodes-max 6 --node-labels workload=db,storage=nvme --node-taints db=yes:NoSchedule
    ```
- **Azure AKS**
  - Ultra Disk StorageClass:
    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata: { name: ultra }
    provisioner: disk.csi.azure.com
    parameters: { skuname: UltraSSD_LRS }
    allowVolumeExpansion: true
    volumeBindingMode: WaitForFirstConsumer
    ```
  - Workload Identity ServiceAccount:
    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: db-eso
      namespace: db
      annotations:
        azure.workload.identity/client-id: "00000000-0000-0000-0000-000000000000"
    ```
  - `az` create nodepool (with labels/taints):
    ```bash
    az aks nodepool add -g rg -n dbpool -c 3 --cluster-name my-aks \
      --node-vm-size Standard_E8ads_v5 --labels workload=db storage=ultra --node-taints db=yes:NoSchedule
    ```
- **Google GKE**
  - Premium PD StorageClass:
    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata: { name: premium-rwo }
    provisioner: pd.csi.storage.gke.io
    parameters: { type: "pd-ssd" }
    volumeBindingMode: WaitForFirstConsumer
    allowVolumeExpansion: true
    ```
  - Workload Identity (ServiceAccount binding):
    ```bash
    gcloud iam service-accounts add-iam-policy-binding \
      db-eso@project.iam.gserviceaccount.com \
      --role roles/iam.workloadIdentityUser \
      --member "serviceAccount:project.svc.id.goog[db/eso]"
    ```
  - `gcloud` node pool with local SSD:
    ```bash
    gcloud container node-pools create db-nvme --cluster my-gke --num-nodes 3 \
      --machine-type c3-highmem-8 --local-ssd-count 2 --node-labels workload=db,storage=nvme \
      --node-taints db=yes:NoSchedule
    ```
- **Oracle OKE**
  - Block Volume StorageClass (High Perf):
    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata: { name: oci-highperf }
    provisioner: blockvolume.csi.oraclecloud.com
    parameters: { vpusPerGB: "30" }
    allowVolumeExpansion: true
    volumeBindingMode: WaitForFirstConsumer
    ```
  - OCI dynamic group + policy (conceptual):
    ```bash
    oci iam dynamic-group create --name db-eso --matching-rule "ALL {instance.compartment.id = 'ocid1.compartment.oc1..aaaa'}"
    oci iam policy create --name eso-policy --statements "[\"Allow dynamic-group db-eso to manage objects in compartment data\"]"
    ```
  - `oci` create nodepool with labels/taints:
    ```bash
    oci ce node-pool create --cluster-id ocid1.cluster.oc1... --name dbpool --initial-node-labels '[{"key":"workload","value":"db"}]' \
      --node-shape VM.Standard3.Flex --node-shape-config '{"ocpus":8,"memoryInGBs":64}' --quantity-per-subnet 3
    ```

---

## 33. Migration Paths to Kubernetes
Migrate incrementally: start with replicas or non‑critical engines; unify ops (backups/observability) via sidecars even on VMs; adopt operators after SLO stability. Maintain rollback path to DBaaS/VM until steady.

**Checklist**
- Phase plan & success criteria.
- Rollback and sync strategies.
- Communication plan.

**Code Examples**
- **Kustomize “feature gate” patch (blue/green cutover):**
  ```yaml
  patches:
    - target: { kind: Service, name: pg-rw }
      patch: |-
        - op: replace
          path: /spec/selector/role
          value: primary-new
  ```
- **Argo Rollout pause (script fragment):**
  ```bash
  argocd app pause db-platform && sleep 300 && argocd app resume db-platform
  ```

---

## 34. Common Anti-Patterns to Avoid
Avoid RWX for primary data paths, missing PDBs, CPU limits on primaries, sidecar sprawl, skipping restore drills, and mixing storage heterogeneously across replicas.

**Checklist**
- No mesh sidecars on DB pods unless proven.
- No CPU limits on primaries.
- Regular PITR/DR drills.

**Code Examples**
- **Bad vs Good (CPU limits):**
  ```yaml
  # BAD
  limits: { cpu: "4", memory: "32Gi" }
  # GOOD
  requests: { cpu: "8", memory: "64Gi" }
  limits:   { memory: "64Gi" }
  ```
- **Bad RWX vs Good RWO:**
  ```yaml
  # BAD for primary data
  accessModes: ["ReadWriteMany"]
  # GOOD
  accessModes: ["ReadWriteOnce"]
  ```

---

## 35. Reference Architectures (Per Engine)
Golden paths per engine covering storage/HA/backups/observability/security; review quarterly and adapt to compliance and performance needs.

**Checklist**
- Postgres (CloudNativePG), MySQL (Percona), SQL Server, MongoDB, Redis.
- TLS, TDE (where applicable), PITR, exporters, dashboards.

**Code Examples**
- **PostgreSQL (CloudNativePG fragment):**
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
- **MySQL (Percona InnoDBCluster fragment):**
  ```yaml
  apiVersion: pxc.percona.com/v1-11-0
  kind: PerconaXtraDBCluster
  metadata: { name: mysql-prod, namespace: db }
  spec: { pxc: { size: 3 }, haproxy: { enabled: true } }
  ```

---

## 36. Repository Templates & Conventions
Standardize repos for speed/safety: manifests, charts, policies, migrations, runbooks, CI. Enforce linters/policy tests; sign images; require CODEOWNERS approvals.

**Checklist**
- `/k8s/base`, `/k8s/overlays/{dev,stg,prod}`, `/helm`, `/policies`, `/runbooks`, `/migrations`.
- CI: kubeconform, helm lint, kyverno, cosign.
- Conventional commits; PR templates.

**Code Examples**
- **Repo tree:**
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
- **PR template (fragment):**
  ```markdown
  - Risk level: Low/Med/High
  - Rollback plan:
  - Evidence links (dashboards/runbooks):
  ```

---

## 37. Appendix: Glossary, Labs & Further Reading
Glossary improves shared language; labs build operational muscle; reading list stays short and official. Tie labs to SLO, DR, and resilience outcomes with evidence capture.

**Checklist**
- Glossary with links to runbooks.
- Labs: fio baselines, failover, PITR, DR cutover/return.
- Evidence template with timings/outcomes.

**Code Examples**
- **Lab Makefile (fragment):**
  ```makefile
  bench:
  	fio --name=randrw --filename=/nvme/test --ioengine=libaio --direct=1 --rw=randrw --bs=4k --rwmixread=70 --size=20G --iodepth=64 --runtime=120 --numjobs=4
  failover:
  	kubectl delete pod -l app=pg,role=primary -n db
  restore:
  	velero restore create --from-backup db-snap
  ```
- **Glossary (snippet):**
  ```markdown
  - **PDB**: PodDisruptionBudget — ensures minimum pods during disruptions.
  - **RWO/RWX**: ReadWriteOnce/ReadWriteMany access modes for PVCs.
  - **PITR**: Point-In-Time Recovery.
  ```

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
