---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Software Licensing & Technology Risk Register (TS/MC Series)"
timestamp: 2026-08-05T23:30:00Z
topics: ["aws", "cloud", "architecture", "licensing", "compliance", "siem", "wazuh", "qwen3", "bedrock", "langchain4j", "ragflow", "langfuse", "costing"]
---
# Software Licensing & Technology Risk Register (TS/MC Series)

This guide establishes the official **Software Licensing & Technology Risk Register (TS/MC Series)** for our AWS Secure 3-Tier Architecture. It documents the core architectural decisions, commercial/open-source licensing assessments, and operational risks associated with our enterprise-grade web and AI infrastructure.

By classifying key software and AI model components under the **TS (Technology Stack)** and **MC (Model Consumption)** series, we ensure complete traceability, clear ownership of technical risk, and alignment with regulatory standards such as the **Malaysian Personal Data Protection Act (PDPA) 2010**.

---

## 🏛️ 1. Technology Stack (TS Series) Registry

The TS Series identifies, tracks, and manages the licensing risks and operational models of software components deployed across our 3-tier architecture.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TS SERIES RISK REGISTER                         │
├─────────┬──────────────────────────────┬──────────────┬────────────────┤
│ ID      │ Component                    │ Risk Level   │ Action Taken   │
├─────────┼──────────────────────────────┼──────────────┼────────────────┤
│ TS-02   │ LangChain4j Framework        │ Medium-Low   │ Accepted Risk  │
│ TS-04   │ Wazuh SIEM Self-Hosting      │ Low          │ Budget Savings │
│ TS-05   │ Software Licensing Framework │ Low          │ Audit Standard │
│ TS-06   │ Self-hosted DB & AI Ops      │ Medium       │ Internal Option│
└─────────┴──────────────────────────────┴──────────────┴────────────────┘
```

### 📋 TS-02: LangChain4j Integration & SLA Risk
* **Classification:** AI Integration Layer
* **Licensing Profile:** Apache License 2.0 (Highly permissive open-source)
* **Risk Context:** LangChain4j lacks an official commercial Service Level Agreement (SLA) or vendor-backed corporate support structure.
* **Risk Evaluation & Accepted Risk:**
  - **The Risk:** In the event of critical framework bugs, security vulnerabilities (CVEs), or breaking API changes by downstream LLM providers, there is no contractually bound vendor to provide emergency patches or guarantee response times.
  - **Why the Risk is Accepted:** LangChain4j is the de facto standard for building AI/LLM applications in the Java ecosystem (supporting Java 21, Spring Boot 3.5.12, and Spring Security 6.x natively). It has a highly active, robust open-source community, wide enterprise adoption, and regular release cycles.
  - **Mitigation Strategy:**
    1. **Forking Strategy:** Maintain an internal git fork of the specific LangChain4j version in use to allow local patch application independent of upstream releases if needed.
    2. **Dependency Pinning:** Pin dependency versions in Maven `pom.xml` to prevent automated, untested minor/patch version upgrades.
    3. **Abstraction Layer:** Use clean interface abstractions in our Java code so that the underlying LLM orchestration framework can be swapped or modified with minimal business logic disruption.

### 📋 TS-04: Standalone Wazuh SIEM Hosting
* **Classification:** Enterprise Security & Compliance
* **Licensing Profile:** GPL v3 (GNU General Public License)
* **Risk Context:** Replaces traditional, high-cost third-party SaaS commercial SIEM subscriptions with a standalone self-hosted instance in AWS.
* **Cost & Budget Impact:**
  - By deploying Wazuh on a dedicated, hardened AWS Graviton ARM64 instance (`t4g.large`), we eliminate the vendor markup fees and per-GB ingestion surcharges common in SaaS SIEM models.
  - This replaces the "vendor SIEM" budget line item under Security, **reducing monthly operational costs by over 57%** (operating at approx. **$65.71 USD / RM 295.70 MYR per month** on Graviton, compared to $153+ USD/month on legacy x86 setups).
* **Mitigation Strategy:**
  - Standardise security configurations, restrict public internet access (restrict port 22 and 443 strictly to Cyberjaya developer CIDRs), and backup OpenSearch/Wazuh indexer directories using automated **AWS Backup** schedules.

### 📋 TS-05: Technology Stack Software & Licensing Framework
* **Classification:** Corporate Compliance & Licensing Audit
* **Licensing Profile:** Governance Framework
* **Context:** Manages open-source and commercial software compliance across the entire 3-tier system to prevent licensing contamination (e.g. copyleft license leakage into proprietary backend code).
* **Compliance Actions:**
  - Restrict production runtimes to permissive licenses such as **Apache 2.0, MIT, and BSD**.
  - Restrict the introduction of AGPL or strong copyleft licenses in the backend API layer.
  - Maintain a dynamic **Software Bill of Materials (SBOM)** generated during GitHub Actions and GitLab CI/CD build phases to automatically flag compliance anomalies.

### 📋 TS-06: Self-hosted Database Operations (Internal Option)
* **Classification:** Storage & In-House Data Management
* **Licensing Profile:** Open-Source Permissive / Dual-Licensing (PostgreSQL License, BSD-3, Apache 2.0)
* **Risk Context:** Running databases (PostgreSQL, Valkey/Redis) and AI orchestrators (Langfuse, RAGFlow) in-house as self-hosted containers/instances rather than relying on commercial SaaS database vendors.
* **Trade-Off Analysis:**
  - **Benefits:** Complete operational control, zero third-party data transit risk, and elimination of premium SaaS database pricing tiers.
  - **Sovereignty Aligned:** Keeps sensitive AI session telemetry, prompt logs, and document vectors strictly localized within our private subnets in the AWS Malaysia (`ap-southeast-5`) region, satisfying strict local PDPA data residency mandates.
* **Mitigation Strategy:**
  - Map self-hosted designs directly to managed **Amazon RDS PostgreSQL (Multi-AZ with pgvector)** and **Amazon ElastiCache for Valkey** for production workloads, while retaining containerized self-hosted setups as a cost-optimized "Internal Option" for development and local testing.

---

## 🧠 2. Model Consumption (MC Series) Registry

The MC Series governs how foundational AI models (LLMs, embedding engines) are consumed, focusing on cost efficiency, data residency, and performance optimisation.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MC SERIES RISK REGISTER                         │
├─────────┬──────────────────────────────┬──────────────┬────────────────┤
│ ID      │ Component                    │ Optimization │ Sovereign Gate │
├─────────┼──────────────────────────────┼──────────────┼────────────────┤
│ MC-01   │ Qwen3 LLM Inference          │ Serverless   │ Bedrock Private│
│ MC-02   │ Qwen3 Embed, Index & Query   │ One-time/Low │ Batch/Cached   │
└─────────┴──────────────────────────────┴──────────────┴────────────────┘
```

