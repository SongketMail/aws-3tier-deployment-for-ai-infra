---
layout: "default"
okf_version: "0.1"
type: "Portal"
title: "AWS 3-Tier Deployment for AI & Web Infra (with OpenTofu)"
timestamp: 2026-08-05T21:48:38Z
topics: ["aws", "cloud", "architecture", "readme", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "bastion", "route53", "dns", "ssl", "disaster-recovery", "gitlab", "efs", "postgresql", "antigravity", "skills", "sovereignty", "compliance", "costing"]
---
# AWS 3-Tier Deployment for AI & Web Infra (with OpenTofu)

Welcome to the **AWS 3-Tier Deployment for AI & Web Infra** repository. This is an enterprise-grade, highly available, secure, and cost-optimized infrastructure project. It is natively deployed using **OpenTofu** and targeted at the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** with full support for Graviton (ARM64) compute, automated pre-baked AMIs, strict security architectures, Valkey-based session stores, and custom regional compliance solutions.

This file serves as a **comprehensive developer portal**, providing absolute alignment with our **GitHub Pages documentation site** and a complete index to our extensive technical guides, submodules, scripts, and deployment mechanisms.

---

## Technical Architecture Overview

Our design is built on the **Zero-Trust Network Principle**, dividing components into distinct physical and logical layers:

```
                                [ INTERNET ]
                                     │
                                     ▼
                               [ AWS WAFv2 ]   <-- (OWASP Top 10 + IP Rate Limiting)
                                     │
                                     ▼
                       [ Application Load Balancer ]  <-- (Public Subnets)
                                     │
                       ┌─────────────┴─────────────┐
                       ▼                           ▼
                [ Frontend Nginx ]          [ Frontend Nginx ]  <-- (ASG EC2 Private Subnets)
                       │                           │
                       └─────────────┬─────────────┘
                                     ▼
                            [ ElasticCache Valkey ]     <-- (Session Caching Layer)
                                     │
                                     ▼
                            [ Multi-AZ RDS PG ]         <-- (Isolated Database Subnets)
```

1. **Presentation / Web Tier (Public Subnets):**
   - **Application Load Balancer (ALB):** Restricts incoming requests strictly to HTTP/HTTPS.
   - **AWS WAFv2:** Filters regional requests, blocking OWASP Top-10 vulnerabilities, SQL injection attempts, and implementing active IP rate limits.
2. **Application / Compute Tier (Private Subnets):**
   - **Auto Scaling Groups (ASG):** Secure, isolated EC2 instances running hardened **Ubuntu 26.04 LTS** (Graviton ARM64 architecture). Direct SSH is disabled; systems are managed passwordlessly using **AWS Systems Manager (SSM)**.
   - **Amazon ElastiCache for Valkey:** High-performance, secure, and license-compliant key-value cache layer configured for fast query/session operations.
3. **Database Tier (Isolated Subnets):**
   - **Multi-AZ RDS PostgreSQL:** Isolate data across multiple availability zones. Ingress is restricted exclusively to port 5432 originating from the compute tier.

