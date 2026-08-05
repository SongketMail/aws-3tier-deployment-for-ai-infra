---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "AWS Malaysia Region & Graviton Defaults Skill"
timestamp: 2026-08-05T21:54:00Z
topics: ["aws", "cloud", "architecture", "skill", "malaysia", "graviton", "arm64", "opentofu", "ami"]
description: "Guidelines and instructions for configuring regional defaults, AWS Graviton architecture, and dynamic AMI selection for ap-southeast-5 (Malaysia)."
name: "aws-malaysia-defaults"
---
# AWS Malaysia Region & Graviton Defaults Skill

This skill governs deployment configurations for the AWS Asia Pacific (Malaysia) region (`ap-southeast-5`), focusing on ARM64 Graviton instances, dynamic AMI selection, and native OpenTofu alignment.

---

## 1. Core Guidelines & Regional Constants

- **Target Region:** Always deploy in `ap-southeast-5` (Malaysia).
- **Default Compute:** Use AWS Graviton (ARM64) instance types by default to optimise costs and performance:
  - **EC2 Instances (Web/Compute):** Use `t4g.micro` (or larger Graviton types like `t4g.medium` depending on CPU requirements).
  - **RDS PostgreSQL Instances:** Use `db.t4g.micro` (running PostgreSQL 16/17).
  - **ElastiCache Valkey:** Use `cache.t4g.micro` (or `cache.t4g.medium`).

---

## 2. Dynamic AMI Selection Logic

When configuring Auto Scaling Groups (ASGs) or standalone instances:
1. Detect the instance family configured in the variables.
2. If the family starts with `t4g` or any other Graviton type, automatically select the standard Amazon Linux 2023 or Ubuntu 26.04 LTS ARM64 AMI.
3. If x86_64 is selected, fallback to the respective x86_64 AMI.
4. Ensure compliance with pre-baked images.

---

## 3. Native OpenTofu Requirements

- **Version Specification:** The project requires `OpenTofu >= 1.6.0` (while preserving backward compatibility with `Terraform >= 1.5.0`).
- Ensure no hardcoded old Terraform providers are used, and utilize OpenTofu commands (`tofu fmt`, `tofu validate`, `tofu plan`, `tofu apply`) natively.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
