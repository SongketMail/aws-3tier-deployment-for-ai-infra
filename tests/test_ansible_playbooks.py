import os
import re
import pytest

def extract_ansible_playbooks_from_md(filepath):
    """
    Extracts all YAML code blocks from a Markdown file that resemble Ansible playbooks.

    A code block is selected if it starts with '```yaml' or '```yml' and contains top-level
    keys like '- name:' and 'hosts:'. Normalizes line endings to LF.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')

    blocks = []
    # Regular expression to extract code blocks
    pattern = re.compile(r'```(?:yaml|yml)\n(.*?)\n```', re.DOTALL)
    for match in pattern.finditer(content):
        code = match.group(1)
        if "hosts:" in code and "tasks:" in code:
            blocks.append(code)
    return blocks

def parse_yaml_tasks(playbook_str):
    """
    Extremely robust YAML-like parser specifically designed for validating Ansible playbooks
    in documentation. It parses sections, validates names, and collects tasks and properties.
    """
    lines = playbook_str.split('\n')
    plays = []
    current_play = None
    current_tasks = []
    in_tasks = False
    current_task = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Check for start of a play:
        # A play always starts with - name: at the very root level (indentation 0)
        if stripped.startswith("- name:") and indent == 0:
            if current_play:
                if current_task:
                    current_tasks.append(current_task)
                current_play["tasks"] = current_tasks
                plays.append(current_play)
            name_val = stripped.split("- name:", 1)[1].strip().strip("\"'\r")
            current_play = {"name": name_val, "hosts": False, "become": False, "become_user": None}
            current_tasks = []
            in_tasks = False
            current_task = None
            continue

        # Check play properties
        if current_play and not in_tasks:
            if stripped.startswith("hosts:"):
                current_play["hosts"] = True
            elif stripped.startswith("become:"):
                val = stripped.split(":", 1)[1].strip()
                current_play["become"] = val in ["yes", "true", "True"]
            elif stripped.startswith("become_user:"):
                val = stripped.split(":", 1)[1].strip().strip("\"'\r")
                current_play["become_user"] = val
            elif stripped.startswith("tasks:"):
                in_tasks = True
                continue

        # Process tasks
        if in_tasks:
            # A task in our clean playbook documentation must always start with - name:
            if stripped.startswith("- name:"):
                if current_task:
                    current_tasks.append(current_task)
                name_val = stripped.split("name:", 1)[1].strip().strip("\"'\r")
                current_task = {"name": name_val, "module": None, "line_no": line}
                continue

            if current_task:
                # Inside a task block: check if key is a module name
                # It must be at the task level (e.g. indented by 6 spaces)
                match = re.match(r"^([a-zA-Z0-9_\.\-]+)\s*:\s*.*$", stripped)
                if match:
                    key = match.group(1)
                    # Ignore task-level parameters and parameters of modules
                    if key not in ["state", "loop", "register", "become", "become_user", "when", "environment", "notify", "creates", "cmd", "owner", "group", "mode", "src", "dest", "path", "regexp", "line", "name", "update_cache", "upgrade", "autoremove", "policy", "rule", "from_ip", "port", "proto"]:
                        if current_task["module"] is None:
                            current_task["module"] = key

    if current_task:
        current_tasks.append(current_task)
    if current_play:
        current_play["tasks"] = current_tasks
        plays.append(current_play)

    return plays

def test_ansible_playbooks_syntax_and_standards():
    """
    Scans the repository for Markdown files and ensures that all embedded Ansible playbooks
    strictly conform to documentation and security standards.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    playbook_count = 0

    for root, _, files in os.walk(workspace_root):
        # Skip hidden directories except .agents
        if any(part.startswith('.') and part != '.agents' for part in root.split(os.sep)):
            continue

        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                playbooks = extract_ansible_playbooks_from_md(filepath)
                if not playbooks:
                    continue

                playbook_count += len(playbooks)
                for playbook in playbooks:
                    plays = parse_yaml_tasks(playbook)

                    # Assert that the parsed blocks indeed have at least one play defined
                    assert len(plays) > 0, f"Malformed Ansible playbook found in {filepath}"

                    for play in plays:
                        # 1. Standard: Every play must have a 'hosts' specifier
                        assert play['hosts'] is True, f"Playbook in {filepath} is missing 'hosts:' configuration"

                        # 2. Standard: Every single task in our Ansible playbooks must have a 'name'
                        for task in play['tasks']:
                            assert task['name'] != '', f"Ansible task missing mandatory 'name:' attribute in {filepath}: {task['line_no']}"

def test_onprem_ansible_fqcn_and_privilege_separation():
    """
    Validates the specific production Ansible configuration for on-premises operations:
    1. Tests that docs/onprem/ansible-orchestration.md contains a playbook.
    2. Verifies strict FQCN (Fully Qualified Collection Names) compliance for all tasks.
    3. Verifies Symmetric Privilege Separation modeling (Play 1: rootful, Play 2: rootless 'songket' user).
    """
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/onprem/ansible-orchestration.md'))
    assert os.path.exists(filepath), "onprem/ansible-orchestration.md does not exist"

    playbooks = extract_ansible_playbooks_from_md(filepath)
    assert len(playbooks) > 0, "No playbooks found in docs/onprem/ansible-orchestration.md"

    plays = parse_yaml_tasks(playbooks[0])

    # Verify Symmetric Privilege Separation
    # There should be exactly two plays modeling the separation pipeline
    assert len(plays) == 2, "The onprem-orchestration playbook must model exactly 2 plays for Symmetric Privilege Separation"

    # Play 1: Rootful Host Hardening
    play1 = plays[0]
    assert play1['become'] is True, "Phase 1 of Symmetric Privilege Separation must run with elevated privileges (become: yes)"
    assert play1['become_user'] is None, "Phase 1 must run as administrative root (become_user must be absent)"

    # Play 2: Rootless Deployment
    play2 = plays[1]
    assert play2['become'] is True, "Phase 2 of Symmetric Privilege Separation must use become: yes to run as user"
    assert play2['become_user'] == 'songket', "Phase 2 must drop privileges to unprivileged user 'songket' (become_user: songket)"

    # Verify FQCN Naming Standards (modules must start with collection namespaces like 'ansible.builtin.' or 'ansible.posix.')
    for play in plays:
        for task in play['tasks']:
            module = task['module']
            if module:
                assert module.startswith('ansible.builtin.') or module.startswith('ansible.posix.'), \
                    f"FQCN Violation: Module '{module}' in task '{task['name']}' must use its Fully Qualified Collection Name (e.g. ansible.builtin.{module})"
