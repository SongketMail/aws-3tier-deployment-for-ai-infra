---
layout: "default"
okf_version: "0.1"
type: "report"
title: "Output of Lynis"
timestamp: 2026-08-10T23:45:00Z
topics: ["lynis", "audits", "hardening", "security", "reports"]
---
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — Lynis Host-Based Auditing
</div>

# Output of Lynis

**Lynis** is an open-source, host-based security auditing tool designed for Unix-based operating systems. It scans configurations, filesystems, kernel parameters, and active services to compute a standardized **Hardening Index (HI)** rating between 1 and 100.

Within ASIMP, Lynis is automatically integrated as the host-level auditing engine to measure baseline security levels (Phase 1) and confirm post-hardening improvements (Phase 3).

---

## 📊 1. Lynis Auditing Terminal Output Example

When Lynis is executed (via `lynis audit system --quick`), it performs comprehensive tests across dozens of security categories. Below is a high-fidelity example of the live scan output:

```text
[+] Initializing Lynis...
    - Program version:                      3.0.9
    - Operating system:                     Ubuntu Linux (24.04 LTS)
    - Kernel version:                       6.8.0-generic
    - Hardening index:                      [62] (Baseline)

[+] System Tools
    - Checking compiler presence...          [ FOUND ] (/usr/bin/gcc)
    - Checking debugger presence...          [ FOUND ] (/usr/bin/gdb)
    - Checking file integrity tool...        [ NOT FOUND ]

[+] Boot and Services
    - Checking service manager...            [ SYSTEMD ]
    - Checking runlevel/target...            [ graphical.target ]
    - Checking active services...            [ OK ]

[+] Kernel and Hardening
    - Checking kernel version...             [ OK ]
    - Checking core dumps configuration...   [ WARNING ] (Disabled in limits.conf but core_pattern not secure)
    - Checking sysctl values...              [ 8 issues found ]
      - net.ipv4.ip_forward:                 [ 1 ] (Expected: 0)
      - net.ipv4.conf.all.accept_redirects:  [ 1 ] (Expected: 0)
      - net.ipv4.tcp_syncookies:             [ 0 ] (Expected: 1)

[+] SSH Support
    - Checking SSH daemon...                 [ RUNNING ]
    - SSH option PermitRootLogin...          [ YES ] (Expected: NO)
    - SSH option PasswordAuthentication...   [ YES ] (Expected: NO)
    - SSH option MaxAuthTries...             [ 6 ] (Expected: <= 3)

[+] File permissions
    - Checking permissions on /etc/shadow... [ OK ] (chmod 0640)
    - Checking permissions on /etc/passwd... [ OK ] (chmod 0644)
    - Checking compiler permissions...       [ WEAK ] (executable by standard users)

========================================================================
  Audit Results
========================================================================
  - Hardening Index:                     62 / 100
  - Security Warnings:                   4
  - Suggestions:                         18
  - Log File:                            /var/log/lynis.log
  - Report File:                         /var/log/lynis-report.dat
========================================================================
```

---

## 📂 2. Structured Machine-Readable Report Example (`lynis-report.dat`)

Lynis writes a complete, structured `.dat` report file containing the raw telemetry parsed by the ASIMP framework. Below are the key security attributes retrieved during audits:

```text
# Lynis Report Data File
# Generated: 2026-08-10 23:34:21 UTC
lynis_version=3.0.9
os_name=Linux
os_version=24.04
hostname=asimp-backend-prod-01
hardening_index=62
warnings_count=4
suggestions_count=18
compiler_present=1
gdb_present=1
firewall_active=0
ssh_port=22
ssh_permit_root_login=yes
ssh_password_auth=yes
sysctl_net_ipv4_ip_forward=1
sysctl_net_ipv4_tcp_syncookies=0
```

---

## 🔒 3. Suggested & Executed Lynis Hardening Policies

After parsing the initial baseline report, ASIMP automatically resolves the reported suggestions by applying targeted Ansible playbooks to harden the host.

### Hardening Delta Summary

| Control Area | Baseline State (Index: 62) | Hardened State (Index: 88) | Remediation Applied |
| :--- | :--- | :--- | :--- |
| **SSH Configuration** | `PermitRootLogin yes`<br>`PasswordAuthentication yes` | `PermitRootLogin no`<br>`PasswordAuthentication no` | Overwritten via `ansible.builtin.lineinfile` in SSH roles. |
| **Local Firewall** | Disabled (`ufw` inactive) | Enabled (`ufw` whitelists Cyberjaya only) | Configured rules via `community.general.ufw`. |
| **Kernel Parameters** | IP Forwarding active<br>SYN Cookies disabled | IP Forwarding disabled<br>SYN Cookies active | Written values to `/etc/sysctl.conf` via `ansible.posix.sysctl`. |
| **System Compilers** | Accessible to all users | Restricted to Root-only (`chmod 0700`) | Enforced binary constraints via `ansible.builtin.file`. |

---

*Verified by the ASIMP Compliance Team | OKF v0.1 Compliant | 2026-08-10*
