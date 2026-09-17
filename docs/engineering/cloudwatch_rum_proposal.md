---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Technical Proposal: CloudWatch RUM Integration & Observability Consolidation"
timestamp: 2026-08-25T10:00:00Z
topics: ["aws", "cloud", "architecture", "cloudwatch", "rum", "opentelemetry", "web-vitals", "costing"]
---
# Technical Proposal: CloudWatch RUM Integration & Observability Consolidation

<div class="arch-badge arch-badge-devops">[DEVOPS EXECUTION]</div>
<div class="arch-badge arch-badge-strategic">[STRATEGIC FINANCIAL]</div>
<div class="arch-badge arch-badge-security">[SECURITY & COMPLIANCE]</div>

```text
Document Reference : PROP-OBS-2026-RUM-01
Classification     : Technical Proposal & Financial Justification
Region             : AWS Malaysia (ap-southeast-5)
Target Audience    : Executive Management & Technical Architecture Board
Subject            : CloudWatch RUM Adoption & Decommissioning of AWS-hosted Dynatrace Agents
Status             : Draft / For Architectural Review
```

---

## Executive Summary

To eliminate operational toil and recurring third-party software licensing overheads, this proposal outlines the architectural consolidation of client-side monitoring under **Amazon CloudWatch Real User Monitoring (RUM)**.

Currently, our hybrid environment relies on an on-premise Dynatrace deployment extending proprietary OneAgents into AWS workloads. This setup incurs dual-observability expenditure, agent-level CPU/memory footprints on EC2 compute tiers, and cross-boundary network egress charges back to the on-premise monitoring core.

By activating native **CloudWatch RUM**, we capture real-world client performance, Core Web Vitals (CWV), client-side JavaScript errors, and end-to-end tracing seamlessly within the **AWS Malaysia (`ap-southeast-5`)** sovereign boundary at a predictable consumption-based rate of **$1.00 USD per 100,000 RUM events**. This transition permits the formal decommissioning of Dynatrace agents within AWS, yielding immediate licensing savings and consolidating monitoring into a single pane of glass alongside existing CloudWatch metrics and alarms.

---

## 1. Problem Statement: The Cost & Overhead of AWS-Hosted Dynatrace

Maintaining third-party enterprise APM agents (Dynatrace OneAgent) inside AWS infrastructure introduces three major operational and financial liabilities:

1. **Dual Licensing & Commercial Redundancy:**
Our AWS estate already incurs baseline CloudWatch costs (~$80 to $90 USD/month in the `ap-southeast-5` baseline audit). Running Dynatrace agents on AWS EC2 instances consumes additional Dynatrace Host Units (HUs) and Digital Experience Monitoring (DEM) units for user sessions, resulting in redundant expenditure across two operational stacks.
2. **Compute Resource Tax & Runtime Friction:**
Dynatrace OneAgents inject deep bytecode instrumentation and native monitoring hooks at the OS and container level. In containerised or right-sized Graviton fleets (`c8g`, `c6g`), this introduces a 2% to 5% continuous memory and CPU tax, artificially inflating compute instance requirements.
3. **Operational Fragmentation & MTTD/MTTR Drag:**
When client-facing incidents occur, engineers currently cross-examine Dynatrace for front-end issues and pivot to AWS CloudWatch for infrastructure, load balancer, and RDS telemetry. Eliminating this context switching directly reduces Mean Time to Detect (MTTD) and Mean Time to Remediate (MTTR).

---

## 2. Technical Architecture: Amazon CloudWatch RUM

CloudWatch RUM provides client-side observability by embedding a lightweight, asynchronous, open-source JavaScript web client (`aws-rum-web`) into our front-end application templates.

```text
[ End-User Browser ]
         │
         ▼  (Lightweight snippet: ~10-20 events/session)
[ CloudWatch RUM App Monitor Endpoint ]
         │
         ├──► CloudWatch Metrics (CWV, Page Load, Latency, Errors)
         ├──► CloudWatch Logs (/aws/vendedlogs/RUMService...)
         └──► AWS X-Ray (End-to-End Distributed Trace linking ALB -> ECS/EC2 -> RDS)
```

With this deployment model:

