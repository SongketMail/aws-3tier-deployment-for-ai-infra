---
layout: "default"
okf_version: "0.2"
type: "reference"
title: "Modernizing Big Data Analytics Architecture: 3-Tier Infra Deployment Blueprint"
timestamp: 2026-08-20T00:00:00Z
topics: ["bda", "lakehouse", "aws", "hybrid", "proxmox", "rke2", "ceph", "mcp"]
sources: ["docs/bda-lakehouse-architecture.md"]
status: "active"
verified: "true"
---
# Modernizing Big Data Analytics Architecture: Establishing an Authoritative Open-Source Single Source of Truth

## Executive Overview & Architectural Context

This architectural blueprint outlines the modernization of a legacy Big Data Analytics (BDA) platform into a 100% open-source enterprise data lakehouse. Designed as an authoritative **Single Source of Truth (SSoT)**, the platform consolidates environmental, geological, hydrological, forestry, and wildlife datasets across multi-departmental enterprise operations.

### Enterprise Assumptions & Public Adaptation
To adapt this enterprise blueprint for public deployment and general industry adoption, all specific public-sector identifiers have been replaced with standard organizational agency designations and internal domain endpoints:
* **Enterprise Environmental Data Platform:** Formerly legacy BDA infrastructure.
* **Internal Endpoints:** Standardized to `https://bda.enterprise.internal` and `https://dashboard.enterprise.internal`.
* **Six (6) Departmental Domains:**
  1. **Department of Wildlife Conservation (DWC):** Handles wildlife encounters, species monitoring, and spatial movement corridors.
  2. **Department of Mineral & Geoscience (DMG - Hydrogeology):** Maps hydrogeological borehole reserves and groundwater potential.
  3. **Department of Mineral & Geoscience (DMG - Geotechnical Landslides):** Calculates slope stability risks and landslide hazard thresholds.
  4. **Department of Forestry (DOF):** Tracks forest fire incidents, biomass susceptibility, and concession boundaries.
  5. **National Water & Climate Institute (NWCI):** Models hydrological vulnerability and climate adaptation indices.
  6. **Meteorological Services Department (MSD) & Global Satellite Thermal Sensing Network (GSTRN):** Serves precipitation curves, weather telemetry feeds, and thermal hotspot alerts.

---

## Architectural Deconstruction of the Legacy BDA Environment

The legacy Big Data Analytics (BDA) platform operated as an early-generation big data deployment characterized by tightly coupled compute and storage architectures, unmanaged database proliferation, fragile point-to-point data ingestion methods, and proprietary visualization systems.

### Legacy Technical Bottlenecks
* **Ingestion Tier:** Dependent on fractured integration pathways. Precipitation data entered via unmonitored local network folder shares; thermal hotspot alerts arrived through unparsed automated emails; geological hazard boundaries were retrieved via point APIs; and departmental datasets were manually transferred over SSH File Transfer Protocol (SFTP) or raw file uploads. Pre-ingestion schema validation, data contracts, and automated provenance tracking were absent.
* **Storage Backbone:** Fragmented across multiple disparate storage fabrics. Distributed file storage was divided between an aging Apache Hadoop cluster—comprising two NameNodes, three DataNodes, and a Network File System (NFS) gateway—and a six-node GlusterFS cluster (`GlusterFS-01` through `GlusterFS-06`).
* **Relational Database Tier:** Split across uncoordinated relational database instances:
  * A high-availability pair of MariaDB nodes (`MariaDB-HA1`, `MariaDB-HA2`) dedicated to web portal management.
  * A five-node MariaDB cluster (`MariaDB-01` through `MariaDB-05`) housing specific data project tables.
  * A three-node PostgreSQL cluster (`Postgresql-app-01` through `Postgresql-app-03`) supporting application state.
  * An independent three-node PostgreSQL cluster (`Postgresql-01` through `Postgresql-03`) executing business queries.
* **Compute Transformations:** Processing ran on legacy Red Hat WildFly application server instances, executing bespoke Java scripts without modern orchestration frameworks or pipeline abstractions.
* **Presentation Tier:** Divided between an end-of-life CMS hosting the primary web portal (`bda.enterprise.internal`), a custom portal (`dashboard.enterprise.internal`), and a proprietary Tableau Server cluster managed by Tableau Server Manager (TSM).

| Legacy Subsystem | Legacy BDA Architecture | Structural Bottlenecks & Failure Modes |
| :--- | :--- | :--- |
| **Ingestion Tier** | Point-to-point SFTP, local folder shares, automated email parsing, manual web uploads. | Absence of schema validation; lack of rate-limiting; silent pipeline failures upon upstream payload modifications; missing audit trails. |
| **Distributed Storage** | Hadoop HDFS (2 NameNodes, 3 DataNodes, NFS), GlusterFS (6 Nodes). | Tight compute-storage coupling; NameNode memory limits on small files; POSIX locking overhead; lack of object-level immutability. |
| **Relational Database Tier** | Disparate MariaDB clusters (7 instances) and PostgreSQL clusters (6 instances). | Siloed datasets; inconsistent business definitions across departments; uncontrolled replication; database maintenance overhead. |
| **Processing & Analytics** | WildFly application servers running custom cleansing and merging scripts. | Monolithic processing engines; lack of parallel distributed compute; inability to handle large geospatial vector calculations efficiently. |
| **Web Portal Tier** | Legacy CMS (Master and 2 HA nodes), custom application servers. | End-of-life CMS vulnerabilities; tightly coupled presentation logic; decentralized user authentication repositories. |
| **Visualization Tier** | Tableau Server cluster (TSM, 3 worker nodes, 2 load balancers, Desktop authoring). | High recurring proprietary licensing fees; vendor lock-in; proprietary workbook formats; restricted external agency sharing. |

