#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0;3m' # No Color

echo -e "${BLUE}=== Starting AWS 3-Tier Infrastructure Deployment ===${NC}"

# Verify OpenTofu is installed
if ! command -v tofu &> /dev/null; then
    echo -e "${RED}[Error] OpenTofu (tofu) CLI is not installed.${NC}"
    echo "To install OpenTofu, please refer to: https://opentofu.org/docs/intro/install/"
    exit 1
fi

# Navigate to terraform directory
cd "$(dirname "$0")/../terraform"

# Ensure .tfvars exists
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

# OpenTofu Initialization
echo -e "${BLUE}Initializing OpenTofu...${NC}"
tofu init

# OpenTofu Format
echo -e "${BLUE}Formatting OpenTofu/HCL configs...${NC}"
tofu fmt -recursive

# OpenTofu Validate
echo -e "${BLUE}Validating OpenTofu configs...${NC}"
tofu validate

# OpenTofu Plan
echo -e "${BLUE}Generating OpenTofu execution plan...${NC}"
tofu plan -out=tfplan

# Ask for approval before applying
read -p "Do you want to apply this deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Applying OpenTofu plan...${NC}"
    tofu apply tfplan
    echo -e "${GREEN}=== Deployment Complete! ===${NC}"
else
    echo -e "${RED}Deployment cancelled by user.${NC}"
fi
