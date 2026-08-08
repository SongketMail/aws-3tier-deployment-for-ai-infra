---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Load Testing Assumptions & Sizing Guide"
timestamp: 2026-08-05T21:48:38Z
topics: ["aws", "cloud", "architecture", "costing", "performance", "valkey", "rds", "postgresql", "waf", "asg"]
---
# Load Testing Assumptions & Sizing Guide

This document establishes the official workload assumptions, concurrent user definitions, architectural profiles, and target performance objectives governing the load testing, scalability audits, and capacity planning for our secure **AWS 3-Tier Web and AI Infrastructure**.

These assumptions align directly with the performance testing findings and multi-VU scale-up roadmaps, detailing the dual impact of traffic loads on both system performance and financial costing in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)**.

---

## 1. Core Load Testing Objectives & SLA Targets

The primary objective of our load testing is to validate that the multi-tier application stack can scale seamlessly up to 10,000 concurrent Virtual Users (VUs) while adhering to strict Service Level Agreements (SLAs) for security, availability, response times, and cost efficiency.

### Service Level Agreement (SLA) Matrix

| Metric Category | Target SLA / Threshold | Critical Alert Limit | Diagnostic Source |
| :--- | :--- | :--- | :--- |
| **API/Web Latency (P95)** | < 250 ms (Static & Cached) | > 500 ms | Application Load Balancer (ALB) |
| **Transaction Latency (P99)** | < 800 ms (DB Dynamic Writes) | > 1,500 ms | RDS Performance Insights |
| **HTTP Error Rate** | < 0.01% (Zero Gateway Failures) | > 0.1% | ALB Access Logs & CloudWatch |
| **ASG Compute CPU** | < 45% average under peak load | > 75% peak | EC2 CloudWatch Metrics |
| **Valkey Cache Hit Rate** | > 99.0% for session lookups | < 95.0% | ElastiCache Redis/Valkey Engine |
| **Database Load (AAS)** | < Active vCPU count of DB instance | > DB vCPU limit | RDS Performance Insights (AAS) |

---

## 2. Multi-VU Sizing Tier Definitions

