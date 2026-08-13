---
layout: "default"
okf_version: "0.1"
type: "Tutorial"
title: "Quickstart Tutorial: Operating Project Automation Utilities"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "python", "tutorial"]
---
# Quickstart Tutorial: Operating Project Automation Utilities

Welcome! This guided, step-by-step tutorial takes you by the hand to help you learn how to run and operate our core project automation utilities: `prepare_docs.py` and `parse_llms.py`.

By the end of this lesson, you will know how to standardise Markdown front matter and compile curated sitemaps into LLM-friendly formats.

---

## Prerequisites

Before we begin, ensure you have the following installed on your machine:
* **Python 3.10** or higher
* Standard shell environment (Bash/Zsh on Linux or macOS)

Verify your Python installation by running:
```bash
python3 --version
```

---

## Step 1: Clone and Set Up your Workspace

Navigate to your workspace directory and verify the project structure:
```bash
# Verify you are in the root directory
ls -F
```
Ensure you see the `scripts/` directory containing our core Python scripts.

---

## Step 2: Standardise Markdown Metadata

We use the Open Knowledge Format (OKF) v0.1 to manage Jekyll-compatible metadata. The `prepare_docs.py` tool automates scanning and standardising this metadata.

To standardise your repository's documentation headers, execute the following command:
```bash
python scripts/prepare_docs.py
```

### Expected Output:
```text
Scanning markdown files under workspace: /app
Processing: README.md
  -> Successfully updated with OKF v0.1 metadata
Processing: docs/architecture.md
  -> Successfully updated with OKF v0.1 metadata
```

This ensures all Markdown files start with compliant front matter at line 1, column 1.

---

## Step 3: Generate LLM-Friendly Index Formats

We curate `llms.txt` to guide AI tools and LLMs to our most critical pages. The `parse_llms.py` script converts this text-based roadmap into an XML context document and a single consolidated full text file.

Run the parser with default parameters to compile both documents:
```bash
python scripts/parse_llms.py
```

### Expected Output:
```text
Generating XML context file at: llms.xml
Generating full consolidated documentation file at: llms-full.txt
Success: Curation files successfully generated.
```

---

## Step 4: Verify the Compiled Output

Let's verify that your generated context documents have the correct structure:

1. Check the first 10 lines of the generated XML context file:
   ```bash
   head -n 10 llms.xml
   ```

2. Confirm the file starts with the `<project>` root element and contains correct `<title>` tags:
   ```xml
   <project>
     <title>AWS 3-Tier Deployment for AI &amp; Web Infra (with OpenTofu)</title>
     <summary>A complete, production-ready infrastructure project and documentation repository...</summary>
   ```

---

## Conclusion & Next Steps

Congratulations! You have completed the automation quickstart tutorial. You have successfully:
1. Checked your Python workspace configuration.
2. Formatted Markdown documentation files recursively to meet OKF standards.
3. Compiled a structured XML context file (`llms.xml`) and consolidated plain text manual (`llms-full.txt`) using the `parse_llms.py` CLI.

For task-specific recipes or in-depth technical references, consult our:
* [How-To: Standardising Metadata](../how-to/manage-metadata.html)
* [Reference: parse_llms.py CLI Specs](../reference/parse_llms.html)
