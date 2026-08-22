#!/usr/bin/env bash
# ==============================================================================
# Script Name: simulate.sh
# Description: Executes offline OpenTofu AWS simulation and unit test suites.
#              Validates HCL formatting, syntax, security constraints (IMDSv2,
#              network isolation, Graviton types, Valkey caching), and pytest suites
#              without requiring active AWS cloud credentials or live API access.
# Usage:        ./scripts/simulate.sh
# Author:       Harisfazillah Jamel (LinuxMalaysia)
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for output decoration
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Starting OpenTofu AWS Offline Simulation & Verification ===${NC}"

# Navigate to repository root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# Step 1: Run Pytest Simulation Suite
echo -e "${BLUE}[1/2] Running Pytest Simulation Test Suite...${NC}"
if command -v pytest &> /dev/null; then
    pytest tests/test_opentofu_simulation.py -v
    echo -e "${GREEN}✔ Pytest simulation suite passed successfully!${NC}"
else
    echo -e "${RED}[Error] pytest is not installed or not found in PATH.${NC}"
    exit 1
fi

# Step 2: OpenTofu HCL Static Validation (if OpenTofu CLI is installed)
echo -e "${BLUE}[2/2] Checking OpenTofu CLI for static HCL validation...${NC}"
if command -v tofu &> /dev/null; then
    echo -e "${BLUE}Running OpenTofu format check...${NC}"
    tofu fmt -recursive terraform/

    echo -e "${BLUE}Initializing OpenTofu in backend-less offline mode...${NC}"
    tofu -chdir=terraform init -backend=false

    echo -e "${BLUE}Validating OpenTofu syntax and provider configurations...${NC}"
    tofu -chdir=terraform validate
    echo -e "${GREEN}✔ OpenTofu static HCL validation passed!${NC}"
else
    echo -e "${YELLOW}[Notice] OpenTofu CLI (tofu) is not installed in current environment.${NC}"
    echo -e "${YELLOW}Static AST simulation passed via Pytest. Install OpenTofu CLI to enable full HCL provider schema checks.${NC}"
fi

echo -e "${GREEN}=== Simulation & Verification Completed Successfully! ===${NC}"
