---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Amazon CloudWatch Full-Stack Observability Platform"
timestamp: 2026-08-25T10:00:00Z
topics: ["aws", "cloud", "architecture", "cloudwatch", "apm", "rum", "opentelemetry", "costing", "metrics", "logging"]
---
# Amazon CloudWatch Full-Stack Observability Platform

<div class="arch-badge arch-badge-devops">[DEVOPS EXECUTION]</div>
<div class="arch-badge arch-badge-strategic">[STRATEGIC FINANCIAL]</div>
<div class="arch-badge arch-badge-security">[SECURITY & COMPLIANCE]</div>

## Overview

This guide establishes the comprehensive **Amazon CloudWatch** full-stack observability architecture for our 3-tier AWS infrastructure in **AWS Malaysia (`ap-southeast-5`)**.

Amazon CloudWatch serves as the single pane of glass for operational monitoring, infrastructure metrics, application performance monitoring (APM), client-side Real User Monitoring (RUM), centralized log management, and proactive synthetic alarming. By leveraging AWS-native CloudWatch capabilities alongside open standards (OpenTelemetry / W3C Trace Context), we achieve full operational visibility while decommissioning high-cost third-party agents (such as Dynatrace OneAgent) within our AWS estate.

---

## 1. Capability & Infrastructure Telemetry Matrix

Amazon CloudWatch natively collects performance telemetry across all operational tiers. Managed services emit hypervisor-level metrics automatically at no additional charge, while guest EC2 instances utilize the open-source **Unified CloudWatch Agent (`amazon-cloudwatch-agent`)** to expose internal OS-level memory, storage, and network interface metrics.

| Infrastructure Tier | CPU Telemetry | Memory Telemetry | Network I/O | Disk Space / IOPS | Implementation Mechanism | Metric Billing Category |
| --- | --- | --- | --- | --- | --- | --- |
| **EC2 Instances** | `CPUUtilization` | `mem_used_percent` | `bytes_sent`, `bytes_recv`, `drop_in`, `drop_out` | `disk_used_percent` | Unified CloudWatch Agent (RPM/DEB package) | Basic hypervisor metrics **Free**; OS memory/disk/net are **Custom Metrics** ($0.30/metric/mo) |
| **Amazon RDS PostgreSQL** | `CPUUtilization` | `FreeableMemory` | `NetworkReceiveThroughput` | `FreeStorageSpace` / `ReadIOPS` | Native Hypervisor Telemetry | Standard 1-min/5-min metrics **Free**; OS Enhanced Monitoring logs billed via CloudWatch Logs ingestion |
| **ElastiCache (Valkey / Redis)** | `CPUUtilization` / `EngineCPUUtilization` | `BytesUsedForCache` / `DatabaseMemoryUsagePercentage` | `NetworkBytesIn` / `NetworkBytesOut` | In-memory eviction tracking / swap usage | Native Engine Telemetry | **100% Free** (Emitted natively into CloudWatch) |
| **Amazon EFS** | N/A (Serverless) | N/A (Serverless) | `DataReadIOBytes` / `DataWriteIOBytes` | `StorageBytes` / `PercentIOLimit` | Native EFS Storage Controller | **100% Free** (Standard metrics) |
| **Application Load Balancers (ALB)** | N/A (L7 Layer) | N/A (L7 Layer) | `ProcessedBytes` / `ActiveConnectionCount` | N/A (HTTP target response time) | Native Load Balancing Ingress | **100% Free** (Standard metrics) |

---

## 2. Infrastructure Delivery: Unified CloudWatch Agent

Because AWS hypervisors cannot inspect guest operating system memory or filesystem mount points due to memory virtualization security boundaries, the FOSS **unified CloudWatch agent** is deployed on all EC2 instances across both x86 (`t3`) and ARM Graviton (`t4g`, `c7g`, `c8g`) hardware.

### Configuration Specification (`/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json`)

```json
{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "root"
  },
  "metrics": {
    "namespace": "CWAgent",
    "append_dimensions": {
      "AutoScalingGroupName": "${aws:AutoScalingGroupName}",
      "InstanceId": "${aws:InstanceId}"
    },
    "metrics_collected": {
      "mem": {
        "measurement": [
          "mem_used_percent",
          "mem_available"
        ]
      },
      "disk": {
        "measurement": [
          "disk_used_percent",
          "disk_free"
        ],
        "resources": [
          "/"
        ]
      },
      "net": {
        "measurement": [
          "bytes_sent",
          "bytes_recv",
          "drop_in",
          "drop_out"
        ],
        "resources": [
          "eth0"
        ]
      }
    }
  }
}
```

