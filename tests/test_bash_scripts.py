"""
Unit tests to validate the health, syntax, and standards of Bash scripts in the repository.

This test module ensures that all shell scripts under the `scripts/` directory
possess correct syntax, follow security best practices (e.g., using set -e),
and contain standard metadata and header documentation.
"""

import os
import subprocess

def get_bash_scripts():
    """
    Retrieves a list of paths to all Bash (.sh) script files in the repository.

    Returns:
        list: A list of absolute paths to Bash scripts.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    scripts_dir = os.path.join(workspace_root, 'scripts')
    bash_scripts = []
    if os.path.exists(scripts_dir):
        for root, _, files in os.walk(scripts_dir):
            for file in files:
                if file.endswith('.sh'):
                    bash_scripts.append(os.path.join(root, file))
    return bash_scripts

def test_bash_script_syntax():
    """
    Runs `bash -n` against every Bash script to verify syntax correctness.

    This ensures that syntax errors are caught before runtime.
    """
    scripts = get_bash_scripts()
    assert len(scripts) > 0, "No Bash scripts found to validate."

    for script_path in scripts:
        rel_path = os.path.basename(script_path)
        # Execute bash -n which checks the syntax without executing the script
        result = subprocess.run(['bash', '-n', script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Syntax error in {rel_path}: {result.stderr}"

def test_bash_script_hardening_and_headers():
    """
    Verifies that all interactive Bash scripts contain proper hardening rules and standard headers.

    Checks:
    1. Standard exit on error flag 'set -e' for executable/deployment scripts.
    2. Proper file headers identifying script name, purpose, and author.
    """
    scripts = get_bash_scripts()
    for script_path in scripts:
        rel_path = os.path.basename(script_path)
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for standard shebang
        assert content.startswith('#!'), f"{rel_path} is missing a shebang line."

        # Check for headers/docstrings in scripts
        assert "Description:" in content, f"{rel_path} is missing standard header 'Description:' metadata."
        assert "Author:" in content, f"{rel_path} is missing standard header 'Author:' metadata."

        # Hardening check: deploy.sh, destroy.sh, and simulate.sh must use exit-on-error (set -e)
        if rel_path in ['deploy.sh', 'destroy.sh', 'simulate.sh']:
            assert "set -e" in content, f"{rel_path} must have 'set -e' configured for safety."
