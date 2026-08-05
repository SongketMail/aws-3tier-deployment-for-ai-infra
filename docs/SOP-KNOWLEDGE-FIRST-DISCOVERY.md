---
layout: "default"
okf_version: "0.1"
type: "SOP"
title: SOP: Knowledge-First Discovery & Context Preservation Protocol
timestamp: 2026-08-05T21:51:00Z
topics: ["okf", "discovery", "context-management", "brain", "dsom", "SOP", "aws", "cloud"]
---
# 📚 SOP: Local Knowledge-First Discovery & OKF Context Protocol

## 1. Executive Intent
To prevent unnecessary API or CLI queries, remote SSH or Session Manager probes, token window exhaustion, and context loss during agentic sessions, all AI agents must strictly adhere to the **Local Knowledge-First Protocol**. All project facts, architecture details, subnet IPs, security rules, and costing options are documented locally via **OKF v0.1 YAML Frontmatter** inside `.agents/brain/` and `docs/`.

---

## 2. Standard Operating Procedure (4-Step Discovery Flow)

```
[ Step 1: User Request / Task ]
               │
               ▼
[ Step 2: Local OKF Search ] ──▶ search on .agents/brain/ & docs/ (using topics: or description:)
               │
               ▼
[ Step 3: Local Context Inspection ] ──▶ read_file target lines on matched .md files
               │
               ▼
[ Step 4: AWS Runtime Execution Gate ] (ONLY if live runtime state or deployment update is needed)
```

### Step 1: Local Frontmatter & Metadata Search
Before issuing any AWS CLI command, checking AWS SSM sessions, querying live OpenTofu state, or executing remote scripts against standalone EC2 or active ASG nodes:
1. Search local OKF frontmatter for relevant `topics:` or `description:` keywords:
   - Example: Search for "valkey" or "asg" or "postgres" or "dr-options" inside the local files to identify existing design guides and architectural layouts.
2. Read `.agents/brain/active_context_manifest.md` to see the current session checkpoints.

### Step 2: Targeted File Viewing
Once the relevant document is located via OKF frontmatter or titles:
- Read specific segments of the matched local file using `read_file` to keep the context window lean and avoid loading entire huge files unnecessarily.

### Step 3: Local Context Synthesis
Map the local specifications (e.g. `ap-southeast-5` regional defaults, instance sizes like `t4g.micro`, security groups ingress definitions) to the task at hand. The local repository is the **Single Source of Truth (SSOT)** for configuration intent.

### Step 4: AWS Runtime Execution Gate
Probing live AWS resources, executing OpenTofu plans, querying remote database ports, or starting SSM Session Manager connections are authorized **ONLY** when:
- Applying actual infrastructure or configuration updates (e.g., via `./scripts/deploy.sh`).
- Fetching actual live runtime telemetry (e.g., live database statistics or running target group health status) that cannot be modeled statically in documentation.

---

## 3. Mandatory Rules Reference
- **Rule 6 (OKF Topics):** All `.md` files must open on line 1 with `---` and contain `topics: [3-5 keywords]` and metadata.
- **Rule 10 (Metadata-First Discovery):** Read targeted file segments to preserve token efficiency.
- **Rule 29 (Local Knowledge-First Mandate):** Always exhaustively search local `.agents/brain/` and `docs/` before digging into remote servers or external web search.
