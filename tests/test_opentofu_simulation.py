"""
Tests for OpenTofu AWS Infrastructure Offline Simulation and Scenario Validation.

This module provides offline unit test suites that validate OpenTofu HCL code structure,
IMDSv2 enforcement, security group network isolation, regional AWS Graviton defaults,
Valkey cache settings, ALB auto-healing integration, SSH Jumphost whitelisting,
and multi-AZ VPC layout without requiring live AWS cloud environment credentials or API access.
"""

from pathlib import Path
import re


REPO_ROOT = Path(__file__).parent.parent
TERRAFORM_DIR = REPO_ROOT / "terraform"
MODULES_DIR = TERRAFORM_DIR / "modules"


def extract_resource_block(content: str, resource_type: str, resource_name: str) -> str:
    """Extract a resource block from HCL content using balanced brace matching."""
    header = f'resource "{resource_type}" "{resource_name}"'
    start_idx = content.find(header)
    if start_idx == -1:
        raise ValueError(f"Could not locate '{header}' in HCL content")
    brace_start = content.find('{', start_idx)
    if brace_start == -1:
        raise ValueError(f"Could not find opening brace for '{header}'")

    depth = 0
    for i in range(brace_start, len(content)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[brace_start : i + 1]
    raise ValueError(f"Could not find matching closing brace for '{header}'")


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
    """Parse HCL and validate IMDSv2 settings on every compute launch template / EC2 resource."""
    asg_main = (MODULES_DIR / "asg" / "main.tf").read_text(encoding="utf-8")
    standalone_main = (MODULES_DIR / "standalone_ec2" / "main.tf").read_text(encoding="utf-8")
    jumphost_main = (MODULES_DIR / "jumphost" / "main.tf").read_text(encoding="utf-8")

    # 1. aws_launch_template.main in asg/main.tf
    asg_lt_block = extract_resource_block(asg_main, "aws_launch_template", "main")
    assert 'metadata_options' in asg_lt_block, "metadata_options missing in aws_launch_template.main"
    assert 'http_tokens                 = "required"' in asg_lt_block or 'http_tokens = "required"' in asg_lt_block, (
        "http_tokens='required' not enforced in aws_launch_template.main"
    )
    assert 'http_put_response_hop_limit = 1' in asg_lt_block, (
        "http_put_response_hop_limit = 1 missing in aws_launch_template.main"
    )

    # 2. aws_instance.standalone in standalone_ec2/main.tf
    standalone_block = extract_resource_block(standalone_main, "aws_instance", "standalone")
    assert 'metadata_options' in standalone_block, "metadata_options missing in aws_instance.standalone"
    assert 'http_tokens                 = "required"' in standalone_block or 'http_tokens = "required"' in standalone_block, (
        "http_tokens='required' not enforced in aws_instance.standalone"
    )
    assert 'http_put_response_hop_limit = 1' in standalone_block, (
        "http_put_response_hop_limit = 1 missing in aws_instance.standalone"
    )

    # 3. aws_instance.jumphost in jumphost/main.tf
    jumphost_block = extract_resource_block(jumphost_main, "aws_instance", "jumphost")
    assert 'metadata_options' in jumphost_block, "metadata_options missing in aws_instance.jumphost"
    assert 'http_tokens                 = "required"' in jumphost_block or 'http_tokens = "required"' in jumphost_block, (
        "http_tokens='required' not enforced in aws_instance.jumphost"
    )
    assert 'http_put_response_hop_limit = 1' in jumphost_block, (
        "http_put_response_hop_limit = 1 missing in aws_instance.jumphost"
    )


def test_opentofu_db_security_group_isolation():
    """Parse aws_security_group.db_sg resource specifically and inspect all ingress rules."""
    sg_main = (MODULES_DIR / "security_groups" / "main.tf").read_text(encoding="utf-8")
    db_sg_block = extract_resource_block(sg_main, "aws_security_group", "db_sg")

    assert "from_port       = var.db_port" in db_sg_block or "from_port   = var.db_port" in db_sg_block, (
        "var.db_port ingress missing in aws_security_group.db_sg"
    )
    assert "security_groups = [aws_security_group.asg_sg.id]" in db_sg_block, (
        "db_sg does not restrict ingress to asg_sg"
    )

    # Assert no 0.0.0.0/0 ingress in db_sg block
    ingress_match = re.search(r'ingress\s*\{([^}]+)\}', db_sg_block)
    assert ingress_match, "Ingress block missing in db_sg"
    ingress_content = ingress_match.group(1)
    assert "0.0.0.0/0" not in ingress_content, "db_sg ingress block contains forbidden public 0.0.0.0/0 CIDR"


def test_opentofu_asg_elb_health_check():
    """Parse aws_autoscaling_group.main resource and validate health_check_type = ELB."""
    asg_main = (MODULES_DIR / "asg" / "main.tf").read_text(encoding="utf-8")
    asg_block = extract_resource_block(asg_main, "aws_autoscaling_group", "main")
    assert 'health_check_type         = "ELB"' in asg_block or 'health_check_type = "ELB"' in asg_block, (
        "aws_autoscaling_group.main does not configure health_check_type = ELB"
    )


def test_opentofu_graviton_regional_defaults():
    """Compare instance types and AWS region against actual variable defaults in variables.tf."""
    vars_tf = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
    region_default = re.search(r'variable "aws_region"\s*\{[^}]*default\s*=\s*"([^"]+)"', vars_tf)
    instance_default = re.search(r'variable "instance_type"\s*\{[^}]*default\s*=\s*"([^"]+)"', vars_tf)
    db_instance_default = re.search(r'variable "db_instance_class"\s*\{[^}]*default\s*=\s*"([^"]+)"', vars_tf)

    assert region_default and region_default.group(1) == "ap-southeast-5", "aws_region default is not ap-southeast-5"
    assert instance_default and "t4g" in instance_default.group(1), "instance_type default is not Graviton t4g"
    assert db_instance_default and "db.t4g" in db_instance_default.group(1), "db_instance_class default is not Graviton db.t4g"


def test_opentofu_valkey_caching_config():
    """Parse aws_elasticache_replication_group.valkey specifically and assert exact engine and port values."""
    elasticache_main = (MODULES_DIR / "elasticache" / "main.tf").read_text(encoding="utf-8")
    valkey_block = extract_resource_block(elasticache_main, "aws_elasticache_replication_group", "valkey")

    assert 'engine                     = "valkey"' in valkey_block or 'engine = "valkey"' in valkey_block, (
        "aws_elasticache_replication_group.valkey does not specify engine = 'valkey'"
    )
    assert 'port                       = 6379' in valkey_block or 'port = 6379' in valkey_block, (
        "aws_elasticache_replication_group.valkey does not specify port = 6379"
    )


def test_opentofu_jumphost_whitelisting():
    """Parse aws_security_group.jumphost_sg and verify SSH ingress on port 22 is restricted to allowed SSH CIDR."""
    jumphost_main = (MODULES_DIR / "jumphost" / "main.tf").read_text(encoding="utf-8")
    jumphost_sg_block = extract_resource_block(jumphost_main, "aws_security_group", "jumphost_sg")

    assert "from_port   = 22" in jumphost_sg_block, "SSH port 22 ingress missing in jumphost_sg"
    assert "to_port     = 22" in jumphost_sg_block, "SSH port 22 egress missing in jumphost_sg"
    assert "cidr_blocks = [var.allowed_ssh_cidr]" in jumphost_sg_block, (
        "jumphost_sg SSH ingress is not restricted to var.allowed_ssh_cidr"
    )


def test_opentofu_vpc_multi_az_layout():
    """Parse variables.tf default availability_zones and verify Multi-AZ deployment spanning 2+ AZs."""
    vars_tf = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
    az_default = re.search(r'variable "availability_zones"\s*\{[^}]*default\s*=\s*\[([^\]]+)\]', vars_tf)
    assert az_default, "availability_zones variable definition missing in variables.tf"

    azs = [az.strip(' "') for az in az_default.group(1).split(',')]
    assert len(azs) >= 2, f"availability_zones must span 2+ AZs for high availability, found: {azs}"
    assert all("ap-southeast-5" in az for az in azs), f"availability_zones must belong to ap-southeast-5, found: {azs}"


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
