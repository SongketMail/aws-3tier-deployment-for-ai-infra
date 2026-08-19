"""
Test suite covering the "Start Here" dual-audience onboarding standard introduced
across README.md, START-HERE.md, SUMMARY.md, docs/SUMMARY.md, docs/_config.yml,
docs/index.md, docs/start-here.md, llms.txt, llms-full.txt, and llms.xml.

These tests specifically target the content added/changed by this PR, rather than
re-validating generic repository-wide compliance rules already covered by
test_md_compliance.py and test_integration_compliance.py.
"""
import os
import re

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _read(rel_path):
    with open(os.path.join(WORKSPACE_ROOT, rel_path), 'r', encoding='utf-8') as f:
        return f.read()


def _extract_front_matter_and_body(content):
    assert content.startswith('---\n'), "content must start with front matter"
    parts = content.split('---', 2)
    assert len(parts) >= 3, "front matter must be terminated"
    return parts[1], parts[2]


def _headings(body):
    """Return the list of markdown heading lines (lines starting with '#')."""
    return [line for line in body.split('\n') if line.strip().startswith('#')]


# ---------------------------------------------------------------------------
# START-HERE.md (root) and docs/start-here.md
# ---------------------------------------------------------------------------

class TestStartHereDualCopyStructure:
    def test_root_start_here_exists(self):
        assert os.path.exists(os.path.join(WORKSPACE_ROOT, 'START-HERE.md'))

    def test_docs_start_here_exists(self):
        assert os.path.exists(os.path.join(WORKSPACE_ROOT, 'docs', 'start-here.md'))

    def test_root_start_here_front_matter_fields(self):
        content = _read('START-HERE.md')
        fm, _ = _extract_front_matter_and_body(content)
        assert 'layout: "default"' in fm
        assert 'okf_version: "0.1"' in fm
        assert 'type: "Portal"' in fm
        assert 'title: "Start Here: Pragmatic Onboarding & Execution Standard"' in fm
        assert 'timestamp: 2026-08-13T15:00:00Z' in fm
        assert '"start-here"' in fm and '"onboarding"' in fm and '"dsom"' in fm

    def test_docs_start_here_front_matter_matches_root(self):
        root_fm, _ = _extract_front_matter_and_body(_read('START-HERE.md'))
        docs_fm, _ = _extract_front_matter_and_body(_read('docs/start-here.md'))
        assert root_fm == docs_fm, (
            "The docs/ copy of the Start Here guide should carry identical OKF "
            "front matter metadata to the root copy"
        )

    def test_root_and_docs_start_here_headings_are_identical(self):
        _, root_body = _extract_front_matter_and_body(_read('START-HERE.md'))
        _, docs_body = _extract_front_matter_and_body(_read('docs/start-here.md'))
        assert _headings(root_body) == _headings(docs_body), (
            "Both onboarding entry points must share an identical heading structure"
        )

    def test_root_and_docs_start_here_bodies_differ_only_by_docs_prefix(self):
        """
        The root copy links into docs/ using a 'docs/' prefix (since it lives at
        the repository root), while the docs/ copy uses paths relative to the
        docs/ directory (no 'docs/' prefix). Beyond that single systematic
        difference, the two files should be identical.
        """
        _, root_body = _extract_front_matter_and_body(_read('START-HERE.md'))
        _, docs_body = _extract_front_matter_and_body(_read('docs/start-here.md'))

        # Re-inserting the 'docs/' prefix into the docs/ copy's markdown links
        # should reproduce the root copy's body exactly.
        reconstructed = re.sub(
            r'\]\((?!http|#)(tutorials/|how-to/|scripts\.md|SOP-KNOWLEDGE-FIRST-DISCOVERY\.md|architecture\.md|modules/|reference/|explanation/|aws-vs-self-hosted-review\.md|jules-platform-guide\.md)',
            r'](docs/\1',
            docs_body,
        )
        assert reconstructed == root_body

    def test_dual_audience_diataxis_quadrants_present(self):
        for path in ('START-HERE.md', 'docs/start-here.md'):
            body = _read(path)
            for quadrant in ('Tutorials', 'How-To Guides', 'Reference Specs', 'Explanation'):
                assert quadrant in body, f"Missing Diátaxis quadrant '{quadrant}' in {path}"
            assert 'Human Developer Pathway' in body
            assert 'Autonomous AI Agent Pathway' in body

    def test_human_pathway_quickstart_commands_present(self):
        for path in ('START-HERE.md', 'docs/start-here.md'):
            body = _read(path)
            assert 'git clone https://github.com/songketmail/aws-3tier-deployment-for-ai-infra.git' in body
            assert 'python3 scripts/prepare_docs.py && python3 scripts/parse_llms.py' in body
            assert re.search(r'^pytest$', body, flags=re.MULTILINE), \
                f"Expected a standalone 'pytest' command in {path}"

    def test_agent_pathway_protocol_steps_in_order(self):
        expected_steps = [
            'BOUNDARY PARSING',
            'CONTEXT ANCHORING',
            'DELTA EXECUTION & VERIFICATION',
            'STRUCTURED DIFF & COMMIT',
        ]
        for path in ('START-HERE.md', 'docs/start-here.md'):
            body = _read(path)
            positions = [body.index(step) for step in expected_steps]
            assert positions == sorted(positions), (
                f"Agent ingestion protocol steps must appear in order in {path}"
            )

    def test_agent_context_governance_rules_present(self):
        for path in ('START-HERE.md', 'docs/start-here.md'):
            body = _read(path)
            assert 'Context Window Minimization' in body
            assert 'Metadata Compliance (OKF v0.1)' in body
            assert 'Multi-Agent Interoperability' in body
            assert 'Eleven (11) dedicated agent skills' in body

    def test_dsom_governance_footer_present(self):
        for path in ('START-HERE.md', 'docs/start-here.md'):
            body = _read(path)
            assert 'Deep State of Mind (DSOM) Governance' in body
            assert 'End of Start Here Standard.' in body

    def test_referenced_relative_links_resolve_from_each_file(self):
        """
        Sanity-check that every relative markdown link inside each Start Here
        document resolves to a real file on disk (targeted regression check,
        complementary to the repo-wide link integrity test).
        """
        for path in ('START-HERE.md', 'docs/start-here.md'):
            content = _read(path)
            links = re.findall(r'\]\(([^)]+)\)', content)
            current_dir = os.path.dirname(os.path.join(WORKSPACE_ROOT, path))
            for url in links:
                if url.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue
                clean_url = url.split('#')[0].split('?')[0]
                resolved = os.path.abspath(os.path.join(current_dir, clean_url))
                assert os.path.exists(resolved), f"Broken link '{url}' referenced from {path}"


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

