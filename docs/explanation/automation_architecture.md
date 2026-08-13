---
layout: "default"
okf_version: "0.1"
type: "Explanation"
title: "Project Automation: Metadata and LLM Curation Architecture"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "automation", "python", "explanation"]
---
# Project Automation: Metadata and LLM Curation Architecture

This explanation guide explores the underlying architecture, data flows, parsing mechanisms, and system design of our project's core automation utilities: `prepare_docs.py` and `parse_llms.py`.

---

## 1. Document Metadata Standardisation (`prepare_docs.py`)

The `prepare_docs.py` tool is designed with a strict, local-first parser pattern to guarantee formatting uniformity and prevent malformed Jekyll headers.

```
       [ Local Workspace ]
                │
         (Recursive Scan)
                │
                ▼
       [ Markdown File (.md) ]
                │
          (Parse YAML) ◄────── (Unescape & Clean)
                │
         (Analyze Content) ─── (Keyword Match to Topics)
                │
        (Inject Missing) ──── (Type, Title, Default Layout)
                │
        (Serialize Block) ─── (OKF v0.1 Key Order standard)
                │
                ▼
         [ Updated .md ]
```

### Parsing Logic
1. **Extraction:** Looks for front matter delimiters (`---`) exactly starting at line 1, column 1.
2. **String Cleaning:** Standardises values by unescaping internal quotes and removing trailing whitespace.
3. **Keyword-Based Topic Synthesis:** Scans the Markdown body content for standard cloud engineering keywords (such as `vpc`, `alb`, `asg`, `rds`, `valkey`, `dr`, `compliance`) to automatically generate contextual tags under the `topics` array.
4. **Serialization Order:** Re-serializes the keys into a fixed standard order to guarantee uniform representation across the entire repository.

---

## 2. LLM-Friendly Curation Pipeline (`parse_llms.py`)

The `parse_llms.py` compiler bridges our curated sitemap (`llms.txt`) with modern AI tools by outputting highly-digestible context documents.

```
                  [ llms.txt ]
                       │
                 (Regex Parser)
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
  (Create XML Context)     (Compile Full Manual)
         │                           │
  (Read Local Files)       (Read Local Files)
         │                           │
  (Strip Front Matter)     (Strip Front Matter)
         │                           │
  (XML Escape Content)     (Merge Markdown Blocks)
         │                           │
         ▼                           ▼
     [ llms.xml ]            [ llms-full.txt ]
```

### Data Flow & Transformations
1. **Parsing:** Parses `llms.txt` using a regex engine to isolate the title, summary, introductory remarks, and sections.
2. **Local Curation Resolving:** Rather than fetching remote links over the network, the compiler matches URLs to relative repository paths (such as `README.md` or `docs/costing.md`) to read them locally.
3. **Stripping Jekyll Metadata:** The compiler extracts the Markdown body and strips Jekyll-specific front matter blocks to ensure that AI models ingest clean, pure Markdown code snippets without configuration noise.
4. **Dual Output Generation:**
   - **XML Context (`llms.xml`):** Compiles sections into separate XML tag structures (`<project>`, `<section>`, `<doc>`), which allows AI systems to perform highly precise system prompts and targeted context retrieval.
   - **Flat Document Manual (`llms-full.txt`):** Consolidates all curated docs into a single plain-text file, which serves as a ready-to-use reference handbook.
