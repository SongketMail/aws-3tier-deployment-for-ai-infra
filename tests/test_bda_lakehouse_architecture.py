"""Tests for the BDA lakehouse guide, skill, and publication registrations."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
BDA_DOC_PATH = WORKSPACE_ROOT / "docs" / "bda-lakehouse-architecture.md"
BDA_SKILL_PATH = (
    WORKSPACE_ROOT / ".agents" / "skills" / "bda-lakehouse-architecture" / "SKILL.md"
)
BDA_SOURCE_PATH = "docs/bda-lakehouse-architecture.md"
BDA_PAGE_URL = (
    "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/"
    "bda-lakehouse-architecture.html"
)


def _read(path):
    """Read a required repository file as UTF-8."""
    assert path.is_file(), (
        f"Required file does not exist: {path.relative_to(WORKSPACE_ROOT)}"
    )
    return path.read_text(encoding="utf-8")


def _front_matter(content):
    """Return simple key/value metadata from a Markdown front matter block."""
    assert content.startswith("---\n"), "Front matter must start on line 1"
    sections = content.split("---", 2)
    assert len(sections) == 3, "Front matter must have a closing delimiter"

    metadata = {}
    for line in sections[1].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


def test_bda_guide_and_skill_have_okf_v02_trust_metadata():
    """The new guide and its skill must expose complete OKF v0.2 trust signals."""
    guide_metadata = _front_matter(_read(BDA_DOC_PATH))
    skill_metadata = _front_matter(_read(BDA_SKILL_PATH))

    assert guide_metadata == {
        "layout": "default",
        "okf_version": "0.2",
        "type": "reference",
        "title": (
            "Modernizing Big Data Analytics Architecture: "
            "3-Tier Infra Deployment Blueprint"
        ),
        "timestamp": "2026-08-20T00:00:00Z",
        "topics": '["bda", "lakehouse", "aws", "hybrid", "proxmox", '
        '"rke2", "ceph", "mcp"]',
        "sources": f'["{BDA_SOURCE_PATH}"]',
        "status": "active",
        "verified": "true",
    }
    assert skill_metadata["okf_version"] == "0.2"
    assert skill_metadata["type"] == "Skill"
    assert skill_metadata["name"] == "bda-lakehouse-architecture"
    assert skill_metadata["sources"] == f'["{BDA_SOURCE_PATH}"]'
    assert skill_metadata["status"] == "active"
    assert skill_metadata["verified"] == "true"


def test_bda_guide_defines_exactly_three_distinct_solutions():
    """The blueprint must retain one cloud, hybrid, and sovereign solution."""
    content = _read(BDA_DOC_PATH)
    solution_headings = re.findall(r"^### Solution (\d): (.+)$", content, re.MULTILINE)

    assert solution_headings == [
        ("1", "All in Cloud (AWS Native & Cloud Managed Services)"),
        (
            "2",
            ("Hybrid - AI On-Premises (Cloud Lakehouse + On-Prem GPU Infrastructure)"),
        ),
        (
            "3",
            (
                "Everything On-Premises using Proxmox VE + RKE2 + "
                "Distributed Ceph Storage"
            ),
        ),
    ]


def test_bda_data_tiers_enforce_retention_and_ai_quarantine():
    """Golden records and AI output must have different retention boundaries."""
    content = _read(BDA_DOC_PATH)

    required_contracts = (
        "Tier 0: Golden Human Truth (Authoritative SSoT)",
        "S3 Object Lock (Compliance Mode)",
        "7-year statutory compliance or 365-day operational compliance",
        "Tier 1: Machine and Sensor Ingestion",
        "S3 Object Lock in Governance Mode",
        "Tier 2: AI Operational and Analytical Sandbox (Isolated Quarantine)",
        "automated 30-day S3 Lifecycle expiration policy",
        "Cannot be promoted directly; requires distillation and formal human certification",
    )
    for contract in required_contracts:
        assert contract in content

    assert "s3:BypassGovernanceRetention" in content
    assert "x-amz-bypass-governance-retention: true" in content
    assert "Iceberg tables reside in dedicated buckets or partitions" in content


def test_bda_mcp_access_is_read_only_and_outputs_are_labelled():
    """MCP tooling must not gain a path to mutate authoritative data."""
    content = _read(BDA_DOC_PATH)

    assert "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY" in content
    assert (
        "Write verbs (`INSERT`, `UPDATE`, `DELETE`, `DROP`, Iceberg commits)" in content
    )
    assert "are blocked at the API gateway" in content
    assert "tagged with `ai_generated_data: true`" in content
    assert "`enterprise_provenance` facet" in content
    assert (
        "Strict access barriers preventing automated writing or promotion to Tier 0"
        in content
    )


def test_cloud_and_hybrid_solutions_document_portability_and_encryption_limits():
    """Managed-service trade-offs and Direct Connect encryption must stay explicit."""
    content = _read(BDA_DOC_PATH)

    assert (
        "Solution 1 is cloud-dependent and AWS-managed rather than fully vendor-neutral"
        in content
    )
    assert (
        "Organizations requiring complete vendor neutrality and portability" in content
    )
    assert "AWS Direct Connect provides a dedicated private physical circuit" in content
    assert "unencrypted by default" in content
    assert "10 Gbps, 100 Gbps, and 400 Gbps" in content
    assert (
        "1 Gbps connections or non-MACsec locations require a Layer 3 IPsec VPN overlay"
        in content
    )
    assert "AI models have zero write permissions back to Cloud Tier 0 SSoT" in content


def test_on_prem_solution_has_consistent_capacity_and_failure_boundaries():
    """The sovereign topology must retain its host, VM, and N+1 capacity model."""
    content = _read(BDA_DOC_PATH)

    assert "11 physical Proxmox VE hosts" in content
    assert (
        "4x AI/GPU hosts, 4x Application hosts, 3x Database/Stateful hosts" in content
    )
    assert (
        "14 virtualized RKE2 production nodes and 5 virtualized K3s management nodes"
        in content
    )
    assert "reserving 15–20% CPU/RAM headroom per tier" in content
    assert "no two RKE2/K3s control-plane VMs or Patroni DB VMs" in content
    assert "3x Control Plane VM Nodes" in content
    assert "4x AI / GPU Worker VM Nodes" in content
    assert "4x Application / Microservices Worker VM Nodes" in content
    assert "3x Database & Stateful Worker VM Nodes" in content
    assert "Ceph CSI (`rbd.csi.ceph.com`)" in content
    assert "CephFS (`cephfs.csi.ceph.com`)" in content


def test_fips_and_performance_cni_profiles_are_not_conflated():
    """Regression: the guide must distinguish FIPS Canal from eBPF Cilium."""
    content = _read(BDA_DOC_PATH)

    assert "When FIPS 140-2 compliance is required" in content
    assert "bundled Canal CNI with FIPS-validated cryptographic modules" in content
    assert (
        "when eBPF performance and advanced networking are required, Cilium CNI is selected"
        in content
    )


def test_sensitive_legacy_identifiers_are_absent_case_insensitively():
    """Public documentation must not reintroduce customer names or endpoints."""
    content = _read(BDA_DOC_PATH).casefold()
    forbidden_terms = (
        "nres",
        "perhilitan",
        "jmg",
        "jpsm",
        "nahrim",
        "bda.nres.gov.my",
        "dashboard.nres.gov.my",
        "nres_provenance",
    )

    for term in forbidden_terms:
        pattern = rf"(?<![a-z0-9_]){re.escape(term.casefold())}(?![a-z0-9_])"
        assert not re.search(pattern, content), f"Forbidden identifier found: {term}"


def test_bda_guide_is_registered_in_all_source_indexes():
    """Readers, Jekyll, print compilation, and LLMs must all discover the guide."""
    registrations = {
        WORKSPACE_ROOT / "README.md": f"]({BDA_SOURCE_PATH})",
        WORKSPACE_ROOT / "docs" / "index.md": "](bda-lakehouse-architecture.html)",
        WORKSPACE_ROOT
        / "docs"
        / "_config.yml": 'url: "/bda-lakehouse-architecture.html"',
        WORKSPACE_ROOT / "docs" / "print_all.md": "bda-lakehouse-architecture.md",
        WORKSPACE_ROOT / "llms.txt": f"]({BDA_SOURCE_PATH})",
        WORKSPACE_ROOT / "sitemap.txt": BDA_PAGE_URL,
    }

    for path, expected in registrations.items():
        assert expected in _read(path), f"Missing BDA registration in {path.name}"


def test_bda_sitemap_xml_entry_is_unique_and_complete():
    """The XML sitemap must publish one well-formed entry with its metadata."""
    root = ET.parse(WORKSPACE_ROOT / "sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    matching_entries = [
        node
        for node in root.findall("sm:url", namespace)
        if node.findtext("sm:loc", namespaces=namespace) == BDA_PAGE_URL
    ]

    assert len(matching_entries) == 1
    entry = matching_entries[0]
    assert entry.findtext("sm:lastmod", namespaces=namespace) == "2026-08-20"
    assert entry.findtext("sm:changefreq", namespaces=namespace) == "monthly"
    assert entry.findtext("sm:priority", namespaces=namespace) == "0.8"


def test_bda_guide_and_skill_end_with_dsom_footers():
    """Both authoritative sources must conclude with DSOM provenance."""
    for path in (BDA_DOC_PATH, BDA_SKILL_PATH):
        final_lines = _read(path).strip().splitlines()[-2:]
        assert "Deep State of Mind (DSOM) For My AI Protocol" in final_lines[0]
        assert "Standard: UK English" in final_lines[1]
        assert "GNU General Public License v3.0" in final_lines[1]