class TestReadmeStartHereEntry:
    def test_readme_links_start_here_in_conceptual_alignment_section(self):
        content = _read('README.md')
        assert (
            '* **[Start Here: Pragmatic Onboarding & Execution Standard](START-HERE.md):** '
            'Dual-audience onboarding standard for Human Engineers and Autonomous AI Agents '
            '(Diátaxis "learn-by-doing" ethos).'
        ) in content

    def test_start_here_entry_appears_before_aws_adoption_roadmap(self):
        content = _read('README.md')
        start_here_pos = content.index('[Start Here: Pragmatic Onboarding & Execution Standard]')
        roadmap_pos = content.index('[AWS Phased Adoption Roadmap & Costing Guide]')
        assert start_here_pos < roadmap_pos

    def test_start_here_entry_under_correct_heading(self):
        content = _read('README.md')
        heading_pos = content.index('### 1. Conceptual Alignment & Architecture')
        entry_pos = content.index('[Start Here: Pragmatic Onboarding & Execution Standard]')
        assert heading_pos < entry_pos


# ---------------------------------------------------------------------------
# SUMMARY.md (root) and docs/SUMMARY.md
# ---------------------------------------------------------------------------

class TestSummaryTablesOfContents:
    def test_root_summary_exists_with_okf_front_matter(self):
        content = _read('SUMMARY.md')
        fm, body = _extract_front_matter_and_body(content)
        assert 'title: "Table of contents"' in fm
        assert 'okf_version: "0.1"' in fm

    def test_root_summary_lists_start_here_guide_after_home(self):
        content = _read('SUMMARY.md')
        home_pos = content.index('* [Home](README.md)')
        start_here_pos = content.index('* [Start Here Guide](START-HERE.md)')
        legal_pos = content.index('* [Legal Notice & Disclaimer](docs/legal-notice.md)')
        assert home_pos < start_here_pos < legal_pos

    def test_root_summary_section_headings_present(self):
        content = _read('SUMMARY.md')
        for heading in (
            '## Tutorials',
            '## How-To Guides',
            '## Reference Specs',
            '## Explanation & Design',
            '## Architecture & Infrastructure Guides',
            '## Onsite On-Premises Volume',
            '## Security Posture & Audits',
            '## OpenTofu Submodules',
        ):
            assert heading in content, f"Missing section heading: {heading}"

    def test_root_summary_links_resolve(self):
        content = _read('SUMMARY.md')
        links = re.findall(r'\]\(([^)]+)\)', content)
        for url in links:
            if url.startswith(('http://', 'https://', '#')):
                continue
            resolved = os.path.abspath(os.path.join(WORKSPACE_ROOT, url.split('#')[0]))
            assert os.path.exists(resolved), f"Broken link in SUMMARY.md: {url}"

    def test_docs_summary_lists_start_here_guide_with_relative_path(self):
        content = _read('docs/SUMMARY.md')
        assert '* [Start Here Guide](start-here.md)' in content, (
            "docs/SUMMARY.md must reference the docs-local start-here.md (no 'docs/' prefix)"
        )

    def test_docs_summary_start_here_entry_ordered_between_home_and_legal_notice(self):
        content = _read('docs/SUMMARY.md')
        home_pos = content.index('* [Home](README.md)')
        start_here_pos = content.index('* [Start Here Guide](start-here.md)')
        legal_pos = content.index('* [Legal Notice & Disclaimer](legal-notice.md)')
        assert home_pos < start_here_pos < legal_pos

    def test_docs_summary_links_resolve_relative_to_docs(self):
        content = _read('docs/SUMMARY.md')
        links = re.findall(r'\]\(([^)]+)\)', content)
        docs_dir = os.path.join(WORKSPACE_ROOT, 'docs')
        for url in links:
            if url.startswith(('http://', 'https://', '#')):
                continue
            resolved = os.path.abspath(os.path.join(docs_dir, url.split('#')[0]))
            assert os.path.exists(resolved), f"Broken link in docs/SUMMARY.md: {url}"


