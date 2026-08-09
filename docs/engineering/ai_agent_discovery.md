---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Explicit AI Agent Data Flow Mapping"
timestamp: 2026-08-09T14:00:00Z
topics: ["devops", "engineering", "ai-agents", "mTLS", "security", "zero-trust"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>

# 🤖 Explicit AI Agent Data Flow Mapping & Handshake Protocol

This runbook establishes the technical architecture, zero-trust network topology, and persistent storage mechanics supporting external **Google Antigravity** and **Google Jules** AI agents executing Knowledge-First Discovery Protocols within our secure AWS 3-tier environment.

---

## 🧭 1. Tracing the "VIP Guest" Network Trajectory

When an authorized external Google AI Agent initiates a Knowledge-First Discovery query, it is treated as a **VIP Guest**. The agent's query follows a strictly isolated, end-to-end encrypted, and highly monitored network trajectory from the public edge down to the private storage layers:

$$\text{WAF v2 / ALB Edge} \longrightarrow \text{API Gateway MCP Proxy} \longrightarrow \text{Private Subnet RAGFlow ASG} \longrightarrow \text{EFS Model Cache / RDS pgvector}$$

### 🗺️ High-Fidelity Network Routing Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                               VIP GUEST NETWORK LIFE-CYCLE                               │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  [Google Antigravity / Jules Agent] (External / Client)                                  │
│                 │                                                                        │
│                 │ (1) Public HTTPS & Mutual TLS (mTLS) Handshake on Port 443              │
│                 ▼                                                                        │
│       [WAF v2 / ALB Edge] (Public Ingress Subnet)                                        │
│                 │                                                                        │
│                 │ (2) Forward validated HTTP traffic                                     │
│                 ▼                                                                        │
│      [API Gateway MCP Proxy] (Private VPC Integration / Lambda Translator)               │
│                 │                                                                        │
│                 │ (3) IAM Role Translation & JSON-RPC to MCP Handshake                   │
│                 ▼                                                                        │
│     [RAGFlow ASG App Nodes] (Private Compute Subnet / g5.xlarge GPU)                     │
│          │                 │                                                             │
│          │ (4a) Read Cache │ (4b) Query Vectors on Port 5432                             │
│          ▼                 ▼                                                             │
│    [Amazon EFS]     [Amazon RDS pgvector] (Private Database Subnet)                      │
│   (Model Weights)    (Multi-AZ Write Master / Read Replicas)                             │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 🛰️ Trajectory Step Breakdown
1. **Edge Entry (WAF v2 / ALB Edge):** The external agent connects to our public edge. AWS WAF v2 filters out malicious payloads (SQL injections, prompt injection variations, and DDoS floods), while the ALB Custom Domain handles the initial cryptographic handshake.
2. **Access Control (API Gateway MCP Proxy):** The request is routed to an Amazon API Gateway instance configured with a private integration. This layer acts as the **Model Context Protocol (MCP) Proxy**.
3. **Private Compute Processing (RAGFlow ASG):** The API Gateway proxy safely delegates the request across the Auto Scaling Group (ASG) compute instances running RAGFlow in the private subnets. Traffic travels exclusively over internal AWS network paths.
4. **Data Retrieval (EFS & RDS pgvector):** The RAGFlow application queries the Multi-AZ Amazon RDS PostgreSQL instance on port 5432 to search vectorized data while referencing the local EFS mount to load pre-cached transformer weights.

---

## 🤝 2. Documenting the Zero-Trust Handshake Protocol

To prevent unauthorized access to private database subnets, an external AI agent must complete a multi-layered **Zero-Trust Handshake** consisting of mTLS authentication, IAM validation, and payload translation:

```
  External Agent              WAFv2 / ALB Edge             API Gateway / MCP           RDS / EFS
        │                            │                            │                        │
        │ ── (1) mTLS Handshake ───▶ │                            │                        │
        │ ◀── (2) Cert Validated ─── │                            │                        │
        │                            │                            │                        │
        │ ────────────────────── (3) Invoke POST /mcp ──────────▶ │                        │
        │                            │                            │                        │
        │                            │                            │ ─ (4) IAM AssumeRole ─┐│
        │                            │                            │ ◀── (STS Credentials)─┘│
        │                            │                            │                        │
        │                            │                            │ ── (5) Query Backend ─▶│
```

### 🔐 A. Mutual TLS (mTLS) Authentication
1. **X.509 Certificate Exchange:** The external agent is provisioned with a cryptographic X.509 client certificate generated by an enterprise-managed private Certificate Authority (CA) in AWS Private CA.
2. **Edge Validation:** API Gateway Custom Domains or ALB Custom Listeners enforce mutual TLS. If the certificate is missing, expired, or not signed by our specific truststore (stored securely in an S3 bucket), the connection is terminated instantly at the perimeter.

### 🔑 B. IAM Roles and Identity Federation
* **Role Assume (`AIAgentDiscoveryRole`):** Once mTLS completes, the authenticated certificate's Distinguished Name (DN) is mapped to a specific AWS IAM Role (`AIAgentDiscoveryRole`) using AWS IAM Roles Anywhere.
* **Least Privilege Policy:** The assumed IAM Role grants zero direct access to database subnets. Instead, it contains a highly restrictive policy allowing **only** the `execute-api:Invoke` permission on specific HTTP POST endpoints of the MCP proxy API.

### 📝 C. API Gateway Model Context Protocol (MCP) Translation
* **Protocol Bridging:** Google Antigravity agents communicate using standard JSON-RPC payloads defined by the open Model Context Protocol (MCP).
* **Lambda Translation Layer:** An AWS Lambda function integrated with the API Gateway intercepts the MCP query, parses the JSON-RPC syntax, sanitizes input variables, and translates it into standard gRPC or HTTPS API requests targeting RAGFlow in the private subnet.
* **Result Isolation:** The database tier never sees the external agent directly. The RDS database subnets remain completely isolated, responding only to local SQL or `pgvector` index queries initiated by the local RAGFlow instances.

---

## ⚡ 3. Preventing Cold Starts via EFS Context Loading

AI and LLM operations are notoriously prone to high **cold start latency** due to the size of deep learning model weights. If a new node in the RAGFlow Auto Scaling Group (ASG) spins up to handle a surge in agent discovery requests, downloading gigabytes of model weights from S3 or external repositories can cause response times to spike, violating our strict SLAs.

To solve this, our architecture leverages **Amazon EFS (Elastic File System)** as a persistent shared model cache:

```
                         ┌─────────────────────────────────┐
                         │    EFS Shared Model Cache       │
                         │  (SentenceTransformers/BGE-M3)  │
                         └─────────────────────────────────┘
                                   │            │
             ┌─────────────────────┘            └─────────────────────┐
             │ (Local NFS Mount)                      │ (Local NFS Mount)
             ▼                                        ▼
┌─────────────────────────┐              ┌─────────────────────────┐
│  RAGFlow ASG Node #1    │              │  RAGFlow ASG Node #2    │
│  (Startup: 15 seconds)  │              │  (Startup: 15 seconds)  │
└─────────────────────────┘              └─────────────────────────┘
```

### ⚙️ How EFS Context Loading Works
1. **Pre-caching Pipeline:** During the initial staging phase, the complete suite of Hugging Face embedding models (such as `BAAI/bge-m3`) and SentenceTransformers weights are pre-downloaded and stored in a dedicated folder `/var/www/shared/models` on the Amazon EFS volume.
2. **Boot-Time Mounting:** When the ASG provisions a new g5.xlarge GPU instance, the systemd initialization script mounts the EFS filesystem immediately using standard high-performance NFSv4 options.
3. **Instantaneous Memory Loading:** Because the model weights are already present locally on the mounted filesystem, RAGFlow bypasses all external network fetches and reads the model weights into GPU memory over AWS's local 10Gbps EFS network interface.
4. **SLA Protection:** Startup-to-readiness latency drops from **10+ minutes** (S3 pull + dependency resolution) to **under 15 seconds**, ensuring seamless auto-scaling execution under heavy agentic query volumes.

---

## 📋 4. Report Optimization Summary Checklist

The table below summarizes the completed optimization actions across our modularized documentation volumes. These enhancements ensure maximum structural isolation, high-fidelity visual formatting, chronological roadmapping, robust AI mechanics, and dual-currency compliance.

| Category | Optimization Action | Status / Target | Realized Technical Impact |
| :--- | :--- | :---: | :--- |
| **Structure** | Separate Executive Financials ($92,509.78 USD / RM 416,294.01 MYR) from DevOps terminal execution scripts. | **[x] Completed** | Executive-level strategic files are now completely isolated under `docs/executive/`, separating business risk/TCO from SRE-level system scripts in `docs/engineering/`. |
| **Formatting** | Use visual metadata badges ([STRATEGIC FINANCIAL], [DEVOPS EXECUTION]) on all modules. | **[x] Completed** | Distinct CSS classes (`.arch-badge-strategic`, `.arch-badge-devops`, `.arch-badge-security`) are now hardcoded at the top of all new files to route readers to relevant topics instantly. |
| **Roadmap** | Link $112.00 USD/mo (≈ RM 504.00 MYR/mo) AWS DRS and hybrid connection costs directly to CRM Go-Live dates. | **[x] Completed** | AWS Elastic Disaster Recovery (AWS DRS) costs ($112.00 USD/mo ≈ RM 504.00 MYR/mo) and AWS Site-to-Site VPN connection costs ($36.00 USD/mo ≈ RM 162.00 MYR/mo) are mapped directly to Phase 3 CRM Go-Live (Weeks 53–60). |
| **AI Mechanics** | Draw explicit network lines showing Google AI Agent mTLS / IAM handshakes into private subnets. | **[x] Completed** | Documented a comprehensive, step-by-step mTLS client certificate verification flow, AWS IAM Roles Anywhere validation, and JSON-RPC to MCP Lambda proxy translation. |
| **Currency** | Consistently present financial figures with dual USD and MYR figures (@ 4.50 MYR/USD exchange rate). | **[x] Completed** | All budgets, operating costs, and savings projections are explicitly calculated in both USD and MYR utilizing the baseline exchange rate of exactly $1.00 USD = RM 4.50 MYR. |

---

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
