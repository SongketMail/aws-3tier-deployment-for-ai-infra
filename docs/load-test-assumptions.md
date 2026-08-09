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

---

## 6. Cost-to-Performance Capability Mapping (Max Performance per Cost Plan)

To bridge the gap between financial blueprints and operational performance, this section defines the **maximum traffic load, concurrent Virtual Users (VUs), and transactional throughput** that each of our budgeted costing profiles can safely handle. By mapping the hardware specifications from our costing plans to empirical load thresholds, we outline the exact return on investment (ROI) for every ringgit (RM) and dollar (USD) spent in the **AWS Malaysia region (`ap-southeast-5`)**.

### A. Complete Capability Mapping Table

The following table maps every costing budget plan defined in [**Estimated Costing**](costing.html) and our load testing sizing models to their absolute maximum performance boundaries under our target 80% Read and 20% Write workload:

| Costing Profile / Budget Tier | Monthly Cost (USD) | Monthly Cost (MYR) | Max Concurrent Load (VU) | Max Web/API Throughput (RPS) | Max DB Write Load (TPS) | Max Concurrent RAG Ingestions |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dev / POC Environment** | $138.50 | RM 623.25 | **100 VU** | 50 RPS | 15 TPS | 5 parses/min |
| **Load-Test 100 VU Sizing** | $141.47 | RM 636.62 | **100 VU** | 60 RPS | 18 TPS | 6 parses/min |
| **Load-Test 500 VU Sizing** | $418.60 | RM 1,883.70 | **500 VU** | 250 RPS | 75 TPS | 15 parses/min |
| **Baseline Cost-Optimised Plan** | $426.75 | RM 1,920.00 | **600 VU** | 300 RPS | 95 TPS | 20 parses/min |
| **Staging Environment (Dual-AZ)** | $668.11 | RM 3,006.50 | **1,200 VU** | 600 RPS | 180 TPS | 35 parses/min |
| **High-Perf Developer-Aligned** | $1,064.46 | RM 4,790.00 | **2,500 VU** | 1,250 RPS | 400 TPS | 80 parses/min |
| **Load-Test 2,500 VU Sizing** | $1,264.56 | RM 5,690.52 | **2,500 VU** | 1,300 RPS | 420 TPS | 85 parses/min |
| **Enterprise Production (Multi-AZ)**| $1,665.61 | RM 7,495.25 | **5,000 VU** | 2,500 RPS | 800 TPS | 150 parses/min |
| **Load-Test 5,000 VU Sizing** | $1,948.12 | RM 8,766.54 | **5,000 VU** | 2,600 RPS | 850 TPS | 160 parses/min |
| **Load-Test 10,000 VU Sizing** | $3,808.88 | RM 17,139.96 | **10,000 VU** | 5,000 RPS | 1,600 TPS | 300 parses/min |

---

### B. Detailed Performance Capabilities per Budget Tier

#### 1. Dev / POC Environment & Load-Test 100 VU Sizing (Budget: ~$138.50 - $141.47 USD / Month)
* **Maximum Load Capacity:** **100 Concurrent VUs**
* **System Capabilities:**
  - **Requests Per Second (RPS):** Up to **50 - 60 RPS** for cached or static assets; handles basic REST API calls at 15 RPS.
  - **Database Write Limit (TPS):** **15 - 18 TPS** on `db.t4g.micro` before experiencing storage queue backlogs.
  - **AI / RAG Capability:** Handles **5 - 6 concurrent document parses** (using light open-source OCR models) or standard embedding processing streams. Memory limitations on the `t4g.medium` compute node constrain heavy layout-parsing pipelines (DeepDoc).
* **Workload Application:** Perfect for internal functional testing, single-developer prototype verification, and API endpoint integration checking.

#### 2. Load-Test 500 VU Sizing & Baseline Cost-Optimised Plan (Budget: ~$418.60 - $426.75 USD / Month)
* **Maximum Load Capacity:** **500 - 600 Concurrent VUs**
* **System Capabilities:**
  - **Requests Per Second (RPS):** Handles up to **250 - 300 RPS** safely at the ALB, with sub-100ms response times for cached pages.
  - **Database Write Limit (TPS):** **75 - 95 TPS** supported by the Multi-AZ `db.m6g.large` database, providing resilient storage write operations.
  - **AI / RAG Capability:** Handles up to **15 - 20 concurrent document chunking** operations. ElastiCache Valkey (`cache.t4g.micro`) optimizes active session lookup processing to keep memory footprint minimal.
