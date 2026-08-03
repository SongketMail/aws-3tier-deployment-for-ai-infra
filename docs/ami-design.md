---
layout: default
title: "Amazon Machine Images (AMI) Design Guide"
---

# Amazon Machine Images (AMI) Design & Hardening Guide

This document describes the **Amazon Machine Images (AMI)** strategy for our Auto Scaling Groups (ASGs). It outlines why custom, pre-baked AMIs are essential for stateless, rapid autoscaling, how to automate AMI construction using HashiCorp Packer and Ansible, and how the **ASIMP** auditing and hardening framework is integrated into the baking pipeline.

---

## 1. Why Pre-Baked AMIs are Critical for Auto Scaling

When an Auto Scaling Group (ASG) detects a surge in CPU utilization or network traffic, it immediately spins up new EC2 instances to share the workload.

If your application depends on a **just-in-time bootstrapping** approach (e.g., executing shell scripts in `user_data` that fetch package updates, download heavy language model weights, install dependencies, and compile binaries at boot-time), you introduce several critical failure modes:
1. **Unacceptable Latency:** Bootstrapping heavy applications can take 10 to 15 minutes. By the time the instance is healthy and added to the ALB target group, the peak load may have already overwhelmed the existing fleet.
2. **External Dependency Failure:** If an external package repository (e.g., Ubuntu APT servers, PyPI, or GitHub) experiences temporary downtime, the newly launched instance will fail to bootstrap, leaving your cluster unable to scale.
3. **Inconsistent Environments:** Multi-instance scaling can result in nodes running slightly different versions of minor packages if updates occurred between launch events.

### The Immutable Infrastructure Paradigm
To solve this, we employ **Immutable Infrastructure** via custom **pre-baked AMIs**.

All software, libraries, configuration files, and system security controls are installed and validated *during the image building phase*. When the ASG scales out, the instance launches from the pre-baked AMI and transitions to a ready-to-run state in **under 45 seconds**, with zero runtime network dependency for configuration.

---

## 2. AMI Requirements Matrix per ASG Tier

To maintain clean separation of concerns and avoid bloated monolithic images, we define three specific, pre-baked AMIs built on top of **Ubuntu 26.04 LTS**:

```
                       [ Ubuntu 26.04 LTS Base AMI ]
                                     │
                        ┌────────────┼────────────┐
                        ▼            ▼            ▼
                   [ Frontend ]  [ Backend ]   [ AI Tier ]
                   • Nginx       • Node.js     • Docker
                   • Syslog      • Python      • Model Cache
                   • ASIMP       • ASIMP       • ASIMP
```

### A. Frontend Nginx Web Server AMI (`ami-frontend-*`)
* **Purpose:** Serves as the high-throughput reverse proxy and static content host.
* **Pre-Baked Software:**
  - Nginx (optimized with HTTP/2 and custom buffer limits).
  - AWS CloudWatch Agent (pre-configured to stream Nginx access and error logs).
  - **ASIMP Hardening:** Restricted SSH configuration, system account lockdowns, and local firewall parameters.

### B. Backend App Tier AMI (`ami-backend-*`)
* **Purpose:** Runs the Backend, Document Management System (DMS), and Model Context Protocol (MCP) APIs.
* **Pre-Baked Software:**
  - Runtime Environments: Node.js (LTS), Python 3.12+, and package managers (`npm`, `pip`).
  - Git client and database connectors (for AWS RDS PostgreSQL communication).
  - Application source code and systemd service handlers.
  - **ASIMP Hardening:** Deep process limits (`limits.conf`), disabling of unused filesystem modules, and standard secure SSH ciphers.

### C. AI Tier RAGFlow + LangFuse AMI (`ami-ai-*`)
* **Purpose:** Executes computation-heavy RAG processing, embeddings generation, and observability flows.
* **Pre-Baked Software:**
  - Docker Engine and Docker Compose (highly optimized for Graviton/ARM64 architectures).
  - Local caching directories mounted and configured for Hugging Face and SentenceTransformers model weights (accelerates initialization).
  - Container images pre-pulled and cached locally inside Docker storage.
  - **ASIMP Hardening:** Kernel parameter tuning (`sysctl.conf`), container isolation profiles, and CIS Level 2 compliance benchmarks.

---

## 3. AMI Build Pipeline with Packer & ASIMP Hardening

We automate our AMI builds using **HashiCorp Packer** combined with **ASIMP (Ansible System Integrity Management Platform)** as the primary configuration provisioner. This guarantees that every pre-baked image is audited and hardened against standard security benchmarks prior to distribution.

### The Immutable Build Workflow
1. **Initialize:** Packer spins up a temporary EC2 instance in a private build subnet using the base Canonical Ubuntu 26.04 LTS AMI.
2. **Provision:** Ansible executes the ASIMP playbooks against the temporary instance.
3. **Auditing (Pre-Harden & Post-Harden):**
   - ASIMP performs an initial security baseline scan using **OpenSCAP** (CIS Level 2) and **Lynis**.
   - ASIMP applies automated upgrades, validates system package integrity via `debsums`, configures secure SSH protocols (Dev-Sec), and implements fine-grained kernel modifications.
   - ASIMP re-runs the security scans, computes the comparative score improvement, logs metrics in `/var/log/asimp-baseline-scores.json`, and outputs visual HTML reports to `/var/log/openscap-after-report.html`.
4. **Bake:** Packer stops the temporary instance, takes a snapshot of the root EBS volume, registers a new AMI (`ami-frontend-yyyy-mm-dd`), and terminates the builder instance.

