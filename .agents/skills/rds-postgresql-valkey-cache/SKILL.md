---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "RDS PostgreSQL & ElastiCache Valkey Skill"
timestamp: 2026-08-05T21:57:00Z
topics: ["aws", "cloud", "architecture", "skill", "rds", "postgresql", "valkey", "elasticache", "cache"]
description: "Instructions for configuring RDS PostgreSQL Multi-AZ databases, setting up ElastiCache for Valkey caching clusters, and maintaining port-level network isolation."
name: "rds-postgresql-valkey-cache"
---
# RDS PostgreSQL & ElastiCache Valkey Skill

This skill governs database clustering, caching integration, port isolation, and pricing choices for RDS PostgreSQL and Amazon ElastiCache for Valkey in `ap-southeast-5`.

---

## 1. Multi-AZ RDS PostgreSQL Settings

- Always deploy RDS PostgreSQL in a Multi-AZ cluster configuration to guarantee high availability and sub-minute failover.
- **Port Isolation:** Strictly limit ingress on port `5432` to the active ASG compute security groups and standalone nodes. No public routes are allowed.
- Keep PostgreSQL tuned using dedicated DB Parameter Groups configured natively via the RDS module.

---

## 2. Amazon ElastiCache for Valkey Caching

- **License Compliance & Cost-Optimization:** Use Valkey as a modern, license-compliant replacement for Redis OSS. It delivers 20% lower on-demand pricing ($0.0128/hr for `cache.t4g.micro` in Malaysia).
- **Security:** Enable both transit and at-rest encryption, and configure a dedicated ElastiCache Subnet Group. Limit ingress strictly to compute nodes on port `6379`.

---

## 3. PostgreSQL Self-Hosted vs. RDS Comparison

When evaluating RDS vs self-hosted Percona Server on EC2:
- RDS Postgres provides managed Multi-AZ replication, automatic patching, and Performance Insights.
- Percona Server on EC2 requires setting up Patroni for high-availability clustering, PgBouncer for connection pooling, and Percona Monitoring and Management (PMM) for telemetry, resulting in higher operational overhead despite cheaper raw compute.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
