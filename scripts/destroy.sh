#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0;3m' # No Color

echo -e "${RED}=== WARNING: Starting AWS 3-Tier Infrastructure Destruction ===${NC}"

# Navigate to terraform directory
cd "$(dirname "$0")/../terraform"

# Verify terraform state exists
if [ ! -d ".terraform" ]; then
    echo -e "${RED}[Error] Terraform is not initialized. Run deploy.sh first or run 'terraform init' in the terraform/ directory.${NC}"
    exit 1
fi

# Ask for confirmation
read -p "Are you absolutely sure you want to completely DESTROY all deployed AWS resources? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Running terraform destroy...${NC}"
    terraform destroy -auto-approve
    echo -e "${RED}=== Infrastructure Destroyed! ===${NC}"
else
    echo -e "${BLUE}Destruction cancelled by user.${NC}"
fi
