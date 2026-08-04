---
layout: default
title: "Disaster Recovery Options & Sovereignty Guide"
---

# Disaster Recovery (DR) Options & National Sovereignty Guide

## 1. Executive Summary & Context

Maintaining system resilience is critical for enterprise deployment. This guide establishes a comprehensive, production-ready Disaster Recovery (DR) playbook modeled directly after the official AWS whitepaper [**"Disaster Recovery of Workloads on AWS: Recovery in the Cloud"**](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html).

This guide addresses three core dimensions:
1. **Existing Architecture Alignment:** Adapting DR practices directly to our Multi-AZ, 3-Tier layout (WAFv2, ALB, private Auto Scaling Groups for Frontend, Backend, and AI tiers, Standalone EC2 staging environments, Multi-AZ RDS PostgreSQL 16 database, Amazon ElastiCache for Valkey, and Amazon EFS shared storage).
2. **Malaysia National Sovereignty:** A strict regulatory compliance review under the **Malaysian Personal Data Protection Act (PDPA) 2010** (including the **Personal Data Protection (Amendment) Act 2024** and the **2025 Cross-Border Personal Data Transfer Guidelines (CBPDT)**).
3. **Financial Transparency (USD / MYR):** Granular cost breakdowns comparing **In-Region Multi-AZ DR** (sovereign, 100% data residency in Malaysia `ap-southeast-5`) and **Cross-Region DR** (replicated to Singapore `ap-southeast-1` or Jakarta `ap-southeast-3`).

All currency estimations use a baseline baseline conversion rate of **1 USD ≈ 4.50 MYR**.

---

## 2. Malaysia National Sovereignty & Regulatory Compliance

When designing DR topologies for applications processing citizen data in Malaysia, **data sovereignty** and **jurisdictional boundaries** are primary architectural drivers.

```
┌────────────────────────────────────────────────────────────────────────┐
│               Data Residency & Transfer Compliance Pathways            │
├──────────────────────────────────────┬─────────────────────────────────┤
│    In-Region DR (ap-southeast-5)     │   Cross-Region DR (Out of MY)   │
├──────────────────────────────────────┼─────────────────────────────────┤
│ • 100% Malaysian Sovereignty         │ • Subject to PDPA Section 129   │
│ • No Cross-Border transfer concerns  │ • Requires Transfer Impact (TIA)│
│ • Fully compliant with 2025 CBPDT    │ • Explicit Data Subject Consent │
│ • Complete immunity to foreign laws  │ • Requires Contractual Clauses  │
└──────────────────────────────────────┴─────────────────────────────────┘
```

### 2.1 The Personal Data Protection Act (PDPA) & 2024/2025 Frameworks
* **Section 129 Principal Prohibition:** Under the Malaysian PDPA 2010, transferring personal data outside of Malaysia is prohibited unless specifically exempted by the Minister or falling under specific statutory exceptions.
* **The 2024 Amendments:** The Personal Data Protection (Amendment) Act 2024 introduced mandatory **Data Breach Notifications (DBN)** and the compulsory appointment of a **Data Protection Officer (DPO)**, escalating the legal risk of data exposure.
* **The 2025 CBPDT Guidelines:** Published in April 2025 by the Personal Data Protection Commissioner, the **Cross Border Personal Data Transfer (CBPDT) Guidelines** clarify that data controllers transferring data outside Malaysia must conduct a **Transfer Impact Assessment (TIA)** to ensure the destination provides "adequate protection" substantially similar to the PDPA.

### 2.2 Sovereign In-Region Multi-AZ DR vs. Cross-Region DR

#### Sovereign In-Region Multi-AZ DR (Absolute Residency)
* **Architectural Flow:** All primary workloads and disaster recovery assets reside entirely within the three physical Availability Zones of the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)**.
* **PDPA Standing:** Fully compliant out of the box. Because data never crosses Malaysia's geographical borders, it is **exempt** from Section 129 restrictions, TIAs, or extra consent requirements.
* **Jurisdictional Immunity:** Data remains protected exclusively under Malaysian courts. It is immune to extraterritorial access requests (such as the US CLOUD Act or Singaporean administrative warrants) that might apply if the data was replicated overseas.

