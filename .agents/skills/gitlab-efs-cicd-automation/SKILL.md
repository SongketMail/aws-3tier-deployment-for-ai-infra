---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "GitLab CI/CD & EFS Storage Skill"
timestamp: 2026-08-05T22:01:00Z
topics: ["aws", "cloud", "architecture", "skill", "gitlab", "cicd", "efs", "nfs", "nginx", "podman", "onprem"]
description: "Guidelines for implementing GitLab CI/CD pipelines, mounting shared AWS EFS storage, tuning NFS mounts, and configuring dynamic Nginx paths."
name: "gitlab-efs-cicd-automation"
---
# GitLab CI/CD & EFS Storage Skill

This skill governs automated application deployment pipelines, mounting persistent Amazon EFS volumes, optimizing Nginx caching parameters, and managing rootless containerized on-premises infrastructures.

---

## 1. GitLab CI/CD & Shared Storage Mounting

- **Pipeline Deployments & Hardening:** Configure GitLab runner pipelines to automatically deploy applications to Auto Scaling Groups and Standalone instances. All deployment/destruction Bash utilities enforce success checks on directory navigation (`cd ... || exit 1`) and use robust variables (as per **Item 2**).
- **Shared Storage:** Mount Amazon Elastic File System (EFS) across all web nodes in the ASG on paths like `/var/www/shared/` to provide immediate, concurrent file sync across scaled instances.
- Ensure EFS target permissions are maintained, and set NFS mount options to `rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport`.

---

## 2. Nginx Path & Metadata Tuning

- **Nginx Config:** Configure Nginx server paths to map static assets directly to the mounted EFS directory.
- **Performance Optimisation:** EFS file operations can introduce latency on metadata-heavy workflows. Tune Nginx using `open_file_cache` directives to cache file descriptors locally and prevent high EFS query rates:
  ```nginx
  open_file_cache max=1000 inactive=20s;
  open_file_cache_valid 30s;
  open_file_cache_min_uses 2;
  open_file_cache_errors on;
  ```

---

## 3. Alternative Pipeline Architectural Models

When scaling beyond EFS-mounted ASGs:
- **S3 Dynamic Pulling:** Instead of standard NFS, configure instances to pull build artifacts directly from Amazon S3 at boot or deployment via SSM Run Command.
- **Docker on AWS ECS:** Containerise the workload and run on ECS Fargate, utilising AWS Fargate task mounts to keep state isolated.

---

## 4. On-Premises Containerisation & Podman Orchestration

- **Onsite On-Premises Volume:** A dedicated Onsite On-Premises documentation volume is available under `docs/onprem/` (featuring `index.md`, `architecture.md`, `podman-quadlet.md`, `ansible-orchestration.md`, `open-source-stack.md`, and `percona-postgresql.md`), documenting unprivileged deployments using rootless Podman 5+, systemd Quadlet orchestration, and Ansible automation (as per **Item 13**).
- **AWS-to-Podman Mappings:** Core AWS components are mapped to containerized, open-source on-premises equivalents running in rootless Podman: AWS ALB/WAF to BunkerWeb, ECS/ASG to unprivileged Spring Boot and React containers, RDS PostgreSQL to self-hosted Percona Server for PostgreSQL 17 with Patroni, etcd, and pg_backrest, ElastiCache to Valkey, Bedrock to local Ollama/RAGFlow/Langfuse, and Cognito to Keycloak/Authentik (as per **Item 11**).

---

## 5. AI Ingestion, Handshakes & EFS Cold-Start Prevention

- **VIP Guest Lifecycle & Handshakes:** The engineering runbook at `docs/engineering/ai_agent_discovery.md` details the 'VIP Guest' lifecycle network trajectory, Zero-Zero Handshake protocols (mTLS, IAM Roles Anywhere, and API Gateway MCP proxy translations) (as per **Item 21**).
- **EFS Cold-Start Prevention:** Standardise EFS shared storage mount scripts to mount cached Hugging Face model weights locally to prevent cold-starts. Includes the completed Optimization Summary Checklist, which maps strategic separations, visual badges, $112.00 USD/mo AWS DRS and hybrid cloud connection costs linked to the CRM Go-Live, and dual-currency costing structures across both volumes.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