*Note on Network Interface Target:* The agent configuration above explicitly targets the primary interface (`"resources": ["eth0"]` on standard Linux AMIs, or `"ens5"` on AWS Nitro/Graviton AMIs). If wildcard discovery (`"resources": ["*"]`) is used, the agent exposes separate dimensioned metric streams for every active network interface (including virtual loopbacks and secondary vNICs), scaling metric volume accordingly.

### Metric Volume & Host Metric Sizing
Configuring primary network interface monitoring as specified above emits 8 custom metric streams per EC2 host (`mem_used_percent`, `mem_available`, `disk_used_percent`, `disk_free`, `bytes_sent`, `bytes_recv`, `drop_in`, `drop_out`). For a 15-node production cluster:
- **Total Custom Metrics:** 15 instances × 8 metrics = 120 custom metrics.
- **Billable Metrics:** 120 metrics − 10 free tier metrics = 110 billable custom metrics.
- **Monthly Host Metric Cost:** 110 metrics × $0.30/metric/month = **$33.00 USD/month (~RM 148.50 MYR)**.

---

## 3. CloudWatch Application Performance Monitoring (Application Signals & APM)

To complete the replacement of on-premise Dynatrace agents in AWS, **Amazon CloudWatch Application Signals** delivers automated APM based on **AWS Distro for OpenTelemetry (ADOT)**.

### APM Feature Comparison: Dynatrace vs. CloudWatch Application Signals

| APM Capability | Dynatrace OneAgent (Host) | CloudWatch APM Native Stack |
| --- | --- | --- |
| **Instrumentation Engine** | Proprietary Bytecode Hook | OpenTelemetry (AWS Distro/ADOT) |
| **Host Footprint** | 200–400 MB RAM, 2–5% CPU | ~15–30 MB RAM, <0.2% CPU |
| **Distributed Tracing** | PurePath (Proprietary) | AWS X-Ray / W3C Trace Context |
| **Golden Metrics** | Automatic Davis AI Baselines | Native Golden Signals (Latency, Volume, Errors, Saturation) |
| **Service Dependency Map** | Smartscape Topology | CloudWatch Application Map |
| **End-User Monitoring** | Dynatrace DEM Sessions | CloudWatch RUM |
| **Host Infrastructure** | Host Units (RAM-based) | CloudWatch Unified Agent |
| **Billing Architecture** | Fixed Annual / Host Units | Metered Consumption (Pay-as-you-go) |

### Key Architectural Advantages
1. **OpenTelemetry Standardization:** Eliminates kernel-level patching failures by using vendor-neutral OTel auto-instrumentation (Java, Python, Node.js, .NET).
2. **Automated Service Map Topology:** Synthesizes distributed traces into live topological graphs (ALB $\rightarrow$ Application Microservices $\rightarrow$ ElastiCache Valkey $\rightarrow$ RDS PostgreSQL).
3. **Service Level Objectives (SLOs) & Error Budgets:** Declarative SLO tracking against latency (P99, P95) and availability SLAs with automated error budget burn-rate alarms.

---

## 4. CloudWatch Real User Monitoring (RUM)

Client-Side Monitoring is handled natively by **CloudWatch RUM**, which embeds the asynchronous `aws-rum-web` JavaScript client into front-end application templates.

### Frontend Web Integration Snippet (`aws-rum-web`)

```javascript
import { AwsRum } from 'aws-rum-web';

try {
  const config = {
    sessionSampleRate: 1.0,
    guestRoleArn: "arn:aws:iam::123456789012:role/RUM-Guest-Role",
    identityPoolId: "ap-southeast-5:example-pool-id",
    endpoint: "https://dataplane.rum.ap-southeast-5.amazonaws.com",
    telemetries: [
      "errors",
      "performance",
      [
        "http",
        {
          addXRayTraceIdHeader: [ /https:\/\/api\.example\.com\/.*/ ],
          urlsToInclude: [ /https:\/\/api\.example\.com\/.*/ ]
        }
      ]
    ],
    allowCookies: true,
    enableXRay: true
  };

  const APPLICATION_ID = 'example-rum-app-id';
  const APPLICATION_VERSION = '1.0.0';
  const APPLICATION_REGION = 'ap-southeast-5';

  const awsRum = new AwsRum(
    APPLICATION_ID,
    APPLICATION_VERSION,
    APPLICATION_REGION,
    config
  );
} catch (error) {
  // Ignore RUM initialization errors in client
}
```

```text
[ End-User Browser ]
         │
         ▼  (Lightweight snippet: ~10-20 events/session)
[ CloudWatch RUM App Monitor Endpoint ]
         │
         ├──► CloudWatch Metrics (Core Web Vitals, Page Load, Latency, Errors)
         ├──► CloudWatch Logs (/aws/vendedlogs/RUMService...)
         └──► AWS X-Ray (End-to-End Distributed Trace linking ALB -> App -> RDS)
```

