---
layout: "default"
okf_version: "0.1"
type: "How-To Guide"
title: "How-To Guide: Standardising Markdown Front Matter Metadata"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "python", "metadata"]
---
# How-To Guide: Standardising Markdown Front Matter Metadata

This practical, problem-oriented guide shows you how to enforce and standardise metadata front matter across all project Markdown files using the `prepare_docs.py` utility.

---

## Task: Rectify Missing or Non-Compliant Headers

When writing new documentation files under `docs/` or `.agents/`, you might forget to include the mandatory Open Knowledge Format (OKF) metadata keys or omit double quotes on string values with special characters. Follow these steps to resolve this.

### Step 1: Create or Move Your Document
Save your newly drafted Markdown file anywhere in the repository. E.g., `docs/engineering/new_guide.md`.

### Step 2: Dry Run or Execute Formatting
Execute the formatter tool from the repository root:
```bash
python scripts/prepare_docs.py
```

The script will:
1. Scan all project folders recursively (ignoring standard hidden directories).
2. Validate that each `.md` file starts with `---` on line 1, column 1.
3. Automatically inject missing core keys with sensible defaults:
   - `layout`: `"default"`
   - `okf_version`: `"0.1"`
   - `type`: Guided by directory structure (e.g., `"Guide"`, `"Module Documentation"`)
   - `title`: Extracted from the first heading (`#`) or base name.
   - `timestamp`: Matched to the file's last modified time.
   - `topics`: Scanned from content-level keywords.

### Step 3: Verify standard compliance
Inspect the formatted file:
```bash
head -n 12 docs/engineering/new_guide.md
```

Ensure all string parameters with special characters are wrapped in double quotes:
```yaml
---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "A Specialized Technical Guide: Ingress Routing"
timestamp: "2026-08-05T22:04:00Z"
topics: ["aws", "cloud", "routing"]
---
```

---

## Customizing Metadata Rules

If you wish to modify the default topics assigned to files, edit the `process_markdown_file` function inside `scripts/prepare_docs.py`:

```python
# To add a custom keyword trigger, modify the keywords list:
keywords = ["vpc", "alb", "asg", "rds", "my-custom-keyword"]
```

Save and run `python scripts/prepare_docs.py` to propagate changes across your workspace.
