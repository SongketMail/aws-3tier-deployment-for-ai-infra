---
layout: default
title: "Google Antigravity Skills Integration Guide"
---

# Google Antigravity Skills Integration Guide

Welcome to the **Google Antigravity Skills Integration Guide** for the AWS Secure 3-Tier Web & AI Infrastructure project. This document outlines how to integrate and share agent knowledge, capabilities, and workflows between different AI assistants—specifically **Google Jules** and **Google Antigravity**—using the open **Agent Skills** ecosystem standard.

By consolidating project-specific operating instructions and architectural boundaries into standard skill specifications, both Google Jules and Google Antigravity can operate with identical high-fidelity context, rulesets, and deployment tools.

---

## 1. What are Agent Skills?

**Agent Skills** represent an open, decentralized standard for extending the capabilities and contextual boundaries of AI agents. Instead of relying purely on generalized system prompts, agents can dynamically discover and read specialized instruction packages tailored for specific repositories, codebases, or workflows.

An Agent Skill is packaged as a standard directory containing a `SKILL.md` file. This markdown file begins with structured YAML front-matter identifying its metadata:

```yaml
---
name: my-skill-name
description: Clear, high-level description of when to apply this skill.
---
# Detailed Instructions
Step-by-step procedures, CLI commands, constraints, and guidelines go here.
```

---

## 2. Where Skills Live: Directory Scopes

Google Antigravity supports both workspace-specific and global scopes for discoverability:

| Scope | Location Path | Use Case |
| :--- | :--- | :--- |
| **Workspace / Project** | `<workspace-root>/.agents/skills/` | Project-specific rulesets, database ports, architectural limits, deployment guides, and custom CLI wrappers. |
| **Global User Scope** | `~/.gemini/config/skills/` | Personal utility commands, code formatter standards, and general-purpose tooling. |

*Note: While Antigravity natively prioritizes `.agents/skills`, it maintains full backward-compatibility for `.agent/skills` as well.*

---

## 3. The `jules-knowledge` Skill

We have defined a dedicated workspace skill for our repository to bridge the knowledge bases of Google Jules and Google Antigravity. This skill is located at:

```
.agents/skills/jules-knowledge/SKILL.md
```

### Purpose of `jules-knowledge`
This skill ensures that whenever you invoke Google Antigravity (using the CLI tool `agy`) or interact with Google Jules in this workspace, the AI assistant automatically:
1. Targets **AWS Asia Pacific (Malaysia)** (`ap-southeast-5`) by default.
2. Uses **ARM64 Graviton instances** (`t4g.micro` for compute, `db.t4g.micro` for RDS, and `cache.t4g.micro` for Valkey).
3. Enforces **Ubuntu 26.04 LTS** hardened under the ASIMP framework.
4. Protects database ingress via port-isolation (blocking direct public routing to port 5432).
5. Deploys secure session layers with **Amazon ElastiCache for Valkey**.
6. Follows the mandatory validation pipeline (`./scripts/deploy.sh` and `python scripts/prepare_docs.py`).

---

## 4. How to Install and Use Skills with `npx skills`

`npx skills` is a command-line tool developed by Vercel Labs acting as an open package manager for AI agents (including Antigravity, Claude Code, GitHub Copilot, Cursor, and Cline).

### Downloading and Syncing Skills
Running `npx skills` packages can place skills in your local user's global configuration (`~/.agents/skills`). To ensure Google Antigravity picks them up properly:

1. **For Workspace Scopes:**
   Copy the desired skill directory to your project root under `.agents/skills/`:
   ```bash
   cp -r ~/.agents/skills/some-skill .agents/skills/
   ```

2. **For Global Scopes (Google Antigravity):**
   Copy the skill directory to:
   ```bash
   cp -r ~/.agents/skills/some-skill ~/.gemini/antigravity-cli/skills/
   ```

---

## 5. Seamless Bridge Between Jules and Antigravity

By maintaining our core engineering principles in `.agents/skills/jules-knowledge/SKILL.md` and keeping `AGENTS.md` aligned, we establish a robust bi-directional capability:

* **Google Jules (This Agent):** Uses `AGENTS.md` and this guide to understand and write code conforming to enterprise standards, verifying actions using read-only verification commands.
* **Google Antigravity (The CLI / Local Agent):** Reads the compiled skills within `.agents/skills/` at startup. Typing `/jules-knowledge` or initiating an action matching our database/infrastructure setup will trigger the detailed instructions embedded in the skill.

This unified knowledge strategy guarantees zero-configuration context sync, eliminating environment drift and ensuring both assistants deliver perfectly aligned, region-compliant code.