### Client-Side Observability Capabilities
- **Core Web Vitals (CWV):** Measures Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS), and Interaction to Next Paint (INP) across Malaysian ISPs and browsers.
- **JavaScript & HTTP Error Tracking:** Automatically captures unhandled exceptions, stack traces, and 4xx/5xx API failures.
- **AWS X-Ray Trace Context Propagation:** Setting `enableXRay: true` and configuring the `http` tuple `["http", { addXRayTraceIdHeader: [ /https:\/\/api\.example\.com\/.*/ ], urlsToInclude: [...] }]` in `telemetries` enables AWS X-Ray header (`X-Amzn-Trace-Id`) injection into client HTTP requests for targeted API domains.
  - *Prerequisites:* Header injection applies strictly to matched API target domains in the `addXRayTraceIdHeader` allowlist array, and downstream CORS policies on ALBs and backend microservices must explicitly allow `X-Amzn-Trace-Id` in the `Access-Control-Allow-Headers` list.

---

## 5. Comprehensive Cost Model & Financial Sizing (AWS Malaysia `ap-southeast-5`)

*Official Pricing Reference: Rates verified against Official AWS CloudWatch Pricing (`aws.amazon.com/cloudwatch/pricing`) for AWS Malaysia (`ap-southeast-5`) region as of September 2026 (1 USD = 4.50 MYR).*

### 5.1 CloudWatch Pricing Dimensions
- **Custom Metrics (Host Agent):** $0.30 per custom metric/month (First 10 metrics free).
- **Application Signals Pricing Schedules:**
  - **Golden-Metrics-Only Mode (Per Signal):** Billed strictly per Golden Signal using the tiered marginal schedule: First 100M signals/month @ **$1.50 per 1M**; Next 900M signals (100M to 1B) @ **$0.75 per 1M**; Above 1B signals (>1B) @ **$0.30 per 1M**.
  - **Transaction Search Mode (Data Ingestion + Indexed Spans):** Billed per GB trace span data ingested ($0.35/GB for first 10 TB) PLUS X-Ray Trace Summaries indexed spans ($0.005 per 1,000 indexed spans / $5.00 per 1M spans).
- **CloudWatch RUM Events:** $1.00 per 100,000 data events (~20 events per complete user session = ~$0.20 per 1,000 user sessions). First 1,000,000 events free as a **one-time per-account allowance**.

### 5.2 Application Signals & RUM Workload Scenarios
- **Baseline APM Workload (Transaction Search Mode):** 10 GB trace ingestion ($3.50) + 5M indexed trace summary spans ($25.00) = **$28.50 USD/month (~RM 128.25 MYR)**.
- **Moderate APM Workload (Transaction Search Mode):** 40 GB trace ingestion ($14.00) + 20M indexed trace summary spans ($100.00) = **$114.00 USD/month (~RM 513.00 MYR)**.
- **Baseline APM Workload (Golden-Metrics-Only Mode):** 5,000,000 signals @ $1.50/1M = **$7.50 USD/month (~RM 33.75 MYR)**.
- **Moderate APM Workload (Golden-Metrics-Only Mode):** 20,000,000 signals @ $1.50/1M = **$30.00 USD/month (~RM 135.00 MYR)**.
- **Baseline RUM Workload:** 250,000 monthly sessions × 20 events/session = 5,000,000 events = **$50.00 USD/month steady-state (~RM 225.00 MYR)** *(Note: Cost after applying the one-time 1M-event account allowance is $40.00 USD / RM 180.00 MYR)*.
- **Moderate RUM Workload:** 1,000,000 monthly sessions × 20 events/session = 20,000,000 events = **$200.00 USD/month steady-state (~RM 900.00 MYR)** *(Note: Cost after applying the one-time 1M-event account allowance is $190.00 USD / RM 855.00 MYR)*.

### 5.3 Consolidated Observability Sizing (15-Node Production Cluster)

| Component | Scope / Function | Monthly Cost (USD) | Monthly Cost (MYR @ 4.50) |
| --- | --- | --- | --- |
| **CloudWatch RUM** | Client-side Core Web Vitals, JS errors (250k–1M sessions, steady-state) | $50.00 – $200.00 | RM 225.00 – RM 900.00 |
| **Application Signals (APM - Transaction Search)** | OTel trace ingestion + X-Ray indexed trace summary spans (5M/10GB to 20M/40GB) | $28.50 – $114.00 | RM 128.25 – RM 513.00 |
| **Application Signals (APM - Golden Metrics)** | Golden Signals only mode (5M to 20M signals) | *$7.50 – $30.00* | *RM 33.75 – RM 135.00* |
| **Host Metrics (CloudWatch Agent)** | 15 EC2 nodes × 8 custom metrics (120 total, 110 billable @ $0.30) | $33.00 | RM 148.50 |
| **Native AWS Metrics** | RDS PostgreSQL, ElastiCache Valkey, EFS, ALB | **$0.00** (Included) | **RM 0.00** |
| **Alarms & Dashboards** | Operational alerts, status screens, Composite Alarms | $5.00 | RM 22.50 |
| **Total CloudWatch Suite (Transaction Search)** | **Full-Stack Enterprise Cloud-Native Observability** | **~$116.50 – $352.00** | **~RM 524.25 – RM 1,584.00** |
| **Total CloudWatch Suite (Golden Metrics Only)** | **Cost-Optimized Full-Stack Observability** | **~$95.50 – $268.00** | **~RM 429.75 – RM 1,206.00** |
| **Dynatrace OneAgent (Current)** | Proprietary OneAgent Host Units + DEM Packs (15 host units list price) | ~$870.00 – $1,110.00+ | ~RM 3,915.00 – RM 4,995.00+ |

