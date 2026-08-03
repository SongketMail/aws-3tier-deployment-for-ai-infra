---
layout: default
title: "Costing Estimate"
---

# Estimated Costing

The monthly cost estimate for the 3-Tier AWS Architecture in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** uses On-Demand rates (~730 hours/month).

---

### Estimated Cost Breakdown (USD)

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

---

### Local Currency Equivalent (MYR)

* **Estimated Total:** **~RM 1,620 - RM 1,700 MYR / month** *(calculated at an exchange rate baseline of 1 USD ≈ 4.50 MYR)*.

---

### Optional Cost Optimization Pathways (Day 2 Operations)

* **RDS Savings Plans / Reserved Instances (1-Yr / 3-Yr):** Committing to the primary PostgreSQL instance can reduce DB compute costs by **30%–35%**, cutting monthly spend by **~$70 USD**.
* **EC2 Compute Savings Plans:** Committing to baseline `t4g` usage via Savings Plans reduces application compute charges by up to **20%–25%**.
* **VPC S3 Gateway Endpoint:** S3 traffic routed through a free VPC Gateway Endpoint eliminates NAT Gateway data processing fees ($0.045/GB) for media uploads.