---

## Target 100% Open-Source Lakehouse Architecture: Storage & Compute Decoupling

The modern data lakehouse pattern physically and logically decouples persistent storage from distributed compute engines. HDFS and GlusterFS are replaced with S3-compatible object storage clusters governed by an open table format.

### Architectural Foundations
1. **Persistent Object Storage & Immutability Contract:** Uses Ceph (via RADOS Gateway), MinIO Enterprise Object Store, or AWS S3.
   * **Object Lock Retention Contract:** S3 Object Lock enforces documented software guarantees rather than physical/hardware locks. Buckets require **Bucket Versioning** to be enabled. Tier 0 evidence storage enforces a defined retention policy (e.g. 7-year statutory compliance or 365-day operational compliance) in **Compliance Mode** alongside legal-hold toggles for regulatory holds. Tested, equivalent Object Lock retention behaviors are documented and validated across AWS S3, Ceph RADOS Gateway (RGW), and MinIO Enterprise Object Store.
   * **Iceberg Maintenance Separation:** Immutable source/evidence storage is separated from mutable analytical lakehouse tables. Apache Iceberg tables reside in dedicated buckets or partitions configured with **Governance Mode** Object Lock or un-locked object paths, allowing Iceberg catalog maintenance jobs (such as snapshot compaction, orphan file purging, and snapshot expiration) to execute without violating WORM retention rules.
2. **Universal Open Table Format (Apache Iceberg):** Replaces relational sprawl and file directories with Apache Iceberg backed by columnar Parquet files. Iceberg provides ACID transactions, in-place schema evolution, hidden partitioning, and snapshot time-travel querying.
3. **Open Catalog (Apache Polaris / Project Nessie):** Manages table registration and commit resolution via an open Iceberg REST catalog.
4. **Decoupled Distributed Compute:**
   * **Trino:** Massive parallel processing (MPP) SQL query engine executing low-latency queries over Iceberg tables.
   * **Apache Spark + Apache Sedona:** Manages batch transformations, Change Data Capture (CDC), and distributed spatial processing via SpatialRDDs and GeoParquet.
5. **Operational Serving Store:** High-availability PostgreSQL enhanced with PostGIS for sub-millisecond point queries and spatial dashboard caching.

| Architectural Layer | Legacy BDA Infrastructure | Modern Open-Source Replacement | Core Architectural Capabilities |
| :--- | :--- | :--- | :--- |
| **Distributed Object Storage** | Hadoop HDFS, GlusterFS. | Ceph Object Storage / MinIO Object Store / AWS S3. | Horizontal scale-out; unified S3 API; software-enforced WORM S3 Object Lock retention; small-file bottleneck elimination. |
| **Open Table Format** | Unstructured CSV/JSON files, uncoordinated DB tables. | Apache Iceberg (backed by Apache Parquet). | Serialized ACID transactions; schema and partition evolution without data restructuring; snapshot time-travel. |
| **Lakehouse Catalog** | Custom MariaDB schemas, local directories. | Apache Polaris (Incubating) / Project Nessie. | Open REST catalog standard; centralized table metadata; cross-engine concurrency arbitration; credential vending. |
| **Analytical Query Engine** | WildFly application servers, local SQL engines. | Trino Distributed SQL Query Engine. | In-memory massively parallel processing; sub-second analytical SQL execution; multi-catalog federation; CBO optimization. |
| **Geospatial Processing Engine** | Local spatial libraries, fragmented PostGIS instances. | Apache Sedona executing on Apache Spark + GeoParquet. | Distributed spatial indexing (R-Tree, Quad-Tree); distributed spatial joins; native GeoParquet vector processing. |
| **Operational Serving Layer** | Fractured MariaDB and PostgreSQL clusters. | Consolidated HA PostgreSQL with PostGIS extension. | High-concurrency spatial index caching; sub-millisecond point queries; serving boundary layers directly to visualizers. |

---

## Data Provenance, Lineage, and Metadata Architecture: The Human-to-AI Quarantine Model

To guarantee data integrity, the architecture enforces a strict boundary: artificial intelligence assists with automation and query processing but is strictly barred from modifying ground-truth human data.

### Three-Tier Physical & Logical Classification
```
Tier 0: Golden Human Truth (Authoritative SSoT)
└── Immutable storage on MinIO/Ceph/S3 with S3 Object Lock (Compliance Mode)
└── Requires human cryptographic signatures and ODCS contract validation
└── Strictly zero unvalidated AI-generated records permitted

Tier 1: Machine and Sensor Ingestion
└── Storage on standard S3 buckets with Governance Mode Object Lock
└── Direct telemetry feeds: MSD precipitation, NWCI hydrological logs, GSTRN thermal hotspots
└── Pre-ingestion validation via Data Contract CLI; human audit required for promotion

Tier 2: AI Operational and Analytical Sandbox (Isolated Quarantine)
└── Isolated object buckets with automated 30-day S3 Lifecycle expiration policy
└── Ephemeral storage for LLM intermediate runs, synthetic models, and MCP outputs
└── Scheduled CronJob cleanup controller with secure-deletion rules for local volumes
└── Strict access barriers preventing automated writing or promotion to Tier 0
```

