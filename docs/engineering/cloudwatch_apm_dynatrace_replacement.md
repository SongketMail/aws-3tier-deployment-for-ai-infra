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

For a representative 15-node production cluster, the fully consolidated CloudWatch observability stack (RUM, APM, host metrics, native service metrics, alarms/dashboards) is estimated at **RM 429.75 – RM 1,584.00 per month ($95.50 – $352.00 USD/month)**, against a current Dynatrace Full-Stack Monitoring spend estimated at **RM 3,915.00 – RM 4,995.00+ per month ($870 – $1,110+ USD/month)** based on 2026 published Dynatrace list pricing for 15 host units. That implies a potential recurring saving in the order of **RM 2,331.00 – RM 4,565.25 per month (~$518 – $1,014.50 USD/month)** depending on session volume, APM mode, and Dynatrace memory unit tiering.

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

CloudWatch Application Signals supports two distinct account-level operational modes:

1. **Transaction Search Mode (Data Ingestion + Indexed Spans):**
   - Trace Span Ingestion Schedule: $0.35 per GB (first 10 TB); $0.20 per GB (next 20 TB); $0.15 per GB (above 30 TB).
   - X-Ray Trace Summaries Schedule: $0.005 per 1,000 indexed spans ($5.00 per 1M spans).
2. **Golden-Metrics-Only Mode (Trace Ingestion & Indexing Disabled):**
   - Golden Signals Tiered Schedule: $1.50 per 1M signals (first 100M); $0.75 per 1M (next 900M); $0.30 per 1M (above 1B).
   - Trace Span Ingestion & Indexing: $0.00.
3. **Free Trial Window:** New accounts receive a 3-month free trial:
   - When **Transaction Search Mode** is enabled: 3 months up to **100 GB of trace data ingestion** or **1 million spans indexed as X-Ray trace summaries** (whichever comes first).
   - When **Transaction Search Mode** is disabled (Golden Metrics only): 3 months up to **100 million signals**.

---

## 5. Cost Estimates for Our Environment

### 5.1 Application Signals — Workload Scenarios

Below are cost estimates calculated under **Transaction Search Mode** (Trace Ingestion @ $0.35/GB + Indexed Spans @ $0.005/1k) and **Golden-Metrics-Only Mode** (Golden Signals @ $1.50/1M):

| Workload Profile | Signals / Spans | Trace Ingestion | Transaction Search Cost (USD) | Golden-Metrics-Only Cost (USD) | Equivalent MYR (Transaction Search) |
| --- | --- | --- | --- | --- | --- |
| **Baseline** | 5,000,000 | 10 GB | **$28.50** | **$7.50** | **RM 128.25** |
| **Moderate Production** | 20,000,000 | 40 GB | **$114.00** | **$30.00** | **RM 513.00** |
| **High-Volume Tier** | 80,000,000 | 150 GB | **$452.50** | **$120.00** | **RM 2,036.25** |

*(Exact Math under Transaction Search Mode: Baseline = 10GB × $0.35 + 5M × $0.005/1k = $3.50 + $25.00 = $28.50 USD; Moderate = 40GB × $0.35 + 20M × $0.005/1k = $14.00 + $100.00 = $114.00 USD).*

### 5.2 CloudWatch RUM (Client-Side)

Official CloudWatch RUM pricing is $1.00 per 100,000 events (~20 events per complete user session):

| Monthly Sessions | Est. Events (@20/session) | Steady-State Cost (USD) | Cost After 1M Allowance (USD) | Monthly Cost (MYR @ 4.50) |
| --- | --- | --- | --- | --- |
| **250,000** | 5,000,000 | **$50.00** | **$40.00** | **RM 225.00** |
| **1,000,000** | 20,000,000 | **$200.00** | **$190.00** | **RM 900.00** |

### 5.3 Consolidated CloudWatch Observability Stack (15-node cluster)