# ---------------------------------------------------------------------------
# docs/_config.yml
# ---------------------------------------------------------------------------

class TestJekyllConfigNavbar:
    def test_start_here_navbar_entry_present(self):
        content = _read('docs/_config.yml')
        assert '- title: "Start Here"' in content
        assert 'url: "/start-here.html"' in content

    def test_start_here_navbar_entry_positioned_between_home_and_docs_portal(self):
        content = _read('docs/_config.yml')
        home_pos = content.index('- title: "Home"')
        start_here_pos = content.index('- title: "Start Here"')
        docs_portal_pos = content.index('- title: "Docs Portal"')
        assert home_pos < start_here_pos < docs_portal_pos

    def test_navbar_entry_is_well_formed_yaml_pair(self):
        content = _read('docs/_config.yml')
        match = re.search(
            r'- title: "Start Here"\s*\n\s*url: "/start-here\.html"',
            content,
        )
        assert match is not None, "Start Here navbar entry must pair title and url on adjacent lines"


# ---------------------------------------------------------------------------
# docs/index.md
# ---------------------------------------------------------------------------

class TestDocsIndexStartHereEntry:
    def test_start_here_entry_present_in_core_configuration(self):
        content = _read('docs/index.md')
        assert (
            '**[Start Here: Onboarding Standard](start-here.html):** Dual-audience onboarding guide '
            'adapting Diátaxis learn-by-doing principle for Human Engineers and AI Agents.'
        ) in content

    def test_start_here_entry_appears_before_architecture_entry(self):
        content = _read('docs/index.md')
        start_here_pos = content.index('[Start Here: Onboarding Standard]')
        architecture_pos = content.index('[System Architecture](architecture.html)')
        assert start_here_pos < architecture_pos

    def test_start_here_entry_under_core_configuration_heading(self):
        content = _read('docs/index.md')
        heading_pos = content.index('### Core Configuration')
        entry_pos = content.index('[Start Here: Onboarding Standard]')
        assert heading_pos < entry_pos


# ---------------------------------------------------------------------------
# llms.txt
# ---------------------------------------------------------------------------

class TestLlmsTxtStartHereEntry:
    def test_start_here_entry_format(self):
        content = _read('llms.txt')
        assert (
            '- [START-HERE.md](START-HERE.md) : Dual-audience onboarding standard adapting '
            'Diátaxis learn-by-doing principle for Human Engineers and AI Agents.'
        ) in content

    def test_start_here_entry_is_first_under_project_resources(self):
        content = _read('llms.txt')
        heading_pos = content.index('## Project Resources')
        start_here_pos = content.index('[START-HERE.md](START-HERE.md)')
        readme_pos = content.index('[README.md](README.md)')
        assert heading_pos < start_here_pos < readme_pos

    def test_start_here_entry_appears_exactly_once(self):
        content = _read('llms.txt')
        assert content.count('[START-HERE.md](START-HERE.md)') == 1


# ---------------------------------------------------------------------------
# llms-full.txt
# ---------------------------------------------------------------------------

