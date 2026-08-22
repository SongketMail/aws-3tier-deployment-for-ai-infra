---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "OpenTofu AWS Infrastructure Building, Simulation, & Multi-Agent Collaboration Runbook"
timestamp: 2026-08-11T10:00:00Z
topics: ["opentofu", "aws", "simulation", "testing", "multi-agent", "collaboration", "devops", "security"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Infrastructure Engineers, SREs, & AI Agents
</div>

# 🛠️ OpenTofu AWS Infrastructure Building, Simulation, & Multi-Agent Collaboration Runbook

This guide establishes the standard operating procedures for developing, simulating, testing, and deploying OpenTofu Infrastructure-as-Code (IaC) targeting Amazon Web Services (AWS) without requiring direct AWS cloud environment credentials or live API access.

Due to security policies and isolation requirements, all OpenTofu module changes, architectural updates, and deployment flows **must be simulated and verified locally** using automated unit testing, static analysis, and mock scenario suites prior to merging. Furthermore, this document specifies protocols for human software engineers and autonomous AI agents (such as **Google Jules** and **Google Antigravity**) collaborating across forks and feature branches.

---

## 🧭 1. Architectural Strategy & Offline Simulation Philosophy

When direct AWS access is restricted for security, cost control, or compliance reasons, OpenTofu code quality and cloud compatibility are maintained through a multi-layer **Offline Cloud Simulation Framework**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Developer & Agent Workspace                          │
│  ┌──────────────────────┐  ┌────────────────────┐  ┌─────────────────┐ │
│  │ OpenTofu HCL Modules │  │ Pytest Test Suite  │  │ OKF Frontmatter │ │
│  └──────────┬───────────┘  └─────────┬──────────┘  └────────┬────────┘ │
└─────────────┼────────────────────────┼──────────────────────┼──────────┘
              │                        │                      │
              ▼                        ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Automated Offline Simulation                        │
│ ┌───────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐ │
│ │ Static AST Analysis   │ │ Unit Test Scenarios  │ │ Mock Plan Engine │ │
│ │ (IMDSv2, SGs, Ports)  │ │ (AZs, Limits, Arch)  │ │ (tofu validate)  │ │
│ └───────────────────────┘ └──────────────────────┘ └──────────────────┘ │
└────────────────────────────────────────┬────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       CI/CD PR Verification Gate                        │
│       ✔ Syntax Checks  ✔ Simulation Unit Tests  ✔ OKF Compliance       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Core Simulation Principles:
1. **Zero Cloud Credential Requirement:** No `AWS_ACCESS_KEY_ID` or active internet connection to AWS API endpoints is required during local simulation and unit testing.
2. **Provider Offline Schema Validation:** Standard provider blocks utilize static AWS provider definitions (`hashicorp/aws` >= 5.0) which validate configuration structure locally.
3. **AST & Pattern Testing:** Pytest unit tests analyze the Abstract Syntax Tree (AST) and regex structure of `.tf` files to enforce strict security constraints (e.g. IMDSv2, isolated security groups, Graviton `t4g.*` sizing).

---

## 🏗️ 2. OpenTofu HCL Code Structure & Building Guidelines

All OpenTofu configurations must follow a modular 3-Tier architecture design under the `terraform/` directory:

```
terraform/
├── main.tf                 # Network foundations & core security group calls
├── compute.tf              # Auto Scaling Group (ASG) & Standalone compute definitions
├── database.tf             # Multi-AZ RDS PostgreSQL & ElastiCache Valkey instances
├── web.tf                  # ALB, WAFv2, and Route 53 DNS resources
├── providers.tf            # Provider configuration (AWS regional defaults: ap-southeast-5)
├── variables.tf            # Strictly typed input variables and defaults
├── outputs.tf              # Exported attributes (ALB DNS, DB Endpoints, SG IDs)
└── modules/                # Encapsulated reusable modules
    ├── vpc/                # Multi-AZ subnets (Public, App, DB)
    ├── security_groups/    # Zero-Trust ingress/egress rules
    ├── alb/                # Application Load Balancer & target groups
    ├── asg/                # Launch templates with IMDSv2 & auto-healing
    ├── rds/                # Isolated PostgreSQL Multi-AZ engine
    ├── elasticache/        # Valkey cache cluster
    ├── jumphost/           # Hardened Cyberjaya SSH Bastion
    ├── route53/            # DNS alias mapping
    ├── standalone_ec2/     # Development/staging compute nodes
    └── waf/                # WAFv2 IP rate limiting rules
```

### Standard Module Rules:
- **IMDSv2 Strict Enforcement:** Launch templates (`modules/asg/main.tf` and `modules/standalone_ec2/main.tf`) must specify `metadata_options` with `http_tokens = "required"` and `http_put_response_hop_limit = 1`.
- **Zero-Trust Network Isolation:** Database security groups must only allow ingress on port 5432 originating from compute tier security groups (`security_groups = [aws_security_group.app.id]`). Direct CIDR ingress (`0.0.0.0/0`) to DB or App subnets is prohibited.
- **ALB-Aware Auto-Healing:** ASG modules must enforce `health_check_type = "ELB"` to synchronize instance lifecycles with ALB target group status.
- **Regional Architecture Defaults:** Default region is pinned to `ap-southeast-5` (Malaysia), utilizing Graviton instances (`t4g.micro` / `t4g.medium` / `db.t4g.micro`) and Valkey caching (`cache.t4g.micro`).

---

## 🧪 3. AWS Cloud Scenario Testing Matrix & Unit Test Integration

Each step in the OpenTofu code building lifecycle must be verified against simulated cloud scenarios using automated `pytest` unit tests in `tests/test_opentofu_simulation.py`.

### AWS Cloud Scenario Testing Matrix:

| Cloud Scenario / Constraint | Test Coverage | Expected Outcome | Verification Tool |
| :--- | :--- | :--- | :--- |
| **1. SSRF Metadata Hardening** | Compute Launch Templates & EC2 Instances | `http_tokens = "required"`, `http_put_response_hop_limit = 1` | `test_opentofu_imdsv2_enforcement` |
| **2. DB Network Isolation** | Database Security Groups | Ingress strictly restricted to App SG on port 5432; no `0.0.0.0/0` ingress | `test_opentofu_db_security_group_isolation` |
| **3. ALB Auto-Healing Integration** | ASG Configuration | `health_check_type = "ELB"` enabled across all scaling groups | `test_opentofu_asg_elb_health_check` |
| **4. Graviton Regional Alignment** | Variables & Defaults | Default region `ap-southeast-5`, Graviton `t4g.*` & `db.t4g.*` types | `test_opentofu_graviton_regional_defaults` |
| **5. Valkey Open-Source Caching** | ElastiCache Module | Caching engine set to `valkey` with default port `6379` | `test_opentofu_valkey_caching_config` |
| **6. Jumphost Cyberjaya Whitelisting**| Jumphost SG | SSH ingress restricted to office CIDR (`103.188.0.0/16` or custom) | `test_opentofu_jumphost_whitelisting` |
| **7. Multi-AZ Network Topology** | VPC Module | 2+ Availability Zones (`ap-southeast-5a`, `ap-southeast-5b`) spanned | `test_opentofu_vpc_multi_az_layout` |
| **8. Module Completeness** | Root Terraform Modules | All 10 modules (`vpc`, `sg`, `alb`, `asg`, `rds`, `valkey`, etc.) present | `test_opentofu_module_structure_completeness` |

### Executing Local Simulation Unit Tests:
```bash
# Run all simulation unit tests locally
pytest tests/test_opentofu_simulation.py -v
```

---

## 🤝 4. Multi-Human and Multi-AI Agent Collaboration Protocol

To ensure seamless collaboration between human software engineers and AI agents (**Google Jules**, **Google Antigravity**, external PR contributors), all code and documentation contributions must strictly observe the following protocol:

### A. Branching & Forking Strategy
- **Branch Naming:** Feature branches must use clear, descriptive prefixes:
  - `feature/opentofu-module-name` (e.g. `feature/opentofu-waf-rules`)
  - `fix/security-group-rule` (e.g. `fix/db-port-isolation`)
  - `docs/aws-simulation-update` (e.g. `docs/opentofu-runbook`)
- **Fork Contributions:** External human contributors or AI agents working in forks must ensure pull requests target the `main` branch of the upstream repository.

### B. OKF Specification & Frontmatter Rules
- Every newly created or updated `.md` file must include **OKF v0.1 YAML Frontmatter** starting on Line 1, Column 1:
  ```yaml
  ---
  layout: "default"
  okf_version: "0.1"
  type: "Guide"
  title: "Descriptive Page Title"
  timestamp: 2026-08-11T10:00:00Z
  topics: ["opentofu", "aws", "simulation", "testing"]
  ---
  ```
- All string values with special characters (colons, parentheses, emojis) **must be double-quoted**.
- Always run `python scripts/prepare_docs.py` to re-format frontmatter and compile `llms.txt` / `llms.xml`.

### C. Automated PR Quality Gates & Pre-Commit Workflow
Before submitting a PR or merging any code:
1. **Format & Validate OpenTofu Code (if OpenTofu CLI is installed):**
   ```bash
   tofu fmt -recursive terraform/
   tofu validate
   ```
2. **Execute Full Test Suite:**
   ```bash
   pytest
   ```
3. **Execute Pre-Commit Verification:**
   - Ensure all relative Markdown links resolve correctly (`test_markdown_relative_links_integrity`).
   - Run `python scripts/prepare_docs.py` and verify all tests pass cleanly.

---

## 🚀 5. Deployment Simulation Walkthrough (Offline Executions)

When introducing a new OpenTofu module or parameter change, follow this step-by-step verification checklist:

1. **Step 1: Write Declarative HCL Code**
   Place your configuration in the appropriate `terraform/` domain file (`compute.tf`, `database.tf`, `web.tf`, or `main.tf`) or module subdirectory.
2. **Step 2: Run Pytest Simulation Suite**
   Execute `pytest tests/test_opentofu_simulation.py` to ensure zero regressions in security group rules, IMDSv2 enforcement, or regional defaults.
3. **Step 3: Run Document Preparation Tool**
   Execute `python scripts/prepare_docs.py` to sync all indexes and validate OKF frontmatter across modified docs.
4. **Step 4: Create PR & Request Review**
   Push changes to your feature branch, open a PR with detailed descriptions, and await automated CI verification.

---

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-11*
