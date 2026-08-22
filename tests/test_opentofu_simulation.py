"""
Tests for OpenTofu AWS Infrastructure Offline Simulation and Scenario Validation.

This module provides offline unit test suites that validate OpenTofu HCL code structure,
IMDSv2 enforcement, security group network isolation, regional AWS Graviton defaults,
Valkey cache settings, ALB auto-healing integration, and multi-agent collaboration parameters
without requiring live AWS cloud environment credentials or API access.
"""

from pathlib import Path
import re


REPO_ROOT = Path(__file__).parent.parent
TERRAFORM_DIR = REPO_ROOT / "terraform"
MODULES_DIR = TERRAFORM_DIR / "modules"


def test_opentofu_module_structure_completeness():
    """Verify that all required OpenTofu 3-tier modules exist in terraform/modules/."""
    expected_modules = [
        "vpc",
        "security_groups",
        "alb",
        "asg",
        "rds",
        "elasticache",
        "jumphost",
        "route53",
        "standalone_ec2",
        "waf",
    ]
    assert MODULES_DIR.is_dir(), "terraform/modules directory missing"
    for mod in expected_modules:
        mod_path = MODULES_DIR / mod
        assert mod_path.is_dir(), f"Expected module '{mod}' not found under terraform/modules/"
        assert (mod_path / "main.tf").is_file(), f"Module '{mod}' missing main.tf file"


def test_opentofu_imdsv2_enforcement():
    """Verify IMDSv2 (http_tokens = required) is strictly enforced on all compute launch templates/instances."""
    asg_main = (MODULES_DIR / "asg" / "main.tf").read_text(encoding="utf-8")
    standalone_main = (MODULES_DIR / "standalone_ec2" / "main.tf").read_text(encoding="utf-8")
    jumphost_main = (MODULES_DIR / "jumphost" / "main.tf").read_text(encoding="utf-8")

    for file_name, content in [
        ("asg/main.tf", asg_main),
        ("standalone_ec2/main.tf", standalone_main),
        ("jumphost/main.tf", jumphost_main),
    ]:
        assert 'metadata_options' in content, f"Missing metadata_options block in {file_name}"
        assert 'http_tokens                 = "required"' in content or 'http_tokens = "required"' in content, (
            f"IMDSv2 http_tokens='required' not enforced in {file_name}"
        )
        assert 'http_put_response_hop_limit = 1' in content, (
            f"http_put_response_hop_limit = 1 not configured in {file_name}"
        )


def test_opentofu_db_security_group_isolation():
    """Verify RDS database security group limits ingress to db_port from application/ASG SG only."""
    sg_main = (MODULES_DIR / "security_groups" / "main.tf").read_text(encoding="utf-8")
    assert "resource \"aws_security_group\" \"db_sg\"" in sg_main, "DB security group (db_sg) missing"
    assert "from_port       = var.db_port" in sg_main, "var.db_port ingress missing in DB SG"
    assert "security_groups = [aws_security_group.asg_sg.id]" in sg_main, (
        "DB SG does not restrict ingress to ASG SG"
    )
    # Ensure ingress block inside DB SG does not allow public 0.0.0.0/0 CIDR
    db_block_match = re.search(r'resource "aws_security_group" "db_sg".*?^}', sg_main, re.MULTILINE | re.DOTALL)
    assert db_block_match, "Failed to parse DB security group block"
    db_block = db_block_match.group(0)

    ingress_match = re.search(r'ingress\s*\{([^}]+)\}', db_block)
    assert ingress_match, "Ingress block missing in DB SG"
    ingress_content = ingress_match.group(1)
    assert "0.0.0.0/0" not in ingress_content, "DB SG ingress block contains forbidden public 0.0.0.0/0 CIDR"


def test_opentofu_asg_elb_health_check():
    """Verify Auto Scaling Group configures health_check_type = ELB for ALB active integration."""
    asg_main = (MODULES_DIR / "asg" / "main.tf").read_text(encoding="utf-8")
    assert 'health_check_type         = "ELB"' in asg_main or 'health_check_type = "ELB"' in asg_main, (
        "ASG does not configure health_check_type = ELB"
    )


def test_opentofu_graviton_regional_defaults():
    """Verify variables.tf specifies ap-southeast-5 and Graviton default instance types."""
    vars_tf = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
    assert 'default     = "ap-southeast-5"' in vars_tf, "Default AWS region is not ap-southeast-5"
    assert 'default     = "t4g.micro"' in vars_tf or 't4g.medium' in vars_tf, "Default compute is not Graviton t4g instance"
    assert 'default     = "db.t4g.micro"' in vars_tf or 'db.m6g' in vars_tf, "Default DB instance is not Graviton tier"


def test_opentofu_valkey_caching_config():
    """Verify ElastiCache Valkey module defaults to valkey engine."""
    elasticache_main = (MODULES_DIR / "elasticache" / "main.tf").read_text(encoding="utf-8")
    assert 'engine                   = "valkey"' in elasticache_main or 'valkey' in elasticache_main, (
        "ElastiCache module does not specify Valkey engine"
    )


