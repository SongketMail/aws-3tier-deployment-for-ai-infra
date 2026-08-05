---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "OpenTofu 3-Tier Infrastructure Design Skill"
timestamp: 2026-08-05T21:55:00Z
topics: ["aws", "cloud", "architecture", "skill", "opentofu", "vpc", "security-groups", "waf", "alb"]
description: "Guidelines for managing, validation, and designing the secure AWS 3-Tier OpenTofu architecture, modules, and security parameters."
name: "opentofu-infrastructure-design"
---
# OpenTofu 3-Tier Infrastructure Design Skill

This skill outlines the engineering standards and validation practices for the highly modular OpenTofu-based AWS 3-Tier Architecture.

---

## 1. 3-Tier Physical & Logical Separation

Always ensure clear boundaries between logical tiers:
- **Presentation / Load Balancing:** Public subnets, protected by AWS WAFv2 (with rate limits and OWASP rules). Only HTTP/HTTPS traffic is allowed.
- **Compute / Application:** Private subnets. Instances running frontend Nginx, backends, and AI models. Whitelisted SSM connectivity. No direct public SSH or public IP allocations.
- **Database / Storage:** Isolated subnets. Restricted access only from specific compute security groups. Direct internet egress/ingress is completely blocked.

---

## 2. Directory & Module Topology

All IaC files must live under the `terraform/` folder and be strictly modularised:
- `terraform/modules/vpc/` - Core networking and NAT gateways.
- `terraform/modules/security_groups/` - Firewall rules.
- `terraform/modules/waf/` - Layer-7 WAFv2 rules.
- `terraform/modules/alb/` - ALB and target routing.
- `terraform/modules/asg/` - Launch templates & scaling rules.
- `terraform/modules/rds/` - Multi-AZ Database.
- `terraform/modules/elasticache/` - Valkey caching.
- `terraform/modules/standalone_ec2/` - Pre-bake dev/staging nodes.
- `terraform/modules/jumphost/` - whitelisted Cyberjaya SSH Bastion.

---

## 3. Best Practices & Validation

- Always enforce two-space indentation across all `.tf` files.
- Declare variables with explicit types (such as `bool` instead of `boolean`).
- Run validation checks using `./scripts/deploy.sh` to ensure proper syntax and clean plan generation before applying updates.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
