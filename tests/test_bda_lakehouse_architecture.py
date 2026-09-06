"""
Tests validating the Big Data Analytics (BDA) Lakehouse Modernization Architecture Guide.

Verifies:
- File existence at docs/bda-lakehouse-architecture.md
- OKF v0.2 front matter headers and trust signals
- Presence of all 3 distinct infrastructure deployment solutions
- Strict sanitization of government agency/project names and endpoints
- Standard Deep State of Mind (DSOM) footer compliance
"""

import os
import re
import pytest

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BDA_DOC_PATH = os.path.join(WORKSPACE_ROOT, 'docs', 'bda-lakehouse-architecture.md')


def _read_bda_doc():
    assert os.path.exists(BDA_DOC_PATH), "docs/bda-lakehouse-architecture.md must exist"
    with open(BDA_DOC_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def test_bda_lakehouse_doc_exists_and_okf_v02_frontmatter():
    """Validates that the document exists and has valid OKF v0.2 front matter metadata."""
    content = _read_bda_doc()
    assert content.startswith('---\n')

    parts = content.split('---', 2)
    assert len(parts) >= 3, "Document must have valid YAML front matter termination"

    front_matter = parts[1]
    assert 'okf_version: "0.2"' in front_matter or "okf_version: '0.2'" in front_matter or 'okf_version: "0.2"' in front_matter
    assert 'type: "reference"' in front_matter or 'type: "reference"' in front_matter or 'type: reference' in front_matter
    assert 'verified: "true"' in front_matter or 'verified: true' in front_matter
    assert 'sources:' in front_matter
    assert 'status: "active"' in front_matter or 'status: active' in front_matter


def test_bda_lakehouse_contains_3_infra_solutions():
    """Validates that all 3 distinct infrastructure deployment solutions are explicitly defined."""
    content = _read_bda_doc()

    assert "Solution 1: All in Cloud (AWS Native & Cloud Managed Services)" in content
    assert "Solution 2: Hybrid - AI On-Premises (Cloud Lakehouse + On-Prem GPU Infrastructure)" in content
    assert "Solution 3: Everything On-Premises using Proxmox VE + RKE2 + Distributed Ceph Storage" in content


def test_bda_lakehouse_government_identifiers_sanitized():
    """Validates that all legacy government agency names, project codes, and domain endpoints are fully sanitized."""
    content = _read_bda_doc()

    forbidden_terms = [
        "NRES",
        "PERHILITAN",
        "JMG",
        "JPSM",
        "NAHRIM",
        "bda.nres.gov.my",
        "dashboard.nres.gov.my",
        "nres_provenance",
    ]

    for term in forbidden_terms:
        assert term not in content, f"Sanitization Error: Forbidden term '{term}' found in docs/bda-lakehouse-architecture.md"


def test_bda_lakehouse_dsom_footer_present():
    """Validates that the document concludes with a valid Deep State of Mind (DSOM) footer."""
    content = _read_bda_doc()
    assert "Deep State of Mind (DSOM) For My AI Protocol" in content