### Data Contracts & Lineage Instrumentation
* **Bitol Open Data Contract Standard (ODCS v3.1.0):** Defines schema models, physical data types, nullability rules, geospatial bounding boxes, and mandatory provenance metadata. Incoming payloads violating contracts are diverted to dead-letter quarantine queues.
* **OpenLineage & Custom `enterprise_provenance` Facet:** Captures operational metadata events. The custom `enterprise_provenance` facet records origin types, verification tier, human author identity, AI involvement flags, and SHA-256 payload signatures.

| Governance Parameter | Tier 0: Golden Human SSoT | Tier 1: Machine & Sensor Telemetry | Tier 2: AI Sandbox & Analytics |
| :--- | :--- | :--- | :--- |
| **Primary Institutional Purpose** | Authoritative national truth, statutory policy formulation, certified legal record. | Empirical environmental observation, telemetry aggregation, baseline monitoring. | Exploratory modelling, scenario simulation, predictive risk computation. |
| **Storage Technology & Retention** | Distributed Object Store; S3 Object Lock in Compliance Mode (Versioning enabled). | Distributed Object Store; S3 Object Lock in Governance Mode. | S3-compatible bucket with 30-day S3 Lifecycle purge + CronJob volume cleanup. |
| **Allowable Ingestion Sources** | Certified human domain surveys, gazetted boundaries, signed enterprise records. | Direct telemetry streams: MSD rain gauges, NWCI water sensors, GSTRN hotspots. | Model outputs, MCP pipeline agents, synthetic climate projections. |
| **AI Role & Permissions** | Read-only access via certified tools. Zero automated AI write access permitted. | Machine learning models execute cleansing, deduplication, and anomaly detection. | Unrestricted generative and predictive computation within sandboxed perimeter. |
| **Lineage & Validation Standard** | Mandatory ODCS v3.1.0 contract validation + OpenLineage `enterprise_provenance` signing. | Automated ODCS contract validation + deterministic quality assertion checks. | OpenLineage job execution tracking; outputs permanently tagged as `AI_GENERATED`. |
| **Promotion Criteria** | Terminal authoritative tier; updates require formal versioning and re-signing. | Promoted to Tier 0 only after automated DQ validation and human officer sign-off. | Cannot be promoted directly; requires distillation and formal human certification. |

---

## Model Context Protocol (MCP) and AI Sandboxing: Confining AI to Operational Tooling

The platform implements the **Model Context Protocol (MCP)** (donated by Anthropic to the Agentic AI Foundation under the Linux Foundation) to standardize AI tool interactions over JSON-RPC 2.0 while enforcing strict security containment.

### MCP Primitive Restrictions & Guardrails
* **Resources:** Read-only access to OpenMetadata data dictionaries, schema definitions, and sanitized database views.
* **Tools:** Restricted to stateless operational utilities (SQL linting, contract validation, DAG monitoring). Write verbs (`INSERT`, `UPDATE`, `DELETE`, `DROP`, Iceberg commits) are blocked at the API gateway.
* **Prompts:** Structured, version-controlled interaction templates enforcing governance rules.
* **Security Boundaries:** MCP servers run in isolated containers within a dedicated DMZ. Database connections operate with `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`. Outputs are written strictly to Tier 2 scratch storage (S3-compatible buckets with 30-day S3 Lifecycle expiration rules) and tagged with `ai_generated_data: true`.

| MCP Server Identifier | Business Domain Alignment | Operational Capability | Primitive Scope | Access Permissions & Safeguards |
| :--- | :--- | :--- | :--- | :--- |
| `mcp-catalog-context` | Enterprise metadata management. | Exposes schema definitions, business terms, and lineage graphs to assist analysts. | Resources: `schema://*`<br>Prompts: `glossary_search` | OpenMetadata REST API; Read-only metadata token; zero raw data payload access. |
| `mcp-trino-query-gen` | Departmental analytics & reporting. | Translates natural language queries into optimized ANSI SQL for Trino execution. | Tools: `validate_sql`, `explain_query`<br>Prompts: `sql_assist` | Trino Query Engine; Read-only credentials; execution timeout limited to 30 seconds. |
| `mcp-pipeline-monitor` | Environmental telemetry queues. | Monitors Airflow DAG runs and NiFi queues; identifies bottlenecks and backpressure. | Tools: `get_dag_status`, `read_flow_metrics` | Airflow REST API & NiFi Diagnostics API; Read-only monitoring role. |
| `mcp-contract-linter` | Data governance & ingestion gates. | Validates draft data contracts against ODCS v3.1.0 specifications; analyzes drift. | Tools: `lint_contract`, `diff_schema` | Local isolated container execution; no network egress; ephemeral scratch memory. |

---

## Enterprise Catalog, Governance, IAM, and API Perimeter

* **Enterprise Data Catalog (OpenMetadata):** Powered by PostgreSQL and OpenSearch. Captures column-level lineage, tracks ODCS contracts, supports Tag-Based Access Control (TBAC), and maps geospatial metadata to ISO 19115:2003 standards.
* **Identity & Access Management (Keycloak):** Centralizes authentication via OpenID Connect (OIDC), OAuth 2.0, and SAML 2.0 with Multi-Factor Authentication (MFA) and Single Sign-On (SSO).
* **Perimeter Gateway (Apache APISIX):** Validates JWT tokens, executes dynamic rate-limiting, terminates TLS, and enforces Mutual TLS (mTLS) for inter-service communication.

