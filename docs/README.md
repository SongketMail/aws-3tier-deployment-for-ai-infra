---
layout: "default"
okf_version: "0.1"
type: "Portal"
title: "Project Documentation Portal (Diátaxis Framework)"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "diataxis", "documentation", "portal"]
---
# Project Documentation Portal (Diátaxis Framework)

Welcome to the comprehensive technical documentation portal for our AWS Secure 3-Tier Infrastructure Lab!

To provide the highest quality information and ensure both developers and AI assistants can navigate our resources easily, this documentation system is structured according to the **Diátaxis Framework** (Tutorials, How-To Guides, Reference, and Explanation).

---

## Navigating by Diátaxis Quadrants

Choose the documentation style that matches your immediate goal:

### 🎓 [Tutorials](./tutorials/quickstart.html)
Guided, step-by-step lessons to help you learn our tools through execution.
* [Quickstart: Operating Project Utilities](./tutorials/quickstart.html)

### 📋 [How-To Guides](./how-to/manage-metadata.html)
Practical, task-oriented recipes to solve specific real-world problems.
* [How-To: Standardising Metadata](./how-to/manage-metadata.html)
* [How-To: Compiling LLM Curation Formats](./how-to/generate-llms-xml.html)

### 📘 [Reference Specs](./reference/prepare_docs.html)
Dry, structured technical details, parameters, API signatures, and CLI specifications.
* [Reference: prepare_docs.py Spec](./reference/prepare_docs.html)
* [Reference: parse_llms.py Spec](./reference/parse_llms.html)
* [Reference: Bash & PDF Scripts](./reference/bash_scripts.html)

### 🧠 [Explanations](./explanation/diataxis.html)
Discussions, design decisions, conceptual models, and deeper technical context.
* [Explanation: The Diátaxis Framework](./explanation/diataxis.html)
* [Explanation: Automation Architecture](./explanation/automation_architecture.html)

---

## Complete Core Architecture Library

Below is our extensive, role-based documentation library covering AWS multi-AZ deployments, local high-availability databases, containerized on-premises runbooks, and compliance audits:

* [System Architecture](./architecture.html) - Physical routing, VPC topologies, and subnets in the Malaysia region (`ap-southeast-5`).
* [AWS Phased Adoption Roadmap](./aws-adoption-roadmap.html) - Week-by-week, multi-year progression plan mapped from business milestones.
* [Disaster Recovery Options](./dr-options.html) - In-region and cross-region DR strategies (AWS DRS, Strategy E) and pricing in USD/MYR.
* [Load Testing Assumptions](./load-test-assumptions.html) - SLA metrics, performance bottlenecks, and sizing tiers from 100 to 10,000 VUs.
* [Strategic TCO Review](./aws-vs-self-hosted-review.html) - Exhaustive financial and operational comparison of AWS-managed platform vs. self-hosted on-premises setups.
* [Onsite On-Premises Portal](./onprem/index.html) - Unprivileged Podman containerization and Ansible orchestration blueprints.
* [Security Posture Assessment](./audits/security-posture-assessment.html) - Hardening scorecards, ASIMP, Lynis, and OpenSCAP compliance checklist.
