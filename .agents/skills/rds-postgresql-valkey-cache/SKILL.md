---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "RDS PostgreSQL & ElastiCache Valkey Skill"
timestamp: 2026-08-05T21:57:00Z
topics: ["aws", "cloud", "architecture", "skill", "rds", "postgresql", "valkey", "elasticache", "cache", "percona", "patroni", "langfuse", "ragflow"]
description: "Instructions for configuring RDS PostgreSQL Multi-AZ databases, setting up ElastiCache for Valkey caching clusters, and maintaining port-level network isolation."
name: "rds-postgresql-valkey-cache"
---
# RDS PostgreSQL & ElastiCache Valkey Skill

This skill governs database clustering, caching integration, port isolation, and pricing choices for RDS PostgreSQL and Amazon ElastiCache for Valkey in `ap-southeast-5`.

---

## 1. Multi-AZ RDS PostgreSQL Settings & Port Isolation

- Always deploy RDS PostgreSQL in a Multi-AZ cluster configuration to guarantee high availability and sub-minute failover.
- **Port Isolation:** Strictly limit ingress on port `5432` to the active ASG compute security groups and standalone nodes. No public routes are allowed.
- **Default Database Ingress:** The default value of the `db_port` variable in the security groups module (`terraform/modules/security_groups/variables.tf`) is aligned and configured to `5432` to natively support PostgreSQL-based database engine configurations (as per **Item 44**).
- Keep PostgreSQL tuned using dedicated DB Parameter Groups configured natively via the RDS module.

---

## 2. Amazon ElastiCache for Valkey Caching

- **License Compliance & Cost-Optimization:** Use Valkey as a modern, license-compliant replacement for Redis OSS. It delivers 20% lower on-demand pricing ($0.0128/hr for `cache.t4g.micro` in Malaysia).
- **Valkey Strategic & Licensing Advantages:** A comprehensive comparison guide (`docs/redis-vs-valkey.md`) documents the strategic, licensing (BSD-3-clause LF vs RSALv2/SSPLv1), and cloud/on-premise deployment advantages of Valkey over Redis, including a 20% lower on-demand cost comparison on AWS `ap-southeast-5` (as per **Item 9**).
- **Security:** Enable both transit and at-rest encryption, and configure a dedicated ElastiCache Subnet Group. Limit ingress strictly to compute nodes on port `6379`.

---

## 3. Database & Cache Stack Technical Comparisons

- **PostgreSQL Self-Hosted vs. RDS Comparison:** When evaluating RDS vs self-hosted Percona Server on EC2:
  - RDS Postgres provides managed Multi-AZ replication, automatic patching, and Performance Insights.
  - Percona Server for PostgreSQL 17 is documented at `docs/onprem/percona-postgresql.md` as an enterprise on-premises high availability database stack utilizing Patroni for cluster management, etcd as a distributed consensus store, pg_backrest for backups, and HAProxy for load balancing, highlighting its binary compatibility and seamless migration from upstream PostgreSQL 17 (as per **Item 12**).
- **Technology Stack Comparison:** The Technology Stack Comparison Guide (`docs/tech-stack-comparison.md`) compares the local containerized developer stack (Spring Boot, React, React Native, Redis, PostgreSQL, RAGFlow, Twilio, Meta) against AWS managed equivalents (as per **Item 50**).
- **Licensing & Tech Risk Register:** The Risk Register (`docs/licensing-risks.md`) tracks critical risk/decision codes such as self-hosted database operations (TS-06), Qwen3 LLM inference via Amazon Bedrock (MC-01), and Qwen3 embedding indexing (MC-02) (as per **Item 46**).

---

## 4. Real-World Scaling Examples & Benchmarks

When designing high-throughput environments, refer to production benchmarks and architectural constraints outlined in the Load Testing Assumptions & Sizing Guide (`docs/load-test-assumptions.md`):
- **Langfuse Scaling:** Handles V3/V4 ClickHouse denormalized migrations and Valkey queue sharding for trace processing.
- **RAGFlow Scaling:** Focuses on DeepDoc OCR GPU sizing and resolving Issue #12526 synchronous retrieval bottlenecks with comparative pro/con layer analysis and active reference links (as per **Item 25**).

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
