# Automation Scripts

The project includes CLI helper scripts and bootstrapping scripts under the `scripts/` directory to automate common tasks, local testing, and instance provisioning.

---

## 1. Local Deployment Script (`scripts/deploy.sh`)

This script automates the full lifecycle of a local Terraform deployment. It performs validation and planning checks before prompting the user for confirmation to apply.

### Steps Executed:
1. **Directory Context:** Changes the working directory to `terraform/`.
2. **Environment Configuration Check:** Checks if `terraform.tfvars` exists. If not, it copies it from `terraform.tfvars.example` and prompts the user to review.
3. **Initialization (`terraform init`):** Downloads required providers and module configurations.
4. **Format Verification (`terraform fmt`):** Formats all configuration files recursively to match canonical HCL syntax.
5. **Validation (`terraform validate`):** Verifies syntax correctness and internal variable consistency.
6. **Execution Planning (`terraform plan`):** Generates a secure plan file `tfplan`.
7. **User Confirmation Prompt:** Asks `Do you want to apply this deployment? (y/n)`. If `y`, it runs `terraform apply tfplan`.

---

## 2. Infrastructure Teardown Script (`scripts/destroy.sh`)

This script provides a clean and automated way to destroy all resources managed by Terraform, preventing accidental dangling resources or billing charges.

### Steps Executed:
1. **Initialization:** Confirms that Terraform has been initialized.
2. **Resource Destruction (`terraform destroy`):** Prompts the user to confirm the termination of all resources. Once confirmed, it cleanly removes all VPC components, load balancers, database clusters, auto-scaling groups, and WAF rules.

---

## 3. Instance Bootstrapping Script (`scripts/user_data.sh`)

This is a standalone bootstrapping script for EC2 instances. It can be used for custom instance images or standalone EC2 deployment tests.

### Features:
- Updates the operating system packages.
- Installs and configures an Apache HTTP web server.
- Fetches Instance Metadata Service v2 (IMDSv2) security tokens dynamically.
- Retrieves instance metadata, including the Instance ID and host Availability Zone, displaying this dynamic diagnostic information on a beautifully styled HTML index page.
