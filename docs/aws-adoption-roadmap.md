---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "AWS Phased Adoption Roadmap & Costing Guide"
timestamp: 2026-08-05T22:10:00Z
topics: ["aws", "cloud", "architecture", "costing", "roadmap", "lifecycle", "compliance"]
---
# AWS Phased Adoption Roadmap & Costing Guide

This guide outlines the step-by-step AWS cloud adoption roadmap, designed to align with our project timeline spanning **2 years of development and 12 months of active support and maintenance (36 months total)**.

To ensure complete privacy and confidentiality, all technical activities are described using generalised enterprise-grade classifications while remaining directly traceable to our core project deliverables. All original Malay terms from the project Gantt chart have been fully translated into **UK English** (e.g., *optimise*, *analysing*, *organise*).

This roadmap illustrates how our AWS infrastructure scales incrementally week-by-week and month-by-month, starting from a absolute minimum cost, single-Availability Zone developer sandbox footprint and evolving into a fully-redundant, highly-available, secure, and compliant multi-AZ enterprise production architecture in the **AWS Asia Pacific (Malaysia) region (`ap-southeast-5`)**.

---

## Gantt Chart Activity Translation Matrix

Below is the definitive translation matrix mapping the original Malay Gantt chart activities to our generalised UK English enterprise delivery lifecycle terms:

