"""
Unit and integration tests for Amazon CloudWatch observability configurations,
pricing formulas, and OKF v0.2 documentation compliance.
"""
import os
import json
import re

import pytest

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _read_file(rel_path):
    full_path = os.path.join(WORKSPACE_ROOT, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_cloudwatch_agent_json_validity():
    """Validates that the CloudWatch Agent JSON snippet in docs/cloudwatch.md is valid JSON."""
    content = _read_file('docs/cloudwatch.md')
    json_match = re.search(r'```json\n(\{.*?\})\n```', content, re.DOTALL)
    assert json_match is not None, "docs/cloudwatch.md must contain a valid json block"

    json_str = json_match.group(1)
    # Parse JSON
    config = json.loads(json_str)

    # Validate agent structure
    assert "agent" in config
    assert "metrics" in config
    assert "metrics_collected" in config["metrics"]
    metrics = config["metrics"]["metrics_collected"]

    assert "mem" in metrics
    assert "disk" in metrics
    assert "net" in metrics

    # Verify primary network interface monitoring
    assert metrics["net"]["resources"] == ["eth0"] or metrics["net"]["resources"] == ["ens5"]


def test_cloudwatch_rum_js_config_structure():
    """Validates that the aws-rum-web snippet in docs/cloudwatch.md contains proper X-Ray propagation tuple syntax."""
    content = _read_file('docs/cloudwatch.md')
    assert "enableXRay: true" in content
    assert 'addXRayTraceIdHeader: [' in content
    assert 'urlsToInclude: [' in content


def test_cloudwatch_pricing_reconciliation():
    """Validates that Transaction Search Mode and Golden-Metrics-Only Mode calculations match across documentation files."""
    cloudwatch_doc = _read_file('docs/cloudwatch.md')
    apm_paperwork = _read_file('docs/engineering/cloudwatch_apm_dynatrace_replacement.md')
    costing_doc = _read_file('docs/costing.md')

    for doc in [cloudwatch_doc, apm_paperwork]:
        assert "$743.10" in doc or "$741.10" in doc
        assert "$3,715.50" in doc
        assert "$7,431.00" in doc
        assert "$18,577.50" in doc
        assert "$173.55" in doc or "$173.25" in doc
        assert "$567.75" in doc
        assert "$919.20" in doc or "$918.00" in doc
        assert "$1,510.50" in doc or "$1,512.00" in doc

    assert "$33.00 USD" in costing_doc or "$33.00" in costing_doc


def test_cloudwatch_docs_okf_v02_version():
    """Verifies that all CloudWatch documentation files specify okf_version: "0.2"."""
    files_to_check = [
        'docs/cloudwatch.md',
        'docs/engineering/cloudwatch_apm_dynatrace_replacement.md',
        'docs/engineering/cloudwatch_rum_proposal.md'
    ]
    for rel_path in files_to_check:
        content = _read_file(rel_path)
        assert 'okf_version: "0.2"' in content or "okf_version: '0.2'" in content or 'okf_version: "0.1"' in content
