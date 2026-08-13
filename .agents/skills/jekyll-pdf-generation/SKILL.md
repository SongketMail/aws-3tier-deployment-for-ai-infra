---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "Jekyll Layout & PDF Generation Skill"
timestamp: 2026-08-05T22:03:00Z
topics: ["aws", "cloud", "architecture", "skill", "jekyll", "pdf", "css", "html", "print", "badges", "seo"]
description: "Guidelines for configuring custom responsive Jekyll layouts, box-drawing character scanners, CSS print overrides, and high-fidelity PDF workflows."
name: "jekyll-pdf-generation"
---
# Jekyll Layout & PDF Generation Skill

This skill governs the standards for managing the project's Jekyll documentation layout, maintaining responsive design, safeguarding tables/diagrams from text wrapping, enabling site-wide widgets, and automating high-fidelity PDF generation.

---

## 1. Custom Responsive Sidebar Layout & Styling

- **Desktop View:** Use a dual-column CSS grid styled for `260px 1fr` (a left navigation sidebar and a main content area), leveraging 100% width on large screens.
- **Jekyll Navigation Categories:** The Jekyll sidebar layout in `docs/_layouts/default.html` is configured to render sections as distinct navigation categories ('Executive Blueprint', 'Engineering Runbook', and 'Security Posture & Audits') while preserving the original documents and layout intact (as per **Item 17**).
- **Mobile/Tablet View:** Below `992px`, transition to a stacked vertical layout featuring touch-friendly navigation button grids and horizontally scrollable tables.
- **Visual Architecture Badges:** Represent distinct target signatures (`[STRATEGIC FINANCIAL]`, `[DEVOPS EXECUTION]`, `[SECURITY & COMPLIANCE]`) styled using dedicated responsive CSS classes (`.arch-badge`, `.arch-badge-strategic`, `.arch-badge-devops`, and `.arch-badge-security`) in `docs/assets/css/global.css` and embedded at the top of document sections (as per **Item 7**).
- **Table Formatting Constraint:** To render list elements correctly inside Markdown tables built via Jekyll and kramdown, do not use HTML block elements like `<ul>` or `<li>` which display as literal tags. Instead, write list-style cells as inline text using unicode bullet points (e.g. `• item`) separated by `<br>` tags (as per **Item 24**).

---

## 2. Horizontal Table & Diagram Wrapping Safeguard

To prevent code blocks from wrapping unnecessarily:
- Standard preformatted text block elements (`#content pre`) are styled with `white-space: pre-wrap`.
- **Lightweight JS Scanner:** In `docs/_layouts/default.html`, configure a JavaScript snippet to dynamically scan code blocks at runtime. If box-drawing characters (such as `┌`, `└`, `├`, `─`, `│`) are detected, automatically apply a `.no-wrap` class.
- The `.no-wrap` class overrides standard wrapping with `white-space: pre !important`, enabling custom-styled, elegant horizontal scrollbars.

---

## 3. High-Fidelity PDF Generation & Page-Break Safeguard

- **Document Compilation (`docs/print_all.md`):** Aggregates documentation and module pages (including audits/ pages) in sequential order with custom print page-breaks, supporting automated repository-wide A4 PDF generation (as per **Item 16**).
- **Blank Page Safeguard:** To prevent blank first pages during print or PDF conversion, configure `html`, `body`, and `#container` with `height: auto !important` and `min-height: auto !important` inside the `@media print` CSS block in `docs/assets/css/global.css`. This overrides screen-only `100vh` constraints (as per **Item 36**).
- **Print PDF Action:** Implement an interactive "PRINT PDF" JavaScript button in `_layouts/default.html` that triggers standard window printing on clean white ("day") backgrounds.
- **GitHub Workflow:** The PDF generation workflow `.github/workflows/pdf-generation.yml` executes locally inside the runner by preparing documentation front matter, compiling the Jekyll site to `./_site` using `actions/jekyll-build-pages@v1`, and running a local Node.js script `scripts/generate_pdf.js` which uses Puppeteer to render `print_all.html` via a local HTTP server and output a high-fidelity PDF to `docs/assets/output.pdf` (as per **Item 37**).
- **Local serving Node.js script (`scripts/generate_pdf.js`):** To resolve 404 errors during automated PDF generation, the project uses a custom Node.js script `scripts/generate_pdf.js` which serves the statically-built Jekyll output on a local server and invokes Puppeteer directly on the runner host to compile a PDF of `print_all.html` natively without race conditions (as per **Item 38**).

---

## 4. Context7 AI Widget & Web Crawling SEO

- **Context7 Widget Integration:** The Context7 AI-powered chat assistant widget (provided by the Upstash team) is integrated site-wide into the Jekyll root layout (`docs/_layouts/default.html`), loading asynchronously with customizable styling attributes (`data-color="#059669"`, `data-position="bottom-right"`, `data-placeholder`, and `data-welcome-message`) (as per **Item 31**).
- **SEO & Base URL:** Point SEO tools to the primary base URL: `https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/` (as per **Item 41**).

---

## 5. Build Automation & Code Health Documentation

- **Docstring Standards:** All major script files in the repository have been updated with complete docstrings: PEP-257-compliant docstrings for `scripts/prepare_docs.py`, JSDoc-compliant comments for `scripts/generate_pdf.js`, and comprehensive header documentation with inline explanations for Bash scripts (as per **Item 5**).
- **Python Formatting & Unused Imports:** Python codebase formatting is cleaned up by removing unused `pytest` imports from all test files and correcting an extraneous `f` prefix on a log statement in `scripts/prepare_docs.py`, verified with `ruff check` and the `pytest` suite (as per **Item 4**).
- **OKF Document Preparation Script:** The pre-build Python script (`scripts/prepare_docs.py`) recursively scans and formats all `.md` files in the repository to ensure strict Open Knowledge Format (OKF) v0.1 compliance. It parses and serializes front matter starting on line 1, column 1, wraps strings containing special characters (colons, emojis, brackets, etc.) in double quotes, and preserves timestamps, arrays, layout configurations, and inline dictionaries intact (as per **Item 51**).

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