| Governance Subsystem | Legacy BDA Stack | Open-Source Replacement | Enterprise Capabilities & Operational Advantages |
| :--- | :--- | :--- | :--- |
| **Enterprise Data Catalog** | MariaDB local data dictionaries; unindexed schemas. | OpenMetadata (backed by PostgreSQL & OpenSearch). | Centralized discovery; automated metadata crawlers; column-level lineage; native ODCS integration. |
| **Lineage & Provenance Engine** | Manual documentation, untracked operational scripts. | OpenLineage Standard (with `enterprise_provenance` facet). | Runtime operational lineage capture; automated tracking across Spark, Airflow, and Trino; cryptographic verification. |
| **Identity & Access (IAM)** | Hardcoded credentials, local user tables. | Keycloak Identity & Access Management. | Centralized OIDC / OAuth 2.0; role-based access control (RBAC); Single Sign-On; Multi-Factor Authentication. |
| **API Perimeter Gateway** | Unmanaged load balancers, direct port exposures. | Apache APISIX Cloud-Native API Gateway. | High-performance dynamic routing; perimeter JWT validation; TLS termination; IP whitelisting; DDoS rate-limiting. |
| **Geospatial Governance** | Undocumented local coordinate systems. | OGC / ISO 19115:2003 Metadata Profiles. | Standardized geospatial metadata; formal EPSG projection definitions (RSO Malaya, Borneo, WGS84). |

---

## Ingestion Pipeline Modernization, Application Portal, and Visualization Overhaul

* **Ingestion (Apache NiFi + Apache Airflow):** NiFi handles streaming ingestion, protocol translation, and boundary polling (MSD rainfall, GSTRN thermal satellites). Airflow orchestrates batch processing, contract verification gates, and Iceberg table maintenance.
* **Web Portal Modernization:** Replaces legacy CMS and monoliths with a decoupled **Next.js / React** microfrontend application deployed behind Apache APISIX and Keycloak.
* **Visualization Overhaul (Apache Superset + deck.gl):** Replaces proprietary Tableau Server with Apache Superset. Connects to Trino via SQLAlchemy, leveraging deck.gl for hardware-accelerated 3D geospatial rendering. Keycloak centralizes user identity and issues JWT tokens containing role and departmental claims. When users authenticate to Apache Superset, Keycloak claims map to Superset roles and Security Manager user profiles, which select and apply dataset Row-Level Security (RLS) SQL filter predicates directly in Superset to restrict query results based on user administrative scope.

| Platform Component | Legacy BDA Architecture | Modern Open-Source Replacement | Core Functional Capabilities |
| :--- | :--- | :--- | :--- |
| **Data Ingestion Engine** | Point-to-point SFTP, manual email parsing, shared folders. | Apache NiFi. | Visual flow design, automated protocol translation, built-in backpressure, end-to-end data provenance. |
| **Pipeline Orchestrator** | Static cron schedules, unmonitored WildFly tasks. | Apache Airflow. | Declarative Python DAGs, data contract validation gates, native OpenLineage instrumentation, automated retries. |
| **Public & Admin Portals** | Legacy CMS, custom monolithic application portals. | Containerized Next.js / React Web Application. | Headless modern architecture, responsive component design, zero legacy CMS vulnerabilities, optimized API integration. |
| **Identity & Authentication** | Local MariaDB/PostgreSQL authentication tables. | Keycloak Identity & Access Management. | Unified SSO, OpenID Connect / OAuth 2.0 federation, MFA enforcement, centralized role mapping. |
| **API Management** | Unmanaged load balancers, direct port exposures. | Apache APISIX API Gateway. | Dynamic routing, SSL termination, JWT token validation, rate-limiting, edge request transformation. |
| **Business Intelligence** | Tableau Server cluster (TSM, 3 worker nodes, Desktop). | Apache Superset. | 100% open-source, unlimited user concurrency, native Trino integration, deck.gl spatial analytics, Row-Level Security. |

---

## Three (3) Infrastructure Deployment Solutions

To provide maximum operational flexibility, this architecture is divided into three distinct infrastructure deployment options depending on security requirements, existing hardware, and cloud strategy.

```
                   +-------------------------------------------------------+
                   |       BIG DATA ANALYTICS LAKEHOUSE ARCHITECTURE       |
                   +-------------------------------------------------------+
                                               |
         +-------------------------------------+-------------------------------------+
         |                                     |                                     |
         v                                     v                                     v
+------------------+                  +------------------+                  +------------------+
|    SOLUTION 1    |                  |    SOLUTION 2    |                  |    SOLUTION 3    |
|   ALL IN CLOUD   |                  |    HYBRID AI     |                  | EVERYTHING ON    |
|   (AWS NATIVE)   |                  |     ON-PREM      |                  | PREM (PROXMOX/   |
+------------------+                  +------------------+                  |  RKE2 / CEPH)    |
                                                                            +------------------+
```

---

### Solution 1: All in Cloud (AWS Native & Cloud Managed Services)

Solution 1 deploys the entire Big Data Analytics platform natively within the AWS Cloud infrastructure (specifically optimized for AWS Asia Pacific regions such as `ap-southeast-5` Malaysia).