* **Workload Application:** Ideal for team-wide user acceptance testing, continuous integration (CI) environments, and small-scale client demonstrations.

#### 3. Staging Environment (Budget: ~$668.11 USD / Month)
* **Maximum Load Capacity:** **1,200 Concurrent VUs**
* **System Capabilities:**
  - **Requests Per Second (RPS):** Safely services **600 RPS** across dual ASG compute nodes (`c7g.xlarge` offering 8 vCPU, 16GB RAM combined).
  - **Database Write Limit (TPS):** **180 TPS** supported by Multi-AZ `db.t4g.large`, managing regular structured data modifications.
  - **AI / RAG Capability:** Supports up to **35 concurrent document parsing** operations. Dedicated Dual-AZ Valkey caching nodes (`cache.t4g.medium`) ensure continuous, lightning-fast state transitions and session synchronisation.
* **Workload Application:** Designed for complete pre-production verification, automated QA regressions, multi-AZ failover testing, and staging security scans.

#### 4. High-Performance Developer-Aligned & Load-Test 2,500 VU Sizing (Budget: ~$1,064.46 - $1,264.56 USD / Month)
* **Maximum Load Capacity:** **2,500 Concurrent VUs**
* **System Capabilities:**
  - **Requests Per Second (RPS):** Sustains **1,250 - 1,300 RPS** at sub-150ms latency across high-performance compute clusters (up to 4x `t4g.xlarge` nodes).
  - **Database Write Limit (TPS):** **400 - 420 TPS** utilizing a Multi-AZ `db.m6g.xlarge` engine, resolving dynamic user data entries cleanly.
  - **AI / RAG Capability:** Processes **80 - 85 concurrent document parses**. Leverages 50 GB standard shared persistent storage (Amazon EFS) to pre-load and cache heavy pre-trained model weights.
* **Workload Application:** Standard production configuration for active AI workloads, supporting high-frequency Langfuse tracing, interactive RAG conversational pipelines, and continuous customer-facing transactions.

#### 5. Enterprise Production Environment & Load-Test 5,000 VU Sizing (Budget: ~$1,665.61 - $1,948.12 USD / Month)
* **Maximum Load Capacity:** **5,000 Concurrent VUs**
* **System Capabilities:**
  - **Requests Per Second (RPS):** Processes **2,500 - 2,600 RPS** with WAF L7 protection and streaming response structures active.
  - **Database Write Limit (TPS):** **800 - 850 TPS** supported by Multi-AZ `db.m7g.xlarge` or `db.m7g.2xlarge` databases equipped with GP3 storage scaling.
  - **AI / RAG Capability:** Processes **150 - 160 concurrent high-fidelity document layout parsings** (DeepDoc/OCR) and continuous vector database indexing streams.
* **Workload Application:** Enterprise-grade environment guaranteeing 99.99% availability, built to absorb massive concurrent campaigns, high-frequency transactional loads, and enterprise-wide AI agent executions.

#### 6. Load-Test 10,000 VU Sizing (Budget: ~$3,808.88 USD / Month)
* **Maximum Load Capacity:** **10,000 Concurrent VUs**
* **System Capabilities:**
  - **Requests Per Second (RPS):** Scales up to **5,000 RPS** utilizing 8x `t4g.xlarge` instances across three availability zones.
  - **Database Write Limit (TPS):** **1,600 TPS** on Multi-AZ `db.m7g.4xlarge` utilizing provisioned IOPS storage to prevent synchronization bottlenecks.
  - **AI / RAG Capability:** Handles **300 concurrent document parsings** simultaneously. Clustered `cache.m7g.large` node group maintains seamless, high-concurrency memory capabilities.
* **Workload Application:** High-end production scaling designed for peak promotional traffic, public utility campaigns, or intensive batch data ingestion schedules.