| Component | Scope | Monthly (USD) | Monthly (MYR @ 4.50) |
| --- | --- | --- | --- |
| **CloudWatch RUM** | Client-side vitals, JS errors (250k–1M sessions, steady-state) | $50 – $200 | RM 225 – RM 900 |
| **Application Signals (APM - Transaction Search)** | OTel trace ingestion + X-Ray indexed trace summary spans (5M/10GB to 20M/40GB) | $28.50 – $114.00 | RM 128.25 – RM 513.00 |
| **Application Signals (APM - Golden Metrics)** | Golden Signals only mode (5M to 20M signals) | *$7.50 – $30.00* | *RM 33.75 – RM 135.00* |
| **Host metrics** | EC2 CPU / memory / disk / net (120 custom metrics, 110 billable) | $33.00 | RM 148.50 |
| **Native AWS metrics** | RDS, ElastiCache Valkey, ALB, EFS | **$0.00** | **RM 0.00** |
| **Alarms & dashboards** | Operational alerts, exec dashboards | $5.00 | RM 22.50 |
| **Total (Transaction Search)** | **Full-stack AWS-native observability** | **≈ $116.50 – $352** | **≈ RM 524.25 – RM 1,584** |
| **Total (Golden Metrics Only)** | **Cost-optimized full-stack observability** | **≈ $95.50 – $268** | **≈ RM 429.75 – RM 1,206** |

---

## 6. High-Volume / Payment-Critical Cost Risk Analysis

A payment-transfer service carries a unique risk profile: high transaction throughput and strict audit trace requirements push against trace ingestion billing.

*Trace Volume & Billing Formula Assumptions:* Monthly operational duration = 730 hours (43,800 minutes). Each transaction includes 1 root transaction span plus 2 downstream microservice spans (3 spans total per transaction @ ~1.872 KB average payload size per span including ~4% index storage overhead). Total Transaction Search cost represents the combined sum of Application Signals Data Ingestion ($0.35/GB) and X-Ray Trace Summaries indexed spans ($0.005 per 1,000 indexed spans). Golden-Metrics-Only Mode calculations apply the tiered marginal signal schedule ($1.50/1M for first 100M; $0.75/1M for 100M–1B; $0.30/1M above 1B).

| Sustained Load | Signals / Spans | Trace Ingestion | Total Transaction Search Cost (USD/mo) | Golden-Metrics-Only Cost (USD/mo) |
| --- | --- | --- | --- | --- |
| **1,000 req/min** | 131,400,000 | ~246 GB | **$743.10** | **$173.55** |
| **5,000 req/min** | 657,000,000 | ~1.23 TB | **$3,715.50** | **$567.75** |
| **10,000 req/min** | 1,314,000,000 | ~2.46 TB | **$7,431.00** | **$919.20** |
| **25,000 req/min** | 3,285,000,000 | ~6.15 TB | **$18,577.50** | **$1,510.50** |

### Critical Finding & Recommendations
At roughly **10,000 req/min sustained** under Transaction Search Mode, total Transaction Search cost ($7,431.00 USD / RM 33,349.50 MYR) substantially exceeds fixed host-unit Dynatrace licensing ($870–$1,110 USD / RM 3,915–4,995 MYR). To mitigate cost risks:
1. **Apply Intelligent Trace Sampling:** Under Transaction Search Mode, enforce 5% steady-state trace sampling, ramping up to 100% capture strictly on 5xx errors and latency anomalies.
2. **Switch Payment Path to Golden-Metrics-Only Mode:** Disable trace span ingestion for the payment service path to cap APM costs strictly at Golden Signals ($919.20 USD at 10,000 req/min under the tiered marginal schedule).
3. **Decouple Compliance Audits:** Route compliance audit trails to CloudWatch Logs or S3, avoiding APM span ingestion for audit retention.
4. **Pilot during Free Trial:** Measure exact signal and trace span volumes during the 3-month free trial before final cutover.

---

## 7. Recommendation & Next Steps

- Validate real payment service TPS and sampling requirements during the trial.
- Confirm actual historical trailing Dynatrace invoices for the 15-node scope.
- Proceed with ADOT rollout across EC2 application nodes in **AWS Malaysia (`ap-southeast-5`)**.

---

## Governance & Compliance Statement

This technical paperwork operates under the **Deep State of Mind (DSOM) AI Protocol** governing AWS infrastructure, ensuring that all runtime observability and security logging remain strictly within sovereign Malaysian data boundaries.