```
+-----------------------------------------------------------------------------------------------+
|                               SOLUTION 1: ALL IN CLOUD (AWS NATIVE)                           |
|                                                                                               |
|  +--------------------------------+  +--------------------------------+  +-----------------+  |
|  |     INGRESS & GOVERNANCE       |  |      LAKEHOUSE & COMPUTE       |  | CLOUD AI & MCP  |  |
|  | - AWS WAFv2 + CloudFront / ALB |  | - AWS S3 Object Lock (Compliance)|  | - Amazon        |  |
|  | - AWS Cognito / Keycloak (ECS) |  | - AWS Glue / Polaris Catalog   |  |   Bedrock       |  |
|  | - AWS Step Functions / MWAA    |  | - Amazon EMR Serverless Spark  |  | - SageMaker     |  |
|  | - OpenMetadata on Amazon EKS   |  | - Amazon Athena / Trino        |  | - MCP Servers   |  |
|  | - Apache APISIX Gateway (ECS)  |  | - Amazon Aurora Postgres      |  |   on ECS/EKS    |  |
|  +--------------------------------+  +--------------------------------+  +-----------------+  |
+-----------------------------------------------------------------------------------------------+
```

#### Core Components & Cloud Services Mapping
1. **Persistent Cloud Storage (Tier 0, 1, 2):**
   * **Tier 0 SSoT:** Amazon S3 Buckets configured with **S3 Object Lock in Compliance Mode** (Versioning enabled), ensuring software-enforced immutability for golden evidence datasets under defined retention periods (e.g., 7 years).
   * **Tier 1 Telemetry:** Amazon S3 Buckets with S3 Object Lock in Governance Mode for MSD telemetry and satellite data.
   * **Tier 2 AI Sandbox:** Amazon S3 Scratch Buckets with automated S3 Lifecycle Rules configured for 30-day object expiration/auto-purge.
2. **Lakehouse Catalog & Metadata:**
   * **AWS Glue Data Catalog** or **Apache Polaris REST Catalog** hosted on Amazon EKS, managing Apache Iceberg table commits and Parquet file manifests in dedicated buckets.
   * **OpenMetadata** hosted on Amazon EKS (backed by Amazon Aurora PostgreSQL and AWS OpenSearch Service) for enterprise data cataloging and column-level lineage.
3. **Distributed Query & Processing Engines:**
   * **Amazon EMR Serverless (Apache Spark + Apache Sedona):** Executes distributed GeoParquet processing, spatial joins, and batch ETL transformations without server provisioning.
   * **Amazon Athena / Amazon EMR Trino:** Distributed massively parallel SQL query engine over Iceberg tables via Glue/Polaris REST catalog.
   * **Amazon Aurora PostgreSQL (Multi-AZ with PostGIS):** Serves as high-concurrency spatial serving store and low-latency cache for interactive dashboards.
4. **Ingestion & Pipeline Orchestration:**
   * **Amazon Managed Workflows for Apache Airflow (MWAA):** Orchestrates batch pipelines, ODCS data contract CLI validation, and OpenLineage events across all six departmental domains.
   * **Apache NiFi on ECS / EKS:** Handles streaming protocol translations and real-time API polling from external sensor sources.
5. **Perimeter Security, Ingress & Identity:**
   * **AWS WAFv2 + Application Load Balancer (ALB) + AWS CloudFront:** Perimeter protection with rate-limiting and OWASP rules.
   * **AWS Cognito / Keycloak on ECS:** Unified OIDC/OAuth 2.0 authentication and Multi-Factor Authentication.
   * **Apache APISIX on ECS/EKS:** Dynamic routing, mTLS termination, and API rate limiting.
6. **Cloud AI & MCP Sandboxing:**
   * **Amazon Bedrock (Anthropic Claude, Titan) & Amazon SageMaker Endpoints:** Provides foundation models for analytical inferencing.
   * **Containerized MCP Servers on AWS Fargate (ECS) / EKS:** Operates with read-only Aurora/Athena database connections and writes outputs exclusively to S3 Tier 2 scratch buckets.

---

### Solution 2: Hybrid - AI On-Premises (Cloud Lakehouse + On-Prem GPU Infrastructure)

Solution 2 retains the core data lakehouse, storage, and batch processing in the AWS Cloud, while bringing AI inference, RAG embeddings, and LLM processing on-premises on local bare-metal GPU servers.

```
+-----------------------------------------------------------------------------------------------+
|                       SOLUTION 2: HYBRID - AI ON-PREMISES ARCHITECTURE                        |
|                                                                                               |
|   +---------------------------------------+       +---------------------------------------+   |
|   |             AWS CLOUD                 |       |         ON-PREMISES DATA CENTRE       |   |
|   | - AWS S3 Object Lock (Tier 0 SSoT)    |       | - Bare-Metal GPU Servers (H100/A100)  |   |
|   | - AWS Glue / Polaris Catalog          |<=====>| - Local Ollama / vLLM / RAGFlow       |   |
|   | - Amazon EMR / Athena / Trino         |  mTLS | - Local Vector DB (Valkey / Qdrant)   |   |
|   | - Managed Airflow (MWAA) / OpenMetadata| Direct| - On-Prem MCP Servers (Podman/K8s)    |   |
|   | - Aurora Postgres + PostGIS           |Connect| - Local Tier 2 Scratch Storage        |   |
|   +---------------------------------------+       +---------------------------------------+   |
+-----------------------------------------------------------------------------------------------+
```

