---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Automation Scripts"
timestamp: 2026-08-22T08:15:00Z
topics: ["aws", "cloud", "opentofu", "simulation", "scripts", "deployment"]
---
# Automation Scripts

The project includes CLI helper scripts and bootstrapping scripts under the `scripts/` directory to automate common tasks, local testing, offline simulation, and instance provisioning.

---

## 1. Local Deployment Script (`scripts/deploy.sh`)

This script automates the full lifecycle of a local OpenTofu deployment to Amazon Web Services (AWS). It performs validation and planning checks before prompting the user for confirmation to apply.

### Steps Executed:
1. **OpenTofu Installation Check:** Verifies that the `tofu` CLI is installed and available in the execution path.
2. **Directory Context:** Changes the working directory to `terraform/`.
3. **Environment Configuration Check:** Checks if `terraform.tfvars` exists. If not, it copies it from `terraform.tfvars.example` and prompts the user to review.
4. **Initialization (`tofu init`):** Downloads required providers and module configurations.
5. **Format Verification (`tofu fmt`):** Formats all configuration files recursively to match canonical HCL syntax.
6. **Validation (`tofu validate`):** Verifies syntax correctness and internal variable consistency.
7. **Execution Planning (`tofu plan`):** Generates a secure plan file `tfplan`.
8. **User Confirmation Prompt:** Asks `Do you want to apply this deployment? (y/n)`. If `y`, it runs `tofu apply tfplan`.

---

## 2. Infrastructure Teardown Script (`scripts/destroy.sh`)

This script provides a clean and automated way to destroy all resources managed by OpenTofu, preventing accidental dangling resources or billing charges.

### Steps Executed:
1. **OpenTofu Installation Check:** Verifies that the `tofu` CLI is installed and available.
2. **Initialization:** Confirms that OpenTofu has been initialized and that `.terraform` config exists.
3. **Resource Destruction (`tofu destroy`):** Prompts the user to confirm the termination of all resources. Once confirmed, it cleanly removes all VPC components, load balancers, database clusters, auto-scaling groups, and WAF rules.

---

## 3. Offline Simulation & Verification Script (`scripts/simulate.sh`)

This script executes offline simulation and unit test suites without requiring active AWS cloud credentials or live AWS API connections. It allows developers and AI agents to test OpenTofu configurations and any newly added scripts against our architecture rules (e.g., IMDSv2 enforcement, zero-trust network isolation, Graviton defaults, and Valkey caching).

### Steps Executed:
1. **Directory Context Anchor:** Sets directory context to the repository root.
2. **Pytest Simulation Suite Execution:** Runs `pytest tests/test_opentofu_simulation.py -v` to perform AST-based structure, rule, and security constraint checks.
3. **OpenTofu HCL Static Validation (if OpenTofu CLI installed):**
   - Formats configurations (`tofu fmt -recursive terraform/`).
   - Initializes backend-less working directory (`tofu -chdir=terraform init -backend=false`).
   - Validates OpenTofu configurations (`tofu -chdir=terraform validate`).

---

## 4. Instance Bootstrapping Script (`scripts/user_data.sh`)

This is a standalone bootstrapping script for EC2 instances. It can be used for custom instance images or standalone EC2 deployment tests.

### Features:
- Updates the operating system packages.
- Installs and configures an Apache HTTP web server.
- Fetches Instance Metadata Service v2 (IMDSv2) security tokens dynamically.
- Retrieves instance metadata, including the Instance ID and host Availability Zone, displaying this dynamic diagnostic information on a beautifully styled HTML index page.

---

## 5. End-to-End Workflow on Any Linux Environment

You can git clone this repository on any Linux distribution (Ubuntu, Debian, RHEL, Fedora, Arch, Amazon Linux) and execute the complete deployment or offline simulation workflow:

```bash
# 1. Clone repository on your Linux host
git clone https://github.com/songketmail/aws-3tier-deployment-for-ai-infra.git
cd aws-3tier-deployment-for-ai-infra

# 2. Configure environment variables and credentials
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# (Edit terraform/terraform.tfvars with your specific IP ranges and passwords)

# 3. Run offline simulation test suite (test scripts and OpenTofu rules without AWS access)
./scripts/simulate.sh

# 4. Begin live AWS deployment (requires AWS CLI / IAM credentials configured)
./scripts/deploy.sh

# 5. Teardown deployed AWS infrastructure cleanly when done
./scripts/destroy.sh
```