* **Core Web Vitals Telemetry:** Directly records Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS), and Interaction to Next Paint (INP) across end-user devices, browsers, and local ISPs within Malaysia.
* **JavaScript & HTTP Error Tracking:** Automatically aggregates unhandled exceptions, stack traces, and 4xx/5xx asynchronous API payload failures.
* **AWS X-Ray Trace Context Propagation:** Enabling `enableXRay: true`, including `"http"` in `telemetries`, and setting `addXRayTraceIdHeader: true` (or defining allowed API target domain patterns) injects standard `X-Amzn-Trace-Id` headers into client HTTP requests.
  - *Prerequisites:* Requires backend microservices to be instrumented with AWS X-Ray SDK or OpenTelemetry, and downstream CORS policies on ALBs/servers to allow the `X-Amzn-Trace-Id` header for cross-origin requests before decommissioning Dynatrace.

---

## 3. Financial Modeling & Sizing Estimation

### 3.1 CloudWatch RUM Cost Model

CloudWatch RUM uses purely consumption-based billing with no minimum commitments, fixed host fees, or base subscription floors:

* **Unit Pricing:** **$1.00 USD per 100,000 data events** ($0.00001 per event).
* **One-Time Account Allowance:** First **1,000,000 events** free as a one-time per-account allowance (standard $1.00 / 100,000 event charges apply thereafter).
* **Event Composition:** Standard page navigation produces approximately **10 to 20 events** per complete user session (Page Load, Navigation Timing, Web Vitals, API calls, and Errors).
* **Effective Session Unit Cost:** ~$0.10 to $0.20 USD per 1,000 user sessions.

### 3.2 Monthly Workload Projections (AWS Malaysia `ap-southeast-5`)

The financial impact across three workload profiles demonstrates the low marginal cost of adding RUM:

| Operational Scenario | Estimated Monthly Sessions | Monthly Events Captured | Steady-State Cost (USD) | Cost After 1M Allowance (USD) | Equivalent MYR (Steady-State @ 4.50) |
| --- | --- | --- | --- | --- | --- |
| **Baseline Profile** | 250,000 sessions | 5,000,000 events | **$50.00** | **$40.00** | **RM 225.00** |
| **Moderate Production** | 1,000,000 sessions | 20,000,000 events | **$200.00** | **$190.00** | **RM 900.00** |
| **Peak Campaign Load** | 3,500,000 sessions | 70,000,000 events | **$700.00** | **$690.00** | **RM 3,150.00** |

*Note: In high-volume environments, CloudWatch RUM supports a native **telemetry sampling rate** (e.g., 25% or 50%), allowing linear expenditure control without sacrificing statistical anomaly detection.*

---

## 4. Architectural Justification & Strategic Benefits

1. **Elimination of Third-Party Agent Fragility:**
Dynatrace OneAgent updates often lag modern Linux kernel builds or introduce glibc compatibility hurdles on lean container baselines. Transitioning client monitoring to CloudWatch RUM decouples host maintenance from application observability.
2. **Unified Incident Remediation (Single Pane of Glass):**
Front-end error anomalies trigger standard CloudWatch Composite Alarms. Operators observe real user impact alongside infrastructure telemetry (ALB response times, RDS CPU, Target Response Times) inside unified CloudWatch Operational Dashboards.
3. **Data Sovereignty Compliance:**
For public sector and enterprise workloads operating under regulatory frameworks in Malaysia, CloudWatch RUM keeps all telemetry, client IP masking, and session diagnostic traces within the local AWS `ap-southeast-5` region, avoiding cross-border data transfers.

---

## 5. Implementation Roadmap & Migration Plan

```text
Phase 1: App Monitor Provisioning (Week 1)
  └── Create CloudWatch RUM App Monitor via AWS CLI / OpenTofu in ap-southeast-5.
  └── Enable Amazon Cognito Identity Pool for guest telemetry authorisation.
  └── Configure Telemetry Data: Core Web Vitals, JS Errors, HTTP 4xx/5xx requests.

Phase 2: Client Web Integration & Canary Test (Week 2)
  └── Embed aws-rum-web snippet into application templates.
  └── Validate X-Ray header propagation across the Application Load Balancer.
  └── Verify CloudWatch RUM dashboard data ingestion and session metrics.

Phase 3: Production Rollout & Dynatrace Decommissioning (Week 3 - 4)
  └── Deploy RUM snippet to production with a 25% initial sampling rate.
  └── Calibrate sampling to steady-state (e.g., 50% or 100% depending on volume).
  └── Decommission Dynatrace OneAgent packages from EC2 launch templates and AMIs.
  └── Reclaim Dynatrace Host Unit / DEM licenses for core on-premise workloads.
```

---

## Governance & Compliance Statement

This technical proposal operates under the **Deep State of Mind (DSOM) AI Protocol** governing AWS infrastructure, ensuring that all runtime observability and security logging remain strictly within sovereign Malaysian data boundaries.
