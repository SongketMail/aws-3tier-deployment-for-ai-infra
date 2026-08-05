---
layout: "default"
okf_version: "0.1"
type: "Agent Operating Instructions"
title: "Agent Operating Instructions & Guidelines (AGENTS.md)"
timestamp: 2026-08-05T21:53:00Z
topics: ["aws", "cloud", "architecture", "agents", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "bastion", "disaster-recovery", "postgresql", "sovereignty", "compliance"]
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

## 3. Core Architectural Constraints & Defaults

Always adhere to these architectural parameters to ensure budget alignment and performance predictability:
* **AWS Region:** Natively target `ap-southeast-5` (Malaysia) as the primary deployment location.
* **Architecture Class:** Secure 3-Tier topology (WAF -> ALB in Public Subnets -> ASG in Private Subnets -> RDS Multi-AZ in Isolated DB Subnets).
* **Target Operating System:** Hardened Ubuntu 26.04 LTS using the Ansible System Integrity Management Platform (ASIMP).
* **Compute Architecture:** AWS Graviton ARM64 architecture (e.g., `t4g.micro` for EC2 and `db.t4g.micro` for RDS PostgreSQL 16/17).
* **Caching Layer:** Valkey (`cache.t4g.micro` or `cache.t4g.medium`) over Redis OSS due to license compliance and cost savings (20% lower pricing in Malaysia).
* **Database Ingress:** Strictly isolated. RDS must only accept incoming connections on port 5432 originating from the active ASG security group and Standalone EC2 instances. Direct public routing is forbidden.
* **Management Access:** All administration, debugging, and staging tasks are conducted via the Systems Manager (SSM) Session Manager or whitelisted Bastion (Cyberjaya office IP ranges only).

---

## 4. Guiding Principles for Google Jules & AI Agents

### A. Always Verify Your Work
After making any modifications (creating, updating, or deleting files), **never assume success**. Always invoke a read-only tool (such as `read_file` or `list_files`) to verify that the file reflects the exact intended changes.

### B. Edit Source, Not Artifacts
Do not edit build outputs or generated files under `dist/`, `build/`, or `_site/` directly. Locate and modify original source files, and run the designated script to rebuild (e.g. running `python scripts/prepare_docs.py` to auto-format Jekyll headers).

### C. Practice Proactive Testing & Validation
Prioritize writing and executing validation steps. Run syntax validation before proposing deployments.

---

## 5. How to Run Automation & Validation

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
