---
layout: "default"
okf_version: "0.1"
type: "Explanation"
title: "The Diátaxis Framework in Our Project Documentation"
timestamp: 2026-08-05T22:04:00Z
topics: ["aws", "cloud", "architecture", "diataxis", "documentation", "explanation"]
---
# The Diátaxis Framework in Our Project Documentation

To deliver an exceptional, production-ready documentation experience, this project structures all of its engineering resources, operations manuals, and scripting details using the **Diátaxis Framework**.

Diátaxis is a systematic, user-centric, and task-oriented approach to software documentation. It resolves the common pitfall where technical documentation becomes a chaotic dump of unorganized information. Instead, Diátaxis organizes documentation into **four distinct quadrants**, each serving a unique user need and cognitive phase.

---

## The Four Quadrants of Diátaxis

Our documentation system is strictly partitioned into the following four domains:

```
                  TEMPORAL / EXPERIENCE
                    ▲
                    │
       TUTORIALS    │    HOW-TO GUIDES
       (Learning)   │    (Problem-solving)
                    │
 PRACTICAL ─────────┼───────── THEORETICAL
                    │
       REFERENCE    │    EXPLANATION
       (Information)│    (Understanding)
                    │
                    ▼
                  SPATIAL / KNOWLEDGE
```

### 1. Tutorials (Learning-Oriented)
* **Purpose:** Introduce absolute beginners to a topic or tool by taking them by the hand through guided, step-by-step exercises.
* **Focus:** Learning through active execution. Focuses on safe, basic environments without overwhelming detail.
* **Our Implementation:** [Tutorials Quickstart](../tutorials/quickstart.html) guides developers through initial setup and basic execution of Python formatting and curation tools.

### 2. How-To Guides (Problem-Oriented)
* **Purpose:** Practical, recipe-like guides that help intermediate and advanced operators solve specific, real-world problems.
* **Focus:** Goal-oriented execution. Assumes basic familiarity with the codebase and tools.
* **Our Implementation:** Our How-To guides demonstrate targeted workflows, such as:
  - [How-To: Standardising Metadata](../how-to/manage-metadata.html)
  - [How-To: Compiling LLM-Friendly Curation Formats](../how-to/generate-llms-xml.md)

### 3. Technical Reference (Information-Oriented)
* **Purpose:** Dry, objective, and highly-structured technical descriptions, API specifications, flags, inputs, outputs, and variables.
* **Focus:** Unbiased information. Operators use Reference material when they know what they want to achieve but need to verify exact signatures or configurations.
* **Our Implementation:** Complete specs for tools and scripts:
  - [Reference: prepare_docs.py Metadata Formatter](../reference/prepare_docs.html)
  - [Reference: parse_llms.py Compiler](../reference/parse_llms.html)
  - [Reference: Deployment, Teardown, and PDF Scripts](../reference/bash_scripts.html)

### 4. Explanations (Understanding-Oriented)
* **Purpose:** Discussions, conceptual context, architecture designs, and historical context explaining the "why" behind the code.
* **Focus:** Comprehension and deep understanding. Translates code decisions into human architecture.
* **Our Implementation:** Includes deep architecture diagrams, explanations of automation tools, and the very file you are reading now!

---

## Why Diátaxis Matters for Developers and AI Agents

Documentation is increasingly consumed by both human developers and **AI Agents / LLMs** (e.g. Google Jules, Google Antigravity, and search engines). Structuring the docs under Diátaxis offers massive benefits for both:

1. **Cognitive Isolation for Humans:** Developers can instantly find the exact document that matches their task phase without having to read unrelated architectural discussions or dry API specs.
2. **Context Efficiency for AI Agents:** By isolating Reference specs from Explanations and How-To Guides, AI agents can read a single reference sheet or how-to recipe, drastically reducing context window size, token costs, and processing latency.
3. **Structured Sitemaps:** It aligns naturally with sitemaps (`sitemap.xml`) and curated LLM entry points (`llms.txt`), directing search crawlers and AI bots to clean, logical hierarchies.
