---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "AWS Disaster Recovery & Sovereignty Skill"
timestamp: 2026-08-05T21:59:00Z
topics: ["aws", "cloud", "architecture", "skill", "disaster-recovery", "sovereignty", "compliance", "pdpa", "drs"]
description: "Instructions for designing PDPA-compliant In-Region/Cross-Region DR architectures, deploying AWS DRS (Strategy E) replication, and addressing AI sovereignty."
name: "aws-disaster-recovery-sovereignty"
---
# AWS Disaster Recovery & Sovereignty Skill

This skill governs disaster recovery design, sovereignty compliance under the Malaysian Personal Data Protection Act (PDPA) 2010, and AI-workload sovereignty integrations.

---

## 1. PDPA & Sovereignty Compliance Boundaries

- **Local Data Protection:** All deployments must comply with Malaysian PDPA 2010 and the 2025 Cross-Border Personal Data Transfer (CBPDT) Guidelines.
- **Security Safeguards:** Ensure field-level encryption, tokenisation, and cryptographic KMS isolation.
- **Cross-Border Transfers:** Conduct strict Transfer Impact Assessments (TIAs) under PDPA Section 129 if data flows outside Malaysia, prioritizing In-Region DR over Cross-Region alternatives.

---

## 2. Disaster Recovery Strategy Decision Matrix

- **In-Region DR:** Highly recommended for strict local compliance. Utilise AWS `ap-southeast-5` Multi-AZ clustering for instant data replication and failover circuit breakers.
- **Cross-Region DR:** Utilise multi-region backups and continuous replication with KMS cryptographic isolation.
- **AWS DRS (Strategy E - Continuous Replication):** Model continuous asynchronous block-level replication (RPO in seconds, RTO in minutes) from on-premises or cloud servers into a lightweight staging subnet using low-cost `t3.small` replication nodes and gp3 volumes.

---

## 3. RAGFlow + Langfuse Sovereign AI Workloads

- For sensitive generative AI workloads (RAGFlow & Langfuse):
  - DeepDoc and OCR parsing are highly GPU-dependent.
  - Evaluate AWS-native GPU instances vs. local on-premises hardware.
  - Bridge secure hybrid connections using cost-effective API integration or Model Context Protocol (MCP) proxies via AWS API Gateway to access remote compute models without compromising data sovereignty boundaries.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