---

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       ├── jekyll-gh-pages.yml   # Automates python document processing & Jekyll deploy
│       └── opentofu.yml          # Format, lint, OIDC-based validation & deploy
├── docs/                         # Jekyll Document System (Source of GitHub Pages Portal)
│   ├── _layouts/                 # Jekyll theme responsive layouts
│   ├── assets/                   # Centralized stylesheets (global.css)
│   ├── modules/                  # Technical sub-specifications for every component
│   └── *.md                      # Extensive engineering guide files
├── scripts/                      # Operation and deployment utility scripts
│   ├── deploy.sh                 # Coordinates OpenTofu linting, format, validate, and plans
│   ├── destroy.sh                # Graceful deletion coordinator for provisioning
│   ├── prepare_docs.py           # Pre-build Python processor prepending front-matter
│   └── user_data.sh              # Cloud-init bootstrapping script
├── terraform/                    # Modularized Infrastructure as Code (IaC) configuration
│   ├── modules/                  # Submodules encapsulating AWS resources
│   │   ├── alb/                  # Load balancer target definitions
│   │   ├── asg/                  # Launch templates & dynamic scaling rules
│   │   ├── elasticache/          # Valkey cluster configuration
│   │   ├── jumphost/             # Cyberjaya whitelisted SSH Bastion setup
│   │   ├── rds/                  # Highly available Postgres instance configuration
│   │   ├── route53/              # Dynamic records mapping DNS values
│   │   ├── security_groups/      # Strict port security definitions
│   │   ├── standalone_ec2/       # Pre-bake AMI dev / test environments
│   │   └── vpc/                  # Multi-AZ subnet allocation structures
│   ├── main.tf                   # Core OpenTofu file mapping variables and submodules
│   ├── outputs.tf                # Global stack endpoints outputs
│   ├── providers.tf              # Declarative block specifying AWS, TLS, Random, etc.
│   ├── variables.tf              # Fully typed input variables
│   └── terraform.tfvars.example  # Production template environment configurations
├── .agents/                      # AI Agent Operating Laws and Spatial Memory
│   ├── brain/                    # Persistent Agent Spatial Memory
│   │   └── active_context_manifest.md # Active session checkpoint summaries
│   ├── skills/                   # Specific procedurial skills
│   │   └── jules-knowledge/SKILL.md # Compiled Google Jules engineering skill
│   └── AGENTS.md                 # Sovereign Constitution & Agent Rulebook (Rule 29)
├── README.md                     # Central documentation index portal (this file)
├── AGENTS.md                     # Root Gateway file redirecting to .agents/AGENTS.md
├── llms.txt                      # AI-optimized plain text directory pointing to resources
├── HISTORY.md                    # Rich project narrative detailing the timeline from Day 0
└── CHANGELOG.md                  # Semantic version history detailing milestones to v1.0.0
```

---

## Documentation Portal Index

Our comprehensive documentation is compiled, auto-formatted, and deployed directly via **GitHub Pages**. Use the catalog below to navigate to specific sections:

### 1. Conceptual Alignment & Architecture
* **[AWS Phased Adoption Roadmap & Costing Guide](docs/aws-adoption-roadmap.md):** Multi-year week-by-week and month-by-month AWS service growth plan mapped from the project Gantt chart.
* **[Developer Design Alignment](docs/developer-design-mapping.md):** Architectural breakdown mapping fragile legacy single-VM developer architectures into enterprise-level highly available managed services.
* **[Separation of Concerns](docs/asg-separation-of-concern.md):** Guidelines for implementing stateless ASG layers, session persistence, and comparative analysis of S3 vs. Amazon EFS.
* **[System Architecture Details](docs/architecture.md):** Comprehensive breakdown of VPC subnetting, route tables, and Multi-AZ network architecture configurations.
* **[OpenTofu Migration Guide](docs/opentofu-migration.md):** Migration patterns, state management comparisons, and CLI syntax transitions between legacy Terraform and OpenTofu.
* **[Google Antigravity Skills Guide](docs/antigravity-skills.md):** Unified standard outlining how to deploy workspace-specific skills and bridge the knowledge-bases of Google Jules and Google Antigravity.
* **[SOP: Knowledge-First Discovery](docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md):** Standard Operating Procedure outlining how AI agents perform local documentation search before probing remote targets.
* **[Technology Stack Comparison](docs/tech-stack-comparison.md):** Architectural mapping and AWS-native options guide for the developer's containerized and external system dependencies.
* **[Redis vs. Valkey Comparison](docs/redis-vs-valkey.md):** Strategic, licensing, and costing comparison (Baseline vs. High-Performance) of Redis OSS vs. Valkey on AWS and on-premises.
* **[Software Licensing & Technology Risk Register (TS/MC Series)](docs/licensing-risks.md):** Complete software licensing compliance framework, technology risk registry, and mitigation plans (TS/MC Series) covering LangChain4j, self-hosted operations, Bedrock with Qwen3 models, and standalone Wazuh SIEM.
* **[Strategic Comparative Review](docs/aws-vs-self-hosted-review.md):** Comprehensive strategic analysis and financial TCO comparison of an AWS-Native Managed Platform against a Self-Hosted / On-Premises Custom Stack in Malaysia.
* **[Load Testing Assumptions & Sizing Guide](docs/load-test-assumptions.md):** Workload definitions, SLA metrics, architectural performance assumptions, and multi-VU sizing models from 100 to 10,000 VUs.
* **[Context7 AI Chat Integration Guide](docs/context7.md):** Detailed guide explaining our floating AI chat widget, how to use it, and background information about Context7 and its provider Upstash.
* **[Security Posture Assessment (SPA) Checklist](docs/audits/security-posture-assessment.md):** Comprehensive security control audit checklist, fully customized for our Java, Spring Boot, PostgreSQL, Valkey, and RAGFlow/Langfuse AI infrastructure.
* **[Legal Notice & Disclaimer](docs/legal-notice.md):** Comprehensive policy statement and disclaimer detailing our project assumptions and liability exclusions.
* **[Output of ASIMP](docs/audits/asimp-output.md):** Example execution output, report format, and baseline metrics generated by ASIMP.
* **[Output of Lynis](docs/audits/lynis-output.md):** High-fidelity example of the Lynis host auditing utility scanning logs, attributes, and suggestions.
* **[Output of OpenSCAP](docs/audits/openscap-output.md):** Detailed example of OpenSCAP CIS Level 2 scan evaluation rules, results, and generated remediations.
* **[AWS Services vs. On-Premises Open-Source Stack Comparison](docs/aws-vs-onprem-stack-comparison.md):** Comprehensive 12-layer comparison guide mapping AWS services to self-hosted equivalents.

### 2. Infrastructure Submodules
* **[VPC Networking](docs/modules/vpc.md):** Dynamic subnetting allocation, NAT Gateway patterns, and Route Table linkages.
* **[Security Groups Firewall](docs/modules/security_groups.md):** Zero-Trust ingress/egress rules and port-level component isolation.
* **[WAF Protection](docs/modules/waf.md):** Layer-7 Web Application Firewall settings, custom rulesets, and IP rate limits.
* **[ALB Target Routing](docs/modules/alb.md):** Target groups routing rules, SSL termination, and endpoint configurations.
* **[ASG Compute Clusters](docs/asg-separation-of-concern.md):** Launch templates, scaling definitions, and automatic ARM64 Graviton architecture detection.
* **[RDS Multi-AZ PostgreSQL](docs/modules/rds.md):** Database clustering, parameter group optimization, and storage encryption details.
* **[ElastiCache Valkey](docs/modules/elasticache.md):** Ultra-fast caching cluster parameters and cost considerations.
* **[Jumphost (SSH Bastion)](docs/modules/jumphost.md):** Secured entrypoints mapping whitelisted Cyberjaya developer offices to downstream resources.
* **[Standalone EC2 Environments](docs/modules/standalone_ec2.md):** Dedicated testing/development servers mimicking identical RDS/S3 linkages.

### 3. Advanced Operational Guides
* **[Disaster Recovery & Sovereignty](docs/dr-options.md):** High-availability failover guidelines, AWS Elastic Disaster Recovery (AWS DRS) Strategy modeling, and Malaysian PDPA compliance pathways.
* **[PostgreSQL Database Comparison](docs/postgresql-comparison.md):** Managed RDS PostgreSQL 17 Multi-AZ vs. self-installed Percona PostgreSQL 17 on EC2 (comparing Patroni/PgBouncer, telemetry, and local costs).
* **[Secure Bastion & Jumphost Operations](docs/jumphost.md):** Manual detailing secure client key configurations, Windows/macOS connection commands, and ASIMP-hardened operating parameters.
* **[Hybrid Cloud Connections](docs/hybrid-onprem.md):** Evaluation comparing high-cost VPN/Direct Connect with modern cost-optimized API-driven and MCP-proxy integration styles.
* **[AMI Hardening Compliance](docs/ami-design.md):** Pre-baked Ubuntu 26.04 LTS AMIs using Packer, Ansible, and the ASIMP security hardening framework.
* **[GitLab CI/CD & Persistent EFS Storage](docs/gitlab-efs-cicd.md):** GitLab pipeline automation mounting EFS, tuning performance with `open_file_cache`, and managing dynamic Nginx paths.
* **[Route 53 & Dynamic DNS Troubleshooting](docs/route53.md):** Domain names matching, certificate auto-validation, and extensive research on ASG dynamic resolver cache issues.
* **[Wazuh Standalone Cloud Installation & Costing](docs/wazuh.md):** Architectural guide outlining the cheapest standalone Wazuh cloud deployment strategies, security whitelisting, and isolated USD/MYR costing plans.
* **[Wazuh SIEM & XDR Deep-Dive Guide](docs/wazuh-detailed.md):** In-depth functional breakdown of Wazuh SIEM & XDR capabilities, deployment modes (cloud/on-prem), and critical operational guidance regarding Antivirus coexistence, passive mode configuration, and Windows Defender integration.

### 4. Financial Cost Estimations
* **[Cost Analysis Guide](docs/costing.md):** Comprehensive price modeling in USD and MYR tailored for the `ap-southeast-5` (Malaysia) region. Includes:
  - **Baseline Cost-Optimized Plan (~$426.75 USD/mo):** Budget-oriented layout leveraging shared instances, Valkey caching, and single NAT routing.
  - **High-Performance Enterprise Plan (~$1,064.46 USD/mo):** High-availability layout leveraging multi-NAT, large compute families, and extensive backup limits.

---

## Getting Started

### Prerequisites
* [OpenTofu](https://opentofu.org/downloads.html) >= 1.6.0 installed on your local control node.
* [AWS CLI](https://aws.amazon.com/cli/) configured with administrative rights targeted to `ap-southeast-5`.
* Python >= 3.10 (to run build/prepare automation).

### Local Execution Pipeline
1. **Initialize & Sync Repository:**
   ```bash
   git clone https://github.com/your-username/aws-3tier-deployment-for-ai-infra.git
   cd aws-3tier-deployment-for-ai-infra
   ```
2. **Setup Environment Variables:**
   ```bash
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   ```
   *Edit the tfvars configuration with your target PostgreSQL credentials and office IP ranges.*
3. **Execute Automated Deployment Script:**
   The `scripts/deploy.sh` handles linting, auto-formatting, syntax validation, and displays the proposed modifications:
   ```bash
   ./scripts/deploy.sh
   ```
4. **Teardown Clean-up:**
   To safely remove and de-provision resources:
   ```bash
   ./scripts/destroy.sh
   ```

---

## CI/CD Deployment with GitHub Actions

The repository integrates a secure deployment pipeline in `.github/workflows/opentofu.yml` utilizing **AWS OIDC (OpenID Connect)**.

### Pipeline Features
* **Conditional Triggers:** OpenTofu plan/apply executions are dynamically bypassed in fork pull-requests where AWS secrets are restricted. This avoids standard deployment failures while maintaining full local verification.
* **Jekyll Compilation Pages:** The `.github/workflows/jekyll-gh-pages.yml` automatically executes the `scripts/prepare_docs.py` before building and publishing our responsive documentation portal.

---

## Contact & Maintenance

For questions regarding development parameters, AMI baking steps, or local security policies, consult [AGENTS.md](AGENTS.md) or open an issue on the centralized repository.
