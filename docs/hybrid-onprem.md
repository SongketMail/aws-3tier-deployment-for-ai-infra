---
layout: default
title: "Hybrid Cloud Integration & Costing Guide"
---

# Hybrid Cloud Integration Guide: AWS & On-Premises

## 1. Executive Summary & Context

To support high-performance operations while maintaining strict cost-efficiency, organizations must determine the most practical strategy for connecting on-premises infrastructure (such as local datacenters, legacy compute, or private office environments) with an AWS-native deployment.

While AWS provides several enterprise-grade physical and virtual private network connectivity options, their upfront, monthly baseline, and data processing charges can be prohibitive for budget-conscious initiatives. Consequently, this guide presents a dual-layered architectural paradigm:
1. **Low-Cost, High-Flexibility Pathways (API and MCP):** The primary recommended choices for agile integrations, utilizing secure HTTP RESTful architectures and the newly released **Model Context Protocol (MCP)** for AI agentic workflows.
2. **Official AWS Hybrid Options (VPN, Direct Connect, and Transit Gateway):** Enterprise-standard private networking pipelines offered for comparative purposes to facilitate corporate security reviews and management approval.

All cost models are calibrated for the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** and estimated in both **United States Dollars (USD)** and **Malaysian Ringgit (MYR)**, utilizing a baseline conversion exchange rate of **1 USD ≈ 4.50 MYR**.

---

## 2. Low-Cost Option 1: Secure API-Based Connections

API-based hybrid integration leverages the public internet to transmit request/response payloads between AWS compute nodes (such as our Auto Scaling Groups or Standalone EC2 instances) and on-premises service endpoints. Rather than establishing a persistent, protocol-level network tunnel, communication is transactional, synchronous, or event-driven.

```
┌─────────────────┐       HTTPS REST / WebSockets        ┌───────────────────┐
│   AWS Cloud     │◄────────────────────────────────────►│    On-Premises    │
│ (Private VPC /  │       (TLS 1.3 + mTLS / Auth)        │  Server/Database  │
│  NAT Gateway)   │                                      │ (Internet-Exposed)│
└─────────────────┘                                      └───────────────────┘
```

### Architectural Implementation & Security
* **Authentication & Authorization:** Connections are secured via OAuth 2.0 Bearer tokens, Amazon Cognito, API Keys, or **Mutual TLS (mTLS)** supported natively by Amazon API Gateway.
* **Network Security & Whitelisting:** Downstream on-premises endpoints are configured to whitelist only the Elastic IP addresses of the AWS NAT Gateway. Inbound AWS traffic to the Application Load Balancer (ALB) is whitelisted at the AWS WAFv2 level or restricted to on-premises gateway IPs.
* **Protocol Support:** Standard REST (HTTPS/JSON) for point-to-point RPCs, or WebSockets (WSS) via Amazon API Gateway for persistent, low-latency bi-directional event streaming.

### Financial Breakdown
API-based connections have **no provisioned hourly costs** for physical line terminations. The billing is entirely pay-as-you-go based on data processing and network transit:
* **Amazon API Gateway REST APIs:** $3.50 per million requests (up to 333 million, with sliding volume discounts).
* **AWS NAT Gateway Charges:** $0.045 per hour base charge ($32.85/month) + $0.045 per GB of outbound data processed.
* **AWS Outbound Data Transfer (Internet Egress):** The first 100 GB per month is free. Beyond that, data transferred from AWS to the internet in Malaysia (`ap-southeast-5`) is charged at **$0.09 per GB**. On-premises data transfer into AWS is entirely free.

---

## 3. Low-Cost Option 2: AI-Native MCP-Based Connections

The **Model Context Protocol (MCP)** is an open-standard protocol designed to link Large Language Models (LLMs) securely with external data sources, content repositories, and enterprise applications. Instead of building bespoke API integrations for AI tools, MCP standardizes how AI agents discover and execute tools or fetch contextual files.

