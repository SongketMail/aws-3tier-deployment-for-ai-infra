---
layout: "default"
okf_version: "0.2"
type: "Skill"
title: "Big Data Analytics Lakehouse Architecture Skill"
timestamp: 2026-08-20T00:00:00Z
topics: ["bda", "lakehouse", "aws", "hybrid", "proxmox", "rke2", "ceph", "mcp", "skills"]
description: "Guidelines and architectural specifications for modernizing Big Data Analytics platforms into 100% open-source Lakehouses with S3 WORM Object Lock, Iceberg, Polaris, Trino, Spark/Sedona, MCP AI quarantine sandboxing, and 3 distinct infrastructure solution blueprints (Cloud, Hybrid, On-Prem Proxmox/RKE2/Ceph)."
name: "bda-lakehouse-architecture"
sources: ["docs/bda-lakehouse-architecture.md"]
status: "active"
verified: "true"
---
# Big Data Analytics Lakehouse Architecture Skill

This skill provides step-by-step procedures, architectural guardrails, and implementation blueprints for modernizing legacy Big Data Analytics platforms into authoritative, 100% open-source data lakehouses.

---

## Core Architectural Guardrails

1. **Storage & Compute Decoupling:** Persistent storage is decoupled from compute using S3-compatible object storage (AWS S3, Ceph RADOS Gateway, or MinIO Enterprise Object Store) and columnar Parquet tables managed by **Apache Iceberg**.
2. **Object Lock Retention Contract:**
   * **Tier 0 SSoT (Golden Evidence):** Bucket Versioning enabled; S3 Object Lock configured in **Compliance Mode** under defined retention rules (e.g. 7-year statutory or 365-day compliance) with legal-hold toggles.
   * **Iceberg Table Maintenance Separation:** Iceberg Parquet files and metadata trees reside in dedicated buckets or partitions governed by Governance Mode Object Lock or unlocked object paths, enabling compaction, snapshot purging, and retention policies without violating WORM holds.
3. **Data Provenance & Human-to-AI Quarantine:**
   * **Tier 0 (Golden Human SSoT):** Strictly zero unvalidated AI writes permitted. Requires human cryptographic signatures and ODCS contract validation.
   * **Tier 1 (Telemetry Ingestion):** Automated telemetry streams (weather, water sensors, thermal hotspots) subject to Data Contract CLI gates and human stewardship.
   * **Tier 2 (AI Sandbox Quarantine):** Ephemeral storage for LLM intermediate runs and MCP outputs, configured with automated 30-day S3 Lifecycle expiration policies and Kubernetes scheduled CronJob volume cleanup controllers.
4. **Model Context Protocol (MCP) Sandboxing:**
   * MCP tools operate over JSON-RPC 2.0. Database connections use `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`.
   * SQL write verbs (`INSERT`, `UPDATE`, `DELETE`, `DROP`, Iceberg commits) are blocked at the Apache APISIX gateway.
   * All intermediate outputs are tagged with `ai_generated_data: true` and `enterprise_provenance`.

---

## Three (3) Infrastructure Deployment Solution Topologies

### Solution 1: All in Cloud (AWS Native)
* **Storage:** AWS S3 (Object Lock Compliance Mode for Tier 0, Governance Mode for Tier 1, 30-day Lifecycle Purge for Tier 2).
* **Catalog:** AWS Glue Data Catalog or Apache Polaris REST Catalog on Amazon EKS.
* **Compute:** Amazon EMR Serverless (Spark + Sedona), Amazon Athena / EMR Trino, AWS MWAA Airflow.
* **Database & Ingress:** Amazon Aurora PostgreSQL (Multi-AZ with PostGIS), AWS WAFv2 + ALB + CloudFront, Keycloak / Cognito on ECS.
* **AI & MCP:** Amazon Bedrock / SageMaker with containerized MCP servers on AWS Fargate using read-only database connections and Tier 2 scratch buckets.

### Solution 2: Hybrid - AI On-Premises
* **Cloud Core Lakehouse:** Core lakehouse storage (S3 WORM Tier 0), Glue/Polaris catalog, Athena/EMR query engine, and MWAA Airflow hosted in AWS Cloud.
* **On-Premises Dedicated GPU Infrastructure:** Bare-metal GPU servers (NVIDIA H100/A100) running local Ollama, vLLM, or RAGFlow inside an on-premises data centre (e.g. Cyberjaya).
* **Hybrid Connectivity:** AWS Direct Connect (1GbE/10GbE private physical circuit; MACsec or IPsec overlay for transit encryption) or IPsec VPN tunnel.
* **On-Prem MCP Servers:** Local MCP tools query Cloud Glue/Polaris and Cloud Trino using read-only database credentials over mTLS via Apache APISIX, enforcing Tier 0 write protection.

### Solution 3: Everything On-Premises (Proxmox VE + RKE2 + Ceph SDS)
* **Proxmox VE Hypervisor Fabric:** 11 physical Proxmox VE hosts (4x AI/GPU, 4x App, 3x DB/Stateful) with PCIe GPU Passthrough for AI worker VMs.
* **Dual-Cluster Kubernetes Architecture:**
  * **RKE2 Production Cluster (14 VM Nodes):** 3x CP (`rke2-cp-01`..`03`), 4x AI GPU worker (`rke2-worker-ai-01`..`04`), 4x App worker (`rke2-worker-app-01`..`04`), 3x DB worker (`rke2-worker-db-01`..`03`). RKE2 v1.30.x release train. Canal CNI for FIPS 140-2 compliance, or Cilium CNI for eBPF performance. Proxmox VE VM anti-affinity rules enforced across physical hosts.
  * **K3s Supporting Cluster (5 VM Nodes):** 3x CP (`k3s-mgmt-01`..`03`), 2x Worker (`k3s-worker-01`..`02`) hosting Prometheus, Grafana, Loki, Vault, and CI/CD runners.
* **Distributed Software-Defined Storage (Ceph SDS):** Ceph RADOS Gateway (S3 Object Storage WORM), Ceph CSI RBD (high-IOPS block storage RWO), CephFS (shared filesystem RWX), NFS external provisioner, and Local Path Provisioner (with CronJob cleanup controller).
* **On-Prem Open-Source Stack:** Ceph RGW/MinIO, Apache Polaris, Trino MPP + Spark/Sedona, PostgreSQL 17 + Patroni + PostGIS, NiFi + Airflow, APISIX + Keycloak, Next.js + Apache Superset with deck.gl spatial maps.

---

Deep State of Mind (DSOM) For My AI Protocol | Enterprise Big Data Lakehouse Architecture Blueprint | 2026-08-20
Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0