#### Core Components & Hybrid Separation
1. **Cloud Core Lakehouse (AWS):**
   * **Data Storage:** AWS S3 with WORM S3 Object Lock housing Tier 0 golden records and Tier 1 raw telemetry.
   * **Processing & Querying:** Amazon EMR (Spark + Sedona), Amazon Athena / Trino, and AWS MWAA Airflow running in the cloud.
   * **Catalog & Serving:** AWS Glue / Apache Polaris catalog and Amazon Aurora Postgres + PostGIS serving layer.
2. **On-Premises Dedicated AI Infrastructure:**
   * **Bare-Metal GPU Compute Nodes:** Local enterprise servers equipped with NVIDIA H100, A100, or L40S GPUs running in an on-premises data centre (e.g. Cyberjaya).
   * **Local AI Inference Engine:** **Ollama**, **vLLM**, or **RAGFlow** running in rootless Podman containers or local Kubernetes, serving local LLMs (Qwen, Llama 3, DeepSeek) for natural language processing, vector embedding generation, and dynamic hazard prediction.
   * **Local Vector Caching:** Valkey / Qdrant instance for ultra-fast local vector search.
3. **Hybrid Secure Connectivity & MCP Integration:**
   * **AWS Direct Connect / Dedicated IPsec VPN:** AWS Direct Connect provides a dedicated 1GbE/10GbE private physical circuit (unencrypted by default; MACsec at Layer 2 or an IPsec overlay at Layer 3 can be configured when encryption in transit is selected) or a dedicated IPsec VPN tunnel connecting the on-premises GPU cluster directly to the AWS VPC.
   * **On-Premises MCP Servers:** MCP servers (`mcp-trino-query-gen`, `mcp-catalog-context`) run locally inside the on-prem GPU cluster.
   * **Read-Only Cloud Access Gateways:** On-prem MCP tools query the Cloud Glue/Polaris Catalog and Cloud Trino engine using read-only database credentials over mTLS via Apache APISIX.
   * **Data Quarantine Enforcement:** All AI inferencing occurs on-premises. Model intermediate outputs are stored on local S3-compatible storage (MinIO) configured with a 30-day S3 Lifecycle expiration rule marked as Tier 2 Scratch. AI models have zero write permissions back to Cloud Tier 0 SSoT.

---

### Solution 3: Everything On-Premises using Proxmox VE + RKE2 + Distributed Ceph Storage

Solution 3 provides complete operational sovereignty and zero vendor lock-in by executing 100% of the platform on-premises using **Proxmox Virtual Environment (VE)**, **Rancher Kubernetes Engine 2 (RKE2)**, and a **Distributed Ceph Storage** fabric.

```
+-----------------------------------------------------------------------------------------------+
|               SOLUTION 3: EVERYTHING ON-PREM (PROXMOX VE + RKE2 + CEPH SDS)                   |
|                                                                                               |
|  +-----------------------------------------------------------------------------------------+  |
|  |                          PROXMOX VE HYPERVISOR CLUSTER (PVE)                            |  |
|  |  +-----------------------+   +-----------------------+   +---------------------------+  |  |
|  |  | 4x AI / GPU Nodes     |   | 4x Application Nodes  |   | 3x Database / State Nodes |  |  |
|  |  | (PCIe GPU Passthrough)|   | (RKE2 Worker Nodes)   |   | (Postgres Patroni / OSDs) |  |  |
|  |  +-----------┬-----------+   +-----------┬-----------+   +-------------┬-------------+  |  |
|  +--------------│---------------------------│-----------------------------│----------------+  |
|                 │                           │                             │                   |
|                 v                           v                             v                   |
|  +-----------------------------------------------------------------------------------------+  |
|  |                       DISTRIBUTED SOFTWARE-DEFINED STORAGE (CEPH SDS)                   |  |
|  |  - Ceph RBD (Block Storage)    - CephFS (Shared Storage)   - RADOS GW (S3 WORM Buckets)   |  |
|  +-----------------------------------------------------------------------------------------+  |
|                                             |                                                 |
|                 +---------------------------+---------------------------+                     |
|                 v                                                       v                     |
|  +----------------------------------------+           +------------------------------------+  |
|  | RKE2 MAIN CLUSTER (14 VM NODES)        |           | K3S SUPPORTING CLUSTER (5 VM NODES)|  |
|  | - 3x Control Plane (HA etcd)           |           | - 3x Control Plane                 |  |
|  | - 4x AI GPU Nodes (Ollama/RAGFlow)     |           | - 2x Worker Nodes                  |  |
|  | - 4x App Nodes (NiFi/Airflow/Superset)  |           | - Prometheus, Grafana, Loki        |  |
|  | - 3x DB Nodes (Patroni Postgres)       |           | - HashiCorp Vault, CI/CD Runners   |  |
|  +----------------------------------------+           +------------------------------------+  |
+-----------------------------------------------------------------------------------------------+
```

#### 1. Hypervisor & Compute Infrastructure (Proxmox VE)
* **Proxmox VE Cluster Sizing & Host Topology:** High-density enterprise hypervisor cluster comprising **11 physical Proxmox VE hosts** (4x AI/GPU hosts, 4x Application hosts, 3x Database/Stateful hosts) with a 100GbE data plane and 10GbE out-of-band management plane.
* **VM Sizing & Anti-Affinity Rules:** The 14 virtualized RKE2 production nodes and 5 virtualized K3s management nodes execute as Virtual Machines (VMs) provisioned across the 11 physical PVE hosts. Strict Proxmox VE VM anti-affinity rules are enforced across physical hosts to prevent single points of failure (SPOFs) (e.g. no two RKE2/K3s control-plane VMs or Patroni DB VMs reside on the same physical PVE host), reserving host CPU/RAM capacity to guarantee high availability.
* **PCIe GPU Passthrough:** Direct hardware assignment of NVIDIA H100/A100/L40S GPUs to virtualized AI worker VMs, bypassing hypervisor overhead for maximum matrix math performance.

