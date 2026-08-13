---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "AWS ASG & Standalone Compute Skill"
timestamp: 2026-08-05T21:56:00Z
topics: ["aws", "cloud", "architecture", "skill", "asg", "ec2", "ssm", "ami", "asimp", "imdsv2", "elb"]
description: "Guidelines for deploying multi-tier ASGs, pairing them with standalone EC2 instances for pre-baking AMIs, and managing them securely via SSM."
name: "aws-asg-standalone-compute"
---
# AWS ASG & Standalone Compute Skill

This skill governs the management of Auto Scaling Groups (ASGs) and standalone EC2 compute environments, focusing on the separation of concerns and staging/pre-baking compliance.

---

## 1. Multi-Tier ASG Separation of Concerns & Auto-Healing

The architecture deploys separate Auto Scaling Groups for distinct application roles:
1. **Frontend Nginx Tier:** Serves static content, manages HTTPS redirection, and acts as a reverse proxy.
2. **Backend Application Tier:** Processes API logic, authenticates requests, and queries the database layer.
3. **AI Tier:** Executes RAGFlow/Langfuse workloads, visual layout analysis, and layout parsing.

- **State Management:** Ensure ASGs are kept completely stateless by offloading dynamic files to Amazon S3 or shared Amazon EFS storage (as detailed in `docs/asg-separation-of-concern.md`, as per **Item 18**).
- **ALB-Aware Auto-Healing:** In the OpenTofu infrastructure definition (`terraform/modules/asg/main.tf`), the Auto Scaling Group (ASG) is configured with `health_check_type = "ELB"` which integrates it directly with the Application Load Balancer (ALB) active health check status for reliable, application-aware auto-healing (as per **Item 20**).
- **Natively Enforced IMDSv2 Requirements:** The project enforces IMDSv2 requirements natively by adding the `metadata_options` block with `http_tokens = "required"` and `http_put_response_hop_limit = 1` across all EC2 computing resources (as per **Item 33**).

---

## 2. Standalone Pairing & AMI Staging

- **AMI Staging Environment:** Pair each of the three ASG application groups with a dedicated Standalone EC2 instance connected to the same databases/shared storage (RDS, S3, or EFS) to serve as a staging and testing environment for pre-baking AMIs (as per **Item 15**).
- These standalone instances act as the development and staging environments where developers can verify configurations, test patches, and pre-bake Amazon Machine Images (AMIs) before rollout.
- **Staging / Pre-Baking OS Selection:** The standalone compute module (at `terraform/modules/standalone_ec2/`) deploys secure standalone Ubuntu 26.04 LTS development and application instances inside secure private subnets, integrated with AWS Systems Manager (SSM) for passwordless management (as per **Item 16**).
- **Legacy-to-Cloud Hardened Alignment:** All target operating systems are upgraded to Ubuntu 26.04 LTS hardened via the ASIMP (Ansible System Integrity Management Platform) framework, mapping legacy single-VM configs to AWS-native managed services and secure private subnets (as per **Item 17**).

---

## 3. Passwordless SSM Management

- Direct SSH to ASG instances inside private subnets is disabled.
- Enforce passwordless instance management via AWS Systems Manager (SSM) Session Manager, using IAM policies to control access securely.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