def test_opentofu_aws_simulation_runbook_exists():
    """Verify that docs/engineering/opentofu_aws_simulation.md exists and includes required sections."""
    doc_path = REPO_ROOT / "docs" / "engineering" / "opentofu_aws_simulation.md"
    assert doc_path.is_file(), "OpenTofu AWS simulation runbook missing"
    content = doc_path.read_text(encoding="utf-8")

    assert "okf_version: \"0.1\"" in content, "Missing OKF version in runbook frontmatter"
    assert "OpenTofu AWS Infrastructure Building, Simulation, & Multi-Agent Collaboration Runbook" in content, (
        "Runbook title mismatch"
    )
    assert "Offline Cloud Simulation Framework" in content, "Missing Simulation Framework section"
    assert "AWS Cloud Scenario Testing Matrix" in content, "Missing Scenario Matrix section"
    assert "Multi-Human and Multi-AI Agent Collaboration Protocol" in content, "Missing Collaboration section"


def test_opentofu_jumphost_whitelisting():
    """Verify the Jumphost security group restricts SSH ingress to the allowed office CIDR only."""
    jumphost_main = (MODULES_DIR / "jumphost" / "main.tf").read_text(encoding="utf-8")
    jumphost_vars = (MODULES_DIR / "jumphost" / "variables.tf").read_text(encoding="utf-8")

    assert "resource \"aws_security_group\" \"jumphost_sg\"" in jumphost_main, "Jumphost security group missing"

    # Isolate the jumphost_sg resource block to inspect its ingress rule in context.
    sg_block_match = re.search(
        r'resource "aws_security_group" "jumphost_sg".*?^}', jumphost_main, re.MULTILINE | re.DOTALL
    )
    assert sg_block_match, "Failed to parse Jumphost security group block"
    sg_block = sg_block_match.group(0)

    ingress_match = re.search(r'ingress\s*\{([^}]+)\}', sg_block)
    assert ingress_match, "Ingress block missing in Jumphost security group"
    ingress_content = ingress_match.group(1)

    assert "from_port   = 22" in ingress_content or "from_port = 22" in ingress_content, (
        "Jumphost SG does not restrict ingress to port 22 (SSH)"
    )
    assert "cidr_blocks = [var.allowed_ssh_cidr]" in ingress_content, (
        "Jumphost SG SSH ingress is not driven by the var.allowed_ssh_cidr whitelist variable"
    )
    # Ensure the SSH ingress rule itself never falls back to an open public CIDR.
    assert "0.0.0.0/0" not in ingress_content, (
        "Jumphost SG SSH ingress block must not allow public 0.0.0.0/0 CIDR access"
    )

    # The whitelist variable must default to the documented Cyberjaya office CIDR.
    assert 'default     = "103.188.0.0/16"' in jumphost_vars, (
        "Jumphost allowed_ssh_cidr variable does not default to the Cyberjaya office CIDR"
    )


def test_opentofu_vpc_multi_az_layout():
    """Verify the VPC module spans 2+ Availability Zones across all subnet tiers."""
    vars_tf = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
    vpc_main = (MODULES_DIR / "vpc" / "main.tf").read_text(encoding="utf-8")

    az_match = re.search(r'variable "availability_zones" \{(.*?)\n\}', vars_tf, re.DOTALL)
    assert az_match, "availability_zones variable not declared in root variables.tf"
    az_block = az_match.group(1)

    az_default_match = re.search(r'default\s*=\s*(\[[^\]]*\])', az_block)
    assert az_default_match, "availability_zones variable has no default list configured"
    az_list = re.findall(r'"([^"]+)"', az_default_match.group(1))

    assert len(az_list) >= 2, "Multi-AZ topology requires at least 2 Availability Zones by default"
    assert "ap-southeast-5a" in az_list and "ap-southeast-5b" in az_list, (
        "Default Availability Zones must include the ap-southeast-5a/5b Malaysia region pair"
    )

    # Public, private-app, and private-db subnet tiers must all fan out across the AZ list.
    az_usages = re.findall(r'availability_zone\s*=\s*var\.availability_zones\[count\.index\]', vpc_main)
    assert len(az_usages) >= 3, (
        "Expected public, private-app, and private-db subnets to each span var.availability_zones"
    )


def test_opentofu_runbook_documented_scenarios_map_to_real_test_functions():
    """
    Regression guard: every verification tool referenced in the runbook's AWS Cloud
    Scenario Testing Matrix must correspond to an actual test function defined in this
    file, preventing documentation from drifting ahead of (or behind) actual coverage.
    """
    doc_path = REPO_ROOT / "docs" / "engineering" / "opentofu_aws_simulation.md"
    doc_content = doc_path.read_text(encoding="utf-8")
    suite_content = Path(__file__).read_text(encoding="utf-8")

    documented_tools = re.findall(r'`(test_opentofu_\w+)`', doc_content)
    assert len(documented_tools) == 8, (
        f"Expected 8 documented scenario verification tools, found {len(documented_tools)}"
    )

    defined_functions = set(re.findall(r'^def (test_opentofu_\w+)\(', suite_content, re.MULTILINE))

    for tool_name in documented_tools:
        assert tool_name in defined_functions, (
            f"Runbook references '{tool_name}' as a verification tool, but no such test "
            f"function is defined in tests/test_opentofu_simulation.py"
        )
