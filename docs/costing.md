---
layout: default
title: "Costing Estimate"
---

# Estimated Costing

We provide two distinct monthly cost estimates for the 3-Tier AWS Architecture in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** utilizing On-Demand rates (~730 hours/month).

1. **Baseline Cost-Optimized Plan:** Ideal for initial development, testing, staging environments, and low-traffic applications.
2. **High-Performance Developer-Aligned Plan:** Spec'd specifically to fulfill the resource requirements of the **Developer's First Design (Nginx, Backend, RAGFlow, LangFuse)** with production-grade performance.

---

## 1. Baseline Cost-Optimized Plan (USD)

This configuration targets baseline usage with smaller resource profiles (`t4g.medium` compute, `db.m6g.large` database) to minimize initial expenditures.

| Tier / AWS Component | Configuration & Resource Sizing | Hourly/Unit Rate | Est. Monthly Cost (USD) |
| --- | --- | --- | --- |
| **Networking & NAT** | 1 NAT Gateway (Outbound API/WhatsApp Traffic)<br><br>• Base provisioned charge<br><br>• Estimated ~50 GB Data Processing | $0.045 / hr<br><br>$0.045 / GB | $32.85<br><br>$2.25 |
| **Presentation Tier** | 1 Application Load Balancer (ALB)<br><br>• Base LCF/hour charge<br><br>• Estimated ~2 LCU average usage | $0.0225 / hr<br><br>$0.008 / LCU-hr | $16.43<br><br>$11.68 |
| **Security Tier** | AWS WAFv2 (Attached to ALB)<br><br>• 1 Regional Web ACL<br><br>• 3 Rules (OWASP Core, SQLi, Rate Limit)<br><br>• ~1 Million HTTP/HTTPS Requests | $5.00 / month<br><br>$1.00 / rule/mo<br><br>$0.60 / M-req | $5.00<br><br>$3.00<br><br>$0.60 |
| **Compute Tier (ASG)** | 2x `t4g.medium` EC2 Instances (ARM Graviton)<br><br>• 2 vCPU, 4GB RAM each<br><br>• 2x 30GB gp3 EBS Root Volumes | $0.0336 / hr / inst<br><br>$0.08 / GB-month | $49.06<br><br>$4.80 |
| **Database Tier (RDS)** | Multi-AZ `db.m6g.large` PostgreSQL<br><br>• 2 vCPU, 8GB RAM (High Availability)<br><br>• 50GB gp3 Storage | $0.304 / hr<br><br>$0.23 / GB-month | $221.92<br><br>$11.50 |
| **Storage Tier (S3)** | Amazon S3 (Encrypted Uploads & Media)<br><br>• ~100 GB Standard Storage<br><br>• ~50,000 PUT/GET API requests | $0.023 / GB-month<br><br>Nominal rates | $2.30<br><br>$0.50 |
| **Data Transfer** | Outbound Internet Data Transfer<br><br>• ~100 GB Outbound (First 100GB Free/mo) | Free Tier | $0.00 |
| **TOTAL ESTIMATED MONTHLY COST** |  |  | **~$361.89 USD** / month |

* **Local Currency Equivalent (MYR):** **~RM 1,620 - RM 1,700 MYR / month** *(calculated at an exchange rate baseline of 1 USD ≈ 4.50 MYR)*.

---

## 2. High-Performance Developer-Aligned Plan (USD)

This configuration scales up computing instances to precisely match the developer's server specifications (**Server 02, Server 03, and Server 04**) with high performance, dedicated throughput, and larger memory margins.

| Tier / AWS Component | Configuration & Resource Sizing | Hourly/Unit Rate | Est. Monthly Cost (USD) |
| --- | --- | --- | --- |
| **Networking & NAT** | 1 NAT Gateway (Outbound API/WhatsApp Traffic)<br><br>• Base provisioned charge<br><br>• Estimated ~50 GB Data Processing | $0.045 / hr<br><br>$0.045 / GB | $32.85<br><br>$2.25 |
| **Presentation Tier** | 1 Application Load Balancer (ALB)<br><br>• Base LCF/hour charge<br><br>• Estimated ~2 LCU average usage | $0.0225 / hr<br><br>$0.008 / LCU-hr | $16.43<br><br>$11.68 |
| **Security Tier** | AWS WAFv2 (Attached to ALB)<br><br>• 1 Regional Web ACL<br><br>• 3 Rules (OWASP Core, SQLi, Rate Limit)<br><br>• ~1 Million HTTP/HTTPS Requests | $5.00 / month<br><br>$1.00 / rule/mo<br><br>$0.60 / M-req | $5.00<br><br>$3.00<br><br>$0.60 |
| **Compute Tier (ASG)** | **2x `t4g.xlarge` EC2 Instances (ARM Graviton)**<br><br>• 4 vCPU, 16GB RAM each (Supports Backend, DMS, RAGFlow, LangFuse)<br><br>• 2x 30GB gp3 EBS Root Volumes | $0.1344 / hr / inst<br><br>$0.08 / GB-month | $196.22<br><br>$4.80 |
| **Database Tier (RDS)** | **Multi-AZ `db.m6g.xlarge` PostgreSQL**<br><br>• 4 vCPU, 16GB RAM (Matches Server 04 Data Tier)<br><br>• 50GB gp3 Multi-AZ Storage | $0.608 / hr<br><br>$0.46 / GB-month | $443.84<br><br>$23.00 |
| **Storage Tier (S3)** | Amazon S3 (Encrypted Uploads & Media)<br><br>• ~100 GB Standard Storage<br><br>• ~50,000 PUT/GET API requests | $0.023 / GB-month<br><br>Nominal rates | $2.30<br><br>$0.50 |
| **Data Transfer** | Outbound Internet Data Transfer<br><br>• ~100 GB Outbound (First 100GB Free/mo) | Free Tier | $0.00 |
| **TOTAL ESTIMATED MONTHLY COST** |  |  | **~$742.47 USD** / month |

* **Local Currency Equivalent (MYR):** **~RM 3,340 MYR / month** *(calculated at an exchange rate baseline of 1 USD ≈ 4.50 MYR)*.

---

## Plan Comparison Summary

```
┌─────────────────────────────────┬─────────────────────────┬─────────────────────────┐
│ Metric                          │ Baseline Plan           │ High-Performance Plan   │
├─────────────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Target Environment              │ Staging, Dev, Testing   │ Production AI Workloads │
├─────────────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Compute Spec (per node)         │ 2 vCPU, 4GB RAM         │ 4 vCPU, 16GB RAM        │
├─────────────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Database Spec (RDS)             │ 2 vCPU, 8GB RAM         │ 4 vCPU, 16GB RAM        │
├─────────────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Monthly Estimate (USD)          │ ~$361.89 USD            │ ~$742.47 USD            │
├─────────────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Monthly Estimate (MYR)          │ ~RM 1,630 MYR           │ ~RM 3,340 MYR           │
└─────────────────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## Optional Cost Optimization Pathways (Day 2 Operations)

* **RDS Savings Plans / Reserved Instances (1-Yr / 3-Yr):** Committing to the primary PostgreSQL instance can reduce DB compute costs by **30%–35%**, cutting monthly spend by **~$70 - $150 USD** depending on the plan.
* **EC2 Compute Savings Plans:** Committing to baseline `t4g` usage via Savings Plans reduces application compute charges by up to **20%–25%**.
* **VPC S3 Gateway Endpoint:** S3 traffic routed through a free VPC Gateway Endpoint eliminates NAT Gateway data processing fees ($0.045/GB) for media uploads.
