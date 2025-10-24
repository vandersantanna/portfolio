<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# Git, GitHub & GitLab Command Reference for DBE / DBRE / DBA / DataOps
*Quick reference focuses on safe, auditable Git workflows for database-centric teams (DBE/DBRE/DBA/DataOps) across Git, GitHub, and GitLab.*

## Table of Contents
- [1. Purpose & Scope](#1-purpose--scope)
- [2. Repository Layout for Database Projects](#2-repository-layout-for-database-projects)
- [3. Identity, Auth & Security](#3-identity-auth--security)
- [4. Remotes & Collaboration Models](#4-remotes--collaboration-models)
- [5. Branching Strategies for DB Work](#5-branching-strategies-for-db-work)
- [6. Commit Hygiene & Messages](#6-commit-hygiene--messages)
- [7. Tagging & Versioning](#7-tagging--versioning)
- [8. Day-to-Day Git Basics (Cheat Sheet)](#8-day-to-day-git-basics-cheat-sheet)
- [9. Working with Changes](#9-working-with-changes)
- [10. Advanced Navigation & Debugging](#10-advanced-navigation--debugging)
- [11. History Rewrite & Secret Remediation](#11-history-rewrite--secret-remediation)
- [12. Schema Migration Tooling Integration](#12-schema-migration-tooling-integration)
- [13. Release & Change Management](#13-release--change-management)
- [14. Environment & Data Safety](#14-environment--data-safety)
- [15. GitHub — CLI & Platform](#15-github--cli--platform)
- [16. GitLab — CLI & Platform](#16-gitlab--cli--platform)
- [17. CI Templates for Database Pipelines](#17-ci-templates-for-database-pipelines)
- [18. GitOps for Databases (Lightweight)](#18-gitops-for-databases-lightweight)
- [19. Compliance, Audit & Traceability](#19-compliance-audit--traceability)
- [20. Performance & Scale](#20-performance--scale)
- [21. Backup, DR & Mirroring](#21-backup-dr--mirroring)
- [22. Troubleshooting Cookbook](#22-troubleshooting-cookbook)
- [23. Operational Playbooks](#23-operational-playbooks)
- [24. Templates & Snippets (Ready-to-Copy)](#24-templates--snippets-ready-to-copy)
- [25. Appendices](#25-appendices)

---

## 1. Purpose & Scope
This guide distills practical, safe Git habits for DBRE/DBA/DataOps teams, emphasizing auditable changes, rollback-friendly releases, and CI-driven verification for schema and data changes. It assumes bash/PowerShell shells and targets common engines (Oracle, SQL Server, PostgreSQL, MySQL, MongoDB, Redis).

```bash
# Show current Git version and supported features (helps debugging runners/agents)
git --version

# Display detailed Git configuration scope to ensure consistent identity and EOL rules
git config --list --show-origin

# Validate that CLI tools are installed and authenticated (GitHub + GitLab)
gh auth status; glab auth status
```

---

## 2. Repository Layout for Database Projects
A predictable repo layout improves reviewability, CI reuse, and drift detection. Keep schema, migrations, seeds, tools, and CI definitions separate. Use LFS for dumps, avoid committing PII and huge binaries to Git history.

```bash
# Scaffold a DB repo structure
mkdir -p schema/{ddl,dml,views,procs,triggers} migrations seeds tools ci
echo "*.dump filter=lfs diff=lfs merge=lfs -text" >> .gitattributes

# Track large artifacts (dumps/backups) via LFS rather than core Git
git lfs install
git lfs track "*.dump" "*.bak" "*.dmp"

# Verify what's being ignored (prevent accidental commits of data files)
git check-ignore -v seeds/* data/* backups/*
```

---

## 3. Identity, Auth & Security
Configure identity, enable commit signing, and prefer SSH for automation. Use minimal-scoped tokens, protect secrets, and require signed commits on protected branches.

```bash
# Set identity + default branch + signing (GPG or SSH signing)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main

# Example: enable SSH-based signing (Git 2.34+)
git config --global gpg.format ssh
git config --global user.signingkey "$(ssh-add -L | head -n1)"
git config --global commit.gpgsign true

# GitHub: set up auth with gh and store minimal-scope token
gh auth login --hostname github.com --protocol ssh
```

---

## 4. Remotes & Collaboration Models
Standardize origin/upstream naming, clarify forking vs shared-branch models, and lock down push rules for production branches/tags.

```bash
# Clone your fork and add upstream for sync
git clone git@github.com:YOURORG/REPO.git
cd REPO && git remote add upstream git@github.com:UPSTREAMORG/REPO.git

# Sync fork before creating a feature branch
git fetch upstream
git checkout main && git merge --ff-only upstream/main

# Show remotes and their URLs to verify SSH
git remote -v
```

---

## 5. Branching Strategies for DB Work
Use trunk-based or GitFlow variants adapted to migrations. Keep migration order deterministic. Reserve hotfix branches for emergency rollbacks.

```bash
# Create a scoped feature branch for a migration
git checkout -b feat/migration-123-add-index

# For hotfix on production schema
git checkout -b hotfix/rollback-idx-foo-prod origin/release/2025.10

# Keep branches short-lived; rebase or merge based on team policy
git pull --rebase origin main
```

---

## 6. Commit Hygiene & Messages
Small, focused commits ease reviews and rollbacks. Use Conventional Commits to signal schema vs data changes and to generate release notes.

```bash
# Stage by hunk for precise commits (great for mixed DDL/DML changes)
git add -p schema/ migrations/

# Commit with Conventional Commit message
git commit -S -m "feat(schema): add idx on orders.customer_id for nightly reports"

# Amend the last commit safely before push
git commit --amend --no-edit
```

---

## 7. Tagging & Versioning
Use annotated, signed tags for releases, matching deployment windows (e.g., batch windows). Align semantic versions to schema state.

```bash
# Create a signed, annotated tag for a release
git tag -s v1.12.0 -m "Release v1.12.0: Q4 batch migration"

# Push tags explicitly (often required by CI release jobs)
git push origin --tags

# List tags sorted by version for quick audit
git tag -l | sort -V
```

---

## 8. Day-to-Day Git Basics (Cheat Sheet)
Daily essentials: inspect changes, diff intelligently for SQL, and grep across repository history for impacted objects.

```bash
# What changed since last commit?
git status; git diff

# See changes for a file with word-diff (useful for SQL tokens)
git diff --word-diff schema/ddl/orders.sql

# Search history for impacted object references
git grep -n "CREATE INDEX idx_orders_customer"
```

---

## 9. Working with Changes
Stash to switch tasks quickly, use worktrees to parallelize work, and cherry-pick isolated fixes across branches/environments.

```bash
# Stash with a label (e.g., WIP on migration)
git stash push -m "WIP: migration-123 seed data" --include-untracked

# Worktree for validating a hotfix while main stays clean
git worktree add ../REPO-hotfix release/2025.10

# Cherry-pick a fix into the release branch
git cherry-pick <commit-sha>
```

---

## 10. Advanced Navigation & Debugging
Use bisect to find the migration that broke pipelines, reflog to recover lost work, and fsck to validate repo integrity.

```bash
# Binary search the commit that introduced a failing migration
git bisect start
git bisect bad HEAD
git bisect good v1.11.0

# Recover a lost branch tip from reflog
git reflog show --date=iso
git checkout -b rescue/branch <sha-from-reflog>

# Validate repository integrity
git fsck --full
```

---

## 11. History Rewrite & Secret Remediation
If secrets leak, remove them across history and rotate credentials. Coordinate force-pushes and notify consumers.

```bash
# Remove a file across history with git filter-repo (pip install git-filter-repo)
git filter-repo --path secrets.txt --invert-paths

# Replace a leaked token pattern across history
git filter-repo --replace-text <(echo "OLD_TOKEN==>REDACTED")

# Force push after coordinated window (use with extreme caution)
git push --force-with-lease origin main
```

---

## 12. Schema Migration Tooling Integration
Keep migrations deterministic and idempotent; verify checksums and apply order. Store rollback scripts alongside forward changes.

```bash
# Example: generate a timestamped migration (Flyway-style name)
touch migrations/V2025_10_15__add_idx_orders_customer.sql

# Validate migration ordering and pending status in CI (pseudo-check)
git diff --name-only origin/main | grep '^migrations/' || echo "No migration changes"

# Keep forward + rollback together
git add migrations/*_add_idx*.sql migrations/*_rollback_idx*.sql
```

---

## 13. Release & Change Management
Cut release branches prior to windows; freeze changes, tag, and backport hotfixes. Generate release notes from commits and MRs/PRs.

```bash
# Cut a release branch
git checkout -b release/2025.10
git push -u origin release/2025.10

# Generate release notes on GitHub from commits/issues/PRs
gh release create v1.12.0 --generate-notes --target release/2025.10

# Backport a hotfix from main to release
git checkout release/2025.10 && git cherry-pick <sha-from-main>
```

---

## 14. Environment & Data Safety
Never commit PII/raw data; prefer masked/anonymized seeds and LFS for bulky dumps. Enforce ignore rules in CI.

```bash
# Ignore local env and data files
echo -e ".env\n.env.*\ndata/\nbackups/" >> .gitignore

# Pre-commit hook to block large/forbidden file types
echo -e '#!/bin/sh\nexec git diff --cached --name-only | xargs -r file' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

# Verify LFS objects are uploaded before release
git lfs ls-files
```

---

## 15. GitHub — CLI & Platform
Leverage `gh` for PRs, reviews, releases, Actions, and secrets. Protect branches and require signed commits + status checks.

```bash
# Create a PR with reviewers and a title
gh pr create --base main --head feat/migration-123-add-index --title "Add idx on orders.customer_id" --reviewer alice,bob

# Add environment-scoped secret for Actions (e.g., stage)
gh secret set DB_PASSWORD --body "$DB_PASSWORD" --env stage

# Dispatch a workflow (e.g., run migration checks)
gh workflow run migration-check.yml --ref feat/migration-123-add-index
```

---

## 16. GitLab — CLI & Platform
Use `glab` for MRs, releases, variables, and pipelines. Protect branches/tags and set approvals for database changes.

```bash
# Create an MR targeting release branch with labels
glab mr create --source feat/migration-123-add-index --target release/2025.10 --title "Add idx on orders.customer_id" --labels "schema,review-needed"

# Set protected, masked variable for CI (scoped to staging env)
glab variable set DB_PASSWORD --value "$DB_PASSWORD" --masked --environment "staging"

# Trigger pipeline with variables
glab pipeline run --branch feat/migration-123-add-index --variable "CHECKSUM_STRICT=true"
```

---

## 17. CI Templates for Database Pipelines
Automate lint, spin ephemeral DBs, run migrations, and verify rollback; keep artifacts for auditing.

```bash
# Validate .gitlab-ci.yml or GitHub Actions workflow locally (lint via Docker container)
docker run --rm -v "$PWD":/repo -w /repo alpine:3.20 sh -lc "apk add --no-cache yq && yq '.stages' .gitlab-ci.yml"

# Start ephemeral PostgreSQL for pipeline checks
docker run -d --name pg-ci -e POSTGRES_PASSWORD=test -p 5432:5432 postgres:16

# Run a migration check script (example)
psql "postgresql://postgres:test@localhost:5432/postgres" -c "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_customer ON orders(customer_id);"
```

---

## 18. GitOps for Databases (Lightweight)
Use Git as the single source of truth for declarative schema/migration state. Promotion occurs by merging from lower to higher environments with gated approvals.

```bash
# Simulate promotion by fast-forward merge (dev -> stage)
git checkout stage && git merge --ff-only origin/dev && git push origin stage

# Lock production to PR/MR only (branch protection/UI), then release via tag
git tag -s v1.12.1 -m "Prod promotion: stage -> prod"
git push origin v1.12.1

# Export diff between envs to confirm no drift
git diff origin/stage..origin/prod -- migrations/ schema/
```

---

## 19. Compliance, Audit & Traceability
Enforce approvals, signed commits, required checks, and retain evidence (artifacts, logs, SBOMs). Map controls to SOX-like requirements.

```bash
# Require signed commits locally (pre-push hook example)
echo -e '#!/bin/sh\nif ! git log -n1 --pretty=%G? | grep -q "G"; then echo "Commit not signed"; exit 1; fi' > .git/hooks/pre-push && chmod +x .git/hooks/pre-push

# Export MR/PR list for audit
gh pr list --state merged --search "label:schema" --limit 50

# Verify tag signatures for a release train
git tag -v v1.12.0
```

---

## 20. Performance & Scale
Tame large repos with sparse checkout, partial clone, and periodic GC/pack maintenance. Prefer path-based ownership to limit CI scope.

```bash
# Partial clone with blobless objects (faster on CI)
git clone --filter=blob:none --sparse git@github.com:YOURORG/BIGREPO.git
cd BIGREPO && git sparse-checkout set migrations schema

# Periodic optimization
git gc --aggressive --prune=now

# Show repo size contributors (LFS vs non-LFS)
git count-objects -vH
```

---

## 21. Backup, DR & Mirroring
Keep bare-mirror backups and test restores; mirror between platforms for resilience; back up runners/executors configuration too.

```bash
# Create/update a bare mirror for backup
git clone --mirror git@github.com:YOURORG/REPO.git /backups/REPO.git && cd /backups/REPO.git && git remote update --prune

# Restore from a bare mirror
git clone /backups/REPO.git restored-REPO && cd restored-REPO

# Set up push mirror to secondary (requires platform-side config)
git remote add mirror git@gitlab.com:YOURGROUP/REPO.git && git push --mirror mirror
```

---

## 22. Troubleshooting Cookbook
Common pain points: SSH auth, CRLF normalization, submodule/LFS quirks, and detached HEAD states.

```bash
# SSH debug
GIT_SSH_COMMAND="ssh -vvv" git ls-remote origin

# Normalize CRLF across the repo (with care)
echo "* text=auto eol=lf" >> .gitattributes
git add --renormalize . && git commit -m "chore: normalize EOL"

# Fix detached HEAD by creating a branch at current commit
git switch -c rescue/detached-head
```

---

## 23. Operational Playbooks
Standardized, command-first playbooks for high-stress scenarios increase safety and repeatability.

```bash
# (A) Broken migration in prod: identify and revert
git log -p -n 5 migrations/ | less
git revert <sha-of-offending-migration>
gh pr create --title "Revert migration <id>" --body "Rollback due to prod failure"

# (B) Secret leaked to history: remediate + rotate
git filter-repo --replace-text <(echo "SECRET=**REDACTED**")
git push --force-with-lease
# rotate secret in platform afterwards (gh secret set / glab variable set)

# (C) Diverged branches before release: safe sync
git checkout release/2025.10 && git pull --rebase origin release/2025.10
git cherry-pick <sha>  # only the vetted commits
```

---

## 24. Templates & Snippets (Ready-to-Copy)
Drop-in snippets to standardize repos and reviews.

```bash
# .gitignore (DB-focused)
cat > .gitignore <<'EOF'
.env
.env.*
data/
backups/
*.dump
*.dmp
*.bak
*.log
.DS_Store
Thumbs.db
EOF

# .gitattributes (SQL-friendly diffs + EOL)
cat > .gitattributes <<'EOF'
*.sql diff=sql
*.ps1 text eol=crlf
*.sh text eol=lf
*.tf text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.dump filter=lfs diff=lfs merge=lfs -text
* text=auto eol=lf
EOF

# Commit message template (Conventional Commits)
cat > .gitmessage.txt <<'EOF'
<type>(<scope>): <short summary>

Body: rationale, risks, rollout/rollback notes

Refs: <issue/PR/MR IDs>
EOF
git config commit.template .gitmessage.txt
```

---

## 25. Appendices
Concise cheats for Git core, GitHub CLI (`gh`), GitLab CLI (`glab`), and API one-liners useful in audits and automation.

```bash
# Git: quick list
git log --oneline --decorate --graph -n 15
git shortlog -sne --since="90 days ago"
git show --stat v1.12.0

# GitHub CLI (gh): list releases and latest assets
gh release list --limit 10
gh release view v1.12.0 --json assets

# GitLab CLI (glab): show pipelines and latest MR
glab pipeline list --per-page 10
glab mr list --state merged --per-page 10
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
