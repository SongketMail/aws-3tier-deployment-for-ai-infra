---
layout: "default"
okf_version: "0.1"
type: "Skill"
title: "Secure SSH Jumphost & AMI Baking Skill"
timestamp: 2026-08-05T21:58:00Z
topics: ["aws", "cloud", "architecture", "skill", "jumphost", "bastion", "ssh", "ami", "packer", "ansible"]
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
- Bake and register the AMIs regularly, and rotate ASG Launch Templates to reference the newest validated AMI.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
