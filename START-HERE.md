---
layout: "default"
okf_version: "0.1"
type: "Portal"
title: "Start Here: Pragmatic Onboarding & Execution Standard"
timestamp: 2026-08-13T15:00:00Z
topics: ["start-here", "diataxis", "onboarding", "agents", "human", "dsom", "okf"]
---
# Start Here: Pragmatic Onboarding & Execution Standard

> *"You don’t need to read everything in this repository to make sense of our architecture, or to start using it in practice. In fact, we recommend that you don’t. The best way to get started is by applying it — to something, however small."*
> — Adapted from the Diátaxis Foundational Principle

---

## 1. Epigraph & Onboarding Philosophy

Welcome to the **AWS 3-Tier Deployment for AI & Web Infra** repository. This document serves as the primary operational entry point designed to deliver immediate, low-friction value for both human operators and autonomous AI agents.

### Dual-Interface Objective
Traditional documentation forces engineering teams and automated systems to absorb vast knowledge bases prior to execution. We reject this paradigm. This platform enforces a **dual-interface onboarding architecture**:
- **For Human Operators:** Clean, structured, Git-native navigation optimized for rapid local environment bootstrapping, architectural comprehension, and peer collaboration.
- **For Autonomous AI Agents (Jules, Google Antigravity, Sub-Agents):** Deterministic, machine-parseable context boundaries, structured metadata schemas (OKF v0.1), and explicit tool-calling execution guidelines.

---

## 2. Dual-Audience Entry Matrix (Diátaxis Navigation Grid)

Our documentation is structured around the four Diátaxis documentation quadrants. Use the routing matrix below to locate the precise resources required for your target role and current operational phase.

| Quadrant | Purpose | Human Developer Pathway | Autonomous AI Agent Pathway |
| :--- | :--- | :--- | :--- |
| **🎓 Tutorials** | Guided learning by execution | • [Quickstart: Operating Project Utilities](docs/tutorials/quickstart.md)<br>• Local sandbox initialization and test execution | • Step-by-step tool invocation verification<br>• Execution sandbox validation protocols |
| **📋 How-To Guides** | Problem-solving for real-world tasks | • [How-To: Standardising Metadata](docs/how-to/manage-metadata.md)<br>• [How-To: Compiling LLM Formats](docs/how-to/generate-llms-xml.md)<br>• [OpenTofu Deployment](docs/scripts.md) | • Task-specific delta generation<br>• [SOP: Knowledge-First Discovery](docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md)<br>• PR comment collaboration recipes |
| **📘 Reference Specs** | Dry, authoritative facts & specifications | • [System Architecture](docs/architecture.md)<br>• [OpenTofu Submodules](docs/modules/vpc.md)<br>• [Script Specs](docs/reference/prepare_docs.md) | • Machine-readable indices (`llms.txt`, `llms.xml`)<br>• Master Knowledge Ledger (`.agents/brain/jules_knowledge_ledger.md`) |
| **🧠 Explanation** | Background, design decisions & rationale | • [Diátaxis Framework](docs/explanation/diataxis.md)<br>• [AWS vs Self-Hosted TCO Review](docs/aws-vs-self-hosted-review.md)<br>• [Jules Platform Guide](docs/jules-platform-guide.md) | • Architectural constraints and boundary checks<br>• Deep State of Mind (DSOM) governance rules |

---

## 3. Immediate Action: The Smallest Viable Task

Do not read the full repository before taking action. Execute the minimal task sequence for your interface below to verify workspace integrity immediately.

### 🛠️ Human Pathway: 3-Step Quickstart Command Chain

Execute these three commands in your terminal to validate dependencies and verify local documentation processing:

```bash
# 1. Clone the repository and navigate to root
git clone https://github.com/songketmail/aws-3tier-deployment-for-ai-infra.git
cd aws-3tier-deployment-for-ai-infra

# 2. Run documentation metadata preparation and LLM index compilation
python3 scripts/prepare_docs.py && python3 scripts/parse_llms.py

# 3. Execute the unit and compliance test suite
pytest
```

---

### 🤖 Agent Pathway: Standardised Task Ingestion Protocol

Autonomous AI Agents (such as Google Jules or Google Antigravity) must follow this 4-step execution protocol upon task assignment:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. BOUNDARY PARSING                                                     │
│ Read OKF front matter in README.md, AGENTS.md, and llms.txt.             │
│ Do NOT load entire directory trees into context.                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. CONTEXT ANCHORING                                                    │
│ Check spatial memory in .agents/brain/active_context_manifest.md and    │
│ consult .agents/brain/jules_knowledge_ledger.md for past decisions.    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. DELTA EXECUTION & VERIFICATION                                       │
│ Apply minimal code/doc edits. Verify changes using read-only tools or   │
│ running `pytest` / `python3 scripts/prepare_docs.py`.                   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. STRUCTURED DIFF & COMMIT                                             │
│ Submit changes using standardized commit messages and pre-commit checks.│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Agent Context Governance (DSOM & OKF Integration)

To preserve context window precision and eliminate token waste, AI Agents operating within this repository are governed by strict context loading constraints:

1. **Context Window Minimization:** Agents must never read all repository files upfront. Search local knowledge in `.agents/brain/` and `docs/` using `topics:` / `description:` metadata filters before probing remote services or reading bulk files.
2. **Metadata Compliance (OKF v0.1):** Every created or updated Markdown file must begin with line 1 column 1 YAML front matter containing mandatory fields (`layout`, `okf_version`, `type`, `title`, `timestamp`, `topics`). Strings containing special characters must be double-quoted.
3. **Multi-Agent Interoperability:** Agents communicate state changes by updating `.agents/brain/active_context_manifest.md` and logging key milestones in `.agents/brain/jules_knowledge_ledger.md`. Eleven (11) dedicated agent skills are maintained in `.agents/skills/` to standardize cross-agent capabilities between Google Jules, Google Antigravity, and CI/CD automation runners.

---

## 5. Architectural Overview at a Glance

For immediate high-level context, our core AWS architecture deploys a Zero-Trust 3-Tier layout in the Malaysia region (`ap-southeast-5`):

```
                                [ INTERNET ]
                                     │
                                     ▼
                               [ AWS WAFv2 ]   <-- (OWASP Top 10 + Rate Limiting)
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

---

## 🧠 Deep State of Mind (DSOM) Governance

This repository operates under the **Deep State of Mind (DSOM) AI Protocol**, enforcing spatial memory persistence in `.agents/brain/`, agent skill modularization in `.agents/skills/`, and strict local knowledge-first discovery.

---
*End of Start Here Standard.*