#### Cross-Region DR (Jurisdictional Border Crossing)
* **Architectural Flow:** Backups, read-replicas, or standby environments are copied from `ap-southeast-5` to **Singapore (`ap-southeast-1`)** or **Jakarta (`ap-southeast-3`)**.
* **PDPA Section 129 Compliance Checklist:** To legally implement Cross-Region replication, the organization must fulfill these strict legal requirements:
  1. **Explicit Data Subject Consent:** Users must actively opt-in to their data being transferred and stored in Singapore/Jakarta, detailed within a clear, updated Privacy Notice.
  2. **Transfer Impact Assessment (TIA):** The DPO must perform and log a formal TIA assessing the recipient country's data laws (e.g., Singapore's PDPA 2012 or Indonesia's UU PDP).
  3. **Data Processor Agreements:** Binding contracts with AWS and any third-party processors enforcing technical and organizational safety standards equivalent to Malaysian standard standards.

---

## 3. Disaster Recovery Spectrum Analysis

We analyze the four standard AWS Disaster Recovery options, alongside AWS Elastic Disaster Recovery (AWS DRS) as a modern, cost-optimized, and near-zero RPO hybrid strategy. Each strategy presents a distinct balance of Recovery Point Objective (RPO), Recovery Time Objective (RTO), implementation complexity, and ongoing operating cost.

```
     Low Cost                                                                                                         High Cost
     High RPO/RTO                                                                                                     Near-Zero RPO/RTO
     ┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
     │                      │                      │                      │                      │  AWS Elastic DR      │
     │   Backup & Restore   │     Pilot Light      │     Warm Standby     │  Multi-Site Active-  │      (AWS DRS)       │
     │                      │                      │                      │        Active        │ (Highly cost-eff.    │
     │                      │                      │                      │                      │   Sub-Minute RPO)    │
     └──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

---

### Strategy A: Backup and Restore

A passive approach where virtual machine images, database snapshots, and configuration files are regularly backed up and restored to a target environment only after an outage is declared.

```
[ Primary: ap-southeast-5 ]                               [ Target (Sovereign or Remote) ]
   ├── AWS Backup  ══════════ (Scheduled Copy) ══════════► [ EBS Snapshots & RDS Backups ]
   └── S3 Replication ═══════ (Cross-Bucket Sync) ═══════► [ S3 Backup Vault ]
```

#### 1. Architectural Setup & Component Layout
* **Database (RDS):** Automated daily snapshots and transaction logs stored via AWS Backup. In-Region copies are kept in a separate secure AWS account; Cross-Region copies sync to Singapore (`ap-southeast-1`) S3 buckets.
* **Compute (ASG):** Launch Templates are backed up. AMIs of the Frontend, Backend, and AI Standalone/ASG nodes are pre-baked using our Packer/Ansible pipeline and stored in local or remote AMI catalogs.
* **Shared Storage (EFS):** Daily EFS backups handled via AWS Backup. EFS filesystems are not pre-provisioned in the target environment to save costs; they are recreated during recovery.
* **DNS & Routing (Route 53):** Route 53 pointing to the primary ALB. No active health check routing is configured. Manual DNS update is required during a failover event.
* **Valkey Cache:** No replication. Caching nodes are left unprovisioned in the target area and cold-booted during restoration.

#### 2. Recovery Objectives
* **Recovery Point Objective (RPO):** **24 Hours** (determined by backup execution intervals).
* **Recovery Time Objective (RTO):** **4 to 8 Hours** (time needed to provision network infrastructure, restore RDS database storage, spin up EC2 instances from AMIs, and update DNS).

#### 3. Trade-offs & Analysis
* **Cost:** Extremely low. No active compute, load balancer, or database instances run in the DR zone.
* **Complexity:** Low configuration complexity, but high manual recovery complexity during an incident.
* **Sovereignty:** If utilizing Cross-Region Backup and Restore, encrypted database snapshots reside in Singapore, which mandates standard PDPA Section 129 consent and TIAs. In-Region backups are completely sovereign.

---

### Strategy B: Pilot Light

A core database and persistent storage layer are kept actively running and synchronized, while the compute/application server layer remains unprovisioned or "turned off" until a disaster occurs.

```
[ Primary ap-southeast-5 ]                                [ Target: ap-southeast-1 or -5b ]
   ├── Multi-AZ RDS Active                                   ├── Read Replica Running (m6g)
   ├── EFS / S3 Source                                       ├── EFS Replica Active (Sync)
   └── ASG (Active Nodes)   (No Active Compute) ════════════►└── ASG Desired Capacity = 0
