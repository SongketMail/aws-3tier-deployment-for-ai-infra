---
layout: default
title: "System Architecture"
---

# System Architecture

This document describes the high-availability 3-tier network topology, AWS component layouts, and routing architectures deployed by this project, fully aligned with our **[Estimated Costing](costing.html)** model.

Additionally, this architecture is fully customized to map and host the **Developer's First Design (RAGFlow + LangFuse AI stack)** in a secure, highly-available, and resilient manner.

---

## Developer's First Design vs. AWS Production Architecture

In the developer's initial design (documented in the printscreen `image.png`), the application was structured across four separate standalone virtual machine servers running on **Ubuntu Server 22.04 LTS**:
- **Server 01 (Frontend - Web Tier):** Nginx Web Server / Reverse Proxy (2 vCPU, 4GB RAM)
- **Server 02 (Backend - App Tier):** Backend + DMS + MCP (4 vCPU, 16GB RAM)
- **Server 03 (AI Tier):** RAGFlow + LangFuse (4 vCPU, 8GB RAM)
- **Server 04 (Database - Data Tier):** SQL Database (4 vCPU, 16GB RAM)

While simple, deploying this directly as four standalone VMs introduces single points of failure (SPOF), security vulnerabilities from direct public internet exposure, manual backup overhead, and a lack of scalability.

To make this suitable for enterprise AWS deployment **without changing the AWS requirements**, we have mapped each of these components directly to a secure, multi-AZ, managed 3-tier architecture:

### Architectural Comparative Mapping

| Developer's Original Server | Original Spec | AWS Production-Ready Component | AWS Architectural Benefits |
| :--- | :--- | :--- | :--- |
| **Server 01: Frontend** | 2 vCPU, 4GB RAM, Ubuntu | **AWS WAFv2 + Application Load Balancer (ALB) + Private Nginx ASG** | **No Public IPs:** Traffic enters via a secure, highly-available ALB with AWS WAFv2 Layer-7 protection (OWASP Top 10 + Rate Limiting). The actual Nginx reverse-proxies run on EC2 instances inside private subnets, hidden from the internet. |
| **Server 02: Backend** | 4 vCPU, 16GB RAM, Ubuntu | **Multi-AZ Auto Scaling Group (ASG) EC2 Instances** | **High Availability & Auto-Scaling:** Spans multiple Availability Zones. Scales compute nodes dynamically on demand. Sized using high-performance Graviton (`t4g.xlarge` / `m6g.xlarge`) running secure **Amazon Linux 2023** (or enterprise Ubuntu). Outbound traffic is securely routed via **NAT Gateways**. |
| **Server 03: AI Tier** | 4 vCPU, 8GB RAM, Ubuntu | **Private ASG / Secure Compute Instances** | **Isolation:** Securely hosted in Private App Subnets, completely isolated from direct public internet access. Communicates securely with the backend via private, internal network paths. Sized as Graviton (`c6g.xlarge` / `t4g.xlarge`). |
| **Server 04: Database** | 4 vCPU, 16GB RAM, Ubuntu | **AWS RDS PostgreSQL (Multi-AZ)** | **Managed Resiliency:** Replaced self-managed SQL database with a fully managed Multi-AZ PostgreSQL database (`db.m6g.xlarge`). Synchronous replication, automated snapshots/failover, zero direct public route, and ingress restricted solely to private compute instances. |

---

## Architectural Schematic

The modified network topology below outlines how the developer's AI and web application servers sit and interact within our AWS secure environment:

```
                                            [ INTERNET ] (Web Client)
                                                 │
                                                 ▼ (HTTPS)
                                           [ AWS WAFv2 ]       <-- Layer 7 Security (Core Rules, Rate Limiting)
                                                 │
                                                 ▼ (HTTPS)
                                  [ Application Load Balancer ] <-- Public Subnets (ap-southeast-5a/5b)
                                                 │
                      ┌──────────────────────────┴──────────────────────────┐
                      ▼ (Forward REST API / HTTP)                           ▼
         ┌─────────────────────────────────────────────────────────────────────────────────────┐
         │                          VPC PRIVATE APPLICATION SUBNETS                            │
         │                                                                                     │
         │  ┌───────────────────────────────────────────────────────────────────────────────┐  │
         │  │                     AUTO SCALING GROUP (ASG) - MULTI-AZ                       │  │
         │  │                                                                               │  │
         │  │   ┌───────────────────────────────────┐   ┌───────────────────────────────────┐   │  │
         │  │   │      Instance A (ap-southeast-5a) │   │      Instance B (ap-southeast-5b) │   │  │
         │  │   │                                   │   │                                   │   │  │
         │  │   │  • Server 01: Nginx Web Server /  │   │  • Server 01: Nginx Web Server /  │   │  │
         │  │   │               Reverse Proxy       │   │               Reverse Proxy       │   │  │
         │  │   │  • Server 02: Backend (App Tier)  │   │  • Server 02: Backend (App Tier)  │   │  │
         │  │   │               Backend + DMS + MCP │   │               Backend + DMS + MCP │   │  │
         │  │   │  • Server 03: AI Tier             │   │  • Server 03: AI Tier             │   │  │
         │  │   │               RAGFlow + LangFuse  │   │               RAGFlow + LangFuse  │   │  │
         │  │   │                                   │   │                                   │   │  │
         │  │   │  (Sizing: t4g.xlarge/m6g.xlarge)  │   │  (Sizing: t4g.xlarge/m6g.xlarge)  │   │  │
         │  │   └─────────────────┬─────────────────┘   └─────────────────┬─────────────────┘   │  │
         │  └─────────────────────┼───────────────────────────────────────┼─────────────────┘  │
         │                        │                                       │                    │
         │                        └───────────────────┬───────────────────┘                    │
         │                                            │                                        │
         │                                            ▼ (Secure Outbound Updates / APIs)        │
         │                                    [ NAT Gateways ]                                 │
         └────────────────────────────────────────────┬────────────────────────────────────────┘
                                                      │ (SQL Protocol)
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
         └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Network Isolation Layers

### 1. Presentation / Web Layer (Public Subnets)
- **Subnets:** `10.0.1.0/24` (AZ `ap-southeast-5a`) and `10.0.2.0/24` (AZ `ap-southeast-5b`).
- **Description:** Hosts public-facing services. This layer routes inbound internet traffic directly through the Internet Gateway (IGW).
- **Resources:**
  - **Application Load Balancer (ALB):** Terminates and routes incoming connections. Replaces the external Nginx reverse proxy direct exposure (from Server 01), dispersing HTTP/HTTPS traffic to private instances.
  - **NAT Gateway:** A highly-available NAT Gateway deployment in public subnets provides secure outbound internet access for package retrieval and DMS API callbacks.
  - **AWS WAFv2 Web ACL:** Directly attached to the ALB with 3 rules (OWASP Core, SQLi, and IP Rate Limiting) to block bad actors at the edge.

### 2. Application Layer (Private Subnets)
- **Subnets:** `10.0.10.0/24` (AZ `ap-southeast-5a`) and `10.0.11.0/24` (AZ `ap-southeast-5b`).
- **Description:** Holds business and compute logic. Instances have no public IP addresses and cannot be accessed directly from the internet.
- **Resources:**
  - **Auto Scaling Group (ASG) EC2 Instances:** Hosts the application code (Nginx web service). Features **t4g.xlarge** or **m6g.xlarge** EC2 Instances (ARM Graviton, 4 vCPU, 16GB RAM each) equipped with **gp3 EBS Root Volumes**. They handle Server 02 (Backend + DMS + MCP) and Server 03 (RAGFlow + LangFuse) workloads securely.

### 3. Database Layer (Isolated Private Subnets)
- **Subnets:** `10.0.20.0/24` (AZ `ap-southeast-5a`) and `10.0.21.0/24` (AZ `ap-southeast-5b`).
- **Description:** Dedicated to backend databases. Deeply isolated without any outbound route to the internet or NAT gateways, minimizing any data extraction surface.
- **Resources:**
  - **Multi-AZ RDS PostgreSQL Instance:** Runs synchronously across multiple availability zones using **Multi-AZ `db.m6g.xlarge` PostgreSQL (4 vCPU, 16GB RAM)** with **gp3 Storage**, corresponding to Server 04's resource needs. This guarantees high-availability, automatic failover, and robust production database performance.

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
- Contains only local VPC route entries (`10.0.0.0/16`), ensuring database traffic never traverses public routes or internet gateways.
