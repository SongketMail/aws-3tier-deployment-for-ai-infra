---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "Google Jules Infrastructure & Cloud Engineering Skill"
timestamp: 2026-08-05T21:48:38Z
topics: ["aws", "cloud", "architecture", "skill", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "bastion", "route53", "dns", "ssl", "acm", "disaster-recovery", "gitlab", "efs", "postgresql", "gpu", "ragflow", "langfuse", "antigravity", "skills", "sovereignty", "compliance", "costing", "wazuh", "siem", "seo"]
description: "Comprehensive workspace instructions, architectural mappings, security boundaries, and automation practices curated from Google Jules. Use this when performing Cloud and Systems Engineering tasks in this repository."
name: "jules-knowledge"
---
# Google Jules Infrastructure & Cloud Engineering Skill

This skill embeds the full engineering knowledge, context, standards, and constraints of Google Jules—an elite Cloud and Systems Engineer assisting in maintaining and optimizing the secure AWS 3-Tier Web & AI Infrastructure workspace. Other AI Agents, including Google Antigravity, must strictly follow and leverage this knowledge base.

---

## 1. Introduction, Core Purpose, and Navigation

1. **Google Antigravity & Agent Skills Integration:** The repository supports Google Antigravity Skills, with this workspace-specific skill located at `.agents/skills/jules-knowledge/SKILL.md` containing comprehensive guidelines, architectural mapping, and standard operating procedures curated from Google Jules.
2. **Developer Integration Guide:** A developer integration guide for Google Antigravity Skills and the Agent Skills ecosystem is documented at `docs/antigravity-skills.md` and registered across all major documentation indices (`docs/index.md`, `README.md`, and `llms.txt`).
3. **AI Agent Guidelines (`AGENTS.md`):** The `AGENTS.md` file in the root directory outlines operating guidelines, standards, and behavioral constraints tailored for AI agents (specifically Google Jules) to ensure deterministic OpenTofu practices and strict adherence to architectural standards.
4. **LLM Crawling Index (`llms.txt`):** The `llms.txt` file is located in the root directory following the `llmstxt.org` specification, serving as an index for LLM web crawlers and AI agents to discover, parse, and navigate all architecture, costing, scripting, and disaster recovery guides.
5. **Developer Portal (`README.md`):** The root `README.md` is fully updated to serve as a comprehensive developer portal, structuring navigation paths to local repository files, OpenTofu (Terraform) submodules, and their fully compiled, respective Jekyll GitHub Pages documentation URLs.
6. **Comprehensive Documentation Standard:** The project requires comprehensive Markdown documentation for all modules, scripts, and workflows to support generating documentation pages for GitHub Pages. Centralized documentation is stored in the `docs/` folder configured for Jekyll.
7. **Sovereign GitHub Pages base URL:** The deployed GitHub Pages site's base URL is `https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/` (as per **Item 41**).

---

## 2. Regional Defaults & Cloud Platform Target

8. **Default Target Region & Compute:** The default deployment target is the AWS Asia Pacific (Malaysia) region (`ap-southeast-5`), using ARM64/Graviton instances (`t4g.micro` for EC2/ASG and `db.t4g.micro` for RDS PostgreSQL 16) by default.
9. **Dynamic AMI Selection:** The Auto Scaling Group (`asg`) module dynamically selects the appropriate Amazon Linux 2023 AMI (ARM64 or x86_64) based on the configured EC2 instance type family.
10. **Native OpenTofu Alignment:** The infrastructure configuration and documentation have been updated to target OpenTofu natively. Outdated Terraform references were corrected, including setting the recommended version specification to `OpenTofu >= 1.6.0` (while preserving backward compatibility with `Terraform >= 1.5.0`).
11. **Sandbox Execution Constraint:** The sandbox execution environment does not have the `terraform` or `tofu` CLI binaries installed by default.

---

## 3. Security, Hardening & Wazuh SIEM/XDR Deep-Dive

