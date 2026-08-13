---
layout: "default"
okf_version: "0.1"
type: "How-To Guide"
title: "How-To Guide: Compiling LLM-Friendly Curation Formats"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "python", "llm"]
---
# How-To Guide: Compiling LLM-Friendly Curation Formats

This guide provides practical instructions on how to use `parse_llms.py` to compile our curated sitemap (`llms.txt`) into high-performance, LLM-digestible formats: structured XML (`llms.xml`) and flat consolidated Markdown text (`llms-full.txt`).

---

## Task 1: Generate Standard XML and Full Documentation

To output the default set of XML and full text documentation, execute the parser with no arguments:

```bash
python scripts/parse_llms.py
```

This reads the default `llms.txt` file and outputs:
- `llms.xml`
- `llms-full.txt`

---

## Task 2: Customize Input and Output Paths

If you are maintaining custom sub-sitemaps (for example, a dedicated developer sitemap or an executive sitemap), you can redirect inputs and outputs using the command-line flags:

```bash
python scripts/parse_llms.py \
  --input docs/custom_llms.txt \
  --xml-output docs/custom_context.xml \
  --full-output docs/custom_full.txt
```

---

## Task 3: Include Optional/Hidden Sections

By default, optional resource blocks in `llms.txt` are omitted from the main XML context document to keep context lengths small.

To override this setting and force the compilation of optional directories, use the `--optional` flag:

```bash
python scripts/parse_llms.py --optional
```

---

## Task 4: Integrate Curation into a Git Hook or CI/CD Pipeline

To ensure that `llms.xml` and `llms-full.txt` always remain synchronised with your documentation updates, configure a pre-commit step or add this command to your deployment workflow:

```bash
# Example pre-commit check script segment
echo "Compiling LLM sitemaps..."
python scripts/parse_llms.py

# Enforce check
git add llms.xml llms-full.txt
```
This guarantees that any changes to individual guide files are immediately compiled into the single manual or indexing files.
