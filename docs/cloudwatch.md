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

Amazon CloudWatch natively collects performance telemetry across all operational tiers. Managed services emit hypervisor-level metrics automatically at no additional charge, while guest EC2 instances utilize the open-source **Unified CloudWatch Agent (`amazon-cloudwatch-agent`)** to expose internal OS-level memory and storage metrics.

| Infrastructure Tier | CPU Telemetry | Memory Telemetry | Network I/O | Disk Space / IOPS | Implementation Mechanism | Metric Billing Category |
| --- | --- | --- | --- | --- | --- | --- |
| **EC2 Instances** | `CPUUtilization` | `mem_used_percent` | `NetworkIn` / `NetworkOut` | `disk_used_percent` | Unified CloudWatch Agent (RPM/DEB package) | Basic metrics **Free**; OS memory/disk are **Custom Metrics** (~$0.30/metric) |
| **Amazon RDS PostgreSQL** | `CPUUtilization` | `FreeableMemory` | `NetworkReceiveThroughput` | `FreeStorageSpace` / `ReadIOPS` | Native Hypervisor Telemetry (Enhanced Monitoring) | **100% Free** (Standard 1-min / 5-min intervals) |
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

### Key Operational Features
- **Zero Proprietary Lock-In:** Replaces Dynatrace OneAgent with a lightweight daemon consuming less than 15 MB of RAM and ~0.1% CPU.
- **Automated Rollout:** Injected seamlessly via EC2 User Data, Systems Manager (SSM) Run Command, or Ansible playbooks.

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

Client-side monitoring is handled natively by **CloudWatch RUM**, which embeds a lightweight asynchronous JavaScript client (`aws-rum-web`) into front-end templates.

```
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
- **W3C Distributed Trace Correlation:** Injects standard trace context headers into API calls, linking user web sessions directly to backend AWS X-Ray traces.

---

## 5. Comprehensive Cost Model & Financial Sizing (AWS Malaysia `ap-southeast-5`)

### 5.1 CloudWatch Pricing Dimensions
- **Custom Metrics (Host Agent):** $0.30 per custom metric/month (First 10 metrics free). Standard 4 metrics/node (`mem_used_percent`, `mem_available`, `disk_used_percent`, `disk_free`) = **$1.20 USD / instance / month**.
- **Application Signals (Golden Metrics):** $1.50 per 1 million signals for the first 100M signals/month.
- **Transaction Search / Trace Ingestion:** $0.35 per GB trace data ingested.
- **CloudWatch RUM Events:** $1.00 per 100,000 data events (~20 events per complete user session = ~$0.20 per 1,000 user sessions).

### 5.2 Consolidated Observability Sizing (15-Node Production Cluster)

| Component | Scope / Function | Monthly Cost (USD) | Monthly Cost (MYR @ 4.50) |
| --- | --- | --- | --- |
| **CloudWatch RUM** | Client-side Core Web Vitals, JS errors (250k–1M sessions) | $50.00 – $200.00 | RM 225.00 – RM 900.00 |
| **Application Signals (APM)** | OTel distributed traces, Service Maps, SLOs (20M signals, 40GB traces) | $11.00 – $44.00 | RM 49.50 – RM 198.00 |
| **Host Metrics (CloudWatch Agent)** | 15 EC2 nodes custom memory & disk metrics (60 metrics total) | $10.00 – $20.00 | RM 45.00 – RM 90.00 |
| **Native AWS Metrics** | RDS PostgreSQL, ElastiCache Valkey, EFS, ALB | **$0.00** (Included) | **RM 0.00** |
| **Alarms & Operational Dashboards** | Operational alerts, status screens, Composite Alarms | $5.00 | RM 22.50 |
| **Total CloudWatch Suite** | **Full-Stack Enterprise Cloud-Native Observability** | **~$76.00 – $269.00** | **~RM 342.00 – RM 1,210.50** |
| **Dynatrace OneAgent (Current)** | Proprietary OneAgent Host Units + DEM Packs (15 nodes) | ~$870.00 – $1,110.00+ | ~RM 3,915.00 – RM 4,995.00+ |

**Net Financial Savings:** Migrating full-stack observability to native Amazon CloudWatch yields a recurring monthly savings of **~RM 2,700 to RM 3,800 MYR** (~$600 to $840 USD/month).

---

## 6. High-Volume / Payment-Critical Cost Risk Analysis

For high-throughput or payment-critical transaction paths (e.g. core banking switches or gateway processors), sustained request rates require explicit sampling controls to prevent unexpected trace ingestion charges.

### Cost Scaling Matrix for High-Throughput Services

| Sustained Load | Signals / month | Trace Ingestion | Monthly APM Cost (USD) | Monthly APM Cost (MYR) |
| --- | --- | --- | --- | --- |
| **1,000 req/min** | 131,000,000 | ~246 GB | **$259.79** | **RM 1,169.00** |
| **5,000 req/min** | 657,000,000 | ~1.23 TB | **$998.92** | **RM 4,495.00** |
| **10,000 req/min** | 1,310,000,000 | ~2.46 TB | **$1,781.51** | **RM 8,017.00** |
| **25,000 req/min** | 3,290,000,000 | ~6.16 TB | **$3,666.29** | **RM 16,498.00** |

*Note: At ~10,000 req/min sustained, un-sampled APM ingestion exceeds fixed host-unit Dynatrace licensing. To prevent cost escalation:*
1. **Apply Intelligent Sampling:** Maintain 5% steady-state trace sampling, ramping up to 100% capture strictly on 5xx errors and latency anomalies.
2. **Audit Pipeline Separation:** Route compliance transaction logs to CloudWatch Logs or S3, keeping Application Signals in golden-metrics-only mode for normal transactions.
3. **Leverage Free Trial:** Utilize the 3-month CloudWatch Application Signals free trial (up to 100 GB trace data or 100M signals) to measure exact throughput before full cutover.

---

## Related Documentation

- [Costing Estimates](costing.html) — Granular breakdown of AWS infrastructure and operational line items.
- [CloudWatch APM Dynatrace Replacement Paperwork](engineering/cloudwatch_apm_dynatrace_replacement.html) — Board-level justification `PAP-APM-2026-CW-02`.
- [CloudWatch RUM Proposal](engineering/cloudwatch_rum_proposal.html) — Technical proposal `PROP-OBS-2026-RUM-01`.
- [AWS vs On-Prem Stack Comparison](aws-vs-onprem-stack-comparison.html) — Mapping AWS services to open-source on-prem equivalents.