| Original Malay Activity | UK English Enterprise Translation | Generalised Project Scope Mapping |
| :--- | :--- | :--- |
| **Mesyuarat Kick Off** | Project Kick-off Meeting | Administrative launch and project alignment |
| **Pengurusan Projek** | Project Management | Continuous delivery, monitoring, and compliance |
| **Fasa 1: Pembangunan Chatbot AI** | **Phase 1: AI Chatbot Engine Development** | Base chat routing and Core AI engine implementation |
| &nbsp;&nbsp;• Kajian Keperluan | &nbsp;&nbsp;• Requirements Analysis & Study | Specifying API payloads and database schema |
| &nbsp;&nbsp;• Rekabentuk dan pembangunan | &nbsp;&nbsp;• Architecture Design & Development | Backend coding and vector database layout design |
| &nbsp;&nbsp;• Membekal, memasang, konfigurasi | &nbsp;&nbsp;• Supply, Installation & Configuration | Provisioning sandbox environment & base infrastructure |
| &nbsp;&nbsp;• Integrasi dengan sistem dalaman | &nbsp;&nbsp;• Integration with Internal Systems | Bridging enterprise core APIs to the AI engine |
| &nbsp;&nbsp;• Pengujian | &nbsp;&nbsp;• System & Integration Testing | End-to-end payload audits and validation |
| &nbsp;&nbsp;• Go Live | &nbsp;&nbsp;• Live Deployment & Go-Live | Provisioning highly-available public-facing load balancers |
| &nbsp;&nbsp;• Latihan | &nbsp;&nbsp;• Technical & Administrator Training | Handover of deployment runbooks to operations teams |
| &nbsp;&nbsp;• Manages Cloud Services | &nbsp;&nbsp;• Managed Cloud Services & Operations | Ongoing cloud optimization, monitoring, and scaling |
| **Fasa 2: Pembangunan WhatsApp Business API** | **Phase 2: Omnichannel Messaging Integration** | WhatsApp API integration & chat webhook flow |
| &nbsp;&nbsp;• Membekal, memasang, konfigurasi | &nbsp;&nbsp;• Supply, Installation & Configuration | Provisioning API webhooks and secure NAT gateways |
| &nbsp;&nbsp;• Integrasi dengan AI Chatbot | &nbsp;&nbsp;• Integration with Core AI Chatbot | Connecting message handlers to the Phase 1 engine |
| &nbsp;&nbsp;• Pengujian | &nbsp;&nbsp;• System & Integration Testing | Auditing high-throughput messaging workloads |
| &nbsp;&nbsp;• Go Live | &nbsp;&nbsp;• Live Deployment & Go-Live | Enabling production webhook receiving channels |
| &nbsp;&nbsp;• Pemantauan interaksi pengguna | &nbsp;&nbsp;• User Interaction & Telemetry Monitoring | Tracing chat payloads via Langfuse observability |
| &nbsp;&nbsp;• Latihan | &nbsp;&nbsp;• Technical & Administrator Training | Operations team training on API token rotations |
| **Fasa 3: Pembangunan CRM** | **Phase 3: Customer Relationship Management (CRM)** | Customer database, task tracking & ticket management |
| &nbsp;&nbsp;• Kajian keperluan | &nbsp;&nbsp;• Requirements Analysis & Study | CRM database schema design and integration scoping |
| &nbsp;&nbsp;• Rekabentuk dan pembangunan | &nbsp;&nbsp;• Architecture Design & Development | Backend UI views and multi-tenant schema coding |
| &nbsp;&nbsp;• Membekal, memasang, konfigurasi | &nbsp;&nbsp;• Supply, Installation & Configuration | Scaling private compute ASG and Multi-AZ RDS |
| &nbsp;&nbsp;• Integrasi dengan sistem dalaman | &nbsp;&nbsp;• Integration with Internal Systems | Direct linking of CRM fields to internal databases |
| &nbsp;&nbsp;• Pengujian | &nbsp;&nbsp;• System & Integration Testing | Auditing CRM security parameters and transaction locks |
| &nbsp;&nbsp;• Go Live / Pelancaran | &nbsp;&nbsp;• Live Deployment, Launch & Go-Live | High-performance public launch of the CRM system |
| &nbsp;&nbsp;• Latihan | &nbsp;&nbsp;• Technical & Administrator Training | Staff onboarding, user manuals, and training sessions |
| &nbsp;&nbsp;• Managed Cloud Services | &nbsp;&nbsp;• Managed Cloud Services & Operations | CRM SLA monitoring and DB read-replica tuning |
| **Fasa 4: Pembangunan Super Mobile App** | **Phase 4: Omnichannel Mobile Application** | Hybrid React Native mobile app development |
| &nbsp;&nbsp;• Kajian keperluan | &nbsp;&nbsp;• Requirements Analysis & Study | Mobile API endpoint definition and push notification plan |
| &nbsp;&nbsp;• Membekal, memasang, konfigurasi | &nbsp;&nbsp;• Supply, Installation & Configuration | Launching secure edge caching (CloudFront + S3) |
| &nbsp;&nbsp;• Rekabentuk dan pembangunan | &nbsp;&nbsp;• Architecture Design & Development | Mobile coding, UI layouts, and local storage tuning |
| &nbsp;&nbsp;• Integrasi dengan sistem dalaman | &nbsp;&nbsp;• Integration with Internal Systems | Bridging push services, mobile SSO, and data syncing |
| &nbsp;&nbsp;• Pengujian | &nbsp;&nbsp;• System & Integration Testing | Beta testing, user acceptance, and load verification |
| &nbsp;&nbsp;• Go Live | &nbsp;&nbsp;• Live Deployment & Go-Live | App store submission and high-throughput production API launch |
| &nbsp;&nbsp;• Ujian keselamatan | &nbsp;&nbsp;• Security Vulnerability & Pen Testing | Rigorous penetration tests, OWASP checks, and WAF tuning |
| &nbsp;&nbsp;• Latihan | &nbsp;&nbsp;• Technical & Administrator Training | Administrative portal onboarding |
| &nbsp;&nbsp;• Managed Cloud Services | &nbsp;&nbsp;• Managed Cloud Services & Operations | Global mobile API latency optimization |
| **Final Acceptance Test** | **Final Acceptance Test (FAT)** | Formal client verification of all consolidated tiers |
| **Project Go Live** | **Official Unified Project Go-Live** | Hard cutover to enterprise-scale production |
| **Documentation & Handover** | **Documentation & Operational Handover** | Delivery of final system runbooks and OpenTofu IaC |
| **Support & Maintenance Period** | **Support, Maintenance & OpEx Optimisation** | 12-month post-launch support and Savings Plan lock-in |