#### 2. Dual-Cluster Open-Source Kubernetes Architecture (RKE2 & K3s)
* **Cluster A: Main Production Cluster (14 VM Nodes - RKE2):**
  * Built on Rancher Kubernetes Engine 2 (RKE2 v1.30.x series, e.g. v1.30.4+rke2r1, following upstream Kubernetes 1.30 ~12-month support window). When FIPS 140-2 compliance is required, RKE2 is deployed using its bundled Canal CNI with FIPS-validated cryptographic modules; when eBPF performance and advanced networking are required, Cilium CNI is selected.
  * **3x Control Plane / Server VM Nodes:** High-Availability etcd quorum (`rke2-cp-01` to `03`).
  * **4x AI / GPU Worker VM Nodes:** Executes Ollama, vLLM, RAGFlow, and Spark/Sedona distributed spatial workloads (`rke2-worker-ai-01` to `04`).
  * **4x Application / Microservices Worker VM Nodes:** Hosts Apache NiFi, Airflow, APISIX, Keycloak, Superset, Next.js, and Trino engines (`rke2-worker-app-01` to `04`).
  * **3x Database & Stateful Worker VM Nodes:** Hosts PostgreSQL Patroni nodes and local Ceph OSD storage daemons (`rke2-worker-db-01` to `03`).
* **Cluster B: Supporting Services Cluster (5 VM Nodes - K3s):**
  * Built on lightweight K3s (v1.30.x series, e.g. v1.30.4+k3s1).
  * **3x Control Plane VM Nodes** (`k3s-mgmt-01` to `03`).
  * **2x Dedicated Worker Agent VM Nodes** (`k3s-worker-01` to `02`) hosting Prometheus, Grafana, Loki, HashiCorp Vault, and local CI/CD runners.

#### 3. Distributed Software-Defined Storage (Ceph SDS)
* **Integrated Ceph Cluster:** Deployed via Proxmox VE / Rook-Ceph across dedicated NVMe/SSD storage pools.
* **RADOS Gateway (S3 Object Storage):** Supplies S3-compatible APIs. Buckets configured with **S3 Object Lock in Compliance Mode** (Versioning enabled) provide software-enforced WORM storage for Tier 0 SSoT records under defined retention periods (e.g., 7 years). Tested, equivalent Object Lock retention behavior is validated across AWS S3, Ceph RGW, and MinIO.
* **Storage Provisioning Types:**
  * **Ceph CSI (`rbd.csi.ceph.com`):** High-IOPS dynamic block storage (ReadWriteOnce / RWO) for PostgreSQL databases, vector indices, and stateful pods.
  * **CephFS (`cephfs.csi.ceph.com`):** Distributed filesystem (ReadWriteMany / RWX) for shared media assets and queue spools.
  * **NFS External Provisioner (`nfs-subdir-external-provisioner`):** Secondary ReadWriteMany (RWX) storage array for legacy shared assets.
  * **Local Path Provisioner:** Ultra-low latency node-local NVMe storage for ephemeral Tier 2 AI scratchpads, managed with an automated CronJob cleanup controller enforcing secure-deletion rules.

#### 4. Complete On-Premises Open-Source Software Stack
* **Object Store & Catalog:** Ceph RADOS Gateway / MinIO + Apache Polaris / Project Nessie REST Catalog on RKE2.
* **Compute & Processing:** Trino Distributed MPP Query Engine + Apache Spark & Sedona on RKE2.
* **Operational Database:** High-Availability PostgreSQL 17 managed by Patroni with etcd, pg_backrest, and PostGIS extension.
* **Ingestion & Orchestration:** Apache NiFi + Apache Airflow DAGs with Data Contract CLI and OpenLineage hooks.
* **Ingress, IAM & Governance:** Apache APISIX Gateway + Keycloak OIDC IAM + OpenMetadata catalog.
* **AI & Local Inference:** Local Ollama / vLLM + RAGFlow on GPU Nodes + Containerized MCP Servers.
* **Presentation:** Next.js / React Web Application + Apache Superset with deck.gl spatial maps.

| Storage Provisioner | Access Mode | Resiliency & HA Profile | Target Workloads | OS Dependencies | Performance Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ceph CSI (RBD)** | ReadWriteOnce (RWO) | Multi-node OSD replication, dynamic failover. | PostgreSQL / Patroni, Vector DBs, Stateful Apps. | `ceph-common`, `rbd` module | High IOPS, Low Latency, Distributed HA. |
| **Ceph CSI (CephFS)** | ReadWriteMany (RWX) | Multi-MDS HA filesystem, distributed replication. | Shared media streams, raw file attachments. | `ceph-common` | Medium-High IOPS, Shared Filesystem. |
| **NFS External** | ReadWriteMany (RWX) | Single NFS server (SPOF unless hardware appliance). | Shared config files, static assets. | `nfs-common` / `nfs-utils` | Low-Medium IOPS, File Locking Bottleneck. |
| **Local Path** | ReadWriteOnce (RWO) | Bound to single host disk (No node failover). | Kafka, Elasticsearch, Ephemeral Tier 2 AI Scratch. | None (Standard filesystem mount) | Maximum Raw NVMe IOPS, Sub-millisecond. |

