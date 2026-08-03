---
layout: default
title: "System Architecture"
---

# System Architecture

This document describes the high-availability 3-tier network topology, AWS component layouts, and routing architectures deployed by this project, fully aligned with our **[Estimated Costing](costing.html)** model.

Additionally, this architecture is fully customized to map and host the **Developer's First Design (RAGFlow + LangFuse AI stack)** in a secure, highly-available, and resilient manner, built using hardened **Ubuntu 26.04 LTS** nodes and integrated with **Amazon ElastiCache for Valkey**.

---

## Developer's First Design vs. AWS Production Architecture

In the developer's initial design, the application was structured across four separate standalone virtual machine servers running on **Ubuntu Server 26.04 LTS**:
- **Server 01 (Frontend - Web Tier):** Nginx Web Server / Reverse Proxy (2 vCPU, 4GB RAM)
- **Server 02 (Backend - App Tier):** Backend + DMS + MCP (4 vCPU, 16GB RAM)
- **Server 03 (AI Tier):** RAGFlow + LangFuse (4 vCPU, 8GB RAM)
- **Server 04 (Database - Data Tier):** SQL Database (4 vCPU, 16GB RAM)

While simple, deploying this directly as four standalone VMs introduces single points of failure (SPOF), security vulnerabilities from direct public internet exposure, manual backup overhead, and a lack of scalability.

To make this suitable for enterprise AWS deployment **without changing the AWS requirements**, we have mapped each of these components directly to a secure, multi-AZ, managed 3-tier architecture:

### Architectural Comparative Mapping

| Developer's Original Server | Original Spec | AWS Production-Ready Component | AWS Architectural Benefits |
| :--- | :--- | :--- | :--- |
| **Server 01: Frontend** | 2 vCPU, 4GB RAM, Ubuntu | **AWS WAFv2 + ALB + Private Nginx ASG & Dedicated Standalone Instance** | **No Public IPs & Local Baking Parity:** Traffic enters via secure ALB/WAF. Private Nginx reverse-proxies run inside private subnets without public IPs. Paired with a dedicated Frontend Standalone instance connected to the same S3 bucket to test configurations and pre-bake custom Nginx `ami-frontend-*` images. Hardened via **ASIMP**. |
| **Server 02: Backend** | 4 vCPU, 16GB RAM, Ubuntu | **Multi-AZ ASG & Dedicated Standalone Instance** | **High Availability & 1:1 Database Parity:** ASG spans multiple AZs and scales compute nodes dynamically. Paired with a dedicated Backend Standalone instance connected to the identical Multi-AZ RDS PostgreSQL database and S3 buckets to securely execute database migrations, test application logic, and pre-bake `ami-backend-*` images. Hardened via **ASIMP**. |
| **Server 03: AI Tier** | 4 vCPU, 8GB RAM, Ubuntu | **Private ASG Compute & Dedicated AI Tier Standalone Instance** | **Isolated Compute & Instant Scaling via EFS Caching:** Securely hosted in Private App Subnets. Paired with a dedicated AI Standalone instance connected to the identical Amazon EFS filesystem, RDS, and S3. Developers warm up Hugging Face model weight caches directly onto EFS from the standalone instance so that auto-scaling ASG nodes can access them instantly. Pre-baked into `ami-ai-*` images. Hardened via **ASIMP**. |
| **Server 04: Database** | 4 vCPU, 16GB RAM, Ubuntu | **AWS RDS PostgreSQL (Multi-AZ) & Amazon ElastiCache for Valkey** | **Managed Resiliency & Enterprise Caching:** Replaced self-managed SQL database with a fully managed Multi-AZ PostgreSQL database (`db.m6g.xlarge`). Synchronous replication, automated snapshots/failover, zero direct public route, and ingress restricted solely to private compute instances. Paired with a secure **Amazon ElastiCache for Valkey** cluster inside the database subnets to act as a high-performance in-memory task broker and session store for RAGFlow + LangFuse, reducing DB load and database overhead. |

