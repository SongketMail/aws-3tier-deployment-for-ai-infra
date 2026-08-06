---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "Jekyll Layout & PDF Generation Skill"
timestamp: 2026-08-05T22:03:00Z
topics: ["aws", "cloud", "architecture", "skill", "jekyll", "pdf", "css", "html", "print"]
description: "Guidelines for configuring custom responsive Jekyll layouts, box-drawing character scanners, CSS print overrides, and high-fidelity PDF workflows."
name: "jekyll-pdf-generation"
---
# Jekyll Layout & PDF Generation Skill

This skill governs the standards for managing the project's Jekyll documentation layout, maintaining responsive design, safeguarding tables/diagrams from text wrapping, and enabling high-fidelity PDF generation.

---

## 1. Custom Responsive Sidebar Layout

- **Desktop View:** Use a dual-column CSS grid styled for `260px 1fr` (a left navigation sidebar and a main content area), leveraging 100% width on large screens.
- **Mobile/Tablet View:** Below `992px`, transition to a stacked vertical layout featuring touch-friendly navigation button grids and horizontally scrollable tables.

---

## 2. Horizontal Table & Diagram Wrapping Safeguard

To prevent code blocks from wrapping unnecessarily:
- Standard preformatted text block elements (`#content pre`) are styled with `white-space: pre-wrap`.
- **Lightweight JS Scanner:** In `docs/_layouts/default.html`, configure a JavaScript snippet to dynamically scan code blocks at runtime. If box-drawing characters (such as `┌`, `└`, `├`, `─`, `│`) are detected, automatically apply a `.no-wrap` class.
- The `.no-wrap` class overrides standard wrapping with `white-space: pre !important`, enabling custom-styled, elegant horizontal scrollbars.

---

## 3. High-Fidelity PDF Generation & Page-Break Safeguard

- **Blank Page Safeguard:** To prevent blank first pages during print or PDF conversion, configure `html`, `body`, and `#container` with `height: auto !important` and `min-height: auto !important` inside the `@media print` CSS block in `docs/assets/css/global.css`. This overrides screen-only `100vh` constraints.
- **Print PDF Action:** Implement an interactive "PRINT PDF" JavaScript button in `_layouts/default.html` that triggers standard window printing on clean white ("day") backgrounds.
- **GitHub Workflow:** Automate PDF publication via `.github/workflows/pdf-generation.yml` using `misaelnieto/web_to_pdf_action@v0.3.1` on merges to the main branch.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
