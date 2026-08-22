"""
Test suite covering the OpenTofu AWS Simulation & Multi-Agent Collaboration Runbook
introduced across README.md, docs/_config.yml, docs/engineering/opentofu_aws_simulation.md,
docs/index.md, docs/print_all.md, llms.txt, sitemap.txt, and sitemap.xml.

These tests specifically target the content added/changed by this PR, rather than
re-validating generic repository-wide compliance rules already covered by
test_md_compliance.py and test_integration_compliance.py.
"""
import os
import re
import xml.etree.ElementTree as ET

import pytest

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DOC_REL_PATH = 'docs/engineering/opentofu_aws_simulation.md'
DOC_URL_PATH = 'engineering/opentofu_aws_simulation.html'
CANONICAL_TITLE = (
    "OpenTofu AWS Infrastructure Building, Simulation, & Multi-Agent Collaboration Runbook"
)
README_ENTRY_TITLE = "OpenTofu AWS Simulation & Multi-Agent Collaboration Runbook"
SITE_BASE_URL = "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra"


def _read(rel_path):
    with open(os.path.join(WORKSPACE_ROOT, rel_path), 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# docs/engineering/opentofu_aws_simulation.md
# ---------------------------------------------------------------------------

class TestOpenTofuSimulationRunbookDocument:
    def test_document_exists(self):
        assert os.path.isfile(os.path.join(WORKSPACE_ROOT, DOC_REL_PATH))

    def test_front_matter_fields(self):
        content = _read(DOC_REL_PATH)
        assert content.startswith('---\n'), "Runbook must start with front matter at line 1, column 1"
        parts = content.split('---', 2)
        assert len(parts) >= 3, "Front matter must be terminated"
        fm = parts[1]

        assert 'layout: "default"' in fm
        assert 'okf_version: "0.1"' in fm
        assert 'type: "Guide"' in fm
        assert f'title: "{CANONICAL_TITLE}"' in fm
        assert 'timestamp: 2026-08-11T10:00:00Z' in fm
        for topic in ("opentofu", "aws", "simulation", "testing", "multi-agent", "collaboration", "devops", "security"):
            assert f'"{topic}"' in fm, f"Missing topic '{topic}' in runbook front matter"

    def test_top_level_heading_matches_title(self):
        content = _read(DOC_REL_PATH)
        assert f"# 🛠️ {CANONICAL_TITLE}" in content

    def test_section_headings_present_in_order(self):
        content = _read(DOC_REL_PATH)
        expected_headings = [
            "## 🧭 1. Architectural Strategy & Offline Simulation Philosophy",
            "## 🏗️ 2. OpenTofu HCL Code Structure & Building Guidelines",
            "## 🧪 3. AWS Cloud Scenario Testing Matrix & Unit Test Integration",
            "## 🤝 4. Multi-Human and Multi-AI Agent Collaboration Protocol",
            "## 🚀 5. Deployment Simulation Walkthrough (Offline Executions)",
        ]
        positions = [content.index(h) for h in expected_headings]
        assert positions == sorted(positions), "Runbook sections must appear in numeric order"

    def test_testing_matrix_has_eight_scenario_rows(self):
        content = _read(DOC_REL_PATH)
        rows = re.findall(r'^\| \*\*\d+\. .+?\| `(test_opentofu_\w+)` \|$', content, re.MULTILINE)
        assert len(rows) == 8, f"Expected 8 scenario rows in the testing matrix, found {len(rows)}"
        assert len(set(rows)) == 8, "Testing matrix scenario rows must reference unique verification tools"

    def test_module_directory_listing_matches_actual_terraform_modules(self):
        content = _read(DOC_REL_PATH)
        modules_dir = os.path.join(WORKSPACE_ROOT, 'terraform', 'modules')
        actual_modules = sorted(
            name for name in os.listdir(modules_dir)
            if os.path.isdir(os.path.join(modules_dir, name))
        )
        assert len(actual_modules) == 10, "Expected exactly 10 terraform modules on disk"
        for module_name in actual_modules:
            assert f"{module_name}/" in content, (
                f"Runbook's terraform/ tree diagram does not list actual module '{module_name}'"
            )

    def test_dsom_footer_present(self):
        content = _read(DOC_REL_PATH)
        assert "Deep State of Mind (DSOM)" in content
        assert content.rstrip().endswith(
            "*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-11*"
        )

    def test_pytest_execution_commands_reference_correct_test_file(self):
        content = _read(DOC_REL_PATH)
        assert "pytest tests/test_opentofu_simulation.py -v" in content
        assert "pytest tests/test_opentofu_simulation.py" in content
        assert re.search(r'^pytest$', content, flags=re.MULTILINE), (
            "Expected a standalone full-suite 'pytest' command in the PR quality gate section"
        )

    def test_contains_no_broken_relative_markdown_links(self):
        """The runbook uses inline code spans for file paths (not markdown links); ensure
        no accidental markdown-link syntax was introduced that would point nowhere."""
        content = _read(DOC_REL_PATH)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        assert links == [], f"Runbook should not contain markdown links, found: {links}"


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

class TestReadmeOpenTofuSimulationEntry:
    def test_entry_present_with_exact_text(self):
        content = _read('README.md')
        expected = (
            f"* **[{README_ENTRY_TITLE}]({DOC_REL_PATH}):** Comprehensive runbook detailing "
            "offline AWS deployment simulations, unit testing matrices, static HCL AST "
            "analysis, and multi-agent/multi-human branch/PR workflows."
        )
        assert expected in content

    def test_entry_appears_exactly_once(self):
        content = _read('README.md')
        assert content.count(f"[{README_ENTRY_TITLE}]") == 1

    def test_entry_under_conceptual_alignment_heading(self):
        content = _read('README.md')
        heading_pos = content.index("### 1. Conceptual Alignment & Architecture")
        entry_pos = content.index(f"[{README_ENTRY_TITLE}]")
        next_heading_pos = content.index("### 2. Infrastructure Submodules")
        assert heading_pos < entry_pos < next_heading_pos

    def test_entry_appears_directly_after_jules_platform_guide(self):
        content = _read('README.md')
        jules_pos = content.index("[Google Jules AI Platform Guide]")
        entry_pos = content.index(f"[{README_ENTRY_TITLE}]")
        assert jules_pos < entry_pos

        # No other bullet entries should sit between the Jules guide and this new entry.
        between = content[jules_pos:entry_pos]
        assert between.count('\n* **[') == 1, (
            "OpenTofu Simulation runbook entry must immediately follow the Jules AI Platform Guide bullet"
        )

    def test_referenced_file_exists(self):
        content = _read('README.md')
        match = re.search(rf"\[{re.escape(README_ENTRY_TITLE)}\]\(([^)]+)\)", content)
        assert match is not None
        resolved = os.path.join(WORKSPACE_ROOT, match.group(1))
        assert os.path.isfile(resolved), f"README links to missing file: {match.group(1)}"


# ---------------------------------------------------------------------------
# docs/_config.yml
# ---------------------------------------------------------------------------

class TestJekyllConfigNavbarOpenTofuEntry:
    def test_navbar_entry_present(self):
        content = _read('docs/_config.yml')
        assert '- title: "OpenTofu Simulation"' in content
        assert f'url: "/{DOC_URL_PATH}"' in content

    def test_navbar_entry_is_well_formed_yaml_pair(self):
        content = _read('docs/_config.yml')
        match = re.search(
            r'- title: "OpenTofu Simulation"\s*\n\s*url: "/engineering/opentofu_aws_simulation\.html"',
            content,
        )
        assert match is not None, "OpenTofu Simulation navbar entry must pair title and url on adjacent lines"

    def test_navbar_entry_positioned_between_jules_and_spa_checklist(self):
        content = _read('docs/_config.yml')
        jules_pos = content.index('- title: "Jules AI Platform"')
        opentofu_pos = content.index('- title: "OpenTofu Simulation"')
        spa_pos = content.index('- title: "SPA Checklist"')
        assert jules_pos < opentofu_pos < spa_pos

    def test_navbar_entry_appears_exactly_once(self):
        content = _read('docs/_config.yml')
        assert content.count('- title: "OpenTofu Simulation"') == 1


# ---------------------------------------------------------------------------
# docs/index.md
# ---------------------------------------------------------------------------

class TestDocsIndexOpenTofuSimulationEntry:
    def test_entry_present_with_exact_text(self):
        content = _read('docs/index.md')
        expected = (
            f"31. **[{README_ENTRY_TITLE}]({DOC_URL_PATH}):** Comprehensive runbook detailing "
            "offline AWS deployment simulations, unit testing matrices, static HCL AST "
            "analysis, and multi-agent/multi-human branch/PR workflows."
        )
        assert expected in content

    def test_entry_is_numbered_31_and_final_core_configuration_item(self):
        content = _read('docs/index.md')
        assert "30. **[Google Jules AI Platform Guide]" in content
        assert "31. **[" + README_ENTRY_TITLE in content
        # No item 32 should exist under Core Configuration.
        assert "32. **[" not in content

    def test_entry_appears_before_onsite_onprem_heading(self):
        content = _read('docs/index.md')
        entry_pos = content.index(f"31. **[{README_ENTRY_TITLE}]")
        onprem_heading_pos = content.index("### Onsite On-Premises Volume")
        assert entry_pos < onprem_heading_pos

    def test_entry_uses_html_extension_not_md(self):
        content = _read('docs/index.md')
        match = re.search(rf"31\. \*\*\[{re.escape(README_ENTRY_TITLE)}\]\(([^)]+)\)", content)
        assert match is not None
        assert match.group(1) == DOC_URL_PATH


# ---------------------------------------------------------------------------
# docs/print_all.md
# ---------------------------------------------------------------------------

class TestPrintAllOrderedPaths:
    def test_ordered_paths_includes_engineering_doc(self):
        content = _read('docs/print_all.md')
        assert "engineering/opentofu_aws_simulation.md" in content

    def test_engineering_doc_positioned_between_migration_guide_and_ami_design(self):
        content = _read('docs/print_all.md')
        assign_line = next(line for line in content.splitlines() if 'ordered_paths' in line)
        paths = re.search(r'"([^"]+)"', assign_line).group(1).split(',')

        migration_idx = paths.index('opentofu-migration.md')
        engineering_idx = paths.index('engineering/opentofu_aws_simulation.md')
        ami_idx = paths.index('ami-design.md')

        assert migration_idx < engineering_idx < ami_idx

    def test_engineering_doc_appears_exactly_once_in_ordered_paths(self):
        content = _read('docs/print_all.md')
        assign_line = next(line for line in content.splitlines() if 'ordered_paths' in line)
        paths = re.search(r'"([^"]+)"', assign_line).group(1).split(',')
        assert paths.count('engineering/opentofu_aws_simulation.md') == 1

    def test_ordered_paths_still_contains_no_duplicate_entries(self):
        """Regression check: inserting the new path must not have duplicated any existing entry."""
        content = _read('docs/print_all.md')
        assign_line = next(line for line in content.splitlines() if 'ordered_paths' in line)
        paths = re.search(r'"([^"]+)"', assign_line).group(1).split(',')
        assert len(paths) == len(set(paths)), "docs/print_all.md ordered_paths must not contain duplicates"


# ---------------------------------------------------------------------------
# llms.txt
# ---------------------------------------------------------------------------

class TestLlmsTxtOpenTofuEntry:
    def test_entry_format(self):
        content = _read('llms.txt')
        expected = (
            f"- [OpenTofu AWS Simulation Runbook]({DOC_REL_PATH}) : Engineering runbook for "
            "offline AWS deployment simulation, unit testing matrices, and multi-agent/"
            "multi-human collaboration workflows."
        )
        assert expected in content

    def test_entry_appears_exactly_once(self):
        content = _read('llms.txt')
        assert content.count('[OpenTofu AWS Simulation Runbook]') == 1

    def test_entry_appears_directly_after_jules_platform_guide(self):
        content = _read('llms.txt')
        jules_pos = content.index('[Google Jules AI Platform Guide]')
        entry_pos = content.index('[OpenTofu AWS Simulation Runbook]')
        assert jules_pos < entry_pos

        between = content[jules_pos:entry_pos]
        assert between.count('\n- [') == 1, (
            "OpenTofu Simulation Runbook entry must immediately follow the Jules AI Platform Guide entry"
        )

    def test_entry_before_documentation_framework_heading(self):
        content = _read('llms.txt')
        entry_pos = content.index('[OpenTofu AWS Simulation Runbook]')
        next_heading_pos = content.index('## Documentation Framework & Project Utilities')
        assert entry_pos < next_heading_pos

    def test_referenced_file_exists(self):
        content = _read('llms.txt')
        match = re.search(r'\[OpenTofu AWS Simulation Runbook\]\(([^)]+)\)', content)
        assert match is not None
        resolved = os.path.join(WORKSPACE_ROOT, match.group(1))
        assert os.path.isfile(resolved)


# ---------------------------------------------------------------------------
# sitemap.txt
# ---------------------------------------------------------------------------

class TestSitemapTxtOpenTofuEntry:
    def test_url_present(self):
        content = _read('sitemap.txt')
        expected_url = f"{SITE_BASE_URL}/{DOC_URL_PATH}"
        assert expected_url in content

    def test_url_appears_exactly_once(self):
        content = _read('sitemap.txt')
        expected_url = f"{SITE_BASE_URL}/{DOC_URL_PATH}"
        assert content.count(expected_url) == 1

    def test_url_is_last_non_empty_line(self):
        content = _read('sitemap.txt')
        lines = [line for line in content.splitlines() if line.strip()]
        assert lines[-1] == f"{SITE_BASE_URL}/{DOC_URL_PATH}"

    def test_all_sitemap_txt_urls_are_well_formed(self):
        content = _read('sitemap.txt')
        for line in content.splitlines():
            if not line.strip():
                continue
            assert line.startswith(f"{SITE_BASE_URL}"), f"Malformed sitemap.txt entry: {line}"


# ---------------------------------------------------------------------------
# sitemap.xml
# ---------------------------------------------------------------------------

class TestSitemapXmlOpenTofuEntry:
    NS = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    def _parse_urls(self):
        tree = ET.parse(os.path.join(WORKSPACE_ROOT, 'sitemap.xml'))
        return tree.getroot().findall('ns:url', self.NS)

    def test_url_entry_present_with_expected_fields(self):
        expected_loc = f"{SITE_BASE_URL}/{DOC_URL_PATH}"
        matches = [
            url_node for url_node in self._parse_urls()
            if url_node.find('ns:loc', self.NS).text.strip() == expected_loc
        ]
        assert len(matches) == 1, f"Expected exactly one sitemap.xml <url> entry for {expected_loc}"

        url_node = matches[0]
        assert url_node.find('ns:lastmod', self.NS).text.strip() == '2026-08-11'
        assert url_node.find('ns:changefreq', self.NS).text.strip() == 'monthly'
        assert url_node.find('ns:priority', self.NS).text.strip() == '0.8'

    def test_url_entry_is_final_entry_in_document(self):
        urls = self._parse_urls()
        expected_loc = f"{SITE_BASE_URL}/{DOC_URL_PATH}"
        assert urls[-1].find('ns:loc', self.NS).text.strip() == expected_loc

    def test_all_locs_are_unique(self):
        urls = self._parse_urls()
        locs = [u.find('ns:loc', self.NS).text.strip() for u in urls]
        assert len(locs) == len(set(locs)), "sitemap.xml must not contain duplicate <loc> URLs"

    def test_sitemap_xml_and_txt_have_matching_url_sets(self):
        """Cross-file consistency: every URL in sitemap.xml should also appear in sitemap.txt."""
        xml_locs = {u.find('ns:loc', self.NS).text.strip() for u in self._parse_urls()}
        txt_content = _read('sitemap.txt')
        txt_urls = {line.strip() for line in txt_content.splitlines() if line.strip()}
        assert xml_locs == txt_urls, "sitemap.xml and sitemap.txt URL sets have diverged"


# ---------------------------------------------------------------------------
# Cross-file consistency
# ---------------------------------------------------------------------------

class TestCrossFileConsistency:
    """Ensures every surface referencing the new runbook agrees on the same canonical
    relative markdown path / compiled HTML URL, preventing broken or mismatched links
    across the documentation index files touched by this PR."""

    @pytest.mark.parametrize("rel_path,md_or_html", [
        ('README.md', 'md'),
        ('llms.txt', 'md'),
        ('docs/index.md', 'html'),
        ('docs/_config.yml', 'html'),
        ('docs/print_all.md', 'md'),
        ('sitemap.txt', 'html'),
        ('sitemap.xml', 'html'),
    ])
    def test_file_references_the_new_doc(self, rel_path, md_or_html):
        content = _read(rel_path)
        if md_or_html == 'md':
            assert 'engineering/opentofu_aws_simulation.md' in content, (
                f"{rel_path} does not reference the new runbook's markdown source path"
            )
        else:
            assert 'engineering/opentofu_aws_simulation.html' in content, (
                f"{rel_path} does not reference the new runbook's compiled HTML path"
            )