---

## Phased Migration Strategy & Implementation Roadmap

```
Phase 1: Foundation & Dual Ingestion (Months 1–3)
└── Deploy Ceph/MinIO with S3 Object Lock; stand up Polaris and OpenMetadata
└── Deploy Apache NiFi to mirror external feeds (MSD, GSTRN) into object storage
└── Run mirrored ingestion alongside legacy systems without operational impact

Phase 2: Compute Modernization & Data Contract Enforcement (Months 4–6)
└── Deploy Trino, Apache Spark, and Apache Sedona compute clusters
└── Formalize ODCS v3.1.0 data contracts across all six departmental domains
└── Execute parallel Spark jobs to migrate legacy data into Apache Iceberg format
└── Integrate OpenLineage runtime emission across Airflow DAGs

Phase 3: AI Operational Sandboxing & MCP Deployment (Months 7–9)
└── Deploy containerized MCP servers with read-only database connections
└── Configure isolated Tier 2 scratch storage with automated 30-day TTLs
└── Restrict AI interactions to operational tooling and schema discovery
└── Enforce cryptographic verification gates for promoting data to Tier 0

Phase 4: Presentation Cutover & Legacy Decommissioning (Months 10–12)
└── Deploy Apache Superset and migrate Tableau dashboards to deck.gl views
└── Launch containerized Next.js web application behind APISIX and Keycloak
└── Validate 30-day parallel operational run across all six departmental domains
└── Decommission Hadoop, GlusterFS, MariaDB, WildFly, Joomla, and Tableau
```

| Implementation Phase | Target Legacy Subsystems | Modern Open-Source Replacements | Operational Risk Factors | Technical Mitigation & Fallback Procedures |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Foundation & Dual Ingestion (Months 1–3)** | Point-to-point SFTP, local folder shares, manual email ingestion. | Ceph / MinIO (WORM), Apache Polaris, OpenMetadata, Apache NiFi. | Upstream format modifications during mirroring; network saturation at boundary. | Operate NiFi in non-intrusive listening mode; legacy production paths remain authoritative; allocate isolated NICs. |
| **Phase 2: Compute & Contract Migration (Months 4–6)** | Hadoop HDFS, GlusterFS, MariaDB/Postgres project stores, WildFly. | Apache Iceberg, Trino, Apache Spark + Sedona, Data Contract CLI. | Data truncation or encoding errors during historical Iceberg Parquet conversions. | Execute automated row-count and partition checksum verifications; preserve raw source stores in read-only mode across all 6 domains. |
| **Phase 3: AI Sandboxing & MCP Deploy (Months 7–9)** | Unmonitored administrative scripts, ad-hoc Python workflows. | Model Context Protocol servers, Keycloak IAM, Tier 2 Sandbox. | Over-privileged AI agents attempting schema adjustments or unauthorized queries. | Enforce read-only database connections; block write verbs at API gateway; isolate MCP network routes. |
| **Phase 4: Cutover & Decommissioning (Months 10–12)** | Tableau Server cluster, legacy CMS, custom application portals. | Apache Superset (deck.gl), Next.js / React portal, Apache APISIX. | Discrepancies between Tableau and Superset spatial maps; user resistance to new UI. | Run 30-day side-by-side verification runs across all 6 departmental domains; validate geospatial rendering against PostGIS base layers; conduct agency training. |

---

## Strategic Architectural Conclusions

The modernization of the Big Data Analytics platform establishes a scalable, 100% open-source data lakehouse designed to serve as an authoritative Single Source of Truth for enterprise data management.

### Key Architectural Takeaways
1. **Complete Compute-Storage Decoupling:** Moving to S3-compatible object storage (Ceph/MinIO/AWS S3) and distributed engines (Trino/Spark/Sedona) eliminates Hadoop NameNode memory limits, POSIX file locking overhead, and relational database sprawl.
2. **Absolute Data Integrity & Immutability:** Apache Iceberg delivers serialized ACID transactions, snapshot time-travel, and schema evolution. Software-enforced S3 Object Lock in Compliance Mode guarantees WORM retention for Tier 0 golden records.
3. **Strict Human-to-AI Quarantine:** The architecture enforces a rigid separation between certified human knowledge (Tier 0) and AI outputs (Tier 2). Artificial intelligence operates strictly as operational tooling via Model Context Protocol (MCP) servers with read-only database roles, preventing automated AI pollution of master datasets.
4. **Flexible Deployment Topologies:** Organizations can deploy via **Solution 1 (All in Cloud on AWS)**, **Solution 2 (Hybrid Cloud Core + On-Prem GPU Cluster)**, or **Solution 3 (100% Sovereign On-Premises via Proxmox VE, RKE2, and Ceph SDS)** without changing data models or application interfaces.
5. **Zero Vendor Lock-In:** Replacing proprietary tools (Tableau, proprietary CMS) with Apache Superset, Next.js, Keycloak, and Apache APISIX eliminates recurring seat licensing, ensures compliance with open standards (Bitol ODCS, OpenLineage, OGC/ISO 19115:2003), and provides full operational autonomy.

---

Deep State of Mind (DSOM) For My AI Protocol | Enterprise Big Data Lakehouse Architecture Blueprint | 2026-08-20
Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0
