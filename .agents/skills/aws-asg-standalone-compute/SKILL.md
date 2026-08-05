---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "AWS ASG & Standalone Compute Skill"
timestamp: 2026-08-05T21:56:00Z
topics: ["aws", "cloud", "architecture", "skill", "asg", "ec2", "ssm", "ami"]
description: "Guidelines for deploying multi-tier ASGs, pairing them with standalone EC2 instances for pre-baking AMIs, and managing them securely via SSM."
name: "aws-asg-standalone-compute"
---
# AWS ASG & Standalone Compute Skill

This skill governs the management of Auto Scaling Groups (ASGs) and standalone EC2 compute environments, focusing on the separation of concerns and staging/pre-baking compliance.

---

## 1. Multi-Tier ASG Separation of Concerns

The architecture deploys separate Auto Scaling Groups for distinct application roles:
1. **Frontend Nginx Tier:** Serves static content, manages HTTPS redirection, and acts as a reverse proxy.
2. **Backend Application Tier:** Processes API logic, authenticates requests, and queries the database layer.
3. **AI Tier:** Executes RAGFlow/Langfuse workloads, visual layout analysis, and layout parsing.

Ensure ASGs are kept completely stateless by offloading dynamic files to Amazon S3 or shared Amazon EFS storage.

---

## 2. Standalone Pairing & AMI Staging

- **AMI Staging Environment:** Pair each of the three ASG application groups with a dedicated Standalone EC2 instance connected to the same databases/shared storage.
- These standalone instances act as the development and staging environments where developers can verify configurations, test patches, and pre-bake Amazon Machine Images (AMIs) before rollout.

---

## 3. Passwordless SSM Management

- Direct SSH to ASG instances inside private subnets is disabled.
- Enforce passwordless instance management via AWS Systems Manager (SSM) Session Manager, using IAM policies to control access securely.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
