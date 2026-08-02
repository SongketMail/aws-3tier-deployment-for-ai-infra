#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0;3m' # No Color

echo -e "${BLUE}=== Starting AWS 3-Tier Infrastructure Deployment ===${NC}"

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

# Terraform Initialization
echo -e "${BLUE}Initializing Terraform...${NC}"
terraform init

# Terraform Format
echo -e "${BLUE}Formatting Terraform configs...${NC}"
terraform fmt -recursive

# Terraform Validate
echo -e "${BLUE}Validating Terraform configs...${NC}"
terraform validate

# Terraform Plan
echo -e "${BLUE}Generating Terraform execution plan...${NC}"
terraform plan -out=tfplan

# Ask for approval before applying
read -p "Do you want to apply this deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Applying Terraform plan...${NC}"
    terraform apply tfplan
    echo -e "${GREEN}=== Deployment Complete! ===${NC}"
else
    echo -e "${RED}Deployment cancelled by user.${NC}"
fi