```

#### 1. Architectural Setup & Component Layout
* **Database (RDS):** A minimal, single-AZ RDS PostgreSQL read-replica is kept online and continuously synchronized via asynchronous replication.
* **Compute (ASG):** Launch Templates are active in the target VPC, but the ASG **Desired Capacity is set to 0**. Standalone staging environments are not provisioned.
* **Shared Storage (EFS):** Continuous replication to a target EFS filesystem using AWS EFS Replication.
* **DNS & Routing:** Route 53 DNS is configured with active health checks. However, failover requires changing the ASG desired capacity to active levels and waiting for compute nodes to bootstrap.
* **Valkey Cache:** Unprovisioned. Provisioned only during failover.

#### 2. Recovery Objectives
* **Recovery Point Objective (RPO):** **< 5 Minutes** (determined by RDS replica lag and EFS replication latency).
* **Recovery Time Objective (RTO):** **30 to 45 Minutes** (time to promote RDS replica to primary, scale the ASG up from 0 to target size, wait for application health checks to pass, and update Route 53).

#### 3. Trade-offs & Analysis
* **Cost:** Moderate. You pay for continuous RDS replica compute and persistent EFS/S3 storage, but avoid active EC2 compute costs.
* **Complexity:** Medium. Requires automating the promotion of the database and the auto-scaling group scale-up.
* **Sovereignty:** Cross-Region replica databases contain active, unencrypted-in-memory data in Singapore/Jakarta. This triggers strict PDPA compliance, requiring a comprehensive TIA and explicit user consent. In-Region Pilot Light (using a separate VPC in the same region) is fully sovereign.

---

### Strategy C: Warm Standby

A scaled-down but fully functional copy of the entire 3-tier architecture is kept running continuously in the target zone. It handles zero (or minimal) active traffic under normal operations but can instantly scale up to handle the production load if the primary site fails.

```
[ Primary ap-southeast-5 ]                                [ Target: ap-southeast-1 or -5b ]
   ├── ALB (Active)                                          ├── ALB (Active Standby)
   ├── ASG (2x t4g.xlarge Active)                            ├── ASG (1x t4g.medium Standby)
   ├── Multi-AZ RDS (Active)   ══ (Async Replication) ══════►├── RDS Read Replica (Active)
   └── Valkey Cache (Active)                                 └── Valkey Cache (Active)
