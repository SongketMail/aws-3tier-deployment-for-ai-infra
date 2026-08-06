---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "AWS Infrastructure Costing Skill"
timestamp: 2026-08-05T22:00:00Z
topics: ["aws", "cloud", "architecture", "skill", "costing", "budget", "pricing"]
description: "Guidelines and instructions for managing and evaluating AWS infrastructure costing models, baseline optimizations, and enterprise high-performance estimations."
name: "aws-infrastructure-costing"
---
# AWS Infrastructure Costing Skill

This skill governs the financial planning, budget constraints, and cost breakdowns of the AWS 3-tier architecture.

---

## 1. Baseline Cost-Optimised Plan (~$426.75 USD/mo)

The baseline plan is optimized for development, staging, and small-scale deployments in the `ap-southeast-5` (Malaysia) region:
- **Networking & VPC:** Uses a single NAT Gateway (~$32.85 USD/mo) and public/private subnets.
- **Compute (Web/App ASG & Standalone):** Employs Graviton-based `t4g.micro` instances.
- **Database (RDS):** Deploys a single RDS `db.t4g.micro` instance (~$12.50 USD/mo).
- **Caching (ElastiCache):** Leverages `cache.t4g.micro` Valkey (~$9.34 USD/mo).
- **Management & DNS:** Includes secure SSH Jumphost Bastion (~$10.98 USD/mo) and Route 53 hosting & query costs (~$1.30 USD/mo).

---

## 2. High-Performance Enterprise Plan (~$1,064.46 USD/mo)

Designed for mission-critical, highly available production workloads:
- **High Availability Networking:** Dual NAT Gateways spanning multiple Availability Zones (~$65.70 USD/mo) to eliminate single points of failure.
- **Clustered Compute:** Employs larger Graviton instance classes (`t4g.medium` or `c7g.large`) and robust auto-scaling triggers.
- **Database (RDS Multi-AZ):** Deploys Multi-AZ `db.t4g.medium` PostgreSQL instances with high-IOPS gp3 storage (~$140 USD/mo).
- **Caching Layer:** Clustered Valkey nodes with high availability.

---

## 3. Financial Prudence & Best Practices

- Periodically audit idle standalone instances and pause them when not in use.
- Prefer Valkey cache clusters over Redis OSS to capture immediate 20% on-demand savings.
- Ensure all cost estimation adjustments are logged in `docs/costing.md` for team visibility.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