**Net Financial Savings:** Comparing the full CloudWatch observability stack ($95.50–$352.00 USD) against Dynatrace list pricing ($870.00–$1,110.00+ USD) yields recurring monthly operational savings of **~$518.00 to $1,014.50 USD/month (~RM 2,331.00 to RM 4,565.25 MYR/month)** depending on APM mode, session volume, and Dynatrace memory tiering.

---

## 6. High-Volume / Payment-Critical Cost Risk Analysis

For high-throughput or payment-critical transaction paths (e.g. core banking switches or gateway processors), sustained request rates require selecting the appropriate Application Signals billing mode to prevent unexpected trace ingestion charges.

### Cost Scaling Comparison: Transaction Search Mode vs. Golden-Metrics-Only Mode

*Trace Volume & Billing Formula Assumptions:* Monthly operational duration = 730 hours (43,800 minutes). Each transaction includes 1 root transaction span plus 2 downstream microservice spans (3 spans total per transaction @ ~1.872 KB average payload size per span including ~4% index storage overhead).
- **Transaction Search Mode Formula:** Total Transaction Search Cost = Data Ingestion ($0.35/GB) + X-Ray Trace Summaries Indexed Spans ($0.005 per 1,000 indexed spans).
- **Golden-Metrics-Only Mode Formula:** Total Golden Signals Cost = Tiered marginal schedule ($1.50/1M for first 100M; $0.75/1M for 100M–1B; $0.30/1M above 1B).

| Sustained Load | Signals / Spans | Trace Ingestion | Total Transaction Search Cost (USD) | Golden-Metrics-Only Cost (USD) |
| --- | --- | --- | --- | --- |
| **1,000 req/min** | 131,400,000 | ~246 GB | **$743.10** | **$173.55** |
| **5,000 req/min** | 657,000,000 | ~1.23 TB | **$3,715.50** | **$567.75** |
| **10,000 req/min** | 1,314,000,000 | ~2.46 TB | **$7,431.00** | **$919.20** |
| **25,000 req/min** | 3,285,000,000 | ~6.15 TB | **$18,577.50** | **$1,510.50** |

*Note: At ~10,000 req/min sustained under Transaction Search Mode, total Transaction Search cost ($7,431.00 USD / RM 33,439.50 MYR) substantially exceeds fixed host-unit Dynatrace licensing ($870–$1,110 USD). To prevent cost escalation:*
1. **Apply Intelligent Trace Sampling:** Under Transaction Search Mode, enforce 5% steady-state trace sampling, ramping up to 100% capture strictly on 5xx errors and latency anomalies.
2. **Switch Payment Path to Golden-Metrics-Only Mode:** Disable trace span ingestion for the payment service path to cap APM costs strictly at Golden Signals ($919.20 USD at 10,000 req/min under the tiered marginal schedule).
3. **Audit Pipeline Separation:** Route compliance audit trails to CloudWatch Logs or S3, avoiding APM span ingestion for audit retention.
4. **Leverage Free Trial:** Utilize the 3-month CloudWatch Application Signals free trial:
   - When **Transaction Search Mode** is enabled: 3 months up to **100 GB of trace data ingestion** or **1 million spans indexed as X-Ray trace summaries** (whichever comes first).
   - When **Transaction Search Mode** is disabled (Golden Metrics only): 3 months up to **100 million signals**.

---

## Related Documentation

- [Costing Estimates](costing.html) — Granular breakdown of AWS infrastructure and operational line items.
- [CloudWatch APM Dynatrace Replacement Paperwork](engineering/cloudwatch_apm_dynatrace_replacement.html) — Board-level justification `PAP-APM-2026-CW-02`.
- [CloudWatch RUM Proposal](engineering/cloudwatch_rum_proposal.html) — Technical proposal `PROP-OBS-2026-RUM-01`.
- [AWS vs On-Prem Stack Comparison](aws-vs-onprem-stack-comparison.html) — Mapping AWS services to open-source on-prem equivalents.