In December 2025, AWS introduced native **MCP Proxy Support in Amazon API Gateway**, integrated directly with **Amazon Bedrock AgentCore**. This allows organizations to transform on-premises applications, custom monitoring systems, or local databases into MCP-compatible endpoints without changing existing codebase patterns.

```
┌────────────────────────────────────────────────────────────────────────┐
│                              AWS VPC                                   │
│  ┌─────────────────┐       HTTPS/MCP       ┌──────────────────────┐    │
│  │ Amazon Bedrock  │◄─────────────────────►│  Amazon API Gateway  │    │
│  │   AgentCore     │                       │   (with MCP Proxy)   │    │
│  └─────────────────┘                       └──────────┬───────────┘    │
└───────────────────────────────────────────────────────┼────────────────┘
                                                        │ Secure HTTPS (Internet)
                                                        ▼ (mTLS / API Key)
                                             ┌──────────────────────┐
                                             │     On-Premises      │
                                             │   Local MCP Server   │
                                             └──────────────────────┘
```

### Architectural Implementation & Security
* **Protocol Translation:** On-premises systems host a lightweight "MCP Server" (e.g., exposing local postgres, CSV data, or SSH scripts). Amazon API Gateway's MCP Proxy translates incoming JSON-RPC 2.0 protocol payloads from AWS Bedrock Agents into standard secure HTTP requests that your local server processes.
* **Enterprise Security & Gateway Services:** Dual authentication is applied:
  1. **Inbound Verification:** Bedrock AgentCore validates the AI agent's credentials and authorization scopes before initiating requests.
  2. **Outbound Verification:** API Gateway manages secure connections, client certificates (mTLS), and API keys to call the on-premises REST endpoints.
* **Semantic Discovery:** Bedrock AgentCore Gateway allows AI agents to dynamically search and select the most relevant REST APIs that best match the context of the user's prompt.

### Financial Breakdown
* **Amazon Bedrock AgentCore Pricing:** Pay-as-you-go. (Refer to the official Amazon Bedrock AgentCore pricing page for updated regional rates).
* **API Gateway MCP Proxy Charges:** Treated as standard API Gateway REST API calls ($3.50 per million requests) with no additional platform premium.
* **Network Egress:** Standard AWS Data Transfer Out ($0.09/GB for ap-southeast-5 beyond the 100 GB free tier).

---

## 4. Official AWS Enterprise Hybrid Connections

For organizations requiring dedicated, low-latency, or highly secure private networking that completely bypasses the public internet, AWS offers three primary structural options.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                 AWS VPC                                  │
│  ┌───────────────────────┐            ┌───────────────────────────────┐  │
│  │ Virtual Private Gwy   │            │     Transit Gateway (TGW)     │  │
│  └──────────┬────────────┘            └───────────────┬───────────────┘  │
└─────────────┼─────────────────────────────────────────┼──────────────────┘
              │ IPSec VPN (Public Internet)             │
              ▼                                         │ Dedicated Physical Fiber
┌──────────────────────────┐                            ▼
│   AWS Site-to-Site VPN   │               ┌──────────────────────────┐
│  Est. $36.50/tunnel/mo   │               │    AWS Direct Connect    │
└──────────────────────────┘               │    Port fee + Partner    │
                                           └──────────────────────────┘
