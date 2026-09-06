import os
import sys

import pytest

# Ensure scripts directory is in sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)

import prepare_docs


def _read_processed_metadata(path):
    """Parse metadata written by ``process_markdown_file``."""
    content = path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    _, front_matter, body = content.split("---", 2)
    return prepare_docs.parse_yaml(front_matter), body.lstrip("\n")


def test_unescape_string():
    """Tests the unescape_string function for double, single, and no quotes."""
    assert prepare_docs.unescape_string('"test"') == "test"
    assert prepare_docs.unescape_string("'test'") == "test"
    assert prepare_docs.unescape_string('"escaped \\" quote"') == 'escaped " quote'
    assert prepare_docs.unescape_string("no_quotes") == "no_quotes"


def test_parse_yaml():
    """Tests parsing YAML front matter, including key-values, lists, inline arrays, and maps."""
    # Write the YAML block with line-start alignment to support re.match correctly
    yaml_str = """layout: default
okf_version: "0.1"
type: "Guide"
title: "Awesome Page"
timestamp: 2026-08-09T15:00:00Z
topics: ["aws", "cloud", "architecture"]
tags:
  - tag1
  - tag2
inline_map: {a: 1, b: 2}"""
    data = prepare_docs.parse_yaml(yaml_str)
    assert data["layout"] == "default"
    assert data["okf_version"] == "0.1"
    assert data["type"] == "Guide"
    assert data["title"] == "Awesome Page"
    assert data["timestamp"] == "2026-08-09T15:00:00Z"
    assert data["topics"] == ["aws", "cloud", "architecture"]
    assert data["tags"] == ["tag1", "tag2"]
    assert data["inline_map"] == "{a: 1, b: 2}"


def test_format_yaml_value():
    """Tests standardizing YAML output values for strings, arrays, timestamps, and inline dicts."""
    assert prepare_docs.format_yaml_value("layout", "default") == '"default"'
    assert (
        prepare_docs.format_yaml_value("timestamp", "2026-08-09T15:00:00Z")
        == "2026-08-09T15:00:00Z"
    )
    assert (
        prepare_docs.format_yaml_value("topics", ["aws", "valkey"])
        == '["aws", "valkey"]'
    )
    assert prepare_docs.format_yaml_value("map", "{a: 1}") == "{a: 1}"


def test_serialize_yaml():
    """Tests metadata serialization, ensuring ordered core OKF keys and alphabetical sorting of others."""
    data = {
        "okf_version": "0.1",
        "layout": "default",
        "custom_key": "custom_value",
        "title": "A Great Page",
        "timestamp": "2026-08-09T15:00:00Z",
        "topics": ["cloud", "onprem"],
    }
    serialized = prepare_docs.serialize_yaml(data)
    lines = serialized.split("\n")
    # Assert core order: layout, okf_version, type (absent), title, timestamp, topics
    assert lines[0] == 'layout: "default"'
    assert lines[1] == 'okf_version: "0.1"'
    assert lines[2] == 'title: "A Great Page"'
    assert lines[3] == "timestamp: 2026-08-09T15:00:00Z"
    assert lines[4] == 'topics: ["cloud", "onprem"]'
    assert lines[5] == 'custom_key: "custom_value"'


def test_should_process_dir():
    """Tests directories filtering, ensuring only relevant folders are scanned."""
    assert prepare_docs.should_process_dir("docs") is True
    assert prepare_docs.should_process_dir(".agents") is True
    assert prepare_docs.should_process_dir(".git") is False
    assert prepare_docs.should_process_dir("src/.hidden") is False


@pytest.mark.parametrize("existing_version", ["0.1", "0.2"])
def test_process_markdown_file_preserves_existing_okf_version(
    tmp_path, existing_version
):
    """Existing legacy and current OKF versions must survive preparation."""
    markdown = tmp_path / "existing-version.md"
    markdown.write_text(
        "---\n"
        'layout: "default"\n'
        f'okf_version: "{existing_version}"\n'
        'type: "Guide"\n'
        'title: "Existing Version"\n'
        "timestamp: 2026-08-20T00:00:00Z\n"
        'topics: ["testing"]\n'
        "---\n"
        "# Existing Version\n\n"
        "Body content remains intact.\n",
        encoding="utf-8",
    )

    prepare_docs.process_markdown_file(str(markdown), str(tmp_path))

    metadata, body = _read_processed_metadata(markdown)
    assert metadata["okf_version"] == existing_version
    assert body == "# Existing Version\n\nBody content remains intact.\n"


@pytest.mark.parametrize(
    ("initial_content", "expected_title", "expected_body"),
    [
        (
            (
                "---\n"
                'layout: "default"\n'
                'type: "Guide"\n'
                'title: "Versionless Guide"\n'
                "timestamp: 2026-08-20T00:00:00Z\n"
                'topics: ["testing"]\n'
                "---\n"
                "# Versionless Guide\n"
            ),
            "Versionless Guide",
            "# Versionless Guide\n",
        ),
        (
            "# Guide Without Front Matter\n",
            "Guide Without Front Matter",
            "# Guide Without Front Matter\n",
        ),
    ],
)
def test_process_markdown_file_defaults_missing_okf_version_to_v02(
    tmp_path, initial_content, expected_title, expected_body
):
    """Versionless front matter and new documents must both adopt OKF v0.2."""
    markdown = tmp_path / "versionless-guide.md"
    markdown.write_text(initial_content, encoding="utf-8")

    prepare_docs.process_markdown_file(str(markdown), str(tmp_path))

    metadata, body = _read_processed_metadata(markdown)
    assert metadata["okf_version"] == "0.2"
    assert metadata["title"] == expected_title
    assert body == expected_body


def test_process_markdown_file_is_idempotent_for_okf_v02(tmp_path):
    """A second preparation pass must not downgrade or duplicate front matter."""
    markdown = tmp_path / "idempotent.md"
    markdown.write_text(
        "---\n"
        'layout: "default"\n'
        'okf_version: "0.2"\n'
        'type: "Guide"\n'
        'title: "Idempotent"\n'
        "timestamp: 2026-08-20T00:00:00Z\n"
        'topics: ["testing"]\n'
        "---\n"
        "# Idempotent\n",
        encoding="utf-8",
    )

    prepare_docs.process_markdown_file(str(markdown), str(tmp_path))
    first_pass = markdown.read_text(encoding="utf-8")
    prepare_docs.process_markdown_file(str(markdown), str(tmp_path))

    assert markdown.read_text(encoding="utf-8") == first_pass
    assert first_pass.count('okf_version: "0.2"') == 1
