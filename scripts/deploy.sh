#!/usr/bin/env bash
# ==============================================================================
# Script Name: deploy.sh
# Description: Automates the entire AWS 3-tier secure web & AI infrastructure
#              deployment using OpenTofu (tofu). Handles initialization, formatting,
#              validation, planning, and interactive/safe application of resources.
# Requirements: OpenTofu CLI installed (https://opentofu.org/docs/intro/install/)
#               and standard AWS IAM credentials configured in the terminal.
# Usage:        ./scripts/deploy.sh
# Author:       Harisfazillah Jamel (LinuxMalaysia)
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output decoration
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0;3m' # No Color

echo -e "${BLUE}=== Starting AWS 3-Tier Infrastructure Deployment ===${NC}"

# Verify OpenTofu is installed in the current environment
if ! command -v tofu &> /dev/null; then
    echo -e "${RED}[Error] OpenTofu (tofu) CLI is not installed.${NC}"
    echo "To install OpenTofu, please refer to: https://opentofu.org/docs/intro/install/"
    exit 1
fi

# Navigate to the root terraform configuration directory
cd "$(dirname "$0")/../terraform" || { echo -e "${RED}[Error] Failed to navigate to terraform directory.${NC}"; exit 1; }

# Ensure terraform.tfvars exists before launching deployment actions
if [ ! -f "terraform.tfvars" ]; then
    echo -e "${RED}[Warning] terraform.tfvars not found.${NC}"
    if [ -f "terraform.tfvars.example" ]; then
        echo "Creating terraform.tfvars from terraform.tfvars.example..."
        cp terraform.tfvars.example terraform.tfvars
        echo -e "${GREEN}Created terraform.tfvars! Please review/update its contents before continuing.${NC}"
        exit 0
    else
        echo -e "${RED}[Error] terraform.tfvars.example missing!${NC}"
        exit 1
    fi
fi

# Step 1: OpenTofu Initialization
# Downloads required provider plugins and sets up the backend.
echo -e "${BLUE}Initializing OpenTofu...${NC}"
tofu init

# Step 2: OpenTofu Format Check
# Standardises HCL syntax across all files recursively.
echo -e "${BLUE}Formatting OpenTofu/HCL configs...${NC}"
tofu fmt -recursive

# Step 3: OpenTofu Validation
# Validates OpenTofu configurations against compiler rules.
echo -e "${BLUE}Validating OpenTofu configs...${NC}"
tofu validate

# Step 4: OpenTofu Plan
# Compiles and generates a declarative execution plan saved to 'tfplan'.
echo -e "${BLUE}Generating OpenTofu execution plan...${NC}"
tofu plan -out=tfplan

# Step 5: Safety check and interactive approval before applying changes
read -r -p "Do you want to apply this deployment? (y/n) " -n 1
echo
if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Applying OpenTofu plan...${NC}"
    tofu apply tfplan
    echo -e "${GREEN}=== Deployment Complete! ===${NC}"
else
    echo -e "${RED}Deployment cancelled by user.${NC}"
fi
