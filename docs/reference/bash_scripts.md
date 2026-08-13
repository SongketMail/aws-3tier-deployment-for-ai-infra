---
layout: "default"
okf_version: "0.1"
type: "Reference"
title: "Technical Reference: Deployment, Teardown, and PDF Scripts"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "bash", "reference"]
---
# Technical Reference: Deployment, Teardown, and PDF Scripts

This reference page provides operational specifications, parameter requirements, execution flows, and failure modes for our automation scripts under `scripts/`.

---

## 1. Local Deployment Automation (`scripts/deploy.sh`)

Automates the validation, canonical formatting, linting, planning, and interactive application of OpenTofu resources.

### Runtime Requirements
* **Interpreter:** Bash (standard GNU or BSD shell environment)
* **OpenTofu Version:** `tofu >= 1.6.0` (Must be installed globally and discoverable in path)
* **Access Configuration:** Correct AWS credentials (IAM role, session keys, or environment variables) configured.

### Execution Flow
1. **Dependency Verification:** Asserves that `tofu` is installed.
2. **Context Shift:** Navigates directory recursively to `terraform/`.
3. **Variables Enforcing:** Verifies `terraform.tfvars` exists; if missing, duplicates `terraform.tfvars.example` and prompts the operator to configure variables before exit.
4. **Initialization:** Runs `tofu init` to configure the backend and load module providers.
5. **Syntax Correction:** Performs canonical recursive styling on all files with `tofu fmt -recursive`.
6. **Validation:** Checks syntax and variable types with `tofu validate`.
7. **Execution Plan Compiled:** Outputs compiled resource plans to `tfplan` via `tofu plan -out=tfplan`.
8. **Interactive Confirmation:** Demands explicit user confirmation: `Do you want to apply this deployment? (y/n)`.

### Input / Output Contracts
* **Inputs:** `terraform/` configurations, `terraform.tfvars`.
* **Outputs:** State updates, created cloud resources, compiled planning binary `tfplan`.

---

## 2. Clean Teardown Automation (`scripts/destroy.sh`)

Safely handles interactive, complete resource removal and destruction, preventing dangling cloud components.

### Runtime Requirements
* Same as `deploy.sh`. Must be executed in initialized contexts (requires `.terraform` directory).

### Execution Flow
1. Verifies that `tofu` is installed.
2. Navigates directory context to `terraform/`.
3. Ensures that the backend has been initialized by verifying existence of `.terraform`.
4. Asks for explicit confirmation: `Are you absolutely sure you want to completely DESTROY all deployed AWS resources? (y/n)`.
5. Runs `tofu destroy -auto-approve` upon user approval.

---

## 3. Instance Bootstrapping (`scripts/user_data.sh`)

Bootstraps newly initialized, standalone EC2 compute instances with standard diagnostics, packages, and telemetry features.

### Execution Flow
1. Performs full system upgrade and patches.
2. Installs and enables Apache2 HTTP daemon.
3. Retrieves metadata token dynamically from the local link-local IMDSv2 address: `http://169.254.169.254/latest/api/token`.
4. Extracts Instance ID and Availability Zone metadata using the IMDSv2 token.
5. Injects structured diagnostic data into a styled Apache HTML landing page at `/var/www/html/index.html`.

---

## 4. Automated A4 PDF compiler (`scripts/generate_pdf.js`)

Uses Puppeteer and a local HTTP server to compile high-fidelity A4 documentation manuals recursively.

### Requirements
* **Runtime:** Node.js >= 18
* **Dependencies:** `puppeteer`
* **Static Assets:** A completed Jekyll site build under the `./_site` folder.

### CLI Execution
```bash
node scripts/generate_pdf.js
```

### Server Configuration
* **Port:** `4000` (Local HTTP server)
* **Output Path:** `docs/assets/output.pdf` (Overwrites the destination file)