12. **Wazuh SIEM & XDR Integration:** A comprehensive Wazuh SIEM & XDR Deep-Dive Guide (`docs/wazuh-detailed.md`) outlines Wazuh's core functions, cloud and on-premises deployment modes, and critical operational guidance regarding Antivirus coexistence (including Windows Defender compatibility, third-party AV compatibility, potential conflict areas, and mutual exclusions configurations). This document is fully integrated into site navigations (`docs/_config.yml`), index files (`docs/index.md`, `README.md`, `llms.txt`), compilation pages (`docs/print_all.md`), and search sitemaps (`sitemap.txt`, `sitemap.xml`) (as per **Item 1**).
13. **Dedicated Licensing & Technology Risk Register (TS/MC Series):** Documented at `docs/licensing-risks.md` and integrated into Jekyll navigation, index files (`docs/index.md`, `README.md`), and guides (`docs/tech-stack-comparison.md`, `docs/costing.md`). It defines and tracks six critical risk/decision codes: LangChain4j SLA (TS-02), standalone Wazuh SIEM (TS-04), permissive/open-source licensing compliance (TS-05), self-hosted database operations (TS-06), Qwen3 LLM inference via Amazon Bedrock (MC-01), and Qwen3 embedding indexing (MC-02) (as per **Item 46**).
14. **Legal Notice & Disclaimer (`docs/legal-notice.md`):** Conforms to OKF v0.1 format and is fully integrated into the layout footer (`docs/_layouts/default.html`), navigation bar (`docs/_config.yml`), index and portal documents (`docs/index.md`, `README.md`, `llms.txt`), print compilation (`docs/print_all.md`), and search sitemaps (`sitemap.txt`, `sitemap.xml`) (as per **Item 8**).
15. **Context7 AI Widget & Page:** A dedicated integration page at `docs/context7.md` contains comprehensive documentation for the Context7 chat assistant widget. This page is formatted in compliance with OKF v0.1 front matter guidelines and integrated across all index files including `docs/_config.yml`, `docs/index.md`, `README.md`, `llms.txt`, and `docs/print_all.md` (as per **Item 30**).

---

## 4. Software Stack Comparison, Role-Based Directories & SEO

16. **AWS-vs-Onprem 12-Layer Stack Comparison Guide:** Documented at `docs/aws-vs-onprem-stack-comparison.md`, this guide maps AWS services to onsite open-source equivalents across all core infrastructure layers (from Frontend to Error Tracking) and is fully integrated across all major portal indexes (as per **Item 10**).
17. **Technology Stack Comparison Guide:** Documented at `docs/tech-stack-comparison.md` and integrated into Jekyll navigation and indexes (`docs/index.md`, `README.md`, `llms.txt`), comparing the local containerized developer stack (Spring Boot, React, React Native, Redis, PostgreSQL, RAGFlow, Twilio, Meta) against AWS equivalents (as per **Item 50**).
18. **Role-Based Architectural Directories:** The architectural documentation is modularised into dedicated, role-based subdirectories: `docs/executive/` (housing the 36-month TCO, non-AWS operational overheads, quarterly OpEx curves, and regulatory risk compliance under PDPA 2010 and 2025 CBPDT Guidelines) and `docs/engineering/` (containing low-level DevOps materials like OpenTofu module structures, systemd DNS troubleshooting steps, Ansible ASIMP hardening playbooks, and EFS shared storage mount scripts) (as per **Item 28**).
19. **Standard SEO Indexer Suite:** The repository contains a suite of standard SEO indexer files in the root directory: `sitemap.txt` (plain text list of all documentation URLs starting with `https://`), `sitemap.xml` (the standard XML sitemap for search engines with location, priority, lastmod, and changefreq tags), and `robots.txt` (which allows all search crawlers and points to the XML sitemap URL) (as per **Item 29**).

---

## 5. Deep State of Mind (DSOM) Framework & Sovereign AI Topology

