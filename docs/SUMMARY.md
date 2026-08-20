---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Table of contents"
timestamp: 2026-08-13T14:56:34Z
topics: ["aws", "cloud", "architecture", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "route53", "dns", "disaster-recovery", "gitlab", "efs", "postgresql", "gpu", "ragflow", "langfuse", "sovereignty"]
---
# Table of contents

* [Home](README.md)
* [Start Here Guide](start-here.md)
* [Legal Notice & Disclaimer](legal-notice.md)

## Tutorials
* [Quickstart: Operating Project Utilities](tutorials/quickstart.md)

## How-To Guides
* [How-To: Standardising Metadata](how-to/manage-metadata.md)
* [How-To: Compiling LLM Curation Formats](how-to/generate-llms-xml.md)

## Reference Specs
* [Reference: prepare_docs.py Spec](reference/prepare_docs.md)
* [Reference: parse_llms.py Spec](reference/parse_llms.md)
* [Reference: Bash & PDF Scripts](reference/bash_scripts.md)

## Explanation & Design
* [Explanation: The Diátaxis Framework](explanation/diataxis.md)
* [Explanation: Automation Architecture](explanation/automation_architecture.md)

## Architecture & Infrastructure Guides
* [System Architecture](architecture.md)
* [AWS Phased Adoption Roadmap](aws-adoption-roadmap.md)
* [Disaster Recovery & Sovereignty](dr-options.md)
* [Load Testing Assumptions & Sizing Guide](load-test-assumptions.md)
* [Strategic Comparative Review (AWS vs. Self-Hosted)](aws-vs-self-hosted-review.md)
* [Technology Stack Comparison](tech-stack-comparison.md)
* [AWS vs. On-Premises Open-Source Stack Comparison](aws-vs-onprem-stack-comparison.md)
* [Wazuh Standalone Installation](wazuh.md)
* [Wazuh SIEM & XDR Deep-Dive](wazuh-detailed.md)
* [PostgreSQL Comparison (RDS vs. Percona)](postgresql-comparison.md)
* [Redis vs. Valkey Comparison](redis-vs-valkey.md)
* [RAGFlow + Langfuse GPU Guide](ragflow-langfuse.md)
* [GitLab EFS CI/CD Integration](gitlab-efs-cicd.md)
* [Secure Jumphost Hardening](jumphost.md)
* [Route 53 & DNS Troubleshooting](route53.md)
* [Context7 AI Chat Integration](context7.md)

## Onsite On-Premises Volume
* [Onsite On-Premises Portal](onprem/index.md)
* [VM & Network Architecture](onprem/architecture.md)
* [Rootless Podman 5+ & systemd Quadlets](onprem/podman-quadlet.md)
* [On-Premises Infrastructure with Ansible](onprem/ansible-orchestration.md)
* [Open-Source Containerized Stack Specs](onprem/open-source-stack.md)
* [Enterprise Percona Server Setup](onprem/percona-postgresql.md)

## Security Posture & Audits
* [SPA Checklist](audits/security-posture-assessment.md)
* [Output of ASIMP](audits/asimp-output.md)
* [Output of Lynis](audits/lynis-output.md)
* [Output of OpenSCAP](audits/openscap-output.md)

## OpenTofu Submodules
* [VPC Module](modules/vpc.md)
* [Security Groups Module](modules/security_groups.md)
* [WAF Module](modules/waf.md)
* [ALB Module](modules/alb.md)
* [ASG Module](modules/asg.md)
* [RDS Module](modules/rds.md)
* [Standalone EC2 Module](modules/standalone_ec2.md)
* [ElastiCache Valkey Module](modules/elasticache.md)
* [Jumphost Module](modules/jumphost.md)
