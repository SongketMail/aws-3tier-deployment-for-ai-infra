import sys
import os

# Ensure scripts directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import prepare_docs

def test_unescape_string():
    """Tests the unescape_string function for double, single, and no quotes."""
    assert prepare_docs.unescape_string('"test"') == "test"
    assert prepare_docs.unescape_string("'test'") == "test"
    assert prepare_docs.unescape_string('"escaped \\" quote"') == 'escaped " quote'
    assert prepare_docs.unescape_string('no_quotes') == "no_quotes"

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
    assert prepare_docs.format_yaml_value("timestamp", "2026-08-09T15:00:00Z") == "2026-08-09T15:00:00Z"
    assert prepare_docs.format_yaml_value("topics", ["aws", "valkey"]) == '["aws", "valkey"]'
    assert prepare_docs.format_yaml_value("map", "{a: 1}") == "{a: 1}"

def test_serialize_yaml():
    """Tests metadata serialization, ensuring ordered core OKF keys and alphabetical sorting of others."""
    data = {
        "okf_version": "0.1",
        "layout": "default",
        "custom_key": "custom_value",
        "title": "A Great Page",
        "timestamp": "2026-08-09T15:00:00Z",
        "topics": ["cloud", "onprem"]
    }
    serialized = prepare_docs.serialize_yaml(data)
    lines = serialized.split("\n")
    # Assert core order: layout, okf_version, type (absent), title, timestamp, topics
    assert lines[0] == 'layout: "default"'
    assert lines[1] == 'okf_version: "0.1"'
    assert lines[2] == 'title: "A Great Page"'
    assert lines[3] == 'timestamp: 2026-08-09T15:00:00Z'
    assert lines[4] == 'topics: ["cloud", "onprem"]'
    assert lines[5] == 'custom_key: "custom_value"'

def test_should_process_dir():
    """Tests directories filtering, ensuring only relevant folders are scanned."""
    assert prepare_docs.should_process_dir("docs") is True
    assert prepare_docs.should_process_dir(".agents") is True
    assert prepare_docs.should_process_dir(".git") is False
    assert prepare_docs.should_process_dir("src/.hidden") is False
