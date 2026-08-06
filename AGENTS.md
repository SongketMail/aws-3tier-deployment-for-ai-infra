---
layout: "default"
okf_version: "0.1"
type: "Agent Operating Instructions"
title: "Agent Operating Instructions & Guidelines (AGENTS.md)"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "agents", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "bastion", "disaster-recovery", "postgresql", "sovereignty", "compliance", "skills"]
---
# Agent Operating Instructions & Guidelines (AGENTS.md)

Welcome, AI Agent! This document is the primary root entrypoint and gateway outlining the standard operating procedures, architectural contexts, and style requirements for all agents—specifically **Google Jules**, **Google Antigravity**, and other advanced LLM-based assistants—collaborating on this project.

---

## 🧭 1. The Gateway to the Constitution

Before you perform any action, review our sovereign rules. This file acts as a high-level router:

- **Root Gateway:** `AGENTS.md` (this file)
- **Sovereign Constitution & Detailed Rulebook:** [**.agents/AGENTS.md**](.agents/AGENTS.md)
- **Standard Operating Procedure (SOP) for Local Discovery:** [**docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md**](docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md)
- **Spatial Memory Manifest:** [**.agents/brain/active_context_manifest.md**](.agents/brain/active_context_manifest.md)

---

## 🔍 2. Rule 29: Local Knowledge-First Mandate

To ensure token efficiency and avoid remote command errors or remote server probing hallucinations, you **MUST FIRST** search local project knowledge in `.agents/brain/` and `docs/` using search tools or `read_file` on OKF frontmatter (`topics:` / `description:`) before:
1. Executing dynamic AWS commands or OpenTofu state validation.
2. Probing live staging/production standalone EC2 or active ASG nodes.
3. Conducting external Google queries.

Remote server execution or live telemetry collection is strictly reserved for applying configuration updates or inspecting dynamic live runtime state that cannot be modeled locally.

---

## 🛠️ 3. Google Antigravity & Agent Skills Suite

To bridge the knowledge bases of Google Jules and Google Antigravity seamlessly, we have deployed a comprehensive suite of 11 Antigravity-compatible Agent Skills under `.agents/skills/`. Each skill consists of a directory with a `SKILL.md` file featuring a combined OKF/Antigravity YAML frontmatter and concludes with the standard Deep State of Mind (DSOM) AI Protocol footer.

### Complete List of Agent Skills:

1. **[`jules-knowledge`](.agents/skills/jules-knowledge/SKILL.md):** Generic cloud engineering skill containing comprehensive workspace instructions, architectural mappings, security boundaries, and automation practices.
2. **[`aws-malaysia-defaults`](.agents/skills/aws-malaysia-defaults/SKILL.md):** Guidelines for configuring regional defaults, AWS Graviton architecture, standard instance sizes, and dynamic ARM64/x86_64 AMI selection for `ap-southeast-5` (Malaysia).
3. **[`opentofu-infrastructure-design`](.agents/skills/opentofu-infrastructure-design/SKILL.md):** Standards for managing, validating, and designing the secure modular 3-tier OpenTofu architecture (VPC, Security Groups, WAF, ALB).
4. **[`aws-asg-standalone-compute`](.agents/skills/aws-asg-standalone-compute/SKILL.md):** Guidelines for deploying multi-tier ASGs, pairing them with standalone EC2 instances for staging/pre-baking AMIs, and managing compute passwordlessly via SSM.
5. **[`rds-postgresql-valkey-cache`](.agents/skills/rds-postgresql-valkey-cache/SKILL.md):** Settings for Multi-AZ RDS PostgreSQL (PostgreSQL 16/17 default), secure ElastiCache Valkey caching clusters, port-level network isolation, and comparative self-hosted vs. RDS database designs.
6. **[`ssh-jumphost-ami-baking`](.agents/skills/ssh-jumphost-ami-baking/SKILL.md):** Guidelines for secure public SSH Jumphost (Bastion) access whitelisting Cyberjaya, protecting private keys, and baking CIS Level 2-compliant Ubuntu 26.04 AMIs with Packer & Ansible.
7. **[`aws-disaster-recovery-sovereignty`](.agents/skills/aws-disaster-recovery-sovereignty/SKILL.md):** Playbook for PDPA-compliant In-Region and Cross-Region DR, deploying AWS DRS (Strategy E) replication, and addressing generative AI sovereign workloads (RAGFlow + Langfuse).
8. **[`aws-infrastructure-costing`](.agents/skills/aws-infrastructure-costing/SKILL.md):** Financial management models evaluating the Baseline Cost-Optimised Plan (~$426.75 USD/mo) and High-Performance Enterprise Plan (~$1,064.46 USD/mo) inside the Malaysia region.
9. **[`gitlab-efs-cicd-automation`](.agents/skills/gitlab-efs-cicd-automation/SKILL.md):** Procedures for GitLab CI/CD pipelines, mounting shared AWS EFS storage, tuning NFS mounts, and configuring dynamic Nginx paths (`open_file_cache`).
10. **[`changelog-milestones-narrative`](.agents/skills/changelog-milestones-narrative/SKILL.md):** Procedures for maintaining standard-compliant semantic changelogs (`CHANGELOG.md`) and strategic engineering history logs (`HISTORY.md`) from Day 0.
11. **[`jekyll-pdf-generation`](.agents/skills/jekyll-pdf-generation/SKILL.md):** Guidelines for custom responsive Jekyll sidebar themes, preventing diagram text wrapping with dynamic JavaScript scanners, print page-break overrides, and high-fidelity PDF workflows.