To structure our scale-up roadmap, we define five distinct workload profiles simulating realistic growth phases. All financial estimations are calculated using a stable reference exchange rate of **1 USD = 4.50 MYR**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       MULTI-VU PERFORMANCE ROADMAP                      │
├───────────────┬───────────────────────┬─────────────────────────────────┤
│ Target Load   │ Deployment Model      │ Key Scaling Bottleneck Target   │
├───────────────┼───────────────────────┼─────────────────────────────────┤
│ 100 VU        │ Baseline Dev/Staging  │ Idle capacity / Base costs      │
│ 500 VU        │ Cost-Optimized        │ Single points of failure (SPOF) │
│ 2,500 VU      │ High-Performance Prod │ Database full scans & disk I/O  │
│ 5,000 VU      │ Heavy Concurrency     │ Valkey session write durability │
│ 10,000 VU     │ Extreme Concurrency   │ Socket pools & WAF L7 latency   │
└───────────────┴───────────────────────┴─────────────────────────────────┘
```

### A. Sizing & Resource Allocation Matrix

| Target Load (VU) | Deployment Phase / Model | Key Compute Sizing (ASG) | Database Engine Spec | Valkey Cache Sizing | Monthly Cost (USD) | Monthly Cost (MYR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **100 VU** | Baseline Dev / Staging | 2x `t4g.micro` | `db.t4g.micro` (Multi-AZ) | 1x `cache.t4g.micro` | $141.47 USD | RM 636.62 MYR |
| **500 VU** | Cost-Optimized Staged | 2x `t4g.medium` | `db.m6g.large` (Multi-AZ) | 1x `cache.t4g.micro` | $418.60 USD | RM 1,883.70 MYR |
| **2,500 VU** | High-Performance Prod | Avg. 4x `t4g.xlarge` | `db.m6g.xlarge` (Multi-AZ) | 2x `cache.t4g.medium` (HA) | $1,264.56 USD | RM 5,690.52 MYR |
| **5,000 VU** | Heavy Concurrency Prod | Min. 4x `t4g.xlarge` | `db.m7g.2xlarge` (Multi-AZ) | 2x `cache.t4g.medium` (HA) | $1,948.12 USD | RM 8,766.54 MYR |
| **10,000 VU** | Extreme Concurrency Prod | Min. 8x `t4g.xlarge` | `db.m7g.4xlarge` (Multi-AZ) | 4x `cache.m7g.large` (Cluster)| $3,808.88 USD | RM 17,139.96 MYR |

---

## 3. Core Architectural Workload Assumptions

To execute high-fidelity simulated tests, the following application-level and user behavior assumptions are defined:

1. **Read-to-Write Ratio:** The standard web traffic mixture is assumed to be **80% Reads and 20% Writes**.
   - Read operations represent session retrievals, reporting queries, database lookups, and asset downloads.
   - Write operations represent active user logins, database updates (e.g., transactional updates), and reporting uploads.
2. **Session Persistence:** In-memory sessions are handled via ElastiCache for Valkey, with fallback persistence to the relational database layer.
3. **Layer-7 Security Filter Overhead:** All public ingress must transit through AWS WAFv2 with OWASP Top 10 Rules, rate-limiting, and deep-packet payload inspections.
4. **Network Boundaries:** Direct Internet access is prohibited for application servers. Outbound egress is routed exclusively through NAT Gateways.
5. **Auto Scaling Responsiveness:** ASG cooldown periods are set to 180 seconds, triggering scale-up events when average compute CPU exceeds 50% for two consecutive 1-minute evaluation periods.

---

## 4. Key Performance Bottlenecks & Critical Remediation

Based on empirical performance testing audits under heavy loads, several system-level bottlenecks were identified and resolved. These findings serve as design rules for future system scale-ups.

### A. Database Query Indexing (2,500 VU Bottleneck)
* **Problem:** Under 2,500 concurrent users, RDS MariaDB/PostgreSQL active database load surged to a peak of 8.0 Average Active Sessions (AAS), blocking transactions on database table handlings (`wait/io/table/sql/handler`).
* **Root Cause:** A complete absence of composite indexes on aggregate and transactional tables, forcing expensive disk filesort operations and full table scans.
* **Remediation:**
  - Create composite index on MariaDB summary tables: `idx_summary_agg (status, tenant_id, total)`.
  - Create composite index on reconciliation lookup tables: `idx_recons_lookup (reference_id, is_reconciled)`.
  - Create composite index on transaction tables: `idx_parking_lookup (refno, user_id)`.

### B. Storage Disk Write Sync & IOPS (2,500 VU Bottleneck)
* **Problem:** High-concurrency update transactions caused PostgreSQL backend processes to stall, creating an `I/O:walSync` disk write wait bottleneck.
* **Root Cause:** The default GP3 general-purpose storage volume ran out of write capabilities under sustained, concurrent transactional traffic.
* **Remediation:** Upgrade PostgreSQL storage from GP3 to **Provisioned IOPS (io2)** with at least 5,000 Custom IOPS and 250 MB/s throughput, reducing sync latency from 150ms to under 8ms.

### C. Web Application Firewall regional ACL Overhead (10,000 VU Bottleneck)
* **Problem:** Layer-7 WAF inspection rules introduced an additional latency overhead of up to 20ms under heavy loads.
* **Root Cause:** Deep packet inspection evaluating hundreds of complex regex patterns for every request.
* **Remediation:** Nest and optimize Web ACL rules, utilize precise regex match patterns, and deploy explicit scope-down statements using `FieldToMatch` settings (e.g., limiting expensive body/payload inspection rules specifically to JSON API requests via `UriPath` and `Method` constraints) to prevent inspection overhead on safe static assets while retaining robust baseline protections.

### D. Socket Exhaustion & Process Sizing (10,000 VU Bottleneck)
* **Problem:** Standard Nginx connections and PHP-FPM worker pools were exhausted, generating minor Gateway Timeout (504) errors.
* **Remediation:**
  - Increase `worker_connections` to 20,480 in Nginx configurations.
  - Tune the keep-alive timeout to 15 seconds to recycle socket connections rapidly.
  - Configure the PHP-FPM process manager to use static allocation (`pm = static`) for dedicated production environments, scaling `pm.max_children` to 120+ based on physical vCPU capacity and measured per-process memory consumption (assuming ~45MB per PHP-FPM process) to prevent physical RAM exhaustion.

### E. In-Memory Session Durability (5,000 VU Warning)
* **Problem:** Under network partition events or failovers, session data stored in Valkey could be lost due to asynchronous replication.
* **Remediation:**
  - For critical transactional data, route writes directly to RDS.
  - If using Valkey for durable session management:
    - **AWS ElastiCache managed clusters:** Configure the Durability parameter and verify `EffectiveDurability=sync` is active.
    - **Self-hosted Valkey instances:** Start the database engine explicitly with `--durability sync` to guarantee synchronous replication logging to replica nodes before acknowledging client writes.

---

## 5. Load Test Sizing Financial Alignments (FinOps)

Operating high-concurrency systems requires robust resources, which increases the monthly AWS spend. To achieve maximum cost efficiency under scale, we define the following day-2 FinOps levers:

1. **Reserved Instances (RIs):** Commit to a 1-year or 3-year standard contract for the primary Multi-AZ `db.m7g` database engines to unlock up to **30% - 35% savings** compared to on-demand rates.
2. **Compute Savings Plans:** Secure a 1-year or 3-year Compute Savings Plan to achieve **25% - 43% discounts** on the dynamic Auto Scaling Group EC2 application servers (`t4g` and `c7g` families).
3. **S3 Intelligent-Tiering and Lifecycle Policies:** Implement automated rules moving historical logs and backup archives to S3 Glacier Flexible Archive, yielding up to **80% - 84% savings** on long-term storage.
4. **VPC S3 Gateway Endpoints:** Configure free S3 Gateway Endpoints in private subnets, allowing application servers to bypass the NAT Gateway and eliminate NAT Gateway data-processing fees ($0.045/GB in `ap-southeast-5`) for log and file transfers.
