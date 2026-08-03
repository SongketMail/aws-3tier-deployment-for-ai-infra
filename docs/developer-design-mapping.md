---
layout: default
title: "Developer Design Mapping"
---

# Developer Design Alignment Guide

This guide details how we transition the **Developer's First Design** (which specified four separate, standalone Ubuntu 26.04 LTS servers) into our secure, highly-available, production-ready **AWS 3-Tier Architecture**, without changing any underlying AWS constraints or requirements.

---

## Rationale for the Architectural Transition

The developer's original design was logical but modeled around static, single-node virtual machines. Running critical production infrastructure on standalone VMs presents several operational risks:
1. **Single Points of Failure (SPOFs):** If any of the servers experiences hardware degradation or guest OS crashes, the entire application goes offline.
2. **Direct Public Exposure:** Placing database or backend servers directly on public-facing networks increases the surface area for brute-force SSH, port-scanning, and SQL injection (SQLi) attacks.
3. **Manual Scalability & High Latency:** VM resources are fixed and cannot scale dynamically in response to user demand or computational peaks.
4. **Backup and Patches overhead:** Managing backups, OS updates, and package security patches manually across multiple VMs takes significant operational effort.

By aligning this layout with our secure AWS design, we retain **all functionality** of the developer's original services (Nginx, Backend, DMS, MCP, RAGFlow, LangFuse, and Postgres) while inheriting cloud-native security, performance, and automation.

---

## Detailed Component Transitions

### 1. Server 01: Frontend Web Tier (Nginx Web Server / Reverse Proxy)
* **Developer's First Design:** A single Ubuntu server running Nginx (2 vCPU, 4GB RAM) exposed to the public internet via port 80/443.
* **AWS Alignment:**
  - **Layer 7 Firewall (AWS WAFv2):** Blocks common exploits (OWASP Top 10, SQLi, XSS) and manages brute-force or DDoS attempts via dynamic IP Rate Limiting.
  - **Application Load Balancer (ALB):** Terminates external SSL/TLS, manages routing rules, and automatically performs health checks to route traffic only to healthy instances.
  - **Private Nginx Web Tier (ASG):** Sized as `t4g.medium` (2 vCPU, 4GB RAM) but deployed within **private subnets** under an Auto Scaling Group (ASG). This ensures the Nginx instance has *no public IP*, can scale out horizontally, and is protected from brute-force exposure.
  - **Dedicated Standalone Instance (AMI Baking):** Paired with a dedicated Frontend Standalone instance inside the private subnets. Connected directly to identical S3 resources to test routing/static templates and pre-bake certified `ami-frontend-*` images.

### 2. Server 02: Backend App Tier (Backend + DMS + MCP)
* **Developer's First Design:** A single Ubuntu server (4 vCPU, 16GB RAM) running Backend, DMS, and MCP APIs.
* **AWS Alignment:**
  - **Zero Direct Ingress:** Deployed inside Private App Subnets, completely blocked from direct public ingress. The ALB only forwards verified requests to this layer on Port 80 (or your custom API port).
  - **Sizing Alignment:** Sized using Graviton `t4g.xlarge` (4 vCPU, 16GB RAM) to perfectly match the developer's CPU/Memory requirements while saving up to 20% in raw compute costs over comparable x86_64 nodes.
  - **Secure Egress:** Outbound integrations (such as external DMS syncs, Webhooks, or payment gateway APIs) traverse a managed **AWS NAT Gateway** in the public subnet, masking instance IPs and preventing inbound traffic.
  - **Dedicated Standalone Instance (AMI Baking & Schema Migrations):** Paired with a dedicated Backend Standalone instance connected to the identical Multi-AZ RDS database and S3 buckets. Used to test application updates, safely run database migrations, and pre-bake `ami-backend-*` images under a 1:1 replica environment.

### 3. Server 03: AI Tier (RAGFlow + LangFuse)
* **Developer's First Design:** A single Ubuntu server (4 vCPU, 8GB RAM) running RAGFlow + LangFuse AI stack.
* **AWS Alignment:**
  - **Intra-VPC Security:** Placed in the same Private App Subnets. Secure, ultra-low-latency private communication paths are used to connect the Backend (Server 02) to RAGFlow + LangFuse (Server 03) via internal DNS or security-group-protected private endpoints.
  - **Sizing Alignment:** Sized as `c6g.xlarge` or `t4g.xlarge` to provide the required 4 vCPU and 8-16GB RAM. If CPU-bound AI processing becomes intensive, the ASG will scale these instances dynamically.
  - **Environment Compatibility:** Fully compatible with containerized environments (Docker Compose / ECS) or native package runtimes.
  - **Dedicated Standalone Instance (AMI Baking & EFS Caching):** Paired with a dedicated AI Standalone instance connected to the identical Amazon EFS filesystem, RDS, and S3. Developers pre-download and warm up AI model caches on EFS using this standalone instance to allow instant bootstrapping across the auto-scaled nodes. Used to pre-bake `ami-ai-*` images.

