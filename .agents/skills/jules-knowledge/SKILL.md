---
name: jules-knowledge
description: Comprehensive workspace instructions, architectural mappings, security boundaries, and automation practices curated from Google Jules. Use this when performing Cloud and Systems Engineering tasks in this repository.
---

# Google Jules Infrastructure & Cloud Engineering Skill

This skill embeds the full engineering knowledge, context, standards, and constraints of Google Jules—an elite Cloud and Systems Engineer assisting in maintaining and optimizing the secure AWS 3-Tier Web & AI Infrastructure workspace.

---

## 1. Core Operating Constraints & Regional Defaults

All agents (including Google Antigravity and Google Jules) must strictly adhere to the following defaults:

* **Primary AWS Region:** Natively target **AWS Asia Pacific (Malaysia)** (`ap-southeast-5`).
* **Compute Architecture:** AWS Graviton ARM64 architecture (e.g., `t4g.micro` for EC2 and `db.t4g.micro` for RDS).
* **Target Operating System:** Hardened **Ubuntu 26.04 LTS** utilizing the ASIMP (Ansible System Integrity Management Platform) security framework.
* **Database Ingress:** RDS must accept ingress traffic on port 5432 **exclusively** from the active application Auto Scaling Group security group and Standalone EC2 nodes. Direct public routing is strictly forbidden.
* **Session and Key-Value Caching:** Deployed with **Amazon ElastiCache for Valkey** (`cache.t4g.micro` or `cache.t4g.medium`). Using Valkey provides high security and yields 20% cost savings over Redis OSS in Malaysia.
* **Management Access:** Direct SSH is disabled on compute nodes. All administration is performed via AWS Systems Manager (SSM) Session Manager or whitelisted SSH Jumphosts restricted to Cyberjaya developer office CIDRs.

---

## 2. Directory Layout & Mental Map

Familiarize yourself with the repository layout before modifying infrastructure or documentation:

```
.
├── terraform/                   # OpenTofu Infrastructure Code
│   ├── main.tf                  # Global resource linkage file
│   ├── providers.tf             # Multi-provider integrations
│   ├── variables.tf             # Strictly typed variables
│   ├── outputs.tf               # Root output endpoints
│   └── modules/                 # Modular, encapsulated components
│       ├── vpc/                 # Network subnets & IGW/NAT config
│       ├── security_groups/     # Port-level isolation & office whitelisting
│       ├── alb/                 # ALB routing, health-checks & TLS
│       ├── waf/                 # Web ACL rate limits & OWASP rulesets
│       ├── asg/                 # Auto Scaling Group launch templates
│       ├── rds/                 # Highly available Multi-AZ DB configuration
│       ├── standalone_ec2/      # Secure pre-baking AMI / dev instances
│       ├── elasticache/         # Valkey cache cluster deployment
│       └── jumphost/            # Bastion setup whitelisting office IPs
│
├── docs/                        # Static Documentation Portal (Jekyll)
│   ├── _layouts/                # Fluid responsive layout configurations
│   ├── assets/                  # Central styling sheets (global.css)
│   └── *.md                     # Deep technical guides and comparisons
│
├── scripts/                     # Automation & Bootstrapping Utilities
│   ├── deploy.sh                # Interactive OpenTofu format, plan, and deploy
│   ├── destroy.sh               # Safe resource teardown automation
│   ├── user_data.sh             # Cloud-init instance bootstrapping
│   └── prepare_docs.py          # Jekyll front-matter validator & utility
```

---

## 3. Financial Cost Baseline & High Performance Profiles

Always keep these two cost targets in mind when designing modifications to the environment:

1. **Baseline Cost-Optimized Plan (~$426.75 USD/mo):**
   - For budget-oriented environments.
   - Deploys single NAT Gateways, shared compute instances, and lower-tier DB configurations.
2. **High-Performance Enterprise Plan (~$1,064.46 USD/mo):**
   - For highly resilient production layouts.
   - Deploys multi-NAT subnets, larger compute instances, and extensive backup profiles.

---

## 4. Mandatory Developer Workflows & Commands

Before declaring any infrastructure or documentation task complete:

### A. Run OpenTofu Validation & Formatting
Always lint and dry-run infrastructure updates using the built-in deploy script:
```bash
./scripts/deploy.sh
```
*This handles `tofu fmt`, `tofu validate`, and creates a secure `tofu plan` matching regional parameters.*

### B. Prepare Jekyll Documentation Headers
If any `.md` file is created or modified in `docs/` or the workspace root, run the pre-build prep script to automatically inject layout configurations and title tags:
```bash
python scripts/prepare_docs.py
```

### C. Verify Your Work Locally
Always confirm your actions with a read-only command (such as `cat`, `ls`, or python-based read scripts) after editing any repository file. Do not assume success without inspecting the target file's updated contents.

---

## 5. Architectural Deep Dives Index

For detailed guidelines, refer to the local files:
- **Architecture Overview:** See [docs/architecture.md](docs/architecture.md)
- **OpenTofu Migration:** See [docs/opentofu-migration.md](docs/opentofu-migration.md)
- **Cost Analysis Details:** See [docs/costing.md](docs/costing.md)
- **Disaster Recovery & National Sovereignty:** See [docs/dr-options.md](docs/dr-options.md)
- **RDS PG 17 vs. Percona PG 17:** See [docs/postgresql-comparison.md](docs/postgresql-comparison.md)
- **RAGFlow + Langfuse GPU Workloads:** See [docs/ragflow-langfuse.md](docs/ragflow-langfuse.md)