### Sample Packer Configuration File (`template.pkr.hcl`)

Below is the Packer configuration used to build the hardened Ubuntu 26.04 LTS backend AMI:

```hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu-hardened" {
  ami_name      = "asimp-ubuntu-26.04-backend-{{timestamp}}"
  instance_type = "t4g.medium" # Build on high-efficiency Graviton
  region        = "ap-southeast-5"

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-*-server-*" # Fallback / target filter for Canonical Ubuntu LTS
      root-device-type    = "ebs"
      virtualization-type = "hvm"
      architecture        = "arm64"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu-hardened"]

  # Run ASIMP Hardening using Ansible
  provisioner "ansible" {
    playbook_file = "../asimp/play.yml"
    user          = "ubuntu"
    use_extra_vars = true
    extra_vars = {
      is_packer_build = true
    }
  }

  # Verify ASIMP reports are present before finalizing image
  provisioner "shell" {
    inline = [
      "echo 'Verifying ASIMP Hardening Reports...'",
      "ls -l /var/log/asimp-baseline-scores.json",
      "ls -l /var/log/openscap-after-report.html"
    ]
  }
}
```

---

## 4. Parameterizing & Referencing Baked AMIs in OpenTofu

Once Packer successfully registers the custom AMIs, they can be referenced inside your OpenTofu configurations dynamically or passed as static overrides.

### Option A: Dynamic AMI Discovery (Recommended)
This approach dynamically queries AWS for the latest hardened AMI matching your tag patterns, ensuring that newly deployed Auto Scaling groups always inherit the latest security patches.

```hcl
# Look up latest pre-baked Backend AMI
data "aws_ami" "latest_hardened_backend" {
  most_recent = true
  owners      = ["self"] # Search within your AWS account

  filter {
    name   = "name"
    values = ["asimp-ubuntu-26.04-backend-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}
```

You then supply this dynamic ID to your ASG launch template:

```hcl
resource "aws_launch_template" "backend" {
  name_prefix   = "backend-launch-template-"
  image_id      = data.aws_ami.latest_hardened_backend.id
  instance_type = "t4g.xlarge"
  # ... remaining options
}
```

### Option B: Static AMI Parameter Override
For high-control staging/production environments where AMI updates must undergo rigid validation before scaling, define the image IDs as input variables:

```hcl
# In variables.tf
variable "backend_ami_id" {
  description = "Pre-baked ASIMP Hardened Ubuntu 26.04 LTS AMI for Backend"
  type        = string
  default     = "" # If empty, config falls back to dynamic SSM or data queries
}

# In main.tf
locals {
  selected_backend_ami = var.backend_ami_id != "" ? var.backend_ami_id : data.aws_ami.latest_hardened_backend.id
}
```

This ensures full agility while retaining rigid compliance validation controls.

---

## 5. Standalone EC2 Instances: Staging and Baking Lifecycle

To achieve complete alignment between active development and the immutable production ASGs, our design utilizes **dedicated Standalone EC2 Instances** as live staging, testing, and pre-baking nodes for each of the three logical application tiers.

```
 [ Dev Code & Config Updates ] ──► [ Dedicated Standalone Instance ]
                                      │  • Runs live on private VPC subnets
                                      │  • Connected to same S3, RDS, EFS
                                      │  • Hardened & audited via ASIMP
                                      ▼
                                [ AMI Captured ]
                                      │
                                      ▼
                          [ ASG Launch Template Updated ] ──► [ ASG Rolling Instance Refresh ]
```

### Environmental Alignment with Shared Backends
To prevent runtime configuration errors and bootstrap failures (such as database connection timeout or missing mount folders), the standalone instances are connected to the identical shared infrastructure as their matching ASGs:
- **Frontend Standalone:** Accesses the identical Amazon S3 static buckets to pull and verify Nginx page templates and asset configuration.
- **Backend Standalone:** Connects directly to the live **Multi-AZ RDS PostgreSQL** database (allowing safe database schema migration and endpoint verification) and **Amazon S3** (for DMS and document uploads).
- **AI Tier Standalone:** Mounts the identical multi-AZ **Amazon EFS** volume (facilitating direct Hugging Face and SentenceTransformers model caching). Developers download and cache model weights directly onto EFS from this standalone instance, which ensures newly-bootstrapped ASG nodes can access cached model weights instantly.

### The Staging-to-AMI Lifecycle Workflow

1. **Active Staging & Application Testing:**
   - Developers perform code updates, install package dependencies, and modify system configuration on the standalone instance.
2. **ASIMP Auditing & Hardening Compliance:**
   - Developers execute the **ASIMP** auditing framework directly on the standalone instance. ASIMP executes OpenSCAP and Lynis compliance audits, applies Ubuntu security hardening configurations, checks package integrity, and produces HTML verification scorecards at `/var/log/openscap-after-report.html`.
3. **AMI Capture & Registration:**
   - Once compliance and functional tests pass successfully, the standalone instance's root volume is frozen.
   - An AMI is registered directly from the standalone instance using Packer or an automated AWS Systems Manager (SSM) backup document:
     ```bash
     aws ec2 create-image \
       --instance-id i-0xxxxxxxstandalone \
       --name "asimp-hardened-backend-$(date +%F)" \
       --no-reboot
     ```
4. **ASG Deployment & Rolling Refresh:**
   - The registered AMI ID is supplied to OpenTofu as a variable override or auto-discovered dynamically.
   - An **ASG Instance Refresh** is triggered, rolling out the new pre-validated, fully-configured image across the active ASG nodes with zero downtime.
