---
layout: "default"
okf_version: "0.1"
type: "Spatial Memory"
title: "Active Context Session Manifest (.agents/brain/active_context_manifest.md)"
timestamp: 2026-08-05T21:52:00Z
topics: ["agents", "context", "manifest", "memory", "brain", "okf"]
---
# Active Context Session Manifest (.agents/brain/active_context_manifest.md)

This active context manifest serves as our agent spatial memory checkpoint. It maps the active session's scope, key files, and completed milestones to preserve semantic context across different conversation threads.

---

## 1. Active Session Context & Objectives

- **Primary Goal:** Adopt and codify the Local Knowledge-First Discovery Protocol and Rule 29.
- **Architectural Context:** Ensure all architectural, operational, costing, and compliance decisions are resolved via local `.md` documents first, before querying external systems or running live cloud probes.
- **Completed Milestones:**
  - Codified Rule 29 in `.agents/AGENTS.md` (the Sovereign Constitution).
  - Created standard operating procedures in `docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md`.

---

## 2. Active File Registry

These files comprise the active memory and operational ruleset of the current session:

| Filepath | OKF Type | Role |
| :--- | :--- | :--- |
| `AGENTS.md` | Agent Operating Instructions | Gateway redirection file in root directory |
| `.agents/AGENTS.md` | Agent Operating Instructions | Sovereign Constitution containing Rule 29 |
| `docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md` | SOP | Standard Operating Procedure detailing the 4-step Discovery Flow |
| `.agents/brain/active_context_manifest.md` | Spatial Memory | This file; tracks active session and checkpoints |
| `.agents/skills/jules-knowledge/SKILL.md` | Skill | Compiled engineering knowledge, constraints, and architecture mappings |

---

## 3. Session Checkpoint & Next Steps

1. **Gatekeepers Updated:** Update the root `AGENTS.md` and document indices (`docs/index.md`, `README.md`, `llms.txt`) to refer to `.agents/AGENTS.md` and `docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md`.
2. **OKF Metadata Validation:** Execute `scripts/prepare_docs.py` to auto-format and apply OKF-compliant headers to newly created/edited files.
3. **Execution Safety Check:** Maintain strict local context lookup before executing any remote OpenTofu validation or server verification.