20. **DSOM Adoption & Entry Points:** Adopted the Deep State of Mind (DSOM) For My AI framework (`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/START-HERE/`). Navigated via Diátaxis principles across 19 entry points (scaffolding, cognitive persona, crawlers, daily operations, MCP integration, subagents, skills, LLM WIKI, defensive GitOps, token efficiency, knowledge-first discovery, boot sequences, state sync, tri-phasic mind, OpenWiki, legal risk, OKF engine, guardrails, and episodic anchors) (as per **Item 52**).
21. **Tri-Phasic Mind Cognitive Model:** Cognition is split into 3 execution states:
    - **Active State (Conscious):** Low-latency MCP server (`tools/mcp/server.py`) interface for real-time task execution.
    - **Twilight State (Subconscious):** Near-real-time inline checks, token usage calculations, pre-flight audits (`tools/audit-pre-flight.sh`), and state compaction.
    - **Deep State (Unconscious/Dream):** Out-of-band scheduled rituals (SOD/EOD palace sync) for semantic consolidation and repository synchronization.
22. **Four Core Functional Subsystems:**
    - **Cognitive Architecture:** System 1 (reactive skills execution) vs System 2 (reflective discovery monologue).
    - **Memory Stratification:** Stratified storage across Token Buffer, Active Context (`.agents/brain/active_context_manifest.md`), Episodic Memory (`.agents/brain/walkthrough.md`), and Semantic Memory (`.agents/brain/wings/`).
    - **Dreaming & Consolidation:** EOD semantic pruning, synthetic failure test generation, and concept linking.
    - **Metacognition & Guardrails:** Self-audit via pytest compliance suites, alignment drift prevention, and immutable constitutional anchors (`.agents/AGENTS.md`).
23. **AI Boot & Initialization Sequence:** Upon reanimation, the AI follows a strict 5-step boot sequence: (1) Genesis Read (`.agents/AGENTS.md`), (2) Memory Restoration (`.agents/brain/`), (3) Master Onboarding Map (`START-HERE.md`), (4) Governance Topography (`docs/governance/`), and (5) Procedural Automation (`.agents/skills/`).

---

## 6. Script Hardening, Testing & Formatting Compliance

24. **Bash Script Navigation & Input Checks:** Bash scripts (`scripts/deploy.sh` and `scripts/destroy.sh`) are hardened to enforce success checks on directory navigation (`cd ... || exit 1`), quote variables consistently, and use standard `read -r -p` flag options for user input (as per **Item 2**).
25. **Python Codebase Formatting Cleanup:** Codebase formatting is cleaned up by removing unused `pytest` imports from all test files and correcting an extraneous `f` prefix on a log statement in `scripts/prepare_docs.py`, verified with `ruff check` and the `pytest` suite (as per **Item 4**).
26. **Complete Script Docstrings:** All major script files in the repository are updated with complete docstrings: PEP-257-compliant docstrings for `scripts/prepare_docs.py`, JSDoc-compliant comments for `scripts/generate_pdf.js`, and comprehensive header documentation with inline explanations for Bash scripts `scripts/deploy.sh`, `scripts/destroy.sh`, and `scripts/user_data.sh` (as per **Item 5**).
27. **Automated Pytest Suite:** The project features a comprehensive `pytest` test suite under the `tests/` directory containing 11 tests that validate: document preparation utilities (`test_prepare_docs.py`), FQCN-compliance and privilege separation in embedded Ansible playbooks (`test_ansible_playbooks.py`), valid systemd INI syntax and unprivileged user namespace mappings (`UserNS=keep-id:uid=2001,gid=2001`) in Podman Quadlet specifications (`test_podman_quadlets.py`), and OKF front matter / DSOM footer compliance across Markdown files (`test_md_compliance.py`) (as per **Item 6**).
28. **DRY Script Refactoring:** The pre-build Python script `scripts/prepare_docs.py` was refactored to eliminate a severe DRY violation (code duplication) by extracting duplicate string-unescaping and quote-stripping code blocks from `parse_yaml()` into a single, clean helper function `unescape_string(val)`. This refactoring preserved full operational parity and strict OKF parsing behavior (as per **Item 34**).
29. **Root Caches & IaC Exclusions:** The root `.gitignore` file includes exclusions for standard Python compilation and caching bytecode (`__pycache__/`, `*.py[cod]`, `*$py.class`) alongside standard OpenTofu/Terraform state and system configurations to ensure the git workspace remains clean during documentation preparation or test runs (as per **Item 35**).

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
