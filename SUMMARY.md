---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Table of contents"
timestamp: 2026-08-13T15:00:00Z
topics: ["aws", "cloud", "architecture", "vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "route53", "dns", "disaster-recovery", "gitlab", "efs", "postgresql", "gpu", "ragflow", "langfuse", "sovereignty"]
---
# Table of contents

* [Home](README.md)
* [Start Here Guide](START-HERE.md)
* [Legal Notice & Disclaimer](docs/legal-notice.md)

## Tutorials
* [Quickstart: Operating Project Utilities](docs/tutorials/quickstart.md)

## How-To Guides
* [How-To: Standardising Metadata](docs/how-to/manage-metadata.md)
* [How-To: Compiling LLM Curation Formats](docs/how-to/generate-llms-xml.md)

## Reference Specs
* [Reference: prepare_docs.py Spec](docs/reference/prepare_docs.md)
* [Reference: parse_llms.py Spec](docs/reference/parse_llms.md)
* [Reference: Bash & PDF Scripts](docs/reference/bash_scripts.md)

## Explanation & Design
* [Explanation: The Diátaxis Framework](docs/explanation/diataxis.md)
* [Explanation: Automation Architecture](docs/explanation/automation_architecture.md)

## Architecture & Infrastructure Guides
* [System Architecture](docs/architecture.md)
* [AWS Phased Adoption Roadmap](docs/aws-adoption-roadmap.md)
* [Disaster Recovery & Sovereignty](docs/dr-options.md)
* [Load Testing Assumptions & Sizing Guide](docs/load-test-assumptions.md)
* [Strategic Comparative Review (AWS vs. Self-Hosted)](docs/aws-vs-self-hosted-review.md)
* [Technology Stack Comparison](docs/tech-stack-comparison.md)
* [AWS vs. On-Premises Open-Source Stack Comparison](docs/aws-vs-onprem-stack-comparison.md)
* [Wazuh Standalone Installation](docs/wazuh.md)
* [Wazuh SIEM & XDR Deep-Dive](docs/wazuh-detailed.md)
* [PostgreSQL Comparison (RDS vs. Percona)](docs/postgresql-comparison.md)
* [Redis vs. Valkey Comparison](docs/redis-vs-valkey.md)
* [RAGFlow + Langfuse GPU Guide](docs/ragflow-langfuse.md)
* [GitLab EFS CI/CD Integration](docs/gitlab-efs-cicd.md)
* [Secure Jumphost Hardening](docs/jumphost.md)
* [Route 53 & DNS Troubleshooting](docs/route53.md)
* [Context7 AI Chat Integration](docs/context7.md)

## Onsite On-Premises Volume
* [Onsite On-Premises Portal](docs/onprem/index.md)
* [VM & Network Architecture](docs/onprem/architecture.md)
* [Rootless Podman 5+ & systemd Quadlets](docs/onprem/podman-quadlet.md)
* [On-Premises Infrastructure with Ansible](docs/onprem/ansible-orchestration.md)
* [Open-Source Containerized Stack Specs](docs/onprem/open-source-stack.md)
* [Enterprise Percona Server Setup](docs/onprem/percona-postgresql.md)

## Security Posture & Audits
* [SPA Checklist](docs/audits/security-posture-assessment.md)
* [Output of ASIMP](docs/audits/asimp-output.md)
* [Output of Lynis](docs/audits/lynis-output.md)
* [Output of OpenSCAP](docs/audits/openscap-output.md)

## OpenTofu Submodules
* [VPC Module](docs/modules/vpc.md)
* [Security Groups Module](docs/modules/security_groups.md)
* [WAF Module](docs/modules/waf.md)
* [ALB Module](docs/modules/alb.md)
* [ASG Module](docs/modules/asg.md)
* [RDS Module](docs/modules/rds.md)
* [Standalone EC2 Module](docs/modules/standalone_ec2.md)
* [ElastiCache Valkey Module](docs/modules/elasticache.md)
* [Jumphost Module](docs/modules/jumphost.md)
