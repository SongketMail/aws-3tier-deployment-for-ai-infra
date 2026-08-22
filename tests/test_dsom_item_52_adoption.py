"""
Tests validating the adoption of the Deep State of Mind (DSOM) For My AI
framework as Item 52 of the Google Jules Master Knowledge Ledger.

This covers the specific content changes introduced across:
- .agents/brain/active_context_manifest.md
- .agents/brain/jules_knowledge_ledger.md
- .agents/skills/jules-knowledge/SKILL.md
- llms-full.txt
- llms.xml
"""
import os
import re

import pytest


WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DSOM_URL = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/START-HERE/"

STALE_PRIMARY_GOAL = "Adopt and codify the Local Knowledge-First Discovery Protocol and Rule 29."


def _read(rel_path):
    full_path = os.path.join(WORKSPACE_ROOT, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# .agents/brain/active_context_manifest.md
# ---------------------------------------------------------------------------

def test_active_context_manifest_front_matter_updated():
    """The manifest's front matter timestamp and topics must reflect the DSOM update."""
    content = _read('.agents/brain/active_context_manifest.md')

    assert "timestamp: 2026-08-14T10:05:00Z" in content
    assert 'topics: ["agents", "context", "manifest", "memory", "brain", "okf", "dsom"]' in content


def test_active_context_manifest_primary_goal_mentions_dsom():
    """The Primary Goal must reference the DSOM framework and its canonical URL."""
    content = _read('.agents/brain/active_context_manifest.md')

    assert "Deep State of Mind (DSOM) For My AI Framework" in content
    assert DSOM_URL in content
    # The previous session's primary goal text must no longer be present verbatim.
    assert STALE_PRIMARY_GOAL not in content


def test_active_context_manifest_lists_dsom_subsystems():
    """The Agent Skills & Brain Integration bullet must enumerate the DSOM building blocks."""
    content = _read('.agents/brain/active_context_manifest.md')

    assert "19 entry points" in content
    assert "Tri-Phasic Mind cognitive architecture" in content
    assert "4 functional subsystems" in content
    assert "Item 52" in content


def test_active_context_manifest_milestones_reference_52_items():
    """Completed milestones and the file registry must both cite 52 knowledge items."""
    content = _read('.agents/brain/active_context_manifest.md')

    assert "organizing all 52 items of Jules knowledge." in content
    assert "Master Ledger indexing all 52 items of Jules knowledge from Day 0 until now" in content
    # The stale count of 51 must not remain anywhere in this file.
    assert "51 items" not in content
    assert "the 51 compiled Jules knowledge items" not in content


# ---------------------------------------------------------------------------
# .agents/brain/jules_knowledge_ledger.md
# ---------------------------------------------------------------------------

def test_ledger_front_matter_timestamp_updated():
    content = _read('.agents/brain/jules_knowledge_ledger.md')
    assert "timestamp: 2026-08-14T10:00:00Z" in content


def test_ledger_intro_and_heading_reflect_52_items():
    content = _read('.agents/brain/jules_knowledge_ledger.md')

    assert "fifty-two (52) distinct items" in content
    assert "## \U0001F9E0 Master Index of Jules Knowledge (52 Items)" in content
    # Old wording must not linger.
    assert "fifty-one (51) distinct items" not in content
    assert "(51 Items)" not in content


def test_ledger_item_52_entry_is_well_formed():
    """Item 52 must document DSOM adoption and map to the jules-knowledge skill."""
    content = _read('.agents/brain/jules_knowledge_ledger.md')

    match = re.search(r'\| \*\*52\*\* \| (.+?) \| (.+?) \|\n', content)
    assert match is not None, "Ledger must contain a row for knowledge item 52"

    description, skill = match.group(1), match.group(2)

    assert "Deep State of Mind (DSOM) For My AI framework" in description
    assert DSOM_URL in description
    assert "19 entry points" in description
    assert "Tri-Phasic Mind cognitive architecture" in description
    assert "Active, Twilight, and Deep states" in description
    assert "4 core functional subsystems" in description
    assert skill.strip() == "`jules-knowledge`"


def test_ledger_item_ids_are_sequential_from_1_to_52():
    """The ledger table must index exactly IDs 1 through 52 with no gaps or duplicates."""
    content = _read('.agents/brain/jules_knowledge_ledger.md')

    ids = [int(i) for i in re.findall(r'\| \*\*(\d+)\*\* \|', content)]

    assert ids == list(range(1, 53)), f"Expected sequential ledger IDs 1-52, got: {ids}"


def test_ledger_does_not_contain_item_53():
    content = _read('.agents/brain/jules_knowledge_ledger.md')
    assert "| **53** |" not in content


# ---------------------------------------------------------------------------
# .agents/skills/jules-knowledge/SKILL.md
# ---------------------------------------------------------------------------

def test_skill_dsom_section_heading_and_position():
    """A new section 5 must introduce the DSOM framework ahead of script hardening."""
    content = _read('.agents/skills/jules-knowledge/SKILL.md')

    dsom_idx = content.find("## 5. Deep State of Mind (DSOM) Framework & Sovereign AI Topology")
    hardening_idx = content.find("## 6. Script Hardening, Testing & Formatting Compliance")

    assert dsom_idx != -1, "SKILL.md must contain the new DSOM section heading"
    assert hardening_idx != -1, "SKILL.md must contain the renumbered Script Hardening section heading"
    assert dsom_idx < hardening_idx, "DSOM section must precede the Script Hardening section"

    # The old section-5 heading for script hardening must no longer exist.
    assert "## 5. Script Hardening, Testing & Formatting Compliance" not in content


def test_skill_dsom_section_contains_expected_items():
    content = _read('.agents/skills/jules-knowledge/SKILL.md')

    assert "20. **DSOM Adoption & Entry Points:**" in content
    assert DSOM_URL in content
    assert "21. **Tri-Phasic Mind Cognitive Model:**" in content
    assert "**Active State (Conscious):**" in content
    assert "**Twilight State (Subconscious):**" in content
    assert "**Deep State (Unconscious/Dream):**" in content
    assert "22. **Four Core Functional Subsystems:**" in content
    assert "**Cognitive Architecture:**" in content
    assert "**Memory Stratification:**" in content
    assert "**Dreaming & Consolidation:**" in content
    assert "**Metacognition & Guardrails:**" in content
    assert "23. **AI Boot & Initialization Sequence:**" in content
    assert "5-step boot sequence" in content


def test_skill_script_hardening_items_renumbered_24_to_29():
    """Items formerly numbered 20-25 under script hardening must now be 24-29."""
    content = _read('.agents/skills/jules-knowledge/SKILL.md')

    assert "24. **Bash Script Navigation & Input Checks:**" in content
    assert "25. **Python Codebase Formatting Cleanup:**" in content
    assert "26. **Complete Script Docstrings:**" in content
    assert "27. **Automated Pytest Suite:**" in content
    assert "28. **DRY Script Refactoring:**" in content
    assert "29. **Root Caches & IaC Exclusions:**" in content

    # None of the previous numbering (20-25) should remain attached to these items.
    for stale_num, bold_title in [
        (20, "Bash Script Navigation & Input Checks"),
        (21, "Python Codebase Formatting Cleanup"),
        (22, "Complete Script Docstrings"),
        (23, "Automated Pytest Suite"),
        (24, "DRY Script Refactoring"),
        (25, "Root Caches & IaC Exclusions"),
    ]:
        assert f"{stale_num}. **{bold_title}:**" not in content


def test_skill_item_numbers_are_sequential_from_1_to_29():
    """All numbered knowledge items in SKILL.md must form an unbroken 1-29 sequence."""
    content = _read('.agents/skills/jules-knowledge/SKILL.md')

    numbers = [int(n) for n in re.findall(r'^(\d+)\. \*\*', content, re.MULTILINE)]

    assert numbers == list(range(1, 30)), f"Expected sequential item numbers 1-29, got: {numbers}"


def test_skill_dsom_footer_still_present():
    """The mandatory DSOM footer must survive the section renumbering edit."""
    content = _read('.agents/skills/jules-knowledge/SKILL.md')
    assert "Deep State of Mind (DSOM) For My AI Protocol" in content


# ---------------------------------------------------------------------------
# llms-full.txt / llms.xml (generated artifacts embedding active_context_manifest.md)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rel_path", ["llms-full.txt", "llms.xml"])
def test_generated_docs_embed_updated_active_context_manifest(rel_path):
    """Both compiled LLM index artifacts must mirror the updated manifest content."""
    content = _read(rel_path)

    assert "Adopt and codify the Deep State of Mind (DSOM) For My AI Framework" in content
    assert DSOM_URL in content
    assert "organizing all 52 items of Jules knowledge." in content
    assert "Master Ledger indexing all 52 items of Jules knowledge from Day 0 until now" in content


@pytest.mark.parametrize("rel_path", ["llms-full.txt", "llms.xml"])
def test_generated_docs_do_not_retain_stale_primary_goal(rel_path):
    """The compiled artifacts must not still show the pre-DSOM primary goal wording."""
    content = _read(rel_path)
    assert STALE_PRIMARY_GOAL not in content


def test_llms_full_active_context_manifest_section_matches_source():
    """The active_context_manifest.md section embedded in llms-full.txt must match the
    current source file's body content (minus front matter) verbatim, guarding against
    stale/regenerated drift between the source doc and the compiled manual."""
    manifest_content = _read('.agents/brain/active_context_manifest.md')
    # Strip YAML front matter (--- ... ---)
    body = manifest_content.split('---', 2)[2].strip()

    llms_full_content = _read('llms-full.txt')

    section_header = "### .agents/brain/active_context_manifest.md (.agents/brain/active_context_manifest.md)"
    assert section_header in llms_full_content

    section_start = llms_full_content.index(section_header)
    # The next top-level '---' after the header marks the end of embedded content for this doc.
    next_section = llms_full_content.find("\n---\n\n### ", section_start)
    if next_section == -1:
        next_section = len(llms_full_content)
    embedded_section = llms_full_content[section_start:next_section]

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        assert stripped in embedded_section, (
            f"Line from active_context_manifest.md missing in llms-full.txt embedded section: {stripped!r}"
        )