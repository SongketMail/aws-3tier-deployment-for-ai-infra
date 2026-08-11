---
layout: "default"
okf_version: "0.1"
type: "report"
title: "Output of OpenSCAP"
timestamp: 2026-08-10T23:45:00Z
topics: ["openscap", "audits", "hardening", "security", "reports"]
---
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — SCAP Compliance & Audits
</div>

# Output of OpenSCAP

The **Security Content Automation Protocol (OpenSCAP)** is a NIST-certified auditing suite used to verify operating system compliance against standard security baselines. Within ASIMP, OpenSCAP evaluates target hosts against the **CIS (Center for Internet Security) Level 2 Server** profile.

This page provides detailed examples of OpenSCAP evaluation commands, XML results, rulesets, and report templates generated during audits.

---

## 📊 1. OpenSCAP CLI Evaluation Command & Output

During Phase 1 (`before`) and Phase 3 (`after`), ASIMP invokes the `oscap xccdf eval` utility to scan system parameters.

### CLI Command Example:
```bash
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis_level2_server \
  --fetch-remote-resources \
  --results /var/log/openscap-before-results.xml \
  --report /var/log/openscap-before-report.html \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml
```

### Terminal Live Output Example:
```text
Title   Ensure Software Updates and Patches are Applied
Rule    xccdf_org.ssgproject.content_rule_ensure_updates_applied
Result  fail

Title   Ensure SSH PermitRootLogin is set to No
Rule    xccdf_org.ssgproject.content_rule_sshd_disable_root_login
Result  fail

Title   Ensure SSH PasswordAuthentication is set to No
Rule    xccdf_org.ssgproject.content_rule_sshd_disable_password_auth
Result  fail

Title   Ensure SYN cookies are enabled
Rule    xccdf_org.ssgproject.content_rule_sysctl_net_ipv4_tcp_syncookies
Result  fail

Title   Verify Permissions on /etc/shadow
Rule    xccdf_org.ssgproject.content_rule_file_permissions_etc_shadow
Result  pass

Title   Ensure AIDE is Installed
Rule    xccdf_org.ssgproject.content_rule_package_aide_installed
Result  fail

========================================================================
OpenSCAP Evaluation Summary
  - Profile:   cis_level2_server
  - Checked:   142 rules
  - Passed:    83 rules
  - Failed:    59 rules
  - Score:     58.4%
========================================================================
```

---

## 📂 2. Parsed XML Score Result Example (`openscap-before-results.xml`)

OpenSCAP outputs a heavy XML results file. ASIMP extracts the score element natively using a runtime-generated Python parsing script (`parse_openscap_score.py`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Benchmark xmlns="http://checklists.nist.gov/xccdf/1.2" id="scap-security-guide">
  <TestResult id="xccdf_org.ssgproject.content_testresult_cis_level2_server">
    <profile idref="xccdf_org.ssgproject.content_profile_cis_level2_server"/>
    <target>asimp-backend-prod-01</target>
    <target-address>10.0.1.15</target-address>
    <!-- OpenSCAP Compliance Score out of 100 -->
    <score system="urn:xccdf:scoring:default">58.4</score>
  </TestResult>
</Benchmark>
```

---

## 🛡️ 3. Automatic Bash Remediation Script Example

In fully privileged environments, ASIMP can automatically generate an official OS-specific Bash remediation script. This script applies system modifications to bring the host into alignment with the CIS Level 2 profile:

### Script Generation Command:
```bash
oscap xccdf generate fix \
  --profile xccdf_org.ssgproject.content_profile_cis_level2_server \
  --fix-type bash \
  --output /var/log/remediate-noble-latest.sh \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml
```

### Remediation Script Sample (`remediate-noble-latest.sh`):
```bash
#!/usr/bin/env bash
# OpenSCAP Remediation Script for CIS Level 2 Server Profile on Ubuntu 24.04
# Automatically compiled by ASIMP

echo "Applying kernel sysctl mitigations..."
sysctl -w net.ipv4.tcp_syncookies=1
sysctl -w net.ipv4.ip_forward=0
sysctl -p

echo "Enforcing SSH security controls..."
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd

echo "Securing local build environments..."
chmod 0700 /usr/bin/gcc
chmod 0700 /usr/bin/g++
```

---

## 🐳 4. Ubuntu USN OVAL Security Audit

In addition to system configurations, ASIMP scans the operating system for unpatched, vulnerable packages using Canonical's official OVAL definition files:

```text
Evaluating OVAL definitions...
Definition oval:com.ubuntu.noble:def:20240001: Check for CVE-2024-3094 (XZ Backdoor)
Result: false (Not vulnerable / Fully Patched)

Definition oval:com.ubuntu.noble:def:20240002: Check for CVE-2024-6387 (RegreSSHion)
Result: false (Not vulnerable / Fully Patched)
```

The parsed result ensures that package levels meet the target zero-vulnerability threshold before final production launch.

---

*Verified by the ASIMP Compliance Team | OKF v0.1 Compliant | 2026-08-10*
