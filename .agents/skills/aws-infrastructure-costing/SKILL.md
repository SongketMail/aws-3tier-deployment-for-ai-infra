---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "AWS Infrastructure Costing Skill"
timestamp: 2026-08-05T22:00:00Z
topics: ["aws", "cloud", "architecture", "skill", "costing", "budget", "pricing", "exchange-rate", "load-testing", "tco"]
description: "Guidelines and instructions for managing and evaluating AWS infrastructure costing models, baseline optimizations, and enterprise high-performance estimations."
name: "aws-infrastructure-costing"
---
# AWS Infrastructure Costing Skill

This skill governs the financial planning, budget constraints, TCO analysis, and cost breakdowns of the AWS 3-tier architecture.

---

## 1. Baseline Cost-Optimised Plan (~$426.75 USD/mo)

The baseline plan is optimized for development, staging, and small-scale deployments in the `ap-southeast-5` (Malaysia) region:
- **Networking & VPC:** Uses a single NAT Gateway (~$32.85 USD/mo) and public/private subnets.
- **Compute (Web/App ASG & Standalone):** Employs Graviton-based `t4g.micro` instances.
- **Database (RDS):** Deploys a single RDS `db.t4g.micro` instance (~$12.50 USD/mo).
- **Caching (ElastiCache):** Leverages `cache.t4g.micro` Valkey (~$9.34 USD/mo).
- **Management & DNS:** Includes secure SSH Jumphost Bastion (~$10.98 USD/mo) and Route 53 hosting & query costs (~$1.30 USD/mo).

---

## 2. High-Performance Enterprise Plan (~$1,064.46 USD/mo)

Designed for mission-critical, highly available production workloads:
- **High Availability Networking:** Dual NAT Gateways spanning multiple Availability Zones (~$65.70 USD/mo) to eliminate single points of failure.
- **Clustered Compute:** Employs larger Graviton instance classes (`t4g.medium` or `c7g.large`) and robust auto-scaling triggers.
- **Database (RDS Multi-AZ):** Deploys Multi-AZ `db.t4g.medium` PostgreSQL instances with high-IOPS gp3 storage (~$140 USD/mo).
- **Caching Layer:** Clustered Valkey nodes with high availability.

---

## 3. Financial Prudence, Sizing Guidelines & Exchange Rates

- **Standard Currency Exchange Rate:** The standardized repository-wide baseline exchange rate for all local currency conversions in the documentation is exactly **$1.00 USD = MYR 4.50**. All financial figures, monthly tier costing tables, phase budgets, and multi-year TCO summaries across all pages are calculated using this reference (as per **Item 40**).
- **Load Testing Sizing Models:** The Load Testing Assumptions & Sizing Guide (`docs/load-test-assumptions.md`) defines multi-VU sizing models from 100 to 10,000 VUs with associated USD/MYR costing models (as per **Item 42**).
- **Interpolated 1,000 VU Sizing Tier:** This tier bridges the gap between the 500 VU and 2,500 VU environments, architected with 2-3x `t4g.xlarge` ASG nodes, Multi-AZ `db.m6g.xlarge` database engine, 1x `cache.t4g.medium` Valkey caching node, with an estimated monthly budget of ~$700.00 USD (RM 3,150.00 MYR) (as per **Item 22**).
- **Cost-to-Performance Capability Mapping:** Bridges the gap between financial plans and operational limits, mapping each environment budget tier (including the interpolated Load-Test 1,000 VU Sizing, Dev/POC, Baseline, Staging, Developer-Aligned, and Enterprise Production) directly to maximum concurrent Virtual Users (VUs), Web/API throughput (RPS), database transactional throughput (TPS), and RAG/AI ingestion capacities without modifying original cost figures (as per **Item 23**).
- **36-Month Timeline Costing:** Details a 36-month timeline mapped to phase-by-phase AWS scaling and includes a combined 36-month financial projection of $47,709.78 USD (≈ RM 214,694.01 MYR) in AWS infrastructure costs and a refined non-AWS operational costing of $44,800.00 USD (≈ RM 201,600.00 MYR) covering software subscriptions, licensing compliance, yearly SPA, load testing, and AWS on-call support (as per **Item 39**).
- **Strategic Comparative Review:** Delivers a high-fidelity architectural, operational, and financial TCO (1-year and 3-year) comparison between an AWS-Native Managed Platform and a Self-Hosted Custom Stack within the Malaysia region (as per **Item 26**).
- **Pristine Markdown Costing Formatting:** The costing report documentation in `docs/costing.md` has been cleaned up to use standard, universally supported Markdown formatting (with direct dollar signs '$', unicode '≈' and '×' signs, and native code blocks) instead of LaTeX/MathJax syntax (like $...$ or $$...$$) to ensure pristine, error-free HTML rendering in Jekyll and GitHub Pages (as per **Item 47**).

---

## 4. Enterprise AI Cost Audit & Native Alternatives

- **AWS ap-southeast-5 Enterprise AI Cost Audit:** Section 7 of `docs/costing.md` contains an official AWS 3-Tier AI Infrastructure Cost Audit & Verification Report for Enterprise RAG/AI workloads (RAGFlow, Langfuse, Valkey, PostgreSQL + pgvector). It breaks down Dev/POC, Staging, and Production tier costing, defines formulas for hidden NAT Gateway charges, details hidden cost traps (IPv4 surcharges, cross-AZ transfers, ALB LCUs), and establishes optimization levers (Savings Plans, Reserved Instances, Valkey adoption, automated non-prod schedules, PrivateLink S3 endpoints) (as per **Item 48**).
- **AWS-Native Alternatives Costing:** The costing guide includes detailed monthly costing calculations in both USD and MYR for AWS-native enterprise-grade alternatives (Amazon Bedrock, Amazon Cognito, AWS End User Messaging, and AWS Lambda/API Gateway) to external SaaS integrations (as per **Item 49**).

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
