---
layout: default
title: "System Architecture"
---

# System Architecture

This document describes the high-availability 3-tier network topology, AWS component layouts, and routing architectures deployed by this Terraform project, fully aligned with our **[Estimated Costing](costing.html)** model.

---

## Architectural Schematic

```
                                  [ INTERNET ]
                                       │
                                       ▼
                                 [ AWS WAFv2 ]   <-- (OWASP Top 10 + IP Rate Limiting)
                                       │
                                       ▼
                         [ Application Load Balancer ]  <-- (Public Subnets)
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
                  [ ASG EC2 Instance ]       [ ASG EC2 Instance ]  <-- (Private App Subnets: 2x t4g.medium)
                         │                           │               │
                         │                           │               ▼
                         │                           │       [ Amazon S3 Bucket ] <-- (Storage Tier)
                         └─────────────┬─────────────┘
                                       ▼
                             [ Multi-AZ RDS DB ]        <-- (Private Database Subnets: db.m6g.large)
```

---

## Network Isolation Layers

### 1. Presentation / Web Layer (Public Subnets)
- **Subnets:** `10.0.1.0/24` (AZ `ap-southeast-5a`) and `10.0.2.0/24` (AZ `ap-southeast-5b`).
- **Description:** Hosts public-facing services. This layer routes inbound internet traffic directly through the Internet Gateway (IGW).
- **Resources:**
  - **Application Load Balancer (ALB):** Terminates and routes incoming connections.
  - **NAT Gateway:** A single NAT Gateway (as provisioned in the baseline costing to optimize monthly spend) deployed in a public subnet to provide private instances secure outbound internet access.
  - **AWS WAFv2 Web ACL:** Directly attached to the ALB with 3 rules (OWASP Core, SQLi, and IP Rate Limiting) to block bad actors at the edge.

### 2. Application Layer (Private Subnets)
- **Subnets:** `10.0.10.0/24` (AZ `ap-southeast-5a`) and `10.0.11.0/24` (AZ `ap-southeast-5b`).
- **Description:** Holds business and compute logic. Instances have no public IP addresses and cannot be accessed directly from the internet.
- **Resources:**
  - **Auto Scaling Group (ASG) EC2 Instances:** Hosts the application code (Nginx web service). Features **2x `t4g.medium` EC2 Instances (ARM Graviton, 2 vCPU, 4GB RAM each)** equipped with **2x 30GB gp3 EBS Root Volumes**. Outbound requests (such as API calls or package updates) are routed securely through the NAT Gateway.

### 3. Database Layer (Isolated Private Subnets)
- **Subnets:** `10.0.20.0/24` (AZ `ap-southeast-5a`) and `10.0.21.0/24` (AZ `ap-southeast-5b`).
- **Description:** Dedicated to backend databases. Deeply isolated without any outbound route to the internet or NAT gateways, minimizing any data extraction surface.
- **Resources:**
  - **Multi-AZ RDS PostgreSQL Instance:** Runs synchronously across multiple availability zones using **Multi-AZ `db.m6g.large` PostgreSQL (2 vCPU, 8GB RAM)** with **50GB gp3 Storage**, guaranteeing high-availability, automatic failover, and robust production database performance.

### 4. Storage Tier (Amazon S3)
- **Description:** Statically hosted media, secure user uploads, and build backups. It is situated outside the VPC but fully integrated.
- **Resources:**
  - **Amazon S3 Bucket:** Fully encrypted standard object storage (with an estimated baseline of ~100 GB storage). Access is managed via IAM policies and secure credentials. Optional Day-2 optimizations include a VPC S3 Gateway Endpoint to bypass NAT processing charges.

---

## Routing Configuration

The architecture manages network traffic flow through three distinct route tables:

### Public Route Table
- Associated with public subnets.
- Routes all outbound traffic (`0.0.0.0/0`) to the **Internet Gateway (IGW)**.

### Private Application Route Table
- Associated with private application subnets.
- Routes all outbound traffic (`0.0.0.0/0`) to the **NAT Gateway** running in the public subnet (with support for multiple NAT Gateways if multi-AZ outbound path high-availability is required).

### Database Route Table
- Associated with private database subnets.
- Contains only local VPC route entries (`10.0.0.0/16`), ensuring database traffic never traverses public routes or internet gateways.
