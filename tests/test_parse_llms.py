import sys
import os

# Ensure scripts directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import parse_llms

def test_parse_llms_file():
    """Tests parsing an llms.txt format into structured dictionaries."""
    sample_text = """# Test Title
> A summary of the test file.

Some extra descriptive info.

## Docs
- [Surreal](https://host/README.md): Tiny jQuery alternative with Locality of Behavior
- [FastHTML](https://host/quickstart.html.md)

## Optional
- [Extra](https://host/extra.md): Extra optional doc
"""
    parsed = parse_llms.parse_llms_file(sample_text)

    assert parsed["title"] == "Test Title"
    assert parsed["summary"] == "A summary of the test file."
    assert parsed["info"] == "Some extra descriptive info."
    assert "Docs" in parsed["sections"]
    assert "Optional" in parsed["sections"]

    docs_links = parsed["sections"]["Docs"]
    assert len(docs_links) == 2
    assert docs_links[0]["title"] == "Surreal"
    assert docs_links[0]["url"] == "https://host/README.md"
    assert docs_links[0]["desc"] == "Tiny jQuery alternative with Locality of Behavior"

    assert docs_links[1]["title"] == "FastHTML"
    assert docs_links[1]["url"] == "https://host/quickstart.html.md"
    assert docs_links[1]["desc"] == ""

def test_escape_xml():
    """Tests escaping XML characters like <, >, &, ", '."""
    assert parse_llms.escape_xml("hello <world>") == "hello &lt;world&gt;"
    assert parse_llms.escape_xml("Tom & Jerry") == "Tom &amp; Jerry"
    assert parse_llms.escape_xml('quote " test') == "quote &quot; test"
    assert parse_llms.escape_xml(None) == ""

def test_get_doc_content(tmp_path):
    """Tests retrieving file content and stripping Jekyll front matter blocks."""
    # Create a mock markdown file with front matter
    mock_file = tmp_path / "test.md"
    mock_file.write_text("""---
layout: default
okf_version: "0.1"
---
# Main Content
This is the test content.""")

    content = parse_llms.get_doc_content(str(mock_file))
    assert content == "# Main Content\nThis is the test content."

    # Create mock file without front matter
    mock_file_no_fm = tmp_path / "test_no_fm.md"
    mock_file_no_fm.write_text("Hello world")
    content_no_fm = parse_llms.get_doc_content(str(mock_file_no_fm))
    assert content_no_fm == "Hello world"

def test_create_ctx():
    """Tests generating a structured XML context file from llms.txt content."""
    sample_text = """# Test Title
> A summary of the test file.

Some extra descriptive info.

## Docs
- [Surreal](README.md): Tiny jQuery alternative
"""
    # Create mock file for README.md
    with open("README.md", "r", encoding="utf-8") as f:
        original_content = f.read()

    xml_output = parse_llms.create_ctx(sample_text)
    assert "<project>" in xml_output
    assert "<title>Test Title</title>" in xml_output
    assert "<summary>A summary of the test file.</summary>" in xml_output
    assert "<section name=\"Docs\">" in xml_output
    assert "<doc title=\"Surreal\" url=\"README.md\" desc=\"Tiny jQuery alternative\">" in xml_output

def test_create_llms_full():
    """Tests generating a consolidated plain text manual from parsed links."""
    sample_text = """# Test Title
> A summary of the test file.

Some extra descriptive info.

## Docs
- [Surreal](README.md): Tiny jQuery alternative
"""
    full_output = parse_llms.create_llms_full(sample_text)
    assert "# Test Title - Full Documentation" in full_output
    assert "A summary of the test file." in full_output
    assert "Some extra descriptive info." in full_output
    assert "## Docs" in full_output
    assert "### Surreal (README.md)" in full_output
    assert "*Tiny jQuery alternative*" in full_output