---

## 4. Core Architectural Constraints & Defaults

Always adhere to these architectural parameters to ensure budget alignment and performance predictability:
* **AWS Region:** Natively target `ap-southeast-5` (Malaysia) as the primary deployment location.
* **Architecture Class:** Secure 3-Tier topology (WAF -> ALB in Public Subnets -> ASG in Private Subnets -> RDS Multi-AZ in Isolated DB Subnets).
* **Target Operating System:** Hardened Ubuntu 26.04 LTS using the Ansible System Integrity Management Platform (ASIMP).
* **Compute Architecture:** AWS Graviton ARM64 architecture (e.g., `t4g.micro` for EC2 and `db.t4g.micro` for RDS PostgreSQL 16/17).
* **Caching Layer:** Valkey (`cache.t4g.micro` or `cache.t4g.medium`) over Redis OSS due to license compliance and cost savings (20% lower pricing in Malaysia).
* **Database Ingress:** Strictly isolated. RDS must only accept incoming connections on port 5432 originating from the active ASG security group and Standalone EC2 instances. Direct public routing is forbidden.
* **Management Access:** All administration, debugging, and staging tasks are conducted via the Systems Manager (SSM) Session Manager or whitelisted Bastion (Cyberjaya office IP ranges only).

---

## 5. Guiding Principles for Google Jules & AI Agents

### A. Always Verify Your Work
After making any modifications (creating, updating, or deleting files), **never assume success**. Always invoke a read-only tool (such as `read_file` or `list_files`) to verify that the file reflects the exact intended changes.

### B. Edit Source, Not Artifacts
Do not edit build outputs or generated files under `dist/`, `build/`, or `_site/` directly. Locate and modify original source files, and run the designated script to rebuild (e.g. running `python scripts/prepare_docs.py` to auto-format Jekyll headers).

### C. Practice Proactive Testing & Validation
Prioritize writing and executing validation steps. Run syntax validation before proposing deployments.

---

## 6. How to Run Automation & Validation

To test your work and maintain compliance, use these built-in scripts:

1. **Jekyll Documentation Preparation:**
   ```bash
   python scripts/prepare_docs.py
   ```
   *Always run this command if you edit or add a Markdown documentation page under `docs/` or the root folder.*

2. **OpenTofu Linter & Plan Validation:**
   ```bash
   ./scripts/deploy.sh
   ```
   *Runs syntax formatting checks (`tofu fmt`), verifies module linkages (`tofu validate`), and outlines intended resources (`tofu plan`).*

---

## 🧭 7. Open Knowledge Format (OKF) & Front Matter Guidelines

Every Markdown file in this repository must begin on line 1, column 1 with a standard `---` YAML front matter block complying with the **OKF v0.1/v0.2 specification**, ending cleanly with a closing `---` line. The YAML front matter block must be followed immediately by the Markdown body content.

### Formatting Rules to Fix broken Web View Parsing:
1. **Line 1, Column 1 Starting:** The opening `---` of the front matter block must start exactly on line 1, column 1 of the document. No leading whitespace or empty lines are allowed.
2. **Double Quote String Values with Special Characters:** Wrap all string values containing emojis, colons, brackets, parentheses, curly braces, ampersands, or other special characters in double quotes. E.g.:
   - `title: "🧠 Deep State of Mind (DSOM)"`
   - `title: "SOP: Knowledge-First Discovery & Context Preservation Protocol"`
   - `layout: "default"`
3. **Escaping Inside Strings:** If a double-quoted string contains double quotes inside it, escape them with a backslash (e.g. `title: "A \"Cool\" Title"`).
4. **Preserve Array Formats & Timestamps Intact:**
   - **Arrays:** Store lists (such as `topics`) in inline JSON-style array format. E.g., `topics: ["aws", "cloud", "architecture"]`.
   - **Timestamps:** Keep ISO 8601 UTC timestamps intact and unquoted to parse natively as YAML datetimes. E.g., `timestamp: 2026-08-05T22:04:00Z`.
5. **OKF v0.1 Core Front Matter Structure:**
   - `layout`: `"default"` (Required for Jekyll layouts)
   - `okf_version`: `"0.1"` (Specifies OKF version)
   - `type`: Categorical label (e.g., `"Guide"`, `"Portal"`, `"Skill"`, `"Changelog"`, `"History"`, `"SOP"`)
   - `title`: Human-readable title (Must be wrapped in double quotes if it contains any special characters)
   - `timestamp`: UTC ISO 8601 timestamp (Unquoted, e.g., `2026-08-05T22:04:00Z`)
   - `topics`: List of keywords in `["a", "b"]` format.

*Always run `python scripts/prepare_docs.py` to auto-validate, reformat, and update these headers after creating or editing Markdown files. The script is designed to ensure strict compliance with these rules.*
