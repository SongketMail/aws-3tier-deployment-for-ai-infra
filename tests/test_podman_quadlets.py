import os
import re
import configparser
import pytest

def extract_quadlets_from_md(filepath):
    """
    Parses a Markdown file and extracts all code blocks that represent systemd Quadlet files.

    A block is recognized as a systemd Quadlet if it has ```ini or ```systemd syntax, or
    contains standard headers like [Pod], [Network], or [Container]. Normalizes line endings to LF.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')

    blocks = []
    # Regular expression to extract code blocks with support for leading spaces
    pattern = re.compile(r'^\s*```(?:ini|systemd|yaml)?\n(.*?)\n\s*```', re.DOTALL | re.MULTILINE)
    for match in pattern.finditer(content):
        code = match.group(1)
        if any(header in code for header in ['[Pod]', '[Network]', '[Container]']):
            blocks.append(code)
    return blocks

def parse_quadlet_ini(quadlet_str):
    """
    Parses a raw Quadlet string into a ConfigParser object.
    Automatically strips comments (starting with # or ;) to prevent configparser errors.
    """
    clean_lines = []
    for line in quadlet_str.split('\n'):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if line_stripped.startswith('#') or line_stripped.startswith(';'):
            continue
        clean_lines.append(line_stripped)

    parser = configparser.ConfigParser(strict=False, interpolation=None)
    # configparser requires option keys to be case-sensitive for systemd options (e.g. UserNS, PublishPort)
    parser.optionxform = str
    parser.read_string('\n'.join(clean_lines))
    return parser

def test_podman_quadlet_compliance():
    """
    Validates that the Podman Quadlet configurations documented in docs/onprem/podman-quadlet.md
    fully comply with systemd INI specifications and security standards.
    """
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/onprem/podman-quadlet.md'))
    assert os.path.exists(filepath), "podman-quadlet.md does not exist"

    quadlets = extract_quadlets_from_md(filepath)
    assert len(quadlets) > 0, "No Quadlet blocks found in docs/onprem/podman-quadlet.md"

    container_count = 0
    pod_count = 0
    network_count = 0

    for quad_str in quadlets:
        config = parse_quadlet_ini(quad_str)

        # 1. Check Pod configurations
        if config.has_section('Pod'):
            pod_count += 1
            assert config.has_option('Pod', 'PodName'), "Pod block missing 'PodName'"
            assert config.has_option('Pod', 'Network'), "Pod block missing 'Network'"
            assert config.get('Pod', 'UserNS') == 'keep-id:uid=2001,gid=2001', \
                "Pod namespace mapping must be set to keep-id:uid=2001,gid=2001 to maintain local host ownership"

        # 2. Check Network configurations
        if config.has_section('Network'):
            network_count += 1
            assert config.has_option('Network', 'NetworkName'), "Network block missing 'NetworkName'"
            assert config.has_option('Network', 'Subnet'), "Network block missing 'Subnet'"

        # 3. Check Container configurations
        if config.has_section('Container'):
            container_count += 1
            assert config.has_option('Container', 'ContainerName'), "Container block missing 'ContainerName'"
            assert config.has_option('Container', 'Image'), "Container block missing 'Image'"
            assert config.has_option('Container', 'UserNS'), "Container block missing 'UserNS' namespace mapping"
            assert config.get('Container', 'UserNS') == 'keep-id:uid=2001,gid=2001', \
                "Container namespace mapping must be set to keep-id:uid=2001,gid=2001 to ensure local storage sovereignty"

    # Make sure we verified at least one of each Quadlet type
    assert pod_count >= 1, "Expected at least one [Pod] Quadlet definition"
    assert network_count >= 1, "Expected at least one [Network] Quadlet definition"
    assert container_count >= 1, "Expected at least one [Container] Quadlet definition"

def test_podman_environmental_and_lingering_documentation():
    """
    Verifies that the Quadlet documentation properly lists lingering setups and core user-level env vars.
    """
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/onprem/podman-quadlet.md'))
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verify lingering references
    assert "loginctl enable-linger songket" in content, "Missing reference to enabling systemd user lingering"
    assert "/var/lib/systemd/linger/songket" in content, "Missing reference to verification of lingering user-space path"

    # Verify core rootless environment variables
    assert "XDG_RUNTIME_DIR" in content, "Missing reference to required XDG_RUNTIME_DIR variable"
    assert "DBUS_SESSION_BUS_ADDRESS" in content, "Missing reference to required DBUS_SESSION_BUS_ADDRESS variable"