---

## Standalone EC2 Instances for AMI Creation and Parity

To ensure seamless, reliable updates and zero-downtime rolling upgrades across our Auto Scaling Groups (ASGs), each application group (Frontend, Backend, and AI Tier) is paired with a dedicated **Standalone EC2 Instance** (running **Ubuntu 26.04 LTS** and hardened via the **ASIMP** framework).

These standalone instances are deployed directly inside the secure **VPC Private Application Subnets** and are configured to connect to the exact same shared resources (AWS RDS PostgreSQL Database, Amazon S3 Buckets, Amazon EFS shared storage, and Amazon ElastiCache Valkey caching) as their corresponding ASGs:

1. **Frontend Standalone Instance:**
   - Connected to **Amazon S3** to manage and verify static assets or remote template files.
   - Used to test Nginx routing/configurations before baking the `ami-frontend-*` image.
2. **Backend Standalone Instance:**
   - Connected to the **Multi-AZ RDS PostgreSQL** database (using identical DB endpoints and credentials), **Amazon S3** (using identical IAM Role permissions), and **Amazon ElastiCache Valkey** (port 6379).
   - Used to verify backend service scripts, run migrations, and test application logic before baking the `ami-backend-*` image.
3. **AI Tier Standalone Instance:**
   - Connected to **Amazon EFS** (via Private Mount Targets) to read/write persistent AI model caches, **Amazon S3** for training documents, **RDS PostgreSQL** for metadata storage, and **Amazon ElastiCache Valkey** (port 6379) for distributed task broker signaling.
   - Used to bootstrap RAGFlow + LangFuse dependencies, warm up Hugging Face/SentenceTransformers cache directories, and test container updates before baking the `ami-ai-*` image.

### Architectural Advantages of Standalone-to-AMI Parity:
- **1:1 Environment Alignment:** Because each standalone instance connects to the exact same database, Valkey cache, and shared storage backends, developers can fully run, test, and validate configurations in a real production-like environment without any risk of deployment divergence.
- **Pre-Audited & Hardened Base:** Standalone instances serve as the staging template. Developers run the **ASIMP** auditing and hardening pipelines directly on these instances, verifying system integrity reports before triggering the Packer/AMI capture.
- **Zero-Downtime Releases:** Once the standalone instance is verified and the AMI is baked, updating the ASG Launch Template and running an Instance Refresh executes a safe rolling update across the live cluster.

---

## Architectural Schematic

The updated network topology below outlines how our three ASG application groups and their matching standalone AMI-baking instances connect to the shared database, Amazon S3, Amazon EFS, and ElastiCache Valkey within our AWS secure environment:

