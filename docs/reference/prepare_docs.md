---
layout: "default"
okf_version: "0.1"
type: "Reference"
title: "Technical Reference: prepare_docs.py Metadata Formatter"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "python", "reference"]
---
# Technical Reference: prepare_docs.py Metadata Formatter

This reference document provides technical specifications, parameters, dependencies, and execution schemas for the `prepare_docs.py` document preparation script.

---

## Programmatic Interface (Python API)

The module is structured as a standalone, zero-dependency Python utility located in `scripts/prepare_docs.py`.

### Functions

#### `unescape_string(val)`
Strips outer quotes and resolves escaped backslashes or quotes.
* **Parameters:** `val` (*str*): Raw string value extracted from YAML.
* **Returns:** (*str*): Unescaped, cleaned string.

#### `parse_yaml(front_matter_str)`
Parses raw YAML front matter block into a flat key-value dictionary. Supports inline arrays `[a, b, c]`, dictionaries, and block bullet points.
* **Parameters:** `front_matter_str` (*str*): The raw string contents of the front matter block.
* **Returns:** (*dict*): Dictionary of parsed metadata.

#### `serialize_yaml(data)`
Serializes metadata properties back into a compliant OKF v0.1/v0.2 formatted YAML block. Core keys are output in fixed order: `layout`, `okf_version`, `type`, `title`, `timestamp`, `topics`. Remaining keys are serialized in alphabetical order.
* **Parameters:** `data` (*dict*): Dictionary of properties.
* **Returns:** (*str*): Formatted YAML block.

#### `process_markdown_file(filepath, workspace_root)`
Examines an individual `.md` file, extracts front matter, verifies/auto-injects required keys, and saves changes.
* **Parameters:**
  - `filepath` (*str*): Absolute file path.
  - `workspace_root` (*str*): Root directory of the repository workspace.

---

## CLI Specifications

The script can be executed as a global system utility.

### Entry Point
```bash
python scripts/prepare_docs.py
```

### Parameters & Arguments
* The tool accepts **no command line arguments**. It automatically resolves workspace roots based on its directory context (`../` relative to the script's physical path).

### Environment & Dependencies
* **Required Runtime:** Python >= 3.8
* **Dependencies:** None. Employs only standard libraries: `os`, `re`, `datetime`.
* **Bytecode Exclusions:** Configured to exclude standard cache paths (`__pycache__/`, `*.pyc`).

---

## Exit Codes
* `0`: Successfully completed scanning and formatting all Markdown documents.
* `1` or non-zero: An unhandled exception occurred during execution.