```

#### 1. Architectural Setup & Component Layout
* **Presentation Tier:** A standby ALB is active. AWS WAFv2 is associated and running.
* **Compute Tier (ASG):** The standby ASG runs continuously with a minimal capacity (e.g., 1x `t4g.medium` instead of the production 2x `t4g.xlarge`). Standalone staging instances are unprovisioned to optimize cost.
* **Database (RDS):** An active RDS PostgreSQL read-replica runs continuously in the standby zone.
* **Valkey Cache:** A minimal single-node ElastiCache Valkey (`cache.t4g.micro`) runs to maintain cache readiness.
* **Shared Storage (EFS):** Continuous EFS Replication keeps model weights and configurations in sync.
* **DNS & Routing:** Route 53 Active-Passive failover routing is configured. Health checks automatically redirect traffic to the standby ALB if the primary fails.

#### 2. Recovery Objectives
* **Recovery Point Objective (RPO):** **< 1 Minute** (near-real-time database and storage replication).
* **Recovery Time Objective (RTO):** **5 to 10 Minutes** (traffic is routed instantly; auto-scaling takes a few minutes to scale compute instances to full production sizing).

#### 3. Trade-offs & Analysis
* **Cost:** High. Requires running a second ALB, active EC2 instances, replica RDS instances, EFS replication, and an ElastiCache node.
* **Complexity:** Medium-High. Requires robust automation for target scaling policies and failover signaling.
* **Sovereignty:** Storing live, unencrypted client data continuously on active databases in foreign regions requires strict PDPA Section 129 audit trails and TIAs.

---

### Strategy D: Multi-Site Active-Active

Traffic is split dynamically across two identical, full-scale production environments running simultaneously in two separate zones. Both sites actively serve client requests.

```
                                [ Route 53 Latency / Geolocation Routing ]
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼ (50% Traffic)                               ▼ (50% Traffic)
         [ Site A: ap-southeast-5 ]                    [ Site B: ap-southeast-1 ]
         ├── ALB (Active)                              ├── ALB (Active)
         ├── ASG (2x t4g.xlarge)                       ├── ASG (2x t4g.xlarge)
         ├── Multi-AZ RDS (Primary)  ◄─ (Bi-dir Sync) ─►├── Multi-AZ RDS (Primary)
         └── Valkey (Active Cluster)                   └── Valkey (Active Cluster)
```

#### 1. Architectural Setup & Component Layout
* **Presentation Tier:** Active ALBs and WAFv2 are deployed in both sites.
* **Compute Tier (ASG):** Full-scale ASGs (2x `t4g.xlarge` nodes) run actively in both regions. All Standalone AMI-baking instances are kept in sync.
* **Database (RDS):** Configured as a cross-region active-active database cluster (utilizing Aurora Global Database or custom bi-directional replication engines), or active-passive database with write-routing to the primary site.
* **Valkey Cache:** Independent active Valkey clusters in each region.
* **Shared Storage (EFS):** Continuous bi-directional synchronization or dual EFS staging setups.
* **DNS & Routing:** Route 53 is configured with Geolocation or Latency-based routing to dynamically distribute user requests.

#### 2. Recovery Objectives
* **Recovery Point Objective (RPO):** **Near Zero (Real-time)**.
* **Recovery Time Objective (RTO):** **Near Zero** (instantaneous failover as both environments are already serving live traffic).

#### 3. Trade-offs & Analysis
* **Cost:** Extremely High. Double the baseline production cost plus significant cross-region data transfer replication fees.
* **Complexity:** Extremely High. Requires solving split-brain scenarios, database write collisions, and high data consistency synchronization challenges.
* **Sovereignty:** Deeply critical. 50% of Malaysian citizen data is processed and stored outside local jurisdiction in real time. This triggers comprehensive PDPA scrutiny, making TIAs, explicit consent notices, and regulatory registration mandatory.

---

### Strategy E: AWS Elastic Disaster Recovery (AWS DRS)

AWS Elastic Disaster Recovery (AWS DRS) minimizes downtime and data loss with fast, reliable recovery of on-premises and cloud-based applications using affordable storage, minimal compute, and point-in-time recovery. It provides sub-minute RPO and minutes-level RTO.

```
[ On-Premises or Remote Cloud Source Servers ]            [ Target Staging Area (ap-southeast-5) ]
   ├── AWS DRS Replication Agent                          ├── Continuous Block-Level Replication (TCP 1500)
   ├── Source Disks (EBS/On-Prem Storage)  ══════════════►├── Lightweight EC2 Replication Servers (t3.small)
   └── Operating System State                             └── Low-Cost EBS Staging Volumes (gp3/sc1)
                                                                        │
                                                                        ▼ (In the Event of Disaster/Drill)
                                                          [ Target Recovery Area (ap-southeast-5) ]
                                                          └── Launches fully-provisioned target instances
