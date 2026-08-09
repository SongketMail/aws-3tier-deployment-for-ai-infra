---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "36-Month TCO & Financial Blueprint"
timestamp: 2026-08-09T14:00:00Z
topics: ["executive", "financial", "tco", "costing", "opex", "licensing"]
---
<div class="arch-badge arch-badge-strategic">
  <strong>[STRATEGIC FINANCIAL]</strong> — C-Suite & Project Managers
</div>

# 🏛️ 36-Month TCO & Financial Blueprint

This document delivers a high-fidelity **Executive Financial Blueprint** detailing the long-term operational expenditures (OpEx), total cost of ownership (TCO), and licensing risk parameters for our secure 3-tier AWS architecture. It provides clear C-suite visibility into the **$92,509.78 USD** (≈ **RM 416,294.01 MYR**) grand project budget.

---

## 📈 1. Combined 36-Month Financial Projection

Our financial projection spans **2 years of active development (24 months)** and **12 months of post-launch support and maintenance (36 months total)**. It maps all infrastructure expenditures directly against non-AWS operational overheads:

| Financial Period | AWS Cloud Cost (USD) | AWS Cloud Cost (MYR) | Non-AWS Operating Cost (USD) | Non-AWS Operating Cost (MYR) | Combined Total Cost (USD) | Combined Total Cost (MYR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Year 1 (Months 1–12)** | $13,023.16 | RM 58,604.22 | $16,600.00 | RM 74,700.00 | $29,623.16 | RM 133,304.22 |
| **Year 2 (Months 13–24)** | $23,343.02 | RM 105,043.59 | $14,100.00 | RM 63,450.00 | $37,443.02 | RM 168,493.59 |
| **Year 3 (Months 25–36)** | $11,343.60 | RM 51,046.20 | $14,100.00 | RM 63,450.00 | $25,443.60 | RM 114,496.20 |
| **Grand Total** | **$47,709.78** | **RM 214,694.01** | **$44,800.00** | **RM 201,600.00** | **$92,509.78** | **RM 416,294.01** |

*Note: All currency conversions utilize our standardized baseline exchange rate of exactly $1.00 USD = MYR 4.50.*

---

## 📊 2. Quarterly OpEx Cost Curves

To assist in corporate cash-flow modeling and quarterly budgeting, the table below provides a granular **Quarterly OpEx Curve** across the 12 quarters of the 36-month timeline:

| Fiscal Period | AWS Cloud Cost (USD) | Non-AWS Operating Cost (USD) | Combined Quarterly Total (USD) | Combined Quarterly Total (MYR) | Primary Milestones & Workloads |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Q1 (Months 1–3)** | $842.61 | $4,150.00 | $4,992.61 | RM 22,466.75 | Project Kick-off, single-AZ developer sandbox, base schema migration. |
| **Q2 (Months 4–6)** | $2,039.33 | $4,150.00 | $6,189.33 | RM 27,851.99 | Scaling to dual-AZ staging environment with dynamic auto-scaling rules. |
| **Q3 (Months 7–9)** | $5,051.22 | $4,150.00 | $9,201.22 | RM 41,405.49 | Chatbot core engine go-live, secure WAF rules association, WhatsApp integrations. |
| **Q4 (Months 10–12)** | $5,090.00 | $4,150.00 | $9,240.00 | RM 41,580.00 | Continuous telemetry tracking with Langfuse, CRM schema inception. |
| **Q5 (Months 13–15)** | $5,590.00 | $3,525.00 | $9,115.00 | RM 41,017.50 | CRM Go-Live, Route 53 health-checks failover setup, EFS replica stream active. |
| **Q6 (Months 16–18)** | $6,450.00 | $3,525.00 | $9,975.00 | RM 44,887.50 | Super Mobile App development, S3 content delivery edge with CloudFront. |
| **Q7 (Months 19–21)** | $6,515.71 | $3,525.00 | $10,040.71 | RM 45,183.20 | GPU-backed g5.xlarge OCR compute nodes integration, Standalone Wazuh SIEM setup. |
| **Q8 (Months 22–24)** | $4,787.31 | $3,525.00 | $8,312.31 | RM 37,405.40 | Security audits, final acceptance testing (FAT), scaling-down staging compute. |
| **Q9 (Months 25–27)** | $2,835.90 | $3,525.00 | $6,360.90 | RM 28,624.05 | Day-2 cost-optimization: Purchasing 1-Year Compute Savings Plans & DB Reserved Instances. |
| **Q10 (Months 28–30)**| $2,835.90 | $3,525.00 | $6,360.90 | RM 28,624.05 | Database indexing optimization, RDS snapshot management. |
| **Q11 (Months 31–33)**| $2,835.90 | $3,525.00 | $6,360.90 | RM 28,624.05 | Support run-rate under optimized savings plan discount parameters. |
| **Q12 (Months 34–36)**| $2,835.90 | $3,525.00 | $6,360.90 | RM 28,624.05 | Final system audits, handover of ownership documentation, 99.99% SLA verification. |
| **GRAND TOTAL** | **$47,709.78** | **$44,800.00** | **$92,509.78** | **RM 416,294.01** | **Total cost of ownership over the entire 3-year lifecycle.** |

---

## 💸 3. Non-AWS Operational Overheads Breakdown

Other non-AWS operational costs are carefully estimated to provide a holistic overview of the project's true operating costs:

1. **Software Subscriptions ($200.00 USD/mo):** $2,400.00 USD per year (≈ RM 10,800.00 MYR/year) for development collaboration licenses, Slack workspaces, Jira, and PM tools.
2. **Software Licensing Compliance:** $1,200.00 USD per year (≈ RM 5,400.00 MYR/year) for static application security testing (SAST), automated SBOM scanning, and legal licensing audits.
3. **Security Posture Assessment (SPA):** $4,500.00 USD per year (≈ RM 20,250.00 MYR/year) for formal penetration testing (pentests) and regulatory threat reporting.
4. **Load Testing (First Year Only):** $2,500.00 USD (≈ RM 11,250.00 MYR) in Year 1 to execute stress/concurrency testing from 100 to 10,000 virtual users (VUs).
5. **3rd Party On-Call AWS Support ($500.00 USD/mo):** $6,000.00 USD per year (≈ RM 27,000.00 MYR/year) for 24/7 incident response SLA coverage by external certified AWS engineering firms.

---

## 🏛️ 4. Software Licensing & Technology Risk Matrix

To comply with enterprise auditing frameworks, our core technology choices have been categorized under the **TS (Technology Stack)** series registry to track risk and mitigate compliance issues:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TS SERIES RISK REGISTER                         │
├─────────┬──────────────────────────────┬──────────────┬────────────────┤
│ ID      │ Component                    │ Risk Level   │ Action Taken   │
├─────────┼──────────────────────────────┼──────────────┼────────────────┤
│ TS-02   │ LangChain4j Framework        │ Medium-Low   │ Accepted Risk  │
│ TS-04   │ Wazuh SIEM Self-Hosting      │ Low          │ Budget Savings │
│ TS-05   │ Software Licensing Framework │ Low          │ Audit Standard │
│ TS-06   │ Self-hosted DB & AI Ops      │ Medium       │ Internal Option│
└─────────┴──────────────────────────────┴──────────────┴────────────────┘
```

### 📋 TS-02: LangChain4j SLA & Corporate Support Risk
* **The Risk:** LangChain4j is open-source (Apache 2.0) and lacks an official corporate SLA or vendor-backed technical support structure. Critical bugs or vulnerability patches must be resolved via the community.
* **Why Accepted:** LangChain4j is the enterprise Java standard for LLM orchestration. Swapping to complex proprietary engines represents a greater integration risk.
* **Mitigation:** Pin dependency versions, maintain an internal git fork of the specific version, and write clean wrapper interfaces to swap orchestration engines if needed.

### 📋 TS-04: Standalone Wazuh SIEM Self-Hosting (Cost Optimization)
* **Strategy:** By self-hosting a standalone Wazuh SIEM cluster on a hardened ARM64 instance in AWS (`t4g.large`), we eliminate premium third-party SaaS licenses.
* **Financial Impact:** Reduces security logging overhead by **57%**, operating at only **$65.71 USD / month** on Graviton, saving over **$1,000.00 USD / year** in vendor markup.

### 📋 TS-05: Technology Stack Licensing Audit
* **Action:** Establish a strict compliance standard restricting production dependencies to highly permissive licenses (**MIT, Apache 2.0, BSD-3**). Ensure zero copyleft leakages (such as GPL/AGPL) infiltrate the backend application layer.

### 📋 TS-06: Self-hosted Database & AI Operations (Internal Option)
* **Strategy:** Retain containerized PostgreSQL and Valkey engines as a zero-cost option for developer sandbox and early local testing, while choosing Multi-AZ Amazon RDS PostgreSQL and Amazon ElastiCache Valkey for production runtimes.

---

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
