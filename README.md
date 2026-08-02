# AWS 3-tier Deployment for AI & Web Infra

A complete, production-ready Terraform project and CI/CD workflow to deploy a highly-available, secure **3-Tier Architecture** on AWS, fully integrated with **AWS WAFv2** for protection against malicious requests and DDoS attacks.

---

## Architecture Overview

This project implements a secure and robust three-tier layout separated logically and physically across multiple Availability Zones (AZs) for high availability:

```
                      [ INTERNET ]
                           │
                           ▼
                     [ AWS WAFv2 ]   <-- (OWASP Top 10 + IP Rate Limiting)
                           │
                           ▼
             [ Application Load Balancer ]  <-- (Public Subnets)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      [ ASG EC2 Instance ]       [ ASG EC2 Instance ]  <-- (Private App Subnets)
             │                           │
             └─────────────┬─────────────┘
                           ▼
                 [ Multi-AZ RDS DB ]        <-- (Private Database Subnets)
```

1. **Presentation/Web Tier (Public Subnets):**
   - **Application Load Balancer (ALB):** Distributes incoming traffic to the application tier.
   - **AWS WAFv2:** Protects the ALB by applying Core/Common Rule Sets, SQL Injection (SQLi) Protection, and Rate Limiting.
2. **Application Tier (Private Subnets):**
   - **Auto Scaling Group (ASG):** Spans across multiple Availability Zones to scale ec2 instances dynamically based on CPU usage. It has no public IP addresses. Outbound connections are routed securely via **NAT Gateways**.
3. **Database Tier (Private Subnets):**
   - **Multi-AZ RDS (MySQL/PostgreSQL):** Only accepts connections from the application tier instances security group. Completely isolated from the internet.

---

## Directory Structure

This repository follows industry-standard conventions suitable for GitHub integration and infrastructure-as-code team projects.

```
.
├── .github/
│   └── workflows/
│       └── terraform.yml       # GitHub Actions pipeline for format, validate, and apply
├── scripts/
│   ├── deploy.sh               # CLI helper to format, validate, plan, and deploy
│   ├── destroy.sh              # CLI helper to tear down the entire infrastructure
│   └── user_data.sh            # Bootstrapping script for EC2 instances
├── terraform/
│   ├── modules/
│   │   ├── vpc/                # Modules for VPC, Subnets, Internet & NAT Gateways
│   │   ├── security_groups/    # Strict Security Group Rules separating layers
│   │   ├── alb/                # Application Load Balancer and target groups
│   │   ├── waf/                # AWS WAFv2 Web ACL configuration and association
│   │   ├── asg/                # Auto Scaling Group, Launch Templates, and scaling policies
│   │   └── rds/                # Multi-AZ RDS Database configuration
│   ├── main.tf                 # Root Terraform configuration calling modules
│   ├── variables.tf            # Variables definition
│   ├── outputs.tf              # Architecture deployment outputs (endpoints, IPs, etc.)
│   ├── providers.tf            # Terraform and AWS provider definitions
│   └── terraform.tfvars.example# Template for environment configuration
├── .gitignore                  # Ignoring tfstate, lock files, and local logs
└── LICENSE
```

---

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.5.0
- [AWS CLI](https://aws.amazon.com/cli/) configured with administrative credentials
- Git (for tracking changes)

---

## Getting Started & Deployment

### Local CLI Deployment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/aws-3tier-deployment-for-ai-infra.git
   cd aws-3tier-deployment-for-ai-infra
   ```

2. **Configure Variables:**
   Create your custom `terraform.tfvars` configuration file:
   ```bash
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   ```
   Open `terraform/terraform.tfvars` in your preferred editor and set your sensitive database password and environment preferences.

3. **Deploy with helper script:**
   The `scripts/deploy.sh` script automates initialization, validation, and planning, ensuring that you review the infrastructure before applying.
   ```bash
   ./scripts/deploy.sh
   ```

4. **Tear down with helper script:**
   When you no longer need the resources, use the destruction script to cleanly remove all AWS services:
   ```bash
   ./scripts/destroy.sh
   ```

---

## CI/CD Pipeline (GitHub Actions)

This repository includes a complete GitHub Actions workflow configured in `.github/workflows/terraform.yml`. It is fully prepared to use **OIDC (OpenID Connect)** to authenticate with AWS securely without hardcoding secret access keys.

### CI/CD Steps
1. **Pull Requests:** When a PR is created to `main`, the workflow executes `terraform fmt`, `terraform init -backend=false`, `terraform validate`, and displays a `terraform plan`.
2. **Merge/Push to Main:** When changes are merged or pushed directly to the `main` branch, the pipeline deploys the infrastructure dynamically to AWS using `terraform apply -auto-approve`.

### Required GitHub Secrets
Configure the following secrets under your GitHub repository **Settings -> Secrets and variables -> Actions**:
- `AWS_ROLE_TO_ASSUME`: The ARN of the IAM Role for OIDC connection.
- `AWS_REGION`: The target AWS region (e.g., `us-east-1`).

---

## Security Best Practices Built-In

- **Zero Direct Public DB Access:** Database instances are stored in deep private subnets with ingress strictly limited to the ASG security group.
- **WAF Layer-7 Rules:** Out-of-the-box rule sets prevent standard attacks such as SQL injection, cross-site scripting (XSS), and automated scraping/flooding via IP Rate Limiting.
- **Storage Encryption:** AWS RDS is deployed with storage volume encryption enabled (`storage_encrypted = true`).
- **No Hardcoded Credentials:** The setup includes templates/examples and utilizes instance profiles for EC2 instead of raw IAM Access Keys.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
