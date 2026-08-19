---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "AWS Secure 3-Tier Architecture Documentation"
timestamp: 2026-08-05T21:48:38Z
topics: ["aws", "cloud", "architecture", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "bastion", "route53", "dns", "ssl", "acm", "disaster-recovery", "gitlab", "efs", "postgresql", "gpu", "ragflow", "langfuse", "antigravity", "skills", "sovereignty", "compliance", "costing"]
---
# AWS Secure 3-Tier Architecture Documentation

Welcome to the official technical documentation for our **AWS 3-Tier Deployment for AI & Web Infra** project. This project is optimized for deployment in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** utilizing AWS Graviton (ARM64) instances, Multi-AZ RDS Postgres, and AWS WAFv2 regional protection.

This deployment is structured natively in OpenTofu, adhering to strict modular boundaries, security best practices, and the **Zero-Trust Network Principle**.

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
2. **[AWS Phased Adoption Roadmap & Costing Guide](aws-adoption-roadmap.html):** Multi-year week-by-week and month-by-month AWS service growth plan mapped from the project Gantt chart.
3. **[Developer Design Alignment Guide](developer-design-mapping.html):** Rationale and comparison of shifting from legacy single-node Ubuntu VMs to an enterprise secure AWS design.
4. **[ASGs & Separation of Concerns Guide](asg-separation-of-concern.html):** Best practice guide detailing auto-scaling with distinct ASGs, stateless principles, and the role of Amazon S3, EFS, or both.
5. **[Root OpenTofu/Terraform Files](root-files.html):** Overview of the root configuration entries (`main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`).
6. **[OpenTofu Migration Guide](opentofu-migration.html):** Detailed compatibility research and transition path for deploying using OpenTofu on AWS.
7. **[AMI Design & Hardening Guide](ami-design.html):** Architectural guide outlining the pre-baked AMI strategy, Packer/Ansible pipeline, and ASIMP compliance integration.
8. **[Route 53 & DNS Troubleshooting](route53.html):** Deep dive into custom domain integration, ACM SSL/TLS setup, and extensive research on resolving ASG private subnet DNS resolution failures.
9. **[Secure Developer Access Guide](jumphost.html):** Comprehensive guide on using our secure SSH Jumphost (Bastion) to access private and standalone nodes from Cyberjaya, with Windows/macOS/Linux client setups and private key security guidelines.
10. **[Hybrid Cloud Integration Guide](hybrid-onprem.html):** Comprehensive evaluation of secure, cost-optimized API and MCP connections alongside official AWS hybrid network solutions (VPN, Direct Connect, Transit Gateway) with granular MYR/USD costing models for ap-southeast-5.
11. **[Disaster Recovery Options & National Sovereignty Guide](dr-options.html):** Production-ready playbook covering the 4 standard AWS cloud DR options aligned with our Multi-AZ architecture, detailed local sovereignty/PDPA/CBPDT compliance reviews, and granular USD/MYR costing comparisons.
12. **[RDS PostgreSQL 17 vs. Percona Server for PostgreSQL 17 Guide](postgresql-comparison.html):** Comprehensive technical comparison of performance, telemetry, observability (PMM vs CloudWatch/Performance Insights), architectural designs, and costs in USD/MYR for ap-southeast-5.
13. **[Redis vs. Valkey Comparison](redis-vs-valkey.html):** Comprehensive strategic, licensing, and costing comparison (Baseline vs. High-Performance) of Redis OSS vs. Valkey on AWS and on-premises.
14. **[RAGFlow + Langfuse GPU Guide](ragflow-langfuse.html):** Architectural and economic analysis of RAGFlow and Langfuse, detailing critical GPU utilization, AWS vs. On-Premises deployment models, and secure API/MCP hybrid connections.
15. **[Google Antigravity Skills Guide](antigravity-skills.html):** Comprehensive integration guide outlining how to share and deploy agent knowledge bases and skills between Google Jules and Google Antigravity.
16. **[SOP: Knowledge-First Discovery](SOP-KNOWLEDGE-FIRST-DISCOVERY.html):** Standard Operating Procedure outlining how AI agents perform local documentation search before probing remote targets.
17. **[Wazuh Standalone Cloud Installation & Costing Guide](wazuh.html):** Detailed installation steps for standalone Wazuh in the cloud (AWS Marketplace AMI and Graviton assistant modes), with independent USD/MYR costing tables for isolated financial tracking.
18. **[Wazuh SIEM & XDR Deep-Dive Guide](wazuh-detailed.html):** In-depth functional breakdown of Wazuh SIEM & XDR capabilities, deployment modes (cloud/on-prem), and critical operational guidance regarding Antivirus coexistence, passive mode configuration, and Windows Defender integration.
19. **[Technology Stack Comparison Guide](tech-stack-comparison.html):** Complete architectural mapping and AWS alternatives comparison for the developer's containerized and external integrations (LangChain4j, Spring Boot, React, Twilio, Meta, Postgres, Valkey).
20. **[Software Licensing & Technology Risk Register (TS/MC Series)](licensing-risks.html):** Complete software licensing compliance framework, technology risk registry, and mitigation plans (TS/MC Series) covering LangChain4j, self-hosted operations, Bedrock with Qwen3 models, and standalone Wazuh SIEM.
21. **[Strategic Comparative Review](aws-vs-self-hosted-review.html):** Comprehensive strategic analysis and financial TCO comparison of an AWS-Native Managed Platform against a Self-Hosted / On-Premises Custom Stack in Malaysia.
22. **[Load Testing Assumptions & Sizing Guide](load-test-assumptions.html):** Workload definitions, SLA metrics, architectural performance assumptions, and multi-VU sizing models from 100 to 10,000 VUs.
23. **[Context7 AI Chat Integration Guide](context7.html):** Guide detailing our AI chat widget, how to use it, the provider (Upstash), and integration details.
24. **[Security Posture Assessment (SPA) Requirement Checklist](audits/security-posture-assessment.html):** Comprehensive security control audit checklist, fully customized for our Java, Spring Boot, PostgreSQL, Valkey, and RAGFlow/Langfuse AI infrastructure.
25. **[Legal Notice & Disclaimer](legal-notice.html):** Official legal disclaimer and privacy policy confirming that all designs, costs, and scenarios are based entirely on assumptions for training and informational purposes.
26. **[Output of ASIMP](audits/asimp-output.html):** Example execution output, report format, and baseline metrics generated by ASIMP.
27. **[Output of Lynis](audits/lynis-output.html):** High-fidelity example of the Lynis host auditing utility scanning logs, attributes, and suggestions.
28. **[Output of OpenSCAP](audits/openscap-output.html):** Detailed example of OpenSCAP CIS Level 2 scan evaluation rules, results, and generated remediations.
29. **[AWS Services vs. On-Premises Open-Source Stack Comparison](aws-vs-onprem-stack-comparison.html):** Detailed layer-by-layer architectural comparison across 12 layers mapping AWS services to self-hosted open-source counterparts.
30. **[Google Jules AI Platform Guide](jules-platform-guide.html):** Comprehensive technical showcase documenting our end-to-end development workflow, PR review collaboration, DSOM governance, and Google Antigravity integration.

