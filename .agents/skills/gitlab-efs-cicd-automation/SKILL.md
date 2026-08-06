---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "GitLab CI/CD & EFS Storage Skill"
timestamp: 2026-08-05T22:01:00Z
topics: ["aws", "cloud", "architecture", "skill", "gitlab", "cicd", "efs", "nfs", "nginx"]
description: "Guidelines for implementing GitLab CI/CD pipelines, mounting shared AWS EFS storage, tuning NFS mounts, and configuring dynamic Nginx paths."
name: "gitlab-efs-cicd-automation"
---
# GitLab CI/CD & EFS Storage Skill

This skill governs automated application deployment pipelines, mounting persistent Amazon EFS volumes, and optimizing Nginx caching parameters for shared storage.

---

## 1. GitLab CI/CD & Shared Storage Mounting

- **Pipeline Deployments:** Configure GitLab runner pipelines to automatically deploy applications to Auto Scaling Groups and Standalone instances.
- **Shared Storage:** Mount Amazon Elastic File System (EFS) across all web nodes in the ASG on paths like `/var/www/shared/` to provide immediate, concurrent file sync across scaled instances.
- Ensure EFS target permissions are maintained, and set NFS mount options to `rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport`.

---

## 2. Nginx Path & Metadata Tuning

- **Nginx Config:** Configure Nginx server paths to map static assets directly to the mounted EFS directory.
- **Performance Optimisation:** EFS file operations can introduce latency on metadata-heavy workflows. Tune Nginx using `open_file_cache` directives to cache file descriptors locally and prevent high EFS query rates:
  ```nginx
  open_file_cache max=1000 inactive=20s;
  open_file_cache_valid 30s;
  open_file_cache_min_uses 2;
  open_file_cache_errors on;
  ```

---

## 3. Alternative Pipeline Architectural Models

When scaling beyond EFS-mounted ASGs:
- **S3 Dynamic Pulling:** Instead of standard NFS, configure instances to pull build artifacts directly from Amazon S3 at boot or deployment via SSM Run Command.
- **Docker on AWS ECS:** Containerise the workload and run on ECS Fargate, utilising AWS Fargate task mounts to keep state isolated.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