```
                                            [ INTERNET ] (Web Client)
                                                 │
                                                 ▼ (HTTPS: app.linuxmalaysia.com)
                                           [ Route 53 ]        <-- DNS Management & Alias Routing
                                                 │
                                                 ▼
                                           [ AWS WAFv2 ]       <-- Layer 7 Security (Core Rules, Rate Limiting)
                                                 │
                                                 ▼ (HTTPS)
                                  [ Application Load Balancer ] <-- Public Subnets (ap-southeast-5a/5b)
                                                 │
                      ┌──────────────────────────┼──────────────────────────┐
                      ▼ (Port 80/443)            ▼ (API / App Port)         ▼ (AI Queue / API)
         ┌─────────────────────────────────────────────────────────────────────────────────────┐
         │                          VPC PRIVATE APPLICATION SUBNETS                            │
         │                                                                                     │
         │  ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐     │
         │  │   FRONTEND WEB ASG   │   │   BACKEND APP ASG    │   │     AI TIER ASG      │     │
         │  │ (Nginx Web Servers)  │   │ (Backend + DMS + MCP)│   │ (RAGFlow + LangFuse) │     │
         │  │   • Sizing: t4g.med  │   │   • Sizing: t4g.xlrg │   │   • Sizing: t4g.xlrg │     │
         │  └──────────┬───────────┘   └──────────┬───────────┘   └──────────┬───────────┘     │
         │             │                          │                          │                 │
         │             │                          │                          │                 │
         │  ┌──────────▼───────────┐   ┌──────────▼───────────┐   ┌──────────▼───────────┐     │
         │  │ FRONTEND STANDALONE  │   │  BACKEND STANDALONE  │   │    AI STANDALONE     │     │
         │  │  (AMI Baker/Staging) │   │  (AMI Baker/Staging) │   │  (AMI Baker/Staging) │     │
         │  │  • Sizing: t4g.micro │   │  • Sizing: t4g.xlrg  │   │  • Sizing: t4g.xlrg  │     │
         │  └──────────┬───────────┘   └──────────┬───────────┘   └──────────┬───────────┘     │
         │             │                          │                          │                 │
         │             │                          │                          │                 │
         │             │                          ▼                          ▼                 │
         │             └───────────────────► [ S3 Bucket ] ◄─────────────────┘                 │
         │                                   [ (Shared Objects)]                               │
         │                                        ▲     ▲                                      │
         │                                        │     │                                      │
         │                               EFS Port │     │ EFS Port                             │
         │                                 (2049) │     │ (2049)                               │
         │                                        ▼     ▼                                      │
         │                                  [ Amazon EFS ] (Model Weights & App Configs)       │
         │                                                                                     │
         │                                    [ NAT Gateways ]                                 │
         └────────────────────────────────────────────┬────────────────────────────────────────┘
                                                      │ (SQL Protocol - Port 5432)
                                                      │ (Valkey Protocol - Port 6379)
                                                      ▼
         ┌─────────────────────────────────────────────────────────────────────────────────────┐
         │                           VPC PRIVATE DATABASE SUBNETS                              │
         │                                                                                     │
         │  ┌───────────────────────────────────────────────────────────────────────────────┐  │
         │  │                    MULTI-AZ RDS DATABASE (POSTGRESQL 16)                      │  │
         │  │                                                                               │  │
         │  │   ┌───────────────────────────────────┐   ┌───────────────────────────────────┐   │  │
         │  │   │     Primary DB (ap-southeast-5a)  │   │     Standby DB (ap-southeast-5b)  │   │  │
         │  │   │                                   │   │     (Synchronous Replication)     │   │  │
         │  │   │  • Server 04: Database Data Tier  │═══»                                   │   │  │
         │  │   │  (Sizing: db.m6g.xlarge, gp3)     │   │  (Automatic Failover Target)      │   │  │
         │  │   └───────────────────────────────────┘   └───────────────────────────────────┘   │  │
         │  └───────────────────────────────────────────────────────────────────────────────┘  │
         │                                                                                     │
         │  ┌───────────────────────────────────────────────────────────────────────────────┐  │
         │  │                    AMAZON ELASTICACHE FOR VALKEY CLUSTER                      │  │
         │  │                                                                               │  │
         │  │   • Port: 6379 (Secure Private Access Only)                                   │  │
         │  │   • Sizing: cache.t4g.micro (Baseline) / cache.t4g.medium (High-Performance)     │  │
         │  │   • Ingress restricted to Private Compute ASG and Standalone Instances        │  │
         │  │   • TLS/SSL In-Transit and At-Rest Encryption Enforced                        │  │
         │  └───────────────────────────────────────────────────────────────────────────────┘  │
         └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Network Isolation Layers

### 1. Presentation / Web Layer (Public Subnets)
- **Subnets:** `10.0.1.0/24` (AZ `ap-southeast-5a`) and `10.0.2.0/24` (AZ `ap-southeast-5b`).
- **Description:** Hosts public-facing services and manages secure domain mappings. This layer routes inbound internet traffic directly through the Internet Gateway (IGW).
- **Resources:**
  - **Route 53 DNS Routing:** Manages custom domain delegations and points A Alias records to the ALB. Integrated with AWS Certificate Manager (ACM) for automatic domain verification.
  - **Application Load Balancer (ALB):** Terminates and routes incoming connections. Replaces the external Nginx reverse proxy direct exposure (from Server 01), dispersing HTTP/HTTPS traffic to private instances.
  - **NAT Gateway:** A highly-available NAT Gateway deployment in public subnets provides secure outbound internet access for package retrieval and DMS API callbacks.
  - **AWS WAFv2 Web ACL:** Directly attached to the ALB with 3 rules (OWASP Core, SQLi, and IP Rate Limiting) to block bad actors at the edge.

### 2. Application Layer (Private Subnets)
- **Subnets:** `10.0.10.0/24` (AZ `ap-southeast-5a`) and `10.0.11.0/24` (AZ `ap-southeast-5b`).
- **Description:** Holds business and compute logic. Instances have no public IP addresses and cannot be accessed directly from the internet.
- **Resources:**
  - **Auto Scaling Group (ASG) EC2 Instances:** Hosts the application code (Nginx web service). Features **t4g.xlarge** or **m6g.xlarge** EC2 Instances (ARM Graviton, 4 vCPU, 16GB RAM each) equipped with **gp3 EBS Root Volumes**. They handle Server 02 (Backend + DMS + MCP) and Server 03 (RAGFlow + LangFuse) workloads securely on hardened Ubuntu 26.04 LTS.
  - **Standalone EC2 Instances:** Deploys a dedicated standalone instance next to each ASG application group (Frontend, Backend, and AI Tiers) inside the private subnets. These instances are connected to the exact same shared databases (RDS), caches (Valkey), and storage systems (S3 and EFS) as their respective ASGs, acting as 1:1 replica environments for application staging, testing, ASIMP auditing/hardening, and pre-baking custom AMIs.

### 3. Database & Caching Layer (Isolated Private Subnets)
- **Subnets:** `10.0.20.0/24` (AZ `ap-southeast-5a`) and `10.0.21.0/24` (AZ `ap-southeast-5b`).
- **Description:** Dedicated to database servers and caching nodes. Deeply isolated without any outbound route to the internet or NAT gateways, minimizing any data extraction surface.
- **Resources:**
  - **Multi-AZ RDS PostgreSQL Instance:** Runs synchronously across multiple availability zones using **Multi-AZ `db.m6g.xlarge` PostgreSQL (4 vCPU, 16GB RAM)** with **gp3 Storage**, corresponding to Server 04's resource needs. This guarantees high-availability, automatic failover, and robust production database performance.
  - **Amazon ElastiCache for Valkey Cluster:** A secure, high-performance in-memory caching cluster running Valkey 7.2. It manages session state, caches database queries, and runs the Celery/Redis task queue for RAGFlow and LangFuse. It operates on port `6379` with transit and at-rest encryption enabled, allowing ingress only from private compute security groups.

### 4. Storage Tier (Amazon S3)
- **Description:** Statically hosted media, secure user uploads, and build backups. It is situated outside the VPC but fully integrated.
- **Resources:**
  - **Amazon S3 Bucket:** Fully encrypted standard object storage. Access is managed via IAM policies and secure credentials.

---

## Routing Configuration

The architecture manages network traffic flow through three distinct route tables:

### Public Route Table
- Associated with public subnets.
- Routes all outbound traffic (`0.0.0.0/0`) to the **Internet Gateway (IGW)**.

### Private Application Route Table
- Associated with private application subnets.
- Routes all outbound traffic (`0.0.0.0/0`) to the **NAT Gateway** running in the public subnet.

### Database Route Table
- Associated with private database subnets.
- Contains only local VPC route entries (`10.0.0.0/16`), ensuring database and cache traffic never traverses public routes or internet gateways.