### Onsite On-Premises Volume
- **[Onsite On-Premises Blueprint Portal](onprem/index.html):** Overview portal and strategic rationale for moving from AWS to rootless, open-source local on-premises deployments.
- **[VM & Network Architecture](onprem/architecture.html):** Physical host configurations, sizing models, multi-tier VLAN isolation, and stateful routing rulesets.
- **[Rootless Podman 5+ & systemd Quadlets](onprem/podman-quadlet.html):** Configuration guidelines for running production containers without administrative root rights using keep-id remapping.
- **[On-Premises Infrastructure with Ansible](onprem/ansible-orchestration.html):** Symmetric privilege separation, FQCN-compliant plays, and local CI/CD pipelines integrating Gitea, Semaphore, and ARA.
- **[Open-Source Containerized Stack Specifications](onprem/open-source-stack.html):** Standard blueprints replacing core AWS managed components with containerized equivalents (BunkerWeb, Valkey, Postgres 17, Keycloak, Ollama, RAGFlow, and Langfuse).
- **[Enterprise Percona Server Setup](onprem/percona-postgresql.html):** Standard blueprints for running production-grade Percona Server for PostgreSQL 17 on-premises using Patroni cluster management, etcd distributed consensus stores, pg_backrest, and HAProxy load balancing.

### Infrastructure Submodules
- **[VPC Module](modules/vpc.html):** Core networking, public/private subnets, internet gateways, and NAT configurations.
- **[Security Groups Module](modules/security_groups.html):** Strict firewall rulesets and port-level isolation.
- **[WAF Module](modules/waf.html):** Layer-7 Web Application Firewall protecting the ALB.
- **[ALB Module](modules/alb.html):** Application Load Balancer and health-check configurations.
- **[ASG Module](modules/asg.html):** Auto Scaling Group, Launch Templates, and dynamic Graviton auto-detection.
- **[RDS Module](modules/rds.html):** Multi-AZ PostgreSQL configuration and parameter group tuning.
- **[Standalone EC2 Module](modules/standalone_ec2.html):** Secure standalone Ubuntu 26.04 LTS development and application environments.
- **[ElastiCache Valkey Module](modules/elasticache.html):** Secure ElastiCache Valkey in-memory caching cluster for session and metadata store.
- **[Jumphost Module](modules/jumphost.html):** Secure public-subnet SSH Jumphost (Bastion) whitelisted for Cyberjaya office with automated downstream ingress configuration.

### Deployment & CI/CD
- **[Automation Scripts](scripts.html):** Details about CLI helpers (`deploy.sh`, `destroy.sh`, `user_data.sh`).
- **[CI/CD Pipeline](cicd.html):** GitHub Actions workflow for automatic formatting, testing, validation, and OIDC deployment.
- **[GitLab EFS CI/CD](gitlab-efs-cicd.html):** Comprehensive guide on GitLab CI/CD, automatic workflows, EFS mounting, dynamic Nginx path configurations, and containerized/S3 alternatives.
- **[Costing Estimate](costing.html):** Comprehensive monthly cost breakdown, local currency estimates, and Day-2 cost optimization pathways.

---

## Prerequisites

Before deploying the infrastructure, ensure you have the following tools installed and configured:

- **[OpenTofu](https://opentofu.org/) >= 1.6.0** (Recommended) or **Terraform >= 1.5.0**
- **[AWS CLI](https://aws.amazon.com/cli/)** configured with admin-level credentials for `ap-southeast-5`
- **Git** for repository and revision tracking
