---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Rootless Podman 5+ & systemd Quadlets"
timestamp: 2026-08-09T15:00:00Z
topics: ["onprem", "virtualization", "podman", "quadlet", "systemd", "rootless"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — Security Hardening & Platform Engineers
</div>

# 🐳 Rootless Podman 5+ & systemd Quadlet Orchestration

This guide outlines our standards for running production workloads within an unprivileged, non-root user space using **Podman 5+** and **systemd Quadlets**. This setup completely eliminates security risks associated with rootful Docker daemons, integrating containers directly into the host OS's native service manager.

---

## ⚙️ 1. Mandatory Environment Variables

Rootless systemd operations require access to user-level D-Bus sockets and state directories. To run commands like `systemctl --user` successfully via SSH, automation scripts, or Ansible, the following environment variables **must** be passed explicitly:

### `XDG_RUNTIME_DIR`
* **Definition:** Specifies the directory where user-specific runtime status files are kept.
* **On-Premises Default:** `/run/user/<UID>` (for our dedicated service account `songket` with UID `2001`, this is `/run/user/2001`).
* **Impact:** Without this, unprivileged systemd commands fail with: `Failed to connect to bus: No such file or directory`.

### `DBUS_SESSION_BUS_ADDRESS`
* **Definition:** Directs D-Bus clients to the user-level message bus socket.
* **On-Premises Default:** `unix:path=/run/user/<UID>/bus` (e.g. `unix:path=/run/user/2001/bus`).
* **Impact:** Authenticates and routes API commands to the correct unprivileged systemd daemon.

---

## 🔒 2. The keep-id Namespace Mapping Solution

When a rootless container is launched, Podman maps UID `0` (root) inside the container to the host user's UID (e.g., `2001` for `songket`). Any non-root UID inside the container (like an internal app user with UID `1000` or `2001`) gets remapped to high-range host subuids (such as `102000`).

This remapping corrupts host directory mounts, as files created by the container will be owned by unresolvable high UIDs, making backups, audits, and database upgrades extremely difficult.

```
┌────────────────────────────────────────────────────────────────────────┐
│                     USER NAMESPACE MAPPING COMPARED                    │
│                                                                        │
│  [ Default Rootless Remap ]                                            │
│    Container User: UID 2001 ──────► Host OS: High SubUID (e.g., 102000)│
│    *Result: Permissions mismatch, backup corruption, file access denied.*│
│                                                                        │
│  [ keep-id Remapping (Active Standard) ]                               │
│    Container User: UID 2001 ──────► Host OS: User songket (UID 2001)   │
│    *Result: Transparent 1:1 file ownership, pristine host backups.*     │
└────────────────────────────────────────────────────────────────────────┘
```

### Storage Sovereignty via `UserNS=keep-id:uid=2001,gid=2001`

We enforce namespace parity by running containers with `keep-id` namespace mapping.
1. We provision a non-root user and group (`songket:songket`, UID/GID `2001:2001`) on the host OS.
2. We create directory trees on the host (e.g. `/var/srv/songketmail/`) and assign them ownership of `2001:2001`.
3. In the Quadlet container file, we declare:
   ```ini
   UserNS=keep-id:uid=2001,gid=2001
   ```
This instructs Podman to translate UID/GID `2001:2001` inside the container directly to UID/GID `2001:2001` on the host, maintaining transparent permissions without requiring administrative privileges.

---

## 📄 3. Declarative Quadlet Specifications

Systemd Quadlets are declarative `.container`, `.volume`, `.pod`, and `.network` configuration files located inside the user's systemd config directory:
`/home/songket/.config/containers/systemd/`

When systemd reloads, the Quadlet generator automatically compiles these files into native, standard systemd system units. Below are production-ready specifications for our core on-premises services:

### A. The Shared Pod definition (`skm_pod.pod`)
```ini
# /home/songket/.config/containers/systemd/skm_pod.pod
[Pod]
PodName=skm_pod
Network=skm_net.network
UserNS=keep-id:uid=2001,gid=2001
PublishPort=8080:8080
PublishPort=8443:8443
```

### B. The Internal Bridge Network (`skm_net.network`)
```ini
# /home/songket/.config/containers/systemd/skm_net.network
[Network]
NetworkName=skm_net
Subnet=10.89.1.0/24
Gateway=10.89.1.1
Internal=false
```

### C. The Application Container (`emailserver.container` Example)
```ini
# /home/songket/.config/containers/systemd/emailserver.container
[Container]
ContainerName=skm_fabric_emailserver
Pod=skm_pod.pod
Image=docker.io/library/postfix:3.9.0
Volume=/var/srv/songketmail/postfix/config:/etc/postfix:Z
Volume=/var/srv/songketmail/postfix/spool:/var/spool/postfix:Z
UserNS=keep-id:uid=2001,gid=2001

[Service]
Restart=always
```
*(The `:Z` volume flag is crucial on systems running SELinux, as it auto-labels mounted storage to match container contexts).*

---

## 🔄 4. Enabling systemd Lingering

By default, user-level systemd processes are killed when the unprivileged host user logs out of their terminal session. To ensure that our rootless application services boot automatically on host startup and survive logouts, we **must** enable systemd lingering.

This is executed once with root privileges on the VM host:
```bash
sudo loginctl enable-linger songket
```

Verification of lingering is performed by inspecting if the user's name exists in the system directory:
```bash
ls /var/lib/systemd/linger/songket
```

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
