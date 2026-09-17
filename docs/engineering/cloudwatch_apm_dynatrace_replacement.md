---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Technical Paperwork: CloudWatch Application Performance Monitoring (APM) & Full-Stack Dynatrace Replacement"
timestamp: 2026-08-25T10:00:00Z
topics: ["aws", "cloud", "architecture", "cloudwatch", "apm", "dynatrace", "opentelemetry", "xray", "costing"]
---
# Technical Paperwork: CloudWatch Application Performance Monitoring (APM) & Full-Stack Dynatrace Replacement

<div class="arch-badge arch-badge-devops">[DEVOPS EXECUTION]</div>
<div class="arch-badge arch-badge-strategic">[STRATEGIC FINANCIAL]</div>
<div class="arch-badge arch-badge-security">[SECURITY & COMPLIANCE]</div>

```text
Document Reference : PAP-APM-2026-CW-02 (Revision 1)
Classification     : Technical Architecture & Financial Justification
Region             : AWS Malaysia (ap-southeast-5)
Target Audience    : Executive Management & Technical Architecture Board
Prepared by        : Infrastructure Engineering
Status             : Ready for Board Review / Commit
```

---

## 1. Executive Summary

This proposal recommends replacing on-premise Dynatrace OneAgent monitoring on our AWS estate with native **Amazon CloudWatch Application Performance Monitoring (CloudWatch Application Signals)**. This closes the last functional gap versus Dynatrace — distributed tracing, service topology mapping, and Service Level Objectives (SLOs) — using an AWS-native, OpenTelemetry-based stack with no per-host agent licensing.

For a representative 15-node production cluster, the fully consolidated CloudWatch observability stack (RUM, APM, host metrics, native service metrics, alarms/dashboards) is estimated at **RM 445.50 – RM 1,269.00 per month ($99 – $282 USD/month)**, against a current Dynatrace Full-Stack Monitoring spend estimated at **RM 3,915.00 – RM 4,995.00+ per month ($870 – $1,110+ USD/month)** based on 2026 published Dynatrace list pricing for 15 host units. That implies a potential recurring saving in the order of **RM 2,646.00 – RM 4,549.50 per month (~$588 – $1,011 USD/month)** depending on session volume and Dynatrace memory unit tiering.

*Note on this revision: figures were verified against AWS's official CloudWatch pricing page (aws.amazon.com/cloudwatch/pricing) for AWS Malaysia (ap-southeast-5) as of September 2026.*

---

## 2. Why Change: Limitations of the Current Dynatrace Model

- **Proprietary OneAgent lock-in:** Kernel-level bytecode instrumentation is a recurring source of compatibility issues during OS patching (glibc/kernel version drift).
- **Fixed host-unit licensing:** Dynatrace Full-Stack Monitoring is billed per 8 GiB memory "host unit," so cost scales with host RAM even when utilization doesn't.
- **Agent overhead:** Third-party agents carry materially higher RAM/CPU footprint (~200–400 MB RAM, 2–5% CPU) than lightweight OpenTelemetry auto-instrumentation (~15–30 MB RAM, <0.2% CPU), a resource cost across every monitored EC2 instance.
- **Governance:** No architectural need to route runtime telemetry outside the **AWS Malaysia (`ap-southeast-5`)** sovereign boundary once native tooling covers the same ground.

---

## 3. Architectural Comparison

| APM Capability | Dynatrace OneAgent | CloudWatch Application Signals |
| --- | --- | --- |
| **Instrumentation** | Proprietary bytecode agent | OpenTelemetry (AWS Distro for OTel / ADOT) |
| **Distributed tracing** | PurePath (proprietary) | AWS X-Ray / W3C Trace Context |
| **Golden metrics** | Davis AI baselines | Native Golden Signals (latency, traffic, errors, saturation) |
| **Service map** | Smartscape topology | CloudWatch Application Map |
| **End-user monitoring** | Dynatrace DEM | CloudWatch RUM |
| **SLO / error budgets** | Supported | Native SLO tracking with burn-rate alarms |
| **Billing basis** | Per-host-unit (8 GiB), fixed | Metered — pay per signal / GB ingested |

---

## 4. How CloudWatch Application Signals Is Priced

Two billing dimensions apply in tandem when transaction span ingestion is active:

- **Golden metrics (Application Signals):** $1.50 per 1M signals for the first 100M signals/month, then $0.75 per 1M up to 1B, then $0.30 per 1M beyond that.
- **Transaction Search / trace span ingestion:** $0.35 per GB for the first 10 TB/month, then $0.20 per GB up to 30 TB, then $0.15 per GB beyond that.
- **Free Trial Window:** New accounts receive 3 months free allowance. The 100 GB ingestion limit applies when transaction spans are enabled, whereas the 100M-signal cap applies when transaction-span ingestion is disabled (whichever threshold is reached first).