```

#### 1. Architectural Setup & Component Layout
* **Source Servers:** Install the AWS Elastic Disaster Recovery Replication Agent on target source servers (on-premises or remote cloud nodes) to initiate secure, block-level data replication.
* **Staging Area Subnet:** Data is continuously replicated to a dedicated, low-cost staging area subnet in the designated AWS account and Region (e.g., `ap-southeast-5`).
* **Compute & Storage Optimization:** Staging costs are highly minimized. Lightweight, automatically managed EC2 replication instances (e.g., `t3.small` nodes) handle incoming blocks, while affordable EBS volumes (gp3 or low-cost sc1) act as the replication target disks.
* **Non-Disruptive Testing:** Allows running seamless, non-disruptive disaster recovery drills and tests at any time without impacting active replication or source servers.
* **Drill/Recovery Launches:** When a failover or drill is initiated, AWS DRS automatically launches target EC2 instances based on the most up-to-date server state or a specified historical point-in-time state.
* **Failback Replication:** After the primary site issue is resolved, data replication is initiated in reverse back to the primary site, ensuring seamless failback.

#### 2. Recovery Objectives
* **Recovery Point Objective (RPO):** **Seconds to Sub-Minute** (continuous, real-time block-level asynchronous replication).
* **Recovery Time Objective (RTO):** **Minutes** (automated launch, conversion, and orchestration of recovery instances).

#### 3. Trade-offs & Analysis
* **Cost:** Highly Cost-Effective. Replicating servers cost only a nominal hourly software license fee ($0.028 per server per hour) plus low-cost staging compute (`t3.small`) and staging EBS volumes, instead of running full warm standby or active-active duplicate environments.
* **Complexity:** Medium. Requires installing replication agents on source servers and configuring launch templates, but failover and failback orchestration are highly automated.
* **Sovereignty:** 100% Sovereign when staging and recovery are targeted inside the **AWS Malaysia Region (`ap-southeast-5`)**. Because the continuous block replication targets local sovereign physical boundaries, it completely satisfies PDPA and 2025 CBPDT requirements for localized residency, avoiding complex cross-border Transfer Impact Assessments (TIAs).

---

## 4. Comprehensive Cost Estimation Model (USD & MYR)

To provide clear financial visibility, we present granular monthly costs for all four DR strategies, comparing:
1. **Sovereign In-Region Multi-AZ DR** (All standby resources deployed inside `ap-southeast-5` using a separate DR VPC).
2. **Cross-Region DR** (Standby resources deployed in Singapore `ap-southeast-1`).

All prices are calibrated for On-Demand rates (~730 hours/month) for our **High-Performance Production Stack**.

---

### 4.1 Granular Monthly DR Cost Matrix (USD / Month)

| Component | Strategy A: Backup & Restore | Strategy B: Pilot Light | Strategy C: Warm Standby | Strategy D: Active-Active | Strategy E: AWS DRS (3 Node Baseline) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Networking & NAT** | $0.00 | $0.00 (No outbound needed) | $32.85 (1x NAT Gateway) | $32.85 (1x NAT Gateway) | $0.00 (Staging in existing private subnet) |
| **Public IPv4 Addr** | $0.00 | $0.00 | $7.30 (1x NAT IP, 1x ALB IP) | $10.95 (1x NAT, 2x ALB IPs) | $0.00 |
| **ALB & WAFv2** | $0.00 | $0.00 | $25.03 (ALB + WAF ACL) | $41.46 (ALB + WAF + Rules) | $0.00 (Cold; deployed during failover) |
| **Compute (ASG)** | $0.00 (Desired = 0) | $0.00 (Desired = 0) | $49.06 (1x `t4g.medium` warm) | $196.22 (2x `t4g.xlarge` active) | $15.18 (1x shared `t3.small` replication node) |
| **Database (RDS)** | $0.00 | $221.92 (1x `db.m6g.large` replica) | $443.84 (Multi-AZ replica) | $443.84 (Multi-AZ active) | $0.00 (Replicated at volume block layer) |
| **Valkey Cache** | $0.00 | $0.00 | $9.34 (`cache.t4g.micro`) | $39.71 (`cache.t4g.medium`) | $0.00 (Unprovisioned in staging) |
| **Storage (EFS)** | $0.00 | $15.00 (50GB replica) | $15.00 (50GB replica) | $15.00 (50GB active) | $15.00 (50GB replica) |
| **Storage (S3)** | $2.30 (100GB backup) | $2.30 (100GB backup) | $2.30 (100GB backup) | $2.30 (100GB active) | $2.30 (100GB backup/snapshots) |
| **DRS Service Fee** | $0.00 | $0.00 | $0.00 | $0.00 | $61.32 (3 servers * $0.028/hr * 730 hrs) |
| **Data Replication** | $5.00 (AWS Backup fees) | $15.00 (RDS & EFS sync) | $30.00 (Live RDS & EFS sync)| $120.00 (High bi-dir sync) | $18.50 (Block staging volumes & snap sync)|
| **TOTAL (In-Region)** | **$7.30 USD** | **$254.22 USD** | **$614.42 USD** | **$902.33 USD** | **$112.30 USD** |
| **TOTAL (Cross-Region)**| **$11.50 USD** | **$289.50 USD** | **$664.80 USD** | **$982.50 USD** | **$135.50 USD** |

*Note: Cross-Region costs are slightly higher due to AWS Cross-Region Data Transfer Egress fees ($0.09/GB from ap-southeast-5) and marginally higher base pricing in ap-southeast-1. AWS DRS cost modeling assumes replicating 3 active EC2 compute nodes (Frontend, Backend, AI Tier) into a secure staging subnet.*

---

### 4.2 Local Currency Equivalent Comparison (MYR / Month)

Using the exchange baseline of **1 USD ≈ 4.50 MYR**, the monthly DR infrastructure spend equates to:

```
┌────────────────────────────────────────────────────────────────────────┐
│               Monthly DR Cost Comparison (MYR equivalent)              │
│                                                                        │
│ In-Region (ap-southeast-5)                                             │
│  ├── Backup & Restore ═► RM 32.85                                      │
│  ├── AWS DRS          ═► RM 505.35     (Highly Recommended)            │
│  ├── Pilot Light     ═► RM 1,143.99                                    │
│  ├── Warm Standby    ═► RM 2,764.89                                    │
│  └── Active-Active   ═► RM 4,060.49                                    │
│                                                                        │
│ Cross-Region (Singapore/Jakarta)                                       │
│  ├── Backup & Restore ═► RM 51.75                                      │
│  ├── AWS DRS          ═► RM 609.75                                      │
│  ├── Pilot Light     ═► RM 1,302.75                                    │
│  ├── Warm Standby    ═► RM 2,991.60                                    │
│  └── Active-Active   ═► RM 4,421.25                                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Decision Matrix & Strategy Trade-offs

