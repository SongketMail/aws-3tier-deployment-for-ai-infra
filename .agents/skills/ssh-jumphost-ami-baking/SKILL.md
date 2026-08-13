---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "Secure SSH Jumphost & AMI Baking Skill"
timestamp: 2026-08-05T21:58:00Z
topics: ["aws", "cloud", "architecture", "skill", "jumphost", "bastion", "ssh", "ami", "packer", "ansible", "asimp", "wazuh", "spa"]
description: "Guidelines for configuring secure SSH Bastion access, whitelisting Cyberjaya office CIDRs, protecting SSH keys, and baking CIS-compliant Ubuntu 26.04 AMIs."
name: "ssh-jumphost-ami-baking"
---
# Secure SSH Jumphost & AMI Baking Skill

This skill governs secure operator access, developer SSH whitelisting, and compliance-driven AMI baking pipelines in the workspace.

---

## 1. Public SSH Jumphost (Bastion) Module

- Deploy a dedicated SSH Bastion instance inside the public subnet.
- **Access Control:** Assign a static Elastic IP and restrict incoming SSH on port `22` exclusively to the configured Cyberjaya developer office CIDR.
- **Downstream Routing:** The Jumphost module automatically injects whitelisted ingress rules into the private application and compute security groups.

---

## 2. Developer Access & SSH Key Hardening

Operators accessing private compute nodes must follow strict SSH safety protocols:
- **Key Permissions (macOS/Linux):** Limit file permissions on the private key file immediately:
  ```bash
  chmod 400 my-private-key.pem
  ```
- **Key Permissions (Windows PowerShell/cmd):** Restrict key file inheritance using PowerShell:
  ```powershell
  icacls.exe my-private-key.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"
  ```
- Establish connections by forwarding SSH agent credentials (`ssh -A`) to transit through the whitelisted Jumphost.

---

## 3. CIS Compliant AMI Baking with Packer/Ansible

- Enforce Ubuntu 26.04 LTS CIS Level 2 compliance for all application ASGs.
- Utilize HashiCorp Packer to spin up staging instances, and configure them via Ansible playbooks using the ASIMP (Ansible System Integrity Management Platform) security framework.
- **FQCN Ansible Playbooks:** The Ansible playbook in `docs/engineering/ansible_asimp_hardening.md` has been refactored to use Fully Qualified Collection Names (FQCN) such as `ansible.builtin.apt`, `ansible.builtin.lineinfile`, and `community.general.ufw` (as per **Item 3**).
- **On-Premises Ansible Playbooks:** On-premises infrastructure is automated using FQCN-compliant Ansible playbooks split between rootful OS tuning (`become: yes`) and rootless unprivileged user operations (`become_user: songket`), integrated with a self-hosted CI/CD stack utilizing Gitea (VCS), Ansible Semaphore (Web UI execution), and Ansible ARA (callback database reporting) (as per **Item 14**).
- Bake and register the AMIs regularly, and rotate ASG Launch Templates to reference the newest validated AMI.

---

## 4. Hardening Audits & Security Hardening Scorecards

- **Audit Output Pages:** High-fidelity audit output pages for ASIMP (`docs/audits/asimp-output.md`), Lynis (`docs/audits/lynis-output.md`), and OpenSCAP (`docs/audits/openscap-output.md`) have been added to the project, demonstrating typical terminal configurations, security hardening scorecards, logs, and compliance audits under a new 'Security Posture & Audits' navigation menu (as per **Item 15**).
- **Security Posture Assessment (SPA) Checklist:** A comprehensive SPA Checklist tailored to the project's Java 21, Spring Boot 3.5.12, React 19, RDS PostgreSQL, Valkey, RAGFlow, Langfuse, and Wazuh SIEM stack is documented at `docs/audits/security-posture-assessment.md` and registered across all index and search portals (as per **Item 18**).
- **Wazuh SIEM Antivirus Coexistence & Mutual Exclusions:** Operational guidance regarding Antivirus coexistence (including Windows Defender compatibility, third-party AV compatibility, potential conflict areas, and mutual exclusions configurations) is detailed in `docs/wazuh-detailed.md` to ensure zero-conflict operations on hardened hosts (as per **Item 1**).

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