---

## 5. Cost Estimates for Our Environment

### 5.1 Application Signals — Workload Scenarios

Application Signals billing combines Golden Signal metering ($1.50/1M signals) and Trace Span Ingestion ($0.35/GB trace data):

| Workload Profile | Signals / month | Trace Ingestion | Monthly Cost (USD) | Monthly Cost (MYR @ 4.50) |
| --- | --- | --- | --- | --- |
| **Baseline** | 5,000,000 | 10 GB | **$11.00** | **RM 49.50** |
| **Moderate Production** | 20,000,000 | 40 GB | **$44.00** | **RM 198.00** |
| **High-Volume Tier** | 80,000,000 | 150 GB | **$172.50** | **RM 776.25** |

*(Exact Math: Baseline = 5M × $1.50/1M + 10GB × $0.35 = $7.50 + $3.50 = $11.00 USD; Moderate = 20M × $1.50/1M + 40GB × $0.35 = $30.00 + $14.00 = $44.00 USD).*

### 5.2 CloudWatch RUM (Client-Side)

Official CloudWatch RUM pricing is $1.00 per 100,000 events (~20 events per complete user session):

| Monthly Sessions | Est. Events (@20/session) | Monthly Cost (USD) | Monthly Cost (MYR @ 4.50) |
| --- | --- | --- | --- |
| **250,000** | 5,000,000 | **$50.00** | **RM 225.00** |
| **1,000,000** | 20,000,000 | **$200.00** | **RM 900.00** |

### 5.3 Consolidated CloudWatch Observability Stack (15-node cluster)

| Component | Scope | Monthly (USD) | Monthly (MYR @ 4.50) |
| --- | --- | --- | --- |
| **CloudWatch RUM** | Client-side vitals, JS errors (250k–1M sessions) | $50 – $200 | RM 225 – RM 900 |
| **Application Signals (APM)** | OTel traces, service map, SLOs (5M/10GB to 20M/40GB) | $11 – $44 | RM 49.50 – RM 198 |
| **Host metrics** | EC2 CPU / memory / disk / net (120 custom metrics, 110 billable) | $33.00 | RM 148.50 |
| **Native AWS metrics** | RDS, ElastiCache Valkey, ALB, EFS | **$0.00** | **RM 0.00** |
| **Alarms & dashboards** | Operational alerts, exec dashboards | $5.00 | RM 22.50 |
| **Total** | **Full-stack AWS-native observability** | **≈ $99 – $282** | **≈ RM 445.50 – RM 1,269** |

---

## 6. High-Volume / Payment-Critical Cost Risk Analysis

A payment-transfer service carries a unique risk profile: high transaction throughput and strict audit trace requirements push against trace ingestion billing.

| Sustained Load | Signals / month | Trace Ingestion | APM Cost (USD/mo) | APM Cost (MYR/mo) |
| --- | --- | --- | --- | --- |
| **1,000 req/min** | 131M | ~246 GB | **$259.79** | **RM 1,169** |
| **5,000 req/min** | 657M | ~1.23 TB | **$998.92** | **RM 4,495** |
| **10,000 req/min** | 1.31B | ~2.46 TB | **$1,781.51** | **RM 8,017** |
| **25,000 req/min** | 3.29B | ~6.16 TB | **$3,666.29** | **RM 16,498** |

### Critical Finding & Recommendations
At roughly **10,000 req/min sustained**, APM trace ingestion alone (≈RM 8,000/month) exceeds the entire 15-host Dynatrace host-unit estimate (RM 3,915–4,995/month). To mitigate cost risks:
1. **Enforce Sampling Controls:** Deploy 5% steady-state sampling with 100% capture only on errors and 5xx responses.
2. **Decouple Compliance Audits:** Route compliance audit trails to CloudWatch Logs or S3, keeping Application Signals in golden-metrics-only mode.
3. **Pilot during Free Trial:** Measure exact transaction signal/span rates on the payment service during the 3-month free trial before final cutover.

---

## 7. Recommendation & Next Steps

- Validate real payment service TPS and sampling requirements during the trial.
- Confirm actual historical trailing Dynatrace invoices for the 15-node scope.
- Proceed with ADOT rollout across EC2 application nodes in **AWS Malaysia (`ap-southeast-5`)**.

---

## Governance & Compliance Statement

This technical paperwork operates under the **Deep State of Mind (DSOM) AI Protocol** governing AWS infrastructure, ensuring that all runtime observability and security logging remain strictly within sovereign Malaysian data boundaries.
