import os
import re

def get_markdown_files(root_dir):
    """
    Recursively scans the root directory for Markdown files, adhering to standard filter rules.
    Skips hidden folders (like .git, .github) but includes .agents.
    """
    md_files = []
    for root, _, files in os.walk(root_dir):
        # Apply should_process_dir filter
        parts = root.split(os.sep)
        skip = False
        for part in parts:
            if part.startswith('.') and part != '.agents':
                skip = True
                break
        if skip:
            continue

        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def parse_yaml_metadata(filepath):
    """
    Parses front matter metadata from a Markdown file.
    Verifies that the YAML block starts at line 1, column 1.
    Normalizes line endings to LF.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')

    # Verify that the front matter block starts exactly at line 1, column 1
    if not content.startswith('---\n'):
        return None, "File does not start with front matter '---' on line 1, column 1"

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, "Malformed or missing front matter termination"

    fm_str = parts[1]
    body = parts[2]

    # Parse YAML keys
    metadata = {}
    lines = fm_str.strip().split('\n')
    current_key = None

    for line in lines:
        if not line.strip():
            continue

        # Check for list items
        if line.strip().startswith('-') and current_key:
            val = line.strip()[1:].strip().strip('"\'')
            if isinstance(metadata[current_key], list):
                metadata[current_key].append(val)
            else:
                metadata[current_key] = [val]
            continue

        match = re.match(r'^([a-zA-Z0-9_\-]+)\s*:\s*(.*)$', line)
        if match:
            key = match.group(1).strip()
            val = match.group(2).strip()
            current_key = key

            # Check for inline list [a, b]
            if val.startswith('[') and val.endswith(']'):
                items = [i.strip().strip('"\'') for i in val[1:-1].split(',') if i.strip()]
                metadata[key] = items
            elif val.startswith('{') and val.endswith('}'):
                metadata[key] = val
            elif val == '':
                metadata[key] = []
            else:
                # Keep quotes intact to verify quoting rules
                metadata[key] = val

    return (metadata, body), None

def test_markdown_okf_front_matter_compliance():
    """
    Scans every Markdown file in the repository to ensure strict OKF (Open Knowledge Format) v0.1
    and Jekyll metadata standards are met.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    md_files = get_markdown_files(workspace_root)
    assert len(md_files) > 0, "No Markdown files found in the repository"

    for filepath in md_files:
        rel_path = os.path.relpath(filepath, workspace_root)
        parsed, error = parse_yaml_metadata(filepath)

        # 1. Assert file contains front matter at line 1, column 1
        assert parsed is not None, f"OKF Compliance Error in {rel_path}: {error}"

        metadata, body = parsed

        # 2. Assert required OKF keys are present
        required_keys = ['layout', 'okf_version', 'type', 'title', 'timestamp', 'topics']
        for key in required_keys:
            assert key in metadata, f"OKF Compliance Error in {rel_path}: Missing mandatory key '{key}'"

        # 3. Assert correct OKF version specification
        assert metadata['okf_version'].strip('"\'') == '0.1', f"OKF Version mismatch in {rel_path}: expected '0.1'"

        # 4. Assert strict double-quoting standard for strings with special characters
        for key, val in metadata.items():
            if isinstance(val, str) and not (val.startswith('[') or val.startswith('{')):
                # Ignore timestamp formats or plain alphanumeric tags
                if key == 'timestamp' or re.match(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$', val):
                    continue

                # Check for special characters like colons, brackets, braces, parentheses, emojis, or symbols
                if re.search(r'[:\[\]\{\}\(\)#&%@|+=><!?*~\s]', val):
                    # Value must be enclosed in double quotes or single quotes
                    is_quoted = (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'"))
                    assert is_quoted, f"OKF Quoting Error in {rel_path} for key '{key}': value {val} must be enclosed in double quotes due to special characters"

def test_markdown_dsom_footer_compliance():
    """
    Validates that every Markdown documentation file inside the designated Sovereign and Engineering volumes
    concludes with a valid Deep State of Mind (DSOM) footer, affirming alignment with standard engineering protocols.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    md_files = get_markdown_files(workspace_root)

    for filepath in md_files:
        rel_path = os.path.relpath(filepath, workspace_root).replace('\\', '/')

        # Only check files belonging to the core DSOM engineering, auditing, onprem, or skills domains
        is_dsom_domain = (
            rel_path.startswith('docs/onprem/') or
            rel_path.startswith('docs/engineering/') or
            rel_path == 'docs/audits/asimp-output.md' or
            rel_path == 'docs/audits/security-posture-assessment.md' or
            rel_path.startswith('.agents/skills/') or
            rel_path == 'AGENTS.md' or
            rel_path == '.agents/AGENTS.md'
        )
        if not is_dsom_domain:
            continue

        parsed, _ = parse_yaml_metadata(filepath)
        if not parsed:
            continue

        metadata, body = parsed

        # Verify the body has reference to Deep State of Mind (DSOM) or DSOM
        assert ("Deep State of Mind" in body or "DSOM" in body), \
            f"DSOM Footer Compliance Error in {rel_path}: document must include the standard Deep State of Mind (DSOM) footer"