---

## High-Level AWS Phased Growth Path

The architecture matures through four logical environments matching the development timeline:

```
                  +-----------------------------------+
                  |  PHASE 1: DEV / POC SANDBOX       |
                  |  • Months 1 - 2 (Week 1 - 8)      |
                  |  • Single-AZ, Low-Cost            |
                  |  • Approx. Cost: $138.50 / month   |
                  +-----------------------------------+
                                    │
                                    ▼
                  +-----------------------------------+
                  |  PHASE 2: OMNICHANNEL TESTING     |
                  |  • Months 3 - 6 (Week 9 - 26)     |
                  |  • Dual-AZ Staging Environment    |
                  |  • Approx. Cost: $482.10 / month   |
                  +-----------------------------------+
                                    │
                                    ▼
                  +-----------------------------------+
                  |  PHASE 3: ENTERPRISE REDUNDANCY   |
                  |  • Months 7 - 14 (Week 27 - 60)   |
                  |  • Highly-Available Production    |
                  |  • Approx. Cost: $1,064.46 / month |
                  +-----------------------------------+
                                    │
                                    ▼
                  +-----------------------------------+
                  |  PHASE 4: MOBILE & SECURE RUN-RATE |
                  |  • Months 15 - 36 (Week 61 - 156) |
                  |  • Savings Plans / Optimised Prod |
                  |  • Approx. Cost: $945.30 / month   |
                  +-----------------------------------+
```

---

## Detailed Chronological Roadmap

### Year 1, Month 1 (Weeks 1–4): Project Initiation & Kick-off
* **Gantt Chart Activity Mapping:** Project Kick-off Meeting, Project Management.
* **AWS Architectural Focus:** Identity access scoping and network design.
* **AWS Services Provisioned:**
  - **AWS IAM Identity Center:** Enforces multi-factor authentication (MFA) and granular role-based access control (RBAC).
  - **AWS Budgets & Billing Alarms:** Confirmed with a baseline budget threshold of $150.00 USD to prevent accidental run-away charges.
  - **Amazon Route 53:** Public hosted zone established for early API domain mapping.
* **Week-by-Week Technical Goals:**
  - **Week 1:** Establish enterprise AWS root account structure, configure IAM administrators, and set budget guardrails.
  - **Week 2:** Draft security policies and Cyberjaya office CIDR access blocks for administrators.
  - **Week 3:** Initial provision of an empty modular VPC structure inside the Malaysia (`ap-southeast-5`) region utilizing OpenTofu.
  - **Week 4:** Set up shared project logging bucket with strict life-cycle rules inside Amazon S3.
* **Phase Cost (USD / MYR):** **$1.00 USD / RM 4.45 MYR** (Route 53 hosted zone base fee + nominal IAM storage).

---

### Year 1, Month 2 (Weeks 5–8): Phase 1 Requirements & Dev Setup
* **Gantt Chart Activity Mapping:** Phase 1 (AI Chatbot Engine Development) - Requirements Study, Supply, Installation & Configuration.
* **AWS Architectural Focus:** Setting up the single-AZ developer sandbox to support early AI Chatbot engine coding and local model verification.
* **AWS Services Provisioned:**
  - **Amazon VPC:** Single public subnet + single private subnet inside `ap-southeast-5a`.
  - **Secure SSH Jumphost (Bastion):** Sized at `t4g.micro` to allow the Cyberjaya developer team to tunnel safely into the private subnet.
  - **Standalone Developer Compute Instance:** 1x `t4g.medium` instance running hardened Ubuntu 26.04 LTS (ASIMP framework) to compile and test the Java/Spring Boot AI Chatbot engine.
  - **Amazon RDS PostgreSQL (Single-AZ):** 1x `db.t4g.medium` PostgreSQL 16 database instance for chat history storage.
  - **Amazon ElastiCache Valkey:** 1x `cache.t4g.micro` node for caching user sessions.
* **Week-by-Week Technical Goals:**
  - **Week 5:** Finalise AI chatbot payload specifications and backend Spring Boot schema designs.
  - **Week 6:** Launch the SSH Jumphost and restrict port 22 access strictly to the Cyberjaya office IP address.
  - **Week 7:** Provision the standalone compute and Valkey nodes, ensuring the security groups block all traffic not originating from the Jumphost.
  - **Week 8:** Deploy Flyway on the database to verify schema migrations.
* **Phase Cost (USD / MYR):** **$138.50 USD / RM 616.33 MYR** (Single-AZ baseline environment).

---

### Year 1, Months 3–6 (Weeks 9–26): Chatbot Core Coding & Integration
* **Gantt Chart Activity Mapping:** Phase 1 (AI Chatbot Engine Development) - Architecture Design & Development, Integration with Internal Systems.
* **AWS Architectural Focus:** Transitioning the sandbox environment to a highly-resilient Dual-AZ Staging Environment to validate auto-scaling, load handling, and database failovers.
* **AWS Services Provisioned:**
  - **Dual-AZ Networking:** Expanded VPC with private subnets across 2 Availability Zones, protected by **2x NAT Gateways** to ensure secure outbound API updates.
  - **Application Load Balancer (ALB):** Public-facing ALB deployed in the public subnets to distribute mock testing traffic.
  - **Auto Scaling Group (ASG):** Sized with a minimum capacity of 2x `c7g.xlarge` (ARM Graviton3) instances to support heavy processing.
  - **Amazon EFS (Elastic File System):** Shared persistent NFS mount to share AI model cache files across the ASG compute tier.
  - **Amazon RDS (Multi-AZ Upgrade):** Database upgraded to Multi-AZ `db.t4g.large` with synchronous replication to prevent a single point of failure (SPOF).
  - **AWS Secrets Manager:** Deployed to secure database credentials, rotating them automatically every 30 days.
* **Week-by-Week Technical Goals:**
  - **Week 9–12:** Write Spring Boot Chatbot logic and vector indexing algorithms.
  - **Week 13–16:** Integrate the application tier with AWS Systems Manager (SSM) and completely disable traditional passwords or direct SSH.
  - **Week 17–20:** Implement auto-scaling policies triggered when average CPU usage exceeds 70% across the ASG.
  - **Week 21–24:** Establish private VPC endpoints to route Amazon S3 media traffic locally, bypassing NAT Gateway charges.
  - **Week 25–26:** Conduct chaos engineering tests, simulating a full Availability Zone outage to verify sub-minute automated DB and ALB failover.
* **Phase Cost (USD / MYR):** **$668.11 USD / RM 2,973.11 MYR** (Dual-AZ Staging Environment).

---

### Year 1, Months 7–8 (Weeks 27–34): Chatbot Go-Live & WhatsApp Integration
* **Gantt Chart Activity Mapping:** Phase 1 (AI Chatbot Engine Development) - Go-Live, Training, Managed Cloud Services; Phase 2 (Omnichannel Messaging Integration) - Supply, Installation & Configuration, Integration with Core AI Chatbot, System & Integration Testing, Go-Live, User Interaction & Telemetry Monitoring.
* **AWS Architectural Focus:** Shifting to the High-Performance Production Plan to launch the Chatbot engine publicly and integrate the high-throughput WhatsApp Business webhook pipelines.
* **AWS Services Provisioned:**
  - **AWS WAFv2:** Associated with the ALB to intercept and filter out OWASP Top-10 attacks, SQL injection attempts, and enforce dynamic IP rate-limiting (e.g., maximum 100 requests per 5 minutes per client IP).
  - **Production Database Tier:** Sized to Multi-AZ `db.m7g.xlarge` (4 vCPU, 16GB RAM) with 250 GB of gp3 storage (3,000 IOPS) to absorb massive concurrent chat transactions.
  - **Production Cache Tier:** Scaled up to ElastiCache Valkey `cache.r7g.large` (Dual Node cluster) to act as a secure, fast query broker.
  - **Amazon API Gateway & AWS Lambda:** Serverless webhook receiver layer deployed to securely absorb massive, bursty incoming WhatsApp callback payloads from Meta, offloading them to **Amazon SQS** queues to prevent thread saturation in the Spring Boot backend.
  - **Amazon CloudWatch Application Signals:** Enabled to track end-to-end user latency and alert on HTTP 5XX spikes.
* **Week-by-Week Technical Goals:**
  - **Week 27:** Establish production ALB SSL certificates using AWS Certificate Manager (ACM).
  - **Week 28:** Deploy AWS WAF and configure the core rule-sets. Run final technical training for administrator teams on emergency scaling.
  - **Week 29:** Launch the serverless webhook API Gateway and AWS Lambda functions, writing integration metrics to CloudWatch.
  - **Week 30:** Connect the WhatsApp endpoint to AWS End User Messaging (Social Channels), removing high-cost external SaaS middlemen.
  - **Week 31–32:** Execute massive simulated load testing, driving over 5,000 concurrent user interaction flows.
  - **Week 33–34:** Go-live with the WhatsApp Omnichannel API, monitoring trace logs in real-time.
* **Phase Cost (USD / MYR):** **$1,665.61 USD / RM 7,411.98 MYR** (High-Performance Multi-AZ Enterprise Production).

---

### Year 1, Months 9–12 (Weeks 35–52): Phase 2 Managed Ops & Phase 3 CRM Inception
* **Gantt Chart Activity Mapping:** Phase 2 (Omnichannel Messaging Integration) - Technical & Administrator Training; Phase 3 (CRM Development) - Requirements Analysis & Study, Architecture Design & Development, Supply, Installation & Configuration.
* **AWS Architectural Focus:** Managing WhatsApp operations while establishing CRM development and isolated schemas on shared high-performance infrastructure to reduce overhead.
* **AWS Services Provisioned:**
  - **Isolated CRM DB Schema:** Configured inside the production RDS instance utilizing Flyway migrations, fully separating CRM tables with strict database roles.
  - **Additional ASG App Targets:** Launch template modified to run specialized CRM JVM profiles on the existing production ASG instances.
  - **Continuous Telemetry Tracking:** Enabled Amazon GuardDuty to monitor account-level DNS abuse and secure IAM roles.
* **Week-by-Week Technical Goals:**
  - **Week 35–38:** Deliver comprehensive operational training on Meta API token rotation.
  - **Week 39–42:** Code backend CRM service APIs and construct robust relational mappings.
  - **Week 43–48:** Deploy database read-replicas inside the isolated database subnets to offload complex CRM query lookups from the write master node.
  - **Week 49–52:** Configure automated nightly snapshots using AWS Backup with cross-region replication.
* **Phase Cost (USD / MYR):** **$1,685.00 USD / RM 7,498.25 MYR** (Production run-rate with nominal storage growth).

---

### Year 2, Months 1–2 (Weeks 53–60): CRM Integration & Go-Live
* **Gantt Chart Activity Mapping:** Phase 3 (CRM Development) - Integration with Internal Systems, System & Integration Testing, Go-Live & Launch, Technical & Administrator Training, Managed Cloud Services & Operations.
* **AWS Architectural Focus:** Securing database performance and ensuring seamless system scaling during the public launch of the CRM system.
* **AWS Services Provisioned:**
  - **AWS Elastic Disaster Recovery (AWS DRS):** Configured as a continuous block-level continuous replication strategy from our on-premises database networks to a secure staging subnet in AWS.
  - **Elastic Load Balancer Routing Rules:** Configured listener paths to route `/crm/*` traffic to a dedicated CRM target group in the ASG.
  - **Amazon Route 53 Health Checks:** Automated DNS failover triggers routing traffic to emergency backup static endpoints.
