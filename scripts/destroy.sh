#!/usr/bin/env bash
# ==============================================================================
# Script Name: destroy.sh
# Description: Safely handles the complete removal and destruction of all deployed
#              AWS 3-tier infrastructure components using OpenTofu (tofu).
#              Performs verification of existing backend/initialization status and
#              demands explicit double-confirmation before applying destructive actions.
# Usage:        ./scripts/destroy.sh
# Author:       Harisfazillah Jamel (LinuxMalaysia)
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output warning indications
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0;3m' # No Color

echo -e "${RED}=== WARNING: Starting AWS 3-Tier Infrastructure Destruction ===${NC}"

# Verify OpenTofu is installed in the current environment
if ! command -v tofu &> /dev/null; then
    echo -e "${RED}[Error] OpenTofu (tofu) CLI is not installed.${NC}"
    echo "To install OpenTofu, please refer to: https://opentofu.org/docs/intro/install/"
    exit 1
fi

# Navigate to the root terraform configuration directory
cd "$(dirname "$0")/../terraform" || { echo -e "${RED}[Error] Failed to navigate to terraform directory.${NC}"; exit 1; }

# Verify OpenTofu state exists
if [ ! -d ".terraform" ]; then
    echo -e "${RED}[Error] OpenTofu is not initialized. Run deploy.sh first or run 'tofu init' in the terraform/ directory.${NC}"
    exit 1
fi

# Ask for explicit confirmation before destroying live cloud resources
read -r -p "Are you absolutely sure you want to completely DESTROY all deployed AWS resources? (y/n) " -n 1
echo
if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Running tofu destroy...${NC}"
    tofu destroy -auto-approve
    echo -e "${RED}=== Infrastructure Destroyed! ===${NC}"
else
    echo -e "${BLUE}Destruction cancelled by user.${NC}"
fi