### 4. Server 04: Database Data Tier (SQL Database)
* **Developer's First Design:** A single Ubuntu server (4 vCPU, 16GB RAM) running self-managed PostgreSQL.
* **AWS Alignment:**
  - **Fully Managed RDS (PostgreSQL 16):** Upgraded to **AWS RDS PostgreSQL** (Multi-AZ deployment) sized at `db.m6g.xlarge` (4 vCPU, 16GB RAM).
  - **Multi-AZ Replication:** Synchronously replicates data across physically separate Availability Zones. In the event of an outage in AZ A, AWS automatically fails over to AZ B with zero manual intervention or data loss.
  - **Absolute Network Isolation:** Deployed inside isolated Private Database Subnets. The database security group restricts incoming traffic *exclusively* to the application security group (ASG), preventing any direct internet access.

---

## Operating System & Hardware Optimizations

To deliver maximum efficiency, we transition the underlying hardware platform from legacy x86 virtual machines to **AWS Graviton (ARM64)** processors:

1. **Price-Performance Efficiency:** AWS Graviton (`t4g` and `m6g` instances) delivers up to **40% better price-performance** compared to equivalent x86 instances, significantly lowering the monthly run costs.
2. **Ubuntu 26.04 LTS Base Operating System:** To leverage the latest performance improvements, security features, and modern container support, we standardize our base platform on **Ubuntu 26.04 LTS (Noble Numbat successor)**.
3. **Amazon Linux 2023 Option:** For lightweight workloads that do not depend on Canonical specific packages, **Amazon Linux 2023 (AL2023)** remains available as a minimal, cloud-optimized option.

---

## Server Hardening & Security Compliance (ASIMP Integration)

In aligning the developer design with AWS enterprise standards, all Ubuntu 26.04 LTS compute resources (both ASG instances and Standalone instances) are hardened and tuned using **ASIMP (Ansible System Integrity Management Platform)** (available at [github.com/linuxmalaysia/ASIMP](https://github.com/linuxmalaysia/ASIMP)).

ASIMP is a host-based, automated security hardening, compliance, and auditing framework that implements a strict **"Measure, Harden, Re-Measure"** paradigm to verify and guarantee security posturing before the machine is allowed to process production traffic.

### The ASIMP Hardening & Auditing Pipeline

```
  [ PHASE 1: Baseline Auditing ]
               │
               ▼ Generates /var/log/asimp-baseline-scores.json
  [ PHASE 2: Hardening & Mitigations ]
               │  • OS updates, debsums packages verification
               │  • OpenStack ansible-hardening & Dev-Sec SSH hardening
               │  • Lynis system level modifications
               ▼
  [ PHASE 3: Verification & Reporting ]
                  • Re-runs audits and outputs comparison scorecard
                  • HTML reports written to /var/log/openscap-after-report.html
```

### Key ASIMP Hardening Capabilities Applied:

1. **Dual-Engine Security Auditing:**
   - **OpenSCAP:** Conducts formal vulnerability and security compliance scanning mapped against the **CIS Security Ubuntu Linux Benchmark Level 2** profile.
   - **Lynis:** Performs comprehensive system configuration auditing, examining OS parameters, boot configurations, cryptography standards, and active network ports.
2. **Pre & Post Scorecard Comparison:**
   - Runs audits prior to hardening to capture initial baselines, then executes them afterwards, logging comparative metrics in `/var/log/asimp-baseline-scores.json`.
   - Generates visually comprehensive, standalone HTML inspection reports at `/var/log/openscap-before-report.html` and `/var/log/openscap-after-report.html`.
3. **Automated Package Updates & debsums Verification:**
   - Standardizes the Ubuntu system upgrade procedures and checks package-level code integrity via `debsums` to detect any unauthorized binary modifications.
4. **Standardized OS Hardening Benchmarks:**
   - Deploys rigorous security compliance controls utilizing OpenStack's `ansible-hardening` role.
   - Standardizes and restricts SSH configuration endpoints using Dev-Sec's certified `ssh-hardening` roles, enforcing secure cipher suites, disabling password-based root access, and specifying key exchange standards.
5. **Detailed System Tuning & Custom Fixes:**
   - Automatically tunes virtual memory configuration parameters, core kernel dumps, file system mounting options (e.g., nodev, nosuid, noexec where appropriate), and limits access to system compilers.

---

## Summary of the AWS Security & HA Multipliers

Through this alignment, the developer gets their exact applications deployed with unmatched production capabilities:

```
┌─────────────────────────┬─────────────────────────────────────────────────┐
│ Feature                 │ How AWS Improves Developer's First Design       │
├─────────────────────────┼─────────────────────────────────────────────────┤
│ High Availability       │ Multi-AZ redundancy for Compute and RDS DB.     │
├─────────────────────────┼─────────────────────────────────────────────────┤
│ DDoS & Web Protection   │ AWS WAFv2 blocking bad traffic before compute.  │
├─────────────────────────┼─────────────────────────────────────────────────┤
│ Elastic Scaling         │ ASG automatically adds instances based on load. │
├─────────────────────────┼─────────────────────────────────────────────────┤
│ Data Protection         │ Automatic, daily snapshots + Multi-AZ backups.  │
├─────────────────────────┼─────────────────────────────────────────────────┤
│ Security Principle      │ Zero-Trust isolated subnets & IAM roles.       │
├─────────────────────────┼─────────────────────────────────────────────────┤
│ System Integrity        │ Hardened and audited via ASIMP framework.       │
└─────────────────────────┴─────────────────────────────────────────────────┘
```
