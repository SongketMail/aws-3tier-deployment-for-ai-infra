---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Onsite On-Premises Blueprint Portal"
timestamp: 2026-08-09T15:00:00Z
topics: ["onprem", "virtualization", "podman", "ansible", "gitea", "ara", "semaphore"]
---
<div class="arch-badge arch-badge-strategic">
  <strong>[STRATEGIC FINANCIAL]</strong> — Sovereignty, Compliance & Governance
</div>
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>

# Onsite On-Premises Architecture & Deployment Volume

Welcome to the **Onsite On-Premises Deployment Volume**. This dedicated portal is compiled for organizations seeking absolute data sovereignty, regulatory compliance (under PDPA 2010 and Bank Negara Malaysia guidelines), and zero-external cloud dependencies.

This volume describes our **Onsite On-Premise Enterprise Blueprint**, where all AWS services are mapped to robust, 100% open-source, local equivalents. Rather than relying on public cloud management planes, the entire stack runs within secure, hardened local **Virtual Machines (VMs)** using unprivileged, rootless **Podman 5+** and declarative **systemd Quadlet** orchestration.

The entire cluster lifecycle, configuration, and continuous deployment are managed entirely on-premises using **Ansible** (fully compliant with FQCN guidelines), utilizing **Gitea** for private version control, **Ansible Semaphore** for automated UI orchestration, and **Ansible ARA** for high-fidelity execution logging and compliance auditing.

---

## 📂 Onsite On-Premises Volume Catalog

This volume is divided into four highly detailed engineering and strategic guides:

### 1. [Onsite On-Premises Virtual Machine & Network Architecture](architecture.html)
*Physical and virtual machine resource topologies, host network mapping, and local unprivileged subnet layouts matching secure 3-tier patterns.*

### 2. [Rootless Podman 5+ & systemd Quadlets Orchestration](podman-quadlet.html)
*Deep technical analysis of running production services under non-root users, systemd lingering, user namespace (`keep-id`) permission remapping, and Quadlet specifications.*

### 3. [On-Premises Infrastructure Management with Ansible](ansible-orchestration.html)
*Symmetric privilege strategies, Fully Qualified Collection Names (FQCN) blueprints, and continuous deployment pipelines using Gitea, Ansible Semaphore, and Ansible ARA.*

### 4. [Open-Source Containerized Stack Specifications](open-source-stack.html)
*High-fidelity mapping of AWS core offerings (ALB, ASG, RDS, Valkey, Bedrock, Cognito) to containerized open-source alternatives (BunkerWeb, Spring Boot, PostgreSQL 17, Valkey, Keycloak, Ollama, RAGFlow, and Langfuse) with Quadlet configuration blueprints.*

### 5. [Enterprise Percona Server for PostgreSQL 17 Setup](percona-postgresql.html)
*Comprehensive blueprints for running production-grade Percona Server for PostgreSQL 17 on-premises using Patroni cluster management, etcd distributed consensus stores, pg_backrest, and HAProxy load balancing.*

---

## 🛡️ Strategic Alignment & Governance

Deploying onsite on-premises is the ultimate control pattern for high-security environments:

- **Absolute Data Sovereignty:** Since data never leaves the local bare-metal or hypervisor-managed disks, compliance with Malaysian cross-border transfer laws is preserved by default.
- **Immunity to Cloud Surcharges:** Eliminates variable cloud costs (such as AWS NAT Gateway traffic fees, regional cross-AZ charges, and IPv4 address surcharges), replacing them with predictable, flat hardware depreciation and local power metrics.
- **Enterprise Automation Parity:** By adopting modern DevOps tooling (Ansible, Gitea, Semaphore, ARA), local deployments match cloud agility while maintaining physical perimeter safety.

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
