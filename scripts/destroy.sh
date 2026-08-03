#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0;3m' # No Color

echo -e "${RED}=== WARNING: Starting AWS 3-Tier Infrastructure Destruction ===${NC}"

# Verify OpenTofu is installed
if ! command -v tofu &> /dev/null; then
    echo -e "${RED}[Error] OpenTofu (tofu) CLI is not installed.${NC}"
    echo "To install OpenTofu, please refer to: https://opentofu.org/docs/intro/install/"
    exit 1
fi

# Navigate to terraform directory
cd "$(dirname "$0")/../terraform"

# Verify OpenTofu state exists
if [ ! -d ".terraform" ]; then
    echo -e "${RED}[Error] OpenTofu is not initialized. Run deploy.sh first or run 'tofu init' in the terraform/ directory.${NC}"
    exit 1
fi

# Ask for confirmation
read -p "Are you absolutely sure you want to completely DESTROY all deployed AWS resources? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Running tofu destroy...${NC}"
    tofu destroy -auto-approve
    echo -e "${RED}=== Infrastructure Destroyed! ===${NC}"
else
    echo -e "${BLUE}Destruction cancelled by user.${NC}"
fi