```

### Option A: AWS Site-to-Site VPN
* **Mechanism:** Establishes encrypted IPsec tunnels over the public internet between an AWS Virtual Private Gateway (VGW) / Transit Gateway and an on-premises firewall/router (Customer Gateway).
* **Bandwidth:** Up to 1.25 Gbps per active tunnel (with ECMP support to group multiple tunnels for higher throughput).
* **Costing:**
  * **AWS Connection Fee:** **$0.05 per hour** per active VPN connection ($36.50 per month per site).
  * **On-Premises Hardware:** Requires a physical VPN appliance (Cisco, Juniper, Fortinet) or open-source software (StrongSwan, pfSense) on-premises.
  * **Data Transfer Out:** Charged at standard AWS Data Transfer Out rates ($0.09 per GB in `ap-southeast-5`).

### Option B: AWS Direct Connect (DX)
* **Mechanism:** A physical, dedicated, high-speed fiber-optic connection from an on-premises datacenter to an AWS Direct Connect Location. Complete bypass of the public internet.
* **Bandwidth:** Fixed port speeds of 1 Gbps, 10 Gbps, or 100 Gbps (Sub-1G connections are available via AWS Direct Connect Partners).
* **Costing:**
  * **AWS Port Hour Charge:** **$0.03 per hour** for 1 Gbps ports (~$21.90/mo) or **$2.25 per hour** for 100 Gbps ports (~$1,642.50/mo).
  * **Data Transfer Out:** Significantly lower than standard internet egress. Direct Connect Data Transfer Out is charged at a highly discounted rate of **$0.021 to $0.041 per GB** (region-dependent).
  * **Partner Telecommunication Costs:** Third-party telco providers charge monthly circuit fees to run fiber from your office to the AWS Direct Connect Point of Presence (PoP) (ranging from $500 to $5,000+ per month).

### Option C: AWS Transit Gateway (TGW)
* **Mechanism:** Acts as a centralized cloud router that simplifies hybrid network topology by interconnecting multiple AWS VPCs, Site-to-Site VPNs, and Direct Connect links through a single logical gateway.
* **Costing:**
  * **AWS Attachment Charge:** **$0.05 per hour** per VPC, VPN, or DX attachment (~$36.50 per month per attachment).
  * **Data Processing Fee:** **$0.02 per GB** for all data passing through the Transit Gateway.

---

## 5. Side-by-Side Hybrid Technology Matrix

| Evaluation Criteria | API-Based Connections | MCP-Based Connections | AWS Site-to-Site VPN | AWS Direct Connect |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Use Case** | Lightweight microservices, Webhooks, database queries | AI Agents, tool calling, Bedrock LLM retrieval | General corporate network extension, secure admin | High-performance, bulk data transfer, hybrid DBs |
| **Underlying Network** | Public Internet (Secure TLS) | Public Internet (Secure TLS / mTLS) | Encrypted IPsec Tunnel over Public Internet | Dedicated, private, physical fiber-optic line |
| **Max Throughput** | Limited only by internet connection | Limited only by internet connection | 1.25 Gbps per active tunnel | 1 Gbps to 100 Gbps (dedicated) |
| **Latency Profile** | Variable (reliant on internet ISP) | Variable (reliant on internet ISP) | Stable, moderate (internet routing) | Ultra-low, deterministic, and SLA-backed |
| **Network Security** | Application Layer (TLS, JWT, Mutual TLS) | Application Layer (mTLS, IAM, API Key, Bedrock Core) | Network Layer (IPsec VPN encryption) | Physical Layer isolation (Direct Connect MACsec opt) |
| **Integration Complexity**| Low (Standard HTTP development) | Low-to-Medium (REST config, Bedrock alignment) | Medium (Network routing, IPSec configuration) | High (Requires telco provider physical provisioning) |
| **Implementation Lead Time**| Instant | Instant | Hours | 30 to 90 Days (Telco fiber pull) |
| **AWS Billing Model** | Pay-as-you-go ($3.50/M requests + DTO) | Pay-as-you-go + standard API gateway rates | Hourly ($0.05/hr) + Data Transfer Out | Hourly Port ($0.03-$2.25/hr) + Partner Loop + DTO |
| **Upfront Capital Cost**| **$0.00** | **$0.00** | **$0.00** (using existing router) | **$1,000 - $5,000+** (Hardware, cross-connects) |

---

## 6. Granular Monthly Hybrid Cost Estimations

To assist leadership in budget selection, we model monthly costs based on two enterprise traffic volumes:
1. **Low-Volume Integration (10 GB Outbound Data Transfer + 1 Million Requests / Month)**
2. **High-Volume Integration (500 GB Outbound Data Transfer + 10 Million Requests / Month)**

All estimates assume deployment in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)** with standard regional rates.

### Scenario A: Low-Volume Integration Cost Modeling (10 GB Outbound / 1M Requests)

This represents an agile staging environment, internal dev tools, or an experimental AI agentic system integrating on-premises files.

```
┌────────────────────────────────────────────────────────────────────────┐
│             Low-Volume Scenario Total Monthly Cost (USD)               │
│                                                                        │
│ API-Based    │ $3.50                                                   │
│ MCP-Based    │ $3.50                                                   │
│ S2S VPN      │ $36.50                                                  │
│ Direct Conn. │ $521.90                                                 │
└────────────────────────────────────────────────────────────────────────┘
```

#### 1. API-Based Connections
* **API Gateway REST Processing:** 1,000,000 requests * $3.50/M = $3.50 USD
* **AWS Data Transfer Out (Egress):** 10 GB (Within free tier threshold of 100 GB) = $0.00 USD
* **NAT Gateway Hourly Fee (Existing):** Shared with existing infrastructure = $0.00 USD
* **TOTAL MONTHLY COST:** **$3.50 USD / ~RM 15.75 MYR**

#### 2. MCP-Based Connections
* **API Gateway with MCP Proxy:** 1,000,000 requests * $3.50/M = $3.50 USD
* **AWS Data Transfer Out (Egress):** 10 GB (Within free tier threshold of 100 GB) = $0.00 USD
* **Bedrock AgentCore Platform Fee:** Pay-as-you-go nominal charges = $0.00 USD (Approx)
* **TOTAL MONTHLY COST:** **$3.50 USD / ~RM 15.75 MYR**

#### 3. AWS Site-to-Site VPN
* **AWS VPN Connection Charge:** 1 tunnel * 730 hours/month * $0.05/hr = $36.50 USD
* **AWS Data Transfer Out (Egress):** 10 GB (Within free tier threshold of 100 GB) = $0.00 USD
* **On-Premises Router Power/Compute:** Nominal standard overhead = $0.00 USD
* **TOTAL MONTHLY COST:** **$36.50 USD / ~RM 164.25 MYR**

#### 4. AWS Direct Connect (DX)
* **AWS 1 Gbps Port Charge:** 730 hours/month * $0.03/hr = $21.90 USD
* **Discounted Data Transfer Out (Egress):** 10 GB * $0.041/GB = $0.41 USD
* **Partner Local Loop Circuit:** Sub-1G Partner line (Est. Baseline Partner Fee) = $500.00 USD
* **TOTAL MONTHLY COST:** **$522.31 USD / ~RM 2,350.40 MYR**

---

### Scenario B: High-Volume Integration Cost Modeling (500 GB Outbound / 10M Requests)

This represents active production workloads, automated ETL syncs, enterprise-wide chat agents, or heavy file replication.

```
┌────────────────────────────────────────────────────────────────────────┐
│            High-Volume Scenario Total Monthly Cost (USD)               │
│                                                                        │
│ API-Based    │ $71.00                                                  │
│ MCP-Based    │ $71.00                                                  │
│ S2S VPN      │ $72.50                                                  │
│ Direct Conn. │ $542.40                                                 │
└────────────────────────────────────────────────────────────────────────┘
```

#### 1. API-Based Connections
* **API Gateway REST Processing:** 10,000,000 requests * $3.50/M = $35.00 USD
* **AWS Data Transfer Out (Egress):** (500 GB - 100 GB Free) = 400 GB * $0.09/GB = $36.00 USD
* **TOTAL MONTHLY COST:** **$71.00 USD / ~RM 319.50 MYR**

#### 2. MCP-Based Connections
* **API Gateway with MCP Proxy:** 10,000,000 requests * $3.50/M = $35.00 USD
* **AWS Data Transfer Out (Egress):** (500 GB - 100 GB Free) = 400 GB * $0.09/GB = $36.00 USD
* **Bedrock AgentCore Platform Fee:** Pay-as-you-go nominal charges = $0.00 USD (Approx)
* **TOTAL MONTHLY COST:** **$71.00 USD / ~RM 319.50 MYR**

#### 3. AWS Site-to-Site VPN
* **AWS VPN Connection Charge:** 1 tunnel * 730 hours/month * $0.05/hr = $36.50 USD
* **AWS Data Transfer Out (Egress):** (500 GB - 100 GB Free) = 400 GB * $0.09/GB = $36.00 USD
* **TOTAL MONTHLY COST:** **$72.50 USD / ~RM 326.25 MYR**

#### 4. AWS Direct Connect (DX)
* **AWS 1 Gbps Port Charge:** 730 hours/month * $0.03/hr = $21.90 USD
* **Discounted Data Transfer Out (Egress):** 500 GB * $0.041/GB = $20.50 USD
* **Partner Local Loop Circuit:** Sub-1G Partner line (Est. Baseline Partner Fee) = $500.00 USD
* **TOTAL MONTHLY COST:** **$542.40 USD / ~RM 2,440.80 MYR**

---

## 7. Strategic Recommendation & Management Decision Tree

To guide management through the selection process, we present a logical decision matrix to streamline technical approval:

```
                      Do you require physical isolation
                     and deterministic network latency?
                                  │
                   ┌──────────────┴──────────────┐
                   │ YES                         │ NO
                   ▼                             ▼
        ┌─────────────────────┐       Are you integrating AI Agents
        │ AWS Direct Connect  │       to access on-premise tools/data?
        │ (Enterprise Budget) │                  │
        └─────────────────────┘       ┌──────────┴──────────┐
                                      │ YES                 │ NO
                                      ▼                     ▼
                           ┌─────────────────────┐  Do you need network-level
                           │  MCP-Based API Gateway  │  encryption/access for
                           │    (Ultra-Low Cost) │  all on-premises servers?
                           └─────────────────────┘          │
                                                  ┌─────────┴─────────┐
                                                  │ YES               │ NO
                                                  ▼                   ▼
                                       ┌─────────────────────┐┌──────────────┐
                                       │ AWS Site-to-Site    ││ API-Based    │
                                       │ VPN Connection      ││ Connection   │
                                       └─────────────────────┘└──────────────┘
```

### Actionable Roadmap for Approvals

1. **Phase 1: Zero-Upfront Trial (API / MCP)**
   * **Recommendation:** Begin with **API-based or MCP-based connections**. It requires $0 in capital expenditure, zero hardware setups on-premises, and allows the AI team to immediately utilize Bedrock AgentCore and local datasets.
   * **Security Action:** Restrict access to the on-premise MCP server by whitelisting the AWS NAT Gateway Elastic IP and enforcing API key rotation.

2. **Phase 2: Hybrid Network Scaling (Site-to-Site VPN)**
   * **Trigger:** If corporate security mandates network-level segmentation (e.g., preventing any endpoint from exposing port 443 to the public internet, even with whitelists), transition to **AWS Site-to-Site VPN**.
   * **Cost Impact:** Adds a modest **$36.50/month (RM 164.25)** flat connection charge plus standard outbound data transfer.

3. **Phase 3: Ultimate Performance (Direct Connect)**
   * **Trigger:** If synchronization volumes exceed **10 TB / month** or latency constraints require single-digit millisecond response times.
   * **Cost Impact:** Heavy capital and partner operating expenditures (RM 2,400+ / mo). Highly discounted AWS egress rates make Direct Connect financially viable only at extreme data transfer volumes.
