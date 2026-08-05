---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "History, Changelog & Milestones Skill"
timestamp: 2026-08-05T22:02:00Z
topics: ["aws", "cloud", "architecture", "skill", "changelog", "history", "milestones", "narrative"]
description: "Guidelines and procedures for maintaining standard-compliant changelogs and strategic engineering history files from Day 0."
name: "changelog-milestones-narrative"
---
# History, Changelog & Milestones Skill

This skill governs the standards for capturing architectural evolutionary decisions, strategic milestones, and maintaining semantically structured changelogs.

---

## 1. The Day 0 Historical Narrative

- Maintain a rich strategic engineering log in `HISTORY.md` detailing the project's starting point from Day 0 (the monolithic, fragile single-VM baseline).
- Clearly explain the rationale behind architectural upgrades—such as why the deployment migrated to highly available AWS managed services, OpenTofu modular networks, and Graviton compute tiers.
- Use the historical narrative to onboard new developers and context-sync AI agents.

---

## 2. Standard-Compliant Changelogs

- Maintain `CHANGELOG.md` in strict adherence to semantic versioning patterns.
- Group changes into clear categories:
  - `Added` for new features or submodules.
  - `Changed` for upgrades, structural modifications, or resource tweaks.
  - `Deprecated` for features slated for removal.
  - `Removed` for cleanups of deprecated items.
  - `Fixed` for bug resolutions, syntax corrections, and hotfixes.
  - `Security` for patches, CVE updates, and IAM whitelisting enhancements.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