* **Week-by-Week Technical Goals:**
  - **Week 53–54:** Complete end-to-end integration mapping between CRM fields and internal legacy systems.
  - **Week 55–56:** Run exhaustive database transaction lock verification under a peak stress model.
  - **Week 57–58:** Launch the public CRM portal. Monitor database CPU and Valkey memory metrics closely during the initial cutover.
  - **Week 59–60:** Complete on-boarding training for internal business teams and hand over the final system guides.
* **Phase Cost (USD / MYR):** **$1,720.00 USD / RM 7,654.00 MYR** (Incorporating active AWS DRS replication streams).

---

### Year 2, Months 3–8 (Weeks 61–86): Super Mobile App & High-Performance AI Ingress
* **Gantt Chart Activity Mapping:** Phase 4 (Omnichannel Mobile Application) - Requirements Analysis & Study, Supply, Installation & Configuration, Architecture Design & Development, Integration with Internal Systems, System & Integration Testing, Live Deployment & Go-Live.
* **AWS Architectural Focus:** Introducing heavy-duty AI processing and secure mobile delivery channels to support the Super Mobile App launch.
* **AWS Services Provisioned:**
  - **Amazon CloudFront:** Global Content Delivery Network (CDN) with edge caching to speed up mobile static asset and image retrieval.
  - **AWS WAFv2 on CloudFront:** Move WAF protection to the global CDN edge to block malicious requests before they even reach the ALB.
  - **High-Performance GPU Compute Tier:** 1x Standalone Staging `g5.xlarge` instance (NVIDIA A10G GPU with 24GB VRAM) to execute specialized DeepDoc visual layouts and high-speed OCR.
* **Week-by-Week Technical Goals:**
  - **Week 61–68:** Code hybrid mobile screens in React Native and define the API contract.
  - **Week 69–74:** Provision S3 upload directories and attach CloudFront to bypass API endpoint processing.
  - **Week 75–80:** Connect mobile push notifications through Amazon Simple Notification Service (SNS).
  - **Week 81–84:** Integrate on-device OCR components with our backend GPU compute.
  - **Week 85–86:** Submit the compiled hybrid application to the Apple App Store and Google Play Store, and cutover the production API endpoints.
* **Phase Cost (USD / MYR):** **$2,150.00 USD / RM 9,567.50 MYR** (Peak pricing incorporating heavy GPU compute nodes and CDN data transfers).

---

### Year 2, Month 9 (Weeks 87–90): Mobile App Security Hardening
* **Gantt Chart Activity Mapping:** Phase 4 (Omnichannel Mobile Application) - Security Vulnerability & Pen Testing, Technical & Administrator Training, Managed Cloud Services & Operations.
* **AWS Architectural Focus:** Running deep audits on mobile APIs and locking down security variables before finalizing the development phase.
* **AWS Services Provisioned:**
  - **Standalone Wazuh SIEM Instance:** Sized at `t4g.large` inside the secure management subnet, continuously gathering and auditing Linux logs from all compute nodes.
  - **Amazon Inspector:** Automated security scanning of EC2 instances and container registries.
* **Week-by-Week Technical Goals:**
  - **Week 87:** Trigger a deep penetration test across all public-facing ALB endpoints.
  - **Week 88:** Apply ASIMP Ansible playbooks to ensure 100% compliance with CIS Level 2 benchmarks.
  - **Week 89:** Finalise training for administrative teams on detecting API credential exposure.
  - **Week 90:** Adjust WAF geo-blocking rules to allow traffic exclusively from approved Southeast Asian networks, blocking foreign botnets.
* **Phase Cost (USD / MYR):** **$2,215.71 USD / RM 9,860.00 MYR** (Peak development footprint with active Wazuh security auditing).

---

### Year 2, Months 10–12 (Weeks 91–104): Final Acceptance Test, Project Go-Live & Handover
* **Gantt Chart Activity Mapping:** Final Acceptance Test, Official Unified Project Go-Live, Documentation & Operational Handover, Support & Maintenance Period.
* **AWS Architectural Focus:** Tearing down auxiliary staging environments, cleaning up temporary EBS volumes, and scaling the core Multi-AZ production cluster to its final stable state.
* **AWS Services Provisioned:**
  - **Consolidated Enterprise Production Stack:** Streamlined, secure Multi-AZ configuration.
  - **Amazon CloudWatch Custom Dashboard:** Real-time single-pane visibility for operations teams.
* **Week-by-Week Technical Goals:**
  - **Week 91–94:** Complete formal Client Final Acceptance Testing across all integrated tiers (Chatbot, WhatsApp, CRM, Mobile).
  - **Week 95–98:** Complete the hard cutover of production databases. Deliver final OpenTofu infrastructure codebase files.
  - **Week 99–104:** Establish the 12-month Support & Maintenance framework. Configure Automated Instance Scheduler routines to shut down developer environments outside business hours, saving 64% on idle staging compute!
* **Phase Cost (USD / MYR):** **$1,285.80 USD / RM 5,721.81 MYR** (Optimised, high-availability baseline run-rate).

---

### Year 3: Support, Maintenance & Cost Optimisation (Months 25–36)
* **Gantt Chart Activity Mapping:** Support & Maintenance Period - 12 months.
* **AWS Architectural Focus:** Applying Day-2 financial optimizations to lock in significant savings for the remaining support year.
* **AWS Services Provisioned:**
  - **AWS Savings Plans:** Apply a 1-Year Compute Savings Plan to EC2 instances, cutting compute costs by **34%**.
  - **RDS Reserved Instances:** Secure a 1-Year Reserved Instance for Multi-AZ PostgreSQL, cutting database costs by **30%**.
  - **ElastiCache Reserved Nodes:** Secure a 1-Year Reserved Node for ElastiCache Valkey, saving **35%** on caching.
* **Month-by-Month Technical Goals:**
  - **Months 25–28:** Purchase the Reserved Instances and monitor the billing console to confirm discounts are successfully applied.
  - **Months 29–32:** Run monthly database indexing optimizations to keep storage footprints below 250 GB.
  - **Months 33–36:** Maintain high uptime (>99.99%) and prepare the final cloud transfer of ownership documents.
* **Phase Cost (USD / MYR):** **$945.30 USD / RM 4,206.59 MYR** (Optimised enterprise production run-rate representing **43.2% savings** over standard on-demand pricing).

---

## Comparative AWS Monthly Cost Matrix

The table below breaks down the monthly run-rate (in USD and MYR) across each distinct development milestone phase, showing the incremental growth and financial efficiency of our roadmap:

```
┌─────────────────────────────────┬─────────────────┬─────────────────┬─────────────────────────────────────────────────┐
│ Milestone Phase                 │ Est. Cost (USD) │ Est. Cost (MYR) │ Primary Architectural Changes & Sizing          │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Month 1 (Kick-off)              │ $1.00           │ RM 4.45         │ Initial DNS public zone mapping.                │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Month 2 (Dev Setup)             │ $138.50         │ RM 616.33       │ Single-AZ sandbox: t4g.medium compute,          │
│                                 │                 │                 │ db.t4g.medium PostgreSQL database, Valkey cache.│
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Months 3 - 6 (Staging)          │ $668.11         │ RM 2,973.11     │ Dual-AZ staging: NAT Gateways, ALB routing,     │
│                                 │                 │                 │ 2x c7g.xlarge ASG instances, Multi-AZ RDS.      │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Months 7 - 8 (Chatbot Go-Live)  │ $1,665.61       │ RM 7,411.98     │ High-Performance Prod: AWS WAFv2 layer,         │
│                                 │                 │                 │ db.m7g.xlarge Multi-AZ RDS, Lambda webhooks.    │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Months 9 - 14 (CRM Rollout)     │ $1,720.00       │ RM 7,654.00     │ Adding CRM schemas, RDS read-replicas, and      │
│                                 │                 │                 │ continuous AWS DRS on-premises replication.     │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Months 15 - 20 (Mobile Launch)  │ $2,150.00       │ RM 9,567.50     │ Adding Amazon CloudFront global CDN edge and    │
│                                 │                 │                 │ dedicated GPU-backed g5.xlarge AI parsing nodes.│
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Months 21 - 22 (Security Pen)   │ $2,215.71       │ RM 9,860.00     │ Launching standalone Wazuh SIEM auditor instance│
│                                 │                 │                 │ and executing automated pen-testing suites.     │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Months 23 - 24 (Project Go-Live)│ $1,285.80       │ RM 5,721.81     │ Streamlining production: shutting down staging  │
│                                 │                 │                 │ instances outside business hours.               │
├─────────────────────────────────┼─────────────────┼─────────────────┼─────────────────────────────────────────────────┤
│ Year 3 (Support & Maintenance)  │ $945.30         │ RM 4,206.59     │ Day-2 financial optimization: lock-in 1-Year    │
│                                 │                 │                 │ Savings Plans for 43%+ overall OpEx discount.   │
└─────────────────────────────────┴─────────────────┴─────────────────┴─────────────────────────────────────────────────┘
```

---

## Strategic Recommendations for Phase-by-Phase Rollout

1. **Leverage "Scale-to-Zero" Webhooks Immediately:** In Phase 2, deploy API Gateway and AWS Lambda webhook integrations right from the start. This keeps initial development costs near **$0.00** while ensuring the backend is ready to handle high traffic spikes.
2. **Standardise on Graviton Compute:** Standardise all application EC2 nodes and RDS instances on AWS Graviton (ARM64). This delivers up to **40% better price-performance** compared to x86 equivalents, which directly lowers the run-rate of the Staging and Production phases.
3. **Establish Free PrivateLink S3 Endpoints early:** Create VPC Gateway Endpoints for S3 during Year 1, Month 2. Since the AI Chatbot and CRM download substantial volumes of document/media objects from S3, routing this traffic locally within the VPC avoids NAT Gateway data processing fees ($0.045/GB).
4. **Automate Non-Production Environments:** Enforce a strict non-production schedule starting from Year 1, Month 3. Automatically stopping Staging and Dev environments outside standard Cyberjaya business hours (12 hours/day, 5 days/week) instantly reduces non-production compute costs by **64%**.

---

## Sovereign and Regulatory Pathway Alignment (Malaysian PDPA 2010)

Keeping data secure and compliant with local regulations is a core priority of this phased roadmap:

* **In-Region Sovereign Processing:** In Phase 1 and Phase 2, all AI processing and messaging pathways are securely locked inside the AWS Malaysia region (`ap-southeast-5`). Sensitive citizen communications and metadata never leave the physical boundaries of the Kuala Lumpur data centers.
* **Cryptographic Isolation:** From Phase 3 onwards, all database layers and CloudWatch log directories are encrypted at-rest using customer-managed keys via **AWS KMS**.
* **AWS DRS Secure Replication Compliance:** The continuous replication channels provisioned in Year 2, Month 1 using AWS Elastic Disaster Recovery utilize highly-secure, encrypted TLS 1.3 tunnels. This allows companies to align with the **Malaysian Personal Data Protection Act (PDPA) 2010 Section 129** cross-border restrictions, ensuring backup target paths are fully documented, audited, and compliant.