### 🤖 MC-01: Qwen3 LLM Inference via Amazon Bedrock
* **Classification:** Large Language Model (LLM) Inference
* **Consumption Model:** Serverless API / Provisioned Throughput
* **Architectural Flow:**
  - All conversational queries, reasoning loops, and prompt chains are processed using the state-of-the-art **Qwen3 LLM** (or equivalent highly-optimised multilingual models) running natively within **Amazon Bedrock**.
* **Sovereignty & Compliance Mapping:**
  - By routing Qwen3 model inference directly through Amazon Bedrock, all prompt payloads, context windows, and generated tokens are processed entirely within secure, private AWS regional boundaries (`ap-southeast-5`).
  - This eliminates data leakage risks associated with routing sensitive corporate information over the public internet to external, third-party AI startups. It provides a clean, audit-ready compliance path for Transfer Impact Assessments (TIAs) under PDPA guidelines.

### 🤖 MC-02: Qwen3 Embedding, Indexing, and Query Optimisation
* **Classification:** Dense Vector Search & Retrieval-Augmented Generation (RAG)
* **Consumption Model:** Static Ingestion + Low Ongoing Query Costs
* **Operational Profile:**
  - **Static Documents (One-time Sweep):** Ingest static corporate documents, technical manuals, and knowledge bases using a high-density, one-time embedding sweep using Qwen3 Embedding models.
  - **Storage:** Store the generated high-dimensional dense vectors in **Amazon RDS PostgreSQL (`pgvector`)** or a secure vector index.
  - **Ongoing Querying (Low Cost):** Since the foundational document corpus is static, ongoing daily operational costs are limited to the tiny vector queries processed during user searches, keeping the average API charge extremely low.
* **Optimisation Lever:**
  - Utilize batch processing for bulk document ingestion during off-peak hours to take advantage of lower pricing tiers and prevent compute thread saturation in the main Spring Boot application ASG.

---

## 🔒 3. Enterprise Governance & Action Items

To maintain a secure compliance posture, the engineering team must execute the following action items regularly:

1. **Conduct Licensing Sweeps (Quarterly):** Run automated Maven and npm dependency license audits to ensure no copyleft components have bypassed the TS-05 licensing framework.
2. **Review LangChain4j Versions (Monthly):** Audit the active LangChain4j fork for security patches and ensure any local overrides are documented under the TS-02 risk mitigation log.
3. **Optimise Bedrock API Allocations (Daily):** Monitor Amazon CloudWatch metrics for Bedrock API invocation counts and token usage to identify opportunities for prompt caching and further lower MC-01/MC-02 ongoing costs.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