To guide executive management through the selection process, we present a technical evaluation matrix:

| Evaluation Dimension | Strategy A: Backup & Restore | Strategy B: Pilot Light | Strategy C: Warm Standby | Strategy D: Active-Active | Strategy E: AWS DRS (Elastic DR) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Target RPO** | 24 Hours | < 5 Minutes | < 1 Minute | Near Real-time | **Seconds to Sub-Minute** |
| **Target RTO** | 4 to 8 Hours | 30 to 45 Minutes | 5 to 10 Minutes | Near Zero | **Minutes** |
| **Relative Cost** | Extremely Low (1x) | Moderate (35x) | High (85x) | Very High (120x) | **Low-to-Moderate (15x)** |
| **Engineering Overhead** | Low (Standard backups) | Medium (Failover scripts) | High (Automated Route 53) | Extremely High | Medium (Agent setup) |
| **Regulatory Risk** | Minimal | Medium (Replica active) | High (Continuous Sync) | Extremely High | Minimal (Sovereign staging) |
| **PDPA Compliance Path** | Simple | Requires TIA & Consent | Requires TIA & Consent | Requires Full Audit | Simple (100% In-Region) |
| **Sovereignty Standing** | **100% Secure (In-Region)**| **100% Secure (In-Region)**| **100% Secure (In-Region)**| **100% Secure (In-Region)**| **100% Secure (In-Region)**|

