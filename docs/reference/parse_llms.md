---
layout: "default"
okf_version: "0.1"
type: "Reference"
title: "Technical Reference: parse_llms.py Compiler"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "python", "reference"]
---
# Technical Reference: parse_llms.py Compiler

This reference document details the command-line interface parameters, Python API signatures, and data contracts for the `parse_llms.py` compiler script.

---

## Programmatic Interface (Python API)

The module is stored at `scripts/parse_llms.py`. It is a standalone utility designed for deep compilation of llms.txt standard files.

### Functions

#### `parse_llms_file(text)`
Parses the raw structured `llms.txt` Markdown string.
* **Parameters:** `text` (*str*): Raw text content.
* **Returns:** (*dict*): A structured dictionary mapping with the following format:
  ```json
  {
    "title": "Project Title",
    "summary": "Blockquote summary text",
    "info": "Additional paragraph description",
    "sections": {
      "Section Name": [
        {"title": "Doc Name", "url": "relative/path.md", "desc": "description text"}
      ]
    }
  }
  ```

#### `get_doc_content(filepath)`
Reads local Markdown files, stripping any Jekyll YAML front matter block to ensure clean plain-text.
* **Parameters:** `filepath` (*str*): The relative path of the file to fetch.
* **Returns:** (*str*): Stripped text contents.

#### `escape_xml(val)`
Converts characters (`<`, `>`, `&`, `"`, `'`) in a string to safe XML entities.
* **Parameters:** `val` (*str*): Raw input string.
* **Returns:** (*str*): XML-escaped output.

#### `create_ctx(text, optional=False)`
Generates highly-structured XML content suitable for direct AI model ingestion.
* **Parameters:**
  - `text` (*str*): Raw content of `llms.txt`.
  - `optional` (*bool*): Whether to compile items in sections labeled "Optional".
* **Returns:** (*str*): Valid, structured XML document string.

#### `create_llms_full(text)`
Aggregates and formats all referenced documents into a single flat Markdown document.
* **Parameters:** `text` (*str*): Raw contents of `llms.txt`.
* **Returns:** (*str*): Merged Markdown document string.

---

## CLI Specifications

The script is invoked from the command line using standard argument parsing flags.

### Usage
```bash
python scripts/parse_llms.py [options]
```

### Argument Flags

| Flag | Long Option | Default | Description |
|---|---|---|---|
| `-i` | `--input` | `llms.txt` | Path to the source `llms.txt` file |
| `-o` | `--xml-output` | `llms.xml` | Destination file for compiled XML context |
| `-f` | `--full-output` | `llms-full.txt` | Destination file for merged full Markdown |
| | `--optional` | `False` | Force compilation of optional sections |

---

## Dependencies
* **Runtime:** Python >= 3.8
* **Requirements:** Standard library only (`os`, `re`, `html`, `argparse`).
