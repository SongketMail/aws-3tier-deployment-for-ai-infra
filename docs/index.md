---
layout: default
title: "AWS Secure 3-Tier Architecture Documentation"
---

# AWS Secure 3-Tier Architecture Documentation

Welcome to the official technical documentation for our **AWS 3-Tier Deployment for AI & Web Infra** project. This project is optimized for deployment in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** utilizing AWS Graviton (ARM64) instances, Multi-AZ RDS Postgres, and AWS WAFv2 regional protection.

This deployment is structured natively in Terraform, adhering to strict modular boundaries, security best practices, and the **Zero-Trust Network Principle**.

---

## Technical Overview

The architecture divides infrastructure components into discrete logical and physical tiers to achieve top-tier scalability, performance, and threat mitigation:

- **Presentation / Web Layer:** Application Load Balancer (ALB) receiving external traffic and filtered through AWS WAFv2 (OWASP rules + rate limiting).
- **Application / Compute Layer:** Auto Scaling Group (ASG) of EC2 instances running inside private subnets, auto-scaled on CPU usage, and managed via AWS Systems Manager (SSM).
- **Database Layer:** Multi-AZ RDS PostgreSQL database deployed within isolated subnets, allowing connections exclusively from the application tier.

---

## Documentation Index

Explore different sections of our infrastructure documentation:

### Core Configuration
1. **[System Architecture](architecture.html):** Deep dive into the physical network structure, routing tables, and AWS resource layout in the Malaysia region, including how the Developer's first design is mapped.
2. **[Developer Design Alignment Guide](developer-design-mapping.html):** Rationale and comparison of shifting from legacy single-node Ubuntu VMs to an enterprise secure AWS design.
3. **[ASGs & Separation of Concerns Guide](asg-separation-of-concern.html):** Best practice guide detailing auto-scaling with distinct ASGs, stateless principles, and the role of Amazon S3, EFS, or both.
4. **[Root OpenTofu/Terraform Files](root-files.html):** Overview of the root configuration entries (`main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`).
5. **[OpenTofu Migration Guide](opentofu-migration.html):** Detailed compatibility research and transition path for deploying using OpenTofu on AWS.
6. **[AMI Design & Hardening Guide](ami-design.html):** Architectural guide outlining the pre-baked AMI strategy, Packer/Ansible pipeline, and ASIMP compliance integration.

### Infrastructure Submodules
- **[VPC Module](modules/vpc.html):** Core networking, public/private subnets, internet gateways, and NAT configurations.
- **[Security Groups Module](modules/security_groups.html):** Strict firewall rulesets and port-level isolation.
- **[WAF Module](modules/waf.html):** Layer-7 Web Application Firewall protecting the ALB.
- **[ALB Module](modules/alb.html):** Application Load Balancer and health-check configurations.
- **[ASG Module](modules/asg.html):** Auto Scaling Group, Launch Templates, and dynamic Graviton auto-detection.
- **[RDS Module](modules/rds.html):** Multi-AZ PostgreSQL configuration and parameter group tuning.
- **[Standalone EC2 Module](modules/standalone_ec2.html):** Secure standalone Ubuntu 26.04 LTS development and application environments.

### Deployment & CI/CD
- **[Automation Scripts](scripts.html):** Details about CLI helpers (`deploy.sh`, `destroy.sh`, `user_data.sh`).
- **[CI/CD Pipeline](cicd.html):** GitHub Actions workflow for automatic formatting, testing, validation, and OIDC deployment.
- **[Costing Estimate](costing.html):** Comprehensive monthly cost breakdown, local currency estimates, and Day-2 cost optimization pathways.

---

## Prerequisites

Before deploying the infrastructure, ensure you have the following tools installed and configured:

- **[Terraform](https://www.terraform.io/downloads.html) >= 1.5.0**
- **[AWS CLI](https://aws.amazon.com/cli/)** configured with admin-level credentials for `ap-southeast-5`
- **Git** for repository and revision tracking