---

## 6. Strategic Recommendations & Roadmap

To balance **business continuity**, **cost-efficiency**, and **strict compliance with Malaysia National Sovereignty (PDPA)**, the following phased roadmap is recommended:

```
                     [ Start: Launch Infrastructure ]
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │ sovereign backup & restore   │ <-- Phase 1: Immediate Deployment
                     │ (100% in ap-southeast-5)     │     Est. Cost: ~$7.30 / mo (RM 32.85)
                     └──────────────┬───────────────┘
                                    │
                    Has the business RTO objective
                    shrunk to under 1 hour?
                                    │
                     ┌──────────────┴──────────────┐
                     │ YES                         │ NO (Remain on Phase 1)
                     ▼                             ▼
                     ┌──────────────────────────────┐
                     │ AWS Elastic DR (AWS DRS)     │ <-- Phase 2: Highly Cost-Effective Near-Zero RPO
                     │ (100% in ap-southeast-5)     │     Est. Cost: ~$112.30 / mo (RM 505.35)
                     └──────────────┬───────────────┘
                                    │
                    Does the database require active
                    hot SQL query read-replicas?
                                    │
                     ┌──────────────┴──────────────┐
                     │ YES                         │ NO (Remain on Phase 2)
                     ▼                             ▼
                     ┌──────────────────────────────┐
                     │ sovereign pilot light        │ <-- Phase 3: Scale Resiliency with Hot DBs
                     │ (100% in ap-southeast-5)     │     Est. Cost: ~$254.22 / mo (RM 1,143.99)
                     └──────────────────────────────┘
```

### Phase 1: Deploy Sovereign In-Region Backup & Restore (Default Baseline)
* **Action:** Configure AWS Backup to take daily snapshots of our Multi-AZ RDS PostgreSQL database, the EFS model volume, and the gp3 EBS volumes of our compute nodes. Store these backups securely inside `ap-southeast-5`.
* **Sovereignty Advantage:** 100% compliant with the Malaysian PDPA. Zero data crosses national borders, completely bypassing Section 129 regulatory hurdles, saving legal/DPO consultation fees.
* **Cost Impact:** Negligible baseline charge (~$7.30 USD / RM 32.85 per month).

### Phase 2: Implement AWS Elastic Disaster Recovery (AWS DRS) (Near-Zero RPO / RTO)
* **Action:** Install the AWS DRS Replication Agent on active servers to continuously replicate block-level changes asynchronously into a dedicated staging area subnet inside `ap-southeast-5`. Configure DRS launch templates to spin up fully-provisioned target instances upon a drill or failover event.
* **Sovereignty Advantage:** Keeps staging and target areas completely localized within the AWS Malaysia region. Absolute data sovereignty is maintained, satisfying the 2025 CBPDT Guidelines natively while achieving sub-minute RPO.
* **Cost Impact:** Exceptionally cost-effective (~$112.30 USD / RM 505.35 per month), avoiding active duplicate server overhead until disaster declaration.

### Phase 3: Transition to Sovereign In-Region Pilot Light (As Real-Time Hot Read Needs Arise)
* **Action:** If the application scales further and business workflows require an active, continuously queryable read-replica for real-time reads/BI reports in addition to DR, deploy an RDS PostgreSQL Read Replica in a separate VPC/subnet configuration within the **Malaysia region (`ap-southeast-5`)**, keeping the ASG desired capacity at 0.
* **Sovereignty Advantage:** Maintains absolute local residency. Enables fast database promotion and compute failover without violating data sovereignty policies.
* **Cost Impact:** Highly cost-optimized (~$254.22 USD / RM 1,143.99 per month), representing a fraction of the cost of running a full Warm Standby or Cross-Region Active-Active cluster.