class TestLlmsFullTxtStartHereSection:
    def test_start_here_section_header_and_description(self):
        content = _read('llms-full.txt')
        assert '### START-HERE.md (START-HERE.md)' in content
        assert (
            '*Dual-audience onboarding standard adapting Diátaxis learn-by-doing principle '
            'for Human Engineers and AI Agents.*'
        ) in content

    def test_start_here_section_precedes_readme_section(self):
        content = _read('llms-full.txt')
        start_here_pos = content.index('### START-HERE.md (START-HERE.md)')
        readme_pos = content.index('### README.md (README.md)')
        assert start_here_pos < readme_pos

    def test_start_here_embedded_body_content_present(self):
        content = _read('llms-full.txt')
        assert '## 1. Epigraph & Onboarding Philosophy' in content
        assert '## 🧠 Deep State of Mind (DSOM) Governance' in content

    def test_jules_platform_guide_section_present(self):
        content = _read('llms-full.txt')
        assert '### Google Jules AI Platform Guide (docs/jules-platform-guide.md)' in content
        assert (
            '*Comprehensive technical showcase documenting our end-to-end development workflow, '
            'PR review collaboration, DSOM governance, and Google Antigravity integration.*'
        ) in content

    def test_root_main_tf_section_reflects_domain_module_refactor(self):
        content = _read('llms-full.txt')
        assert (
            '### 2. Infrastructure Domain Modules (`main.tf`, `compute.tf`, `database.tf`, `web.tf`)'
        ) in content
        # The stale, pre-refactor description referencing a single monolithic
        # module-calling sequence must no longer be present.
        assert 'Networking -> Security Groups -> ALB -> WAF -> ASG -> RDS -> Route 53' not in content

    def test_root_main_tf_embedded_content_no_longer_lists_removed_modules(self):
        """
        Regression check: the embedded terraform/main.tf content used to
        contain the alb/waf/asg/rds/standalone_ec2/jumphost/elasticache_valkey/
        route53 module blocks inline. After the refactor into compute.tf,
        database.tf, and web.tf, those blocks must not appear duplicated
        within the Root main.tf doc entry.
        """
        content = _read('llms-full.txt')
        start = content.index('### Root main.tf (terraform/main.tf)')
        end = content.index('### Root variables.tf (terraform/variables.tf)')
        section = content[start:end]
        for stale_module in (
            'module "alb"', 'module "waf"', 'module "asg"', 'module "rds"',
            'module "route53"', 'module "standalone_ec2"',
            'module "elasticache_valkey"', 'module "jumphost"',
        ):
            assert stale_module not in section, (
                f"{stale_module} should have been removed from the embedded main.tf content"
            )
        assert 'module "vpc"' in section
        assert 'module "security_groups"' in section


# ---------------------------------------------------------------------------
# llms.xml
# ---------------------------------------------------------------------------

class TestLlmsXmlStartHereDoc:
    def test_start_here_doc_entry_attributes(self):
        content = _read('llms.xml')
        assert (
            '<doc title="START-HERE.md" url="START-HERE.md" '
            'desc="Dual-audience onboarding standard adapting Diátaxis learn-by-doing '
            'principle for Human Engineers and AI Agents.">'
        ) in content

    def test_start_here_doc_entry_is_first_in_project_resources_section(self):
        content = _read('llms.xml')
        section_pos = content.index('<section name="Project Resources">')
        start_here_pos = content.index('<doc title="START-HERE.md"')
        readme_pos = content.index('<doc title="README.md"')
        assert section_pos < start_here_pos < readme_pos

    def test_start_here_doc_entry_appears_exactly_once(self):
        content = _read('llms.xml')
        assert content.count('<doc title="START-HERE.md"') == 1

    def test_jules_platform_guide_doc_entry_present(self):
        content = _read('llms.xml')
        assert (
            '<doc title="Google Jules AI Platform Guide" url="docs/jules-platform-guide.md" '
            'desc="Comprehensive technical showcase documenting our end-to-end development '
            'workflow, PR review collaboration, DSOM governance, and Google Antigravity '
            'integration.">'
        ) in content

    def test_root_main_tf_doc_entry_no_longer_lists_removed_modules(self):
        content = _read('llms.xml')
        start = content.index('<doc title="Root main.tf"')
        end = content.index('<doc title="Root variables.tf"')
        section = content[start:end]
        for stale_module in (
            'module "alb"', 'module "waf"', 'module "asg"', 'module "rds"',
            'module "route53"', 'module "standalone_ec2"',
            'module "elasticache_valkey"', 'module "jumphost"',
        ):
            assert stale_module not in section
        assert 'module "vpc"' in section
        assert 'module "security_groups"' in section

    def test_doc_open_and_close_tags_are_balanced(self):
        """
        llms.xml embeds raw markdown (including literal '<br>' tags and special
        characters) as element body text, so it is not strictly well-formed XML.
        Instead, verify structural balance of the custom <doc>...</doc> wrapper
        tags, which is the invariant the generation script guarantees.
        """
        content = _read('llms.xml')
        open_count = len(re.findall(r'<doc title="', content))
        close_count = content.count('</doc>')
        assert open_count == close_count
        assert open_count > 0