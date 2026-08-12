---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Wazuh SIEM & XDR Deep-Dive: Cloud, On-Premises & AV Compatibility"
timestamp: 2026-08-10T12:00:00Z
topics: ["wazuh", "siem", "xdr", "security", "antivirus", "windows-defender", "cloud", "onprem"]
---
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — Security Operations & Hardening Guidance
</div>
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SecOps
</div>

# Wazuh SIEM & XDR Deep-Dive: Cloud, On-Premises & AV Compatibility

Modern IT infrastructure requires unified visibility across all assets—including endpoints, servers, containers, cloud resources, and user identities. Wazuh is an enterprise-grade, open-source security monitoring platform that fulfills this requirement by acting as both a **SIEM** (Security Information and Event Management) and an **XDR** (Extended Detection and Response) platform.

This guide explores the functions of Wazuh, why it is critical for modern secure architectures, its deployment options, and how it coexists with Antivirus (AV) programs, including Microsoft Windows Defender and other third-party products.

---

## 🏛️ 1. Wazuh Core Functions & Why We Need It

Wazuh goes beyond traditional log collection. It functions by deploying a lightweight agent on target hosts and forwarding security telemetry to a centralized Wazuh manager cluster. The key features that make Wazuh indispensable include:

### A. Centralized Log Analysis & Correlation (SIEM)
Wazuh collects, parses, and normalizes log data from operating systems, applications (web servers, databases), cloud APIs, network firewalls, and containers. The Wazuh manager runs these logs through an extensive, customisable rule engine, correlating events in real-time to alert security operations teams of suspicious activity.

### B. File Integrity Monitoring (FIM / Syscheck)
Wazuh tracks changes to system files, directories, registry keys (on Windows), and file attributes in real-time or via scheduled sweeps. FIM detects unauthorized modifications, helping organizations identify rootkits, unauthorized user activities, and potential compromise indicators.

### C. Vulnerability Detection
By scanning package managers, system patches, and application versions on enrolled agents, Wazuh correlates local software states with global CVE (Common Vulnerabilities and Exposures) databases. This provides a continuous, automated vulnerability scanner across your entire fleet.

### D. Security Configuration Assessment (SCA)
Wazuh runs automated checks against system configurations, comparing them with industry standards such as Center for Internet Security (CIS) benchmarks. SCA ensures that OS settings, SSH configurations, firewall policies, and password requirements are hardened to limit the attack surface.

### E. Active Response & Threat Mitigation
Wazuh agents can execute automatic, immediate defensive measures when specified alerts are triggered. These actions include blocking an attacking IP address at the firewall (iptables/UFW/Windows Firewall), killing rogue processes, or isolating a compromised host from the network.

---

## ☁️ 2. Wazuh Deployment Models: Cloud vs. On-Premises

Depending on your organizational requirements, compliance needs, and budget, Wazuh can be deployed in the cloud or as a self-hosted on-premises solution.

### Cloud Deployments

#### Standalone EC2 (Best & Cheapest for AWS)
As detailed in our [Wazuh Standalone Cloud Installation & Costing Guide](wazuh.html), launching a clean Ubuntu LTS instance using AWS Graviton (such as `t4g.large` in the Malaysia region `ap-southeast-5`) and running the All-in-One assistant script is highly cost-effective.
* **Monthly Cost:** ~$65.71 USD (approx. RM 295.70 MYR).
* **Pros:** Highly customized, ARM64 pricing efficiency, full administrative control.
* **Cons:** Manual setup and maintenance of OS updates.

#### Official AWS Marketplace AMI
A pre-packaged Amazon Machine Image (AMI) provided by the Wazuh team on `c5a.xlarge`.
* **Monthly Cost:** ~$153.16 USD (approx. RM 689.23 MYR).
* **Pros:** Fast provisioning, official baseline configurations.
* **Cons:** Restricted to x86_64 architecture, more expensive compute node.

#### Wazuh Cloud (SaaS)
Fully managed SaaS offering maintained directly by Wazuh.
* **Pros:** Zero-management backend, automatic updates, high availability managed by the vendor.
* **Cons:** High subscription costs, potential data sovereignty and latency concerns for Malaysian PDPA compliance.

---

### On-Premises Deployments

For organizations operating under strict national sovereignty rules (e.g., Malaysia's PDPA 2010 and 2025 CBPDT Guidelines), on-premises deployments ensure all telemetry data remains within local physical bounds:

#### VM-Based Standalone
Deploying the three core components (Wazuh Indexer, Wazuh Manager, and Wazuh Dashboard) onto a single hardened Ubuntu VM or physical server inside a dedicated Management VLAN.

#### Rootless Podman & systemd Quadlets
For containerized microservices architectures, Wazuh can be deployed on-premises as a multi-container stack. This stack runs under unprivileged user namespaces (`UserNS=keep-id:uid=2001,gid=2001`) with storage mapped natively to encrypted physical volumes.

---

## 🛡️ 3. Antivirus Coexistence & Compatibility

A critical question when deploying endpoint monitoring is: **Does the Wazuh agent conflict with antivirus (AV) software?**

### Compatibility with Windows Defender
**Yes, Wazuh is 100% compatible with Microsoft Windows Defender.**

In fact, Wazuh features native integration with Windows Defender. Instead of competing, they work cooperatively:
1. **Event Log Ingestion:** Wazuh actively reads and parses events from the `Microsoft-Windows-Windows Defender/Operational` channel.
2. **Coordinated Alerting:** If Windows Defender blocks malware or detects a threat, Wazuh captures the event log, triggers a high-severity alert on the Wazuh Dashboard, and alerts security analysts.
3. **Double Defense:** Defender handles real-time signature matching, quarantine, and local disinfection, while Wazuh correlates Defender's logs with network telemetry, Active Directory events, and FIM triggers.

---

### Compatibility with Third-Party AV (Symantec, McAfee, CrowdStrike, SentinelOne, etc.)
The Wazuh agent is generally fully compatible with modern EDRs (Endpoint Detection & Response) and traditional AV programs. However, as with any security agent that performs deep system inspection, **certain conflict points can occur if not configured properly.**

#### Potential Conflict Points:
* **Simultaneous File Access (CPU/Disk I/O Spike):** When Wazuh's File Integrity Monitoring (FIM / Syscheck) scans system folders, it reads file metadata and hashes (MD5/SHA256). If an active AV simultaneously scans those same files as they are opened, this can lead to severe disk I/O bottlenecks and temporary system performance drops.
* **False Positive Flags (Interception Block):** Because the Wazuh agent monitors processes, checks open ports, and reads raw event logs, a highly aggressive third-party AV or EDR might flag the Wazuh agent's system activity as malicious behavior, potentially killing the `wazuh-agentd` service or blocking its connection to the manager.
* **Active Response Mitigation Collisions:** If a third-party AV detects a threat and locks a file, while Wazuh triggers an Active Response script to kill the associated process, the two agents might collide, causing execution failures or corrupting state locks.

---

### Resolution: Mutual Exclusions Configuration
To prevent performance degradation and false positives, administrators must configure **mutual exclusions** on both systems.

#### Step 1: Configure AV Exclusions for Wazuh
Add the Wazuh installation directories to your third-party AV's whitelist/exclusion policies so that the AV does not scan Wazuh's local database files or monitor its binaries:
* **Windows:** `C:\Program Files (x86)\ossec-agent\`
* **Linux:** `/var/ossec/`
* **macOS:** `/Library/Ossec/`

#### Step 2: Configure Wazuh Exclusions for the AV
In the Wazuh agent configuration (`ossec.conf`), ensure that Wazuh's Syscheck (FIM) ignores the active folders of your antivirus software to prevent unnecessary, overlapping scan loops:

```xml
<!-- Example of Wazuh agent's ossec.conf Syscheck section -->
<syscheck>
  <!-- Ignore local Windows Defender databases and temp files -->
  <ignore>C:\ProgramData\Microsoft\Windows Defender</ignore>

  <!-- Ignore Third-Party Antivirus signature/definition folders -->
  <ignore>C:\ProgramData\McAfee</ignore>
  <ignore>C:\Program Files\CrowdStrike</ignore>
</syscheck>
```

---

### "Passive Mode" Configurations in Wazuh
If your organization requires the third-party antivirus to be the **only active defender** (handling blocklist checks, process kills, and quarantines), you can configure the Wazuh agent to operate in a **purely passive metadata and log aggregation mode**.

To enforce Wazuh "Passive Mode", adjust these settings in your central or local agent configuration:

#### 1. Disable Active Response
Ensure that Wazuh does not attempt to execute automatic blocks, file removals, or process terminations, leaving response actions entirely to the AV:
```xml
<active-response>
  <disabled>yes</disabled>
</active-response>
```

#### 2. Tune File Integrity Monitoring (Syscheck)
Instead of real-time file monitoring, which constantly hooks file changes, switch Syscheck to scheduled, low-priority scanning (e.g., once every 12 or 24 hours during off-peak times) to eliminate disk I/O collisions:
```xml
<syscheck>
  <scan_on_start>no</scan_on_start>
  <frequency>86400</frequency> <!-- Scan once per day (in seconds) -->
  <realtime>no</realtime> <!-- Disable real-time monitoring -->
</syscheck>
```

#### 3. Focus Strictly on Event Log and Process Aggregation
Configure the agent to only ingest application logs and OS-generated security events, letting the AV handle active on-access file scanning:
```xml
<localfile>
  <log_format>eventlog</log_format>
  <location>Security</location>
</localfile>
```

---

## 🚀 4. Understanding XDR: What is it, and why is Wazuh an XDR?

### What is XDR?
**XDR** stands for **Extended Detection and Response**. It is an evolutionary step beyond traditional EDR (Endpoint Detection and Response) and classic SIEM tools.

* **EDR:** Focuses strictly on monitoring physical endpoints (laptops, desktops, servers) for threat signatures and execution paths.
* **SIEM:** Focuses on aggregating massive volumes of log data from different network components for historical query, compliance, and correlation.
* **XDR:** Unifies both models. It extends beyond endpoint protection by seamlessly integrating security telemetry from **multiple layers**—endpoints, network traffic, cloud platforms, containers, and identity access systems—into a single, correlated data stream. XDR doesn't just detect; it automatically coordinates **active responses** across these diverse layers.

```
                  ┌──────────────────────────────────────────────┐
                  │                 WAZUH XDR                    │
                  └──────┬────────────────────────────────┬──────┘
                         │                                │
     ┌───────────────────┴───────────┐       ┌────────────┴──────────────────┐
     │      EXTENDED DETECTION       │       │       EXTENDED RESPONSE       │
     └───────────────────────────────┘       └───────────────────────────────┘
       • Endpoint / Server Logs                • Host Isolation (mTLS Block)
       • Cloud API Audits (AWS CloudTrail)     • Network Firewall Ingress Ban
       • Container Runtime Inspection          • Active Directory User Account Lock
       • Local Network Socket Mon              • Process Killing (Malware Kill)
```

---

### Why Wazuh is a True XDR Platform

Wazuh is classified as a genuine XDR platform because it bridges the gaps between network security, cloud activity, host behavior, and active security automation:

#### 1. Multi-Vector Telemetry Integration (Extended Detection)
Rather than looking only at process execution on a VM, Wazuh correlates multiple domains simultaneously:
* **Endpoints:** Ingests local system calls, RAM changes, shell commands, and file hash alterations.
* **Network Traffic:** Parses logs from Suricata, Snort, or Bro/Zeek to detect network scans and SQL injection vectors.
* **Cloud Infrastructure:** Directly monitors cloud APIs (such as AWS CloudTrail, Amazon GuardDuty, and VPC Flow Logs) to track infrastructure modifications, MFA deletions, and unauthorized security group configuration changes.
* **Containers & Kubernetes:** Integrates with Docker socket event streams and Kubernetes API audits to detect container escapes or privilege-escalation attempts.
* **Identity and Access:** Monitors authentication patterns (Active Directory, LDAP, Keycloak, or AWS Cognito) to flag brute-force attacks and credential stuffing.

#### 2. Cross-Layer Threat Correlation
If a malicious actor executes an attack, Wazuh does not treat the events in isolation. For example:
1. An attacker attempts a brute-force login on Keycloak (**Identity Layer**).
2. The login succeeds, and the actor immediately spins up a rogue instance (**Cloud Layer**).
3. The new instance starts port scanning other private VPC nodes (**Network Layer**).
4. The actor attempts to modify a host's SSH authorized keys file (**Endpoint Layer**).

Wazuh correlates these distinct vectors into a single, cohesive security incident chain, enabling security teams to see the complete lifecycle of the attack.

#### 3. Automated Cooperative Countermeasures (Extended Response)
An XDR must be capable of orchestrating responses across its scope. Wazuh supports this via dynamic **Active Response**:
* **Endpoint response:** Instantly terminates a flagged ransomware process or deletes a dropped malicious script.
* **Network response:** Automatically executes a script to update a local firewall blocklist or triggers an API call to a corporate edge proxy (like BunkerWeb) to block a brute-forcing IP address.
* **Access response:** Can execute a command to lock or disable a compromised local user account in the OS directory.

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-10 Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
