---
layout: default
title: "Root Terraform Configuration"
---

# Root Terraform Configuration

The root folder of the `terraform/` directory orchestrates the execution order, specifies environmental variables, defines provider versions, and outputs key service endpoints.

---

## Files Overview

### 1. `providers.tf`
Specifies minimum required Terraform version requirements and registers external providers.
- **Minimum Terraform Version:** `>= 1.5.0`
- **AWS Provider Version:** `~> 5.0`
- **Region configuration:** Dynamically loaded from variables (defaults to `ap-southeast-5`).

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

### 2. `main.tf`
Serves as the central manifest, calling modules in sequential dependency orders (Networking -> Security Groups -> ALB -> WAF -> ASG -> RDS) and passing cross-module attributes.
- **Example:** VPC subnet IDs are fed directly into ALB subnets, ASG subnets, and RDS subnets.
- **Example:** Security Group IDs are automatically mapped to protect dependencies.

### 3. `variables.tf`
Declares environmental configurations, default configurations, and input parameter structures.
- **Defaults for Malaysia Deployment:**
  - `aws_region`: `"ap-southeast-5"`
  - `db_engine`: `"postgres"`
  - `db_engine_version`: `"16"`
  - `db_instance_class`: `"db.t4g.micro"` (Graviton architecture)
  - `instance_type`: `"t4g.micro"` (Graviton compute)

### 4. `outputs.tf`
Exposes crucial deployment endpoints, such as the public ALB endpoint, the RDS endpoint, and the WAF Web ACL ARN for application clients.

```hcl
output "alb_dns_name" {
  value       = module.alb.alb_dns_name
  description = "Public Load Balancer Endpoint"
}

output "rds_endpoint" {
  value       = module.rds.db_instance_endpoint
  description = "Isolated RDS Database Endpoint"
}

output "waf_web_acl_arn" {
  value       = module.waf.waf_web_acl_arn
  description = "WAF v2 Web ACL ARN"
}
```

### 5. `terraform.tfvars.example`
A template file used to configure local infrastructure credentials and system settings safely. Copy this template before running your deployments:

```bash
cp terraform.tfvars.example terraform.tfvars
```
