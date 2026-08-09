---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "DNS & systemd-resolved Troubleshooting"
timestamp: 2026-08-09T14:00:00Z
topics: ["devops", "engineering", "runbook", "dns", "route53"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>

# 🛠️ DNS & systemd-resolved Troubleshooting

This runbook documents low-level diagnostics and resolutions for **systemd-resolved** DNS caching failures, private subnet DNS resolution blocks, and Route 53 hosted zones setups.

---

## 🔍 1. Troubleshooting systemd-resolved DNS Caching

Ubuntu 26.04 LTS utilizes `systemd-resolved` to handle DNS resolution. In high-concurrency environments, resolver cache corruption or misconfigured upstream links can block the compute instances from resolving external API webhooks (such as the Meta WhatsApp Business API).

### Symptoms
* Inability to resolve domains with error `Temporary failure in name resolution`.
* Dig queries direct to `127.0.0.53` timeout, while queries to Google's public resolver (`8.8.8.8`) succeed.

### 🛠️ Diagnostic Commands Runbook

1. **Verify Link-Specific DNS Configuration:**
   Check what upstream DNS servers are currently assigned to active interfaces:
   ```bash
   resolvectl status
   ```

2. **Query Stats & Cache Performance:**
   Audit active cache hits, misses, and current configuration:
   ```bash
   resolvectl statistics
   ```

3. **Flush Resolver Cache immediately:**
   Clear cache blocks to resolve stale records:
   ```bash
   resolvectl flush-caches
   ```

4. **Verify Symlink Configuration:**
   Ensure `/etc/resolv.conf` is symlinked correctly to the systemd-resolved stub listener:
   ```bash
   ls -la /etc/resolv.conf
   # Expected output:
   # /etc/resolv.conf -> ../run/systemd/resolve/stub-resolv.conf
   ```
   If the symlink is broken, recreate it:
   ```bash
   sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
   sudo systemctl restart systemd-resolved
   ```

---

## 🗺️ 2. Route 53 Resolver Configuration inside Private Subnets

To resolve private domains within a VPC (e.g., routing `/crm/*` to specific internal endpoints), we must enable private DNS support within our OpenTofu VPC module:

```hcl
# Location: terraform/modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true # Required for Route 53 Private Hosted Zones
  enable_dns_hostnames = true # Required for internal VPC DNS mapping

  tags = {
    Name = "secure-3tier-vpc"
  }
}
```

### Route 53 Health Checks & Failover
We utilize Route 53 active-passive failover. In the event of primary ALB failure in `ap-southeast-5a/b`, Route 53 health checks dynamically reroute traffic to the backup static landing page:

```bash
# Verify active DNS routing endpoints
dig secure-app.songketmail.github.io
```

---

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
