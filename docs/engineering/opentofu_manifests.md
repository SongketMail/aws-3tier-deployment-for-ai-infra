---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "OpenTofu Module Manifests"
timestamp: 2026-08-09T14:00:00Z
topics: ["devops", "engineering", "runbook", "opentofu", "security"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>

# 🛠️ OpenTofu Module Manifests

This runbook isolates the modular, declarative OpenTofu (v1.8.2) Infrastructure-as-Code (IaC) manifests for the secure 3-tier architecture. It details key module boundaries, strict security structures, and security-compliance parameters.

---

## 🔒 1. Mandating IMDSv2 (Instance Metadata Service v2)

To satisfy security audit frameworks (CIS Level 2), all compute resources must strictly enforce IMDSv2. Traditional IMDSv1 is disabled to prevent Server-Side Request Forgery (SSRF) metadata exfiltration.

```hcl
# Location: terraform/modules/asg/main.tf
resource "aws_launch_template" "main" {
  name_prefix   = "secure-3tier-launch-template-"
  image_id      = var.ami_id
  instance_type = var.instance_type

  # Strict IMDSv2 Enforcement
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
    http_endpoint               = "enabled"
  }

  network_interfaces {
    associate_public_ip_address = false
    security_groups             = [var.app_security_group_id]
  }

  user_data = filebase64("${path.module}/../../scripts/user_data.sh")
}
```

---

## 🛡️ 2. Zero-Trust Security Groups Manifest

We enforce the **Zero-Trust Network Principle**. Application servers in the private subnets only accept connections from the Application Load Balancer (ALB) on port 80/443. The RDS Database instance only accepts ingress traffic from the compute tier security group on port 5432.

```hcl
# Location: terraform/modules/security_groups/main.tf

# 1. Application Load Balancer Security Group
resource "aws_security_group" "alb" {
  name        = "secure-3tier-alb-sg"
  description = "Allows public HTTP/HTTPS traffic to ALB"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow inbound HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow inbound HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. Private Database Security Group
resource "aws_security_group" "rds" {
  name        = "secure-3tier-rds-sg"
  description = "Restricts database traffic strictly to compute tier"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow PG ingress exclusively from compute instances"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id] # Strict source-based chaining
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## ⚙️ 3. Safe Variables Declaration

Variables are strictly typed to guarantee compiler-level checking during `tofu plan` executions:

```hcl
# Location: terraform/variables.tf

variable "enable_standalone_ec2" {
  description = "Toggle to provision standalone compute nodes mirroring the ASG"
  type        = bool
  default     = false
}

variable "office_ip_range" {
  description = "Whitelisted Cyberjaya developer office CIDR for secure jumphost ingress"
  type        = string
  default     = "202.185.0.0/16" # Example whitelisted CIDR block
}
```

---

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
