---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Onsite On-Premises VM & Network Architecture"
timestamp: 2026-08-09T15:00:00Z
topics: ["onprem", "virtualization", "networking", "topology", "vlan"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — Network Security & Auditing Teams
</div>

# 🏛️ Onsite On-Premises Virtual Machine & Network Architecture

This guide details the physical host allocation, hypervisor configuration, virtual machine (VM) partitioning, and private VLAN layout for our onsite on-premises deployment. It maps the AWS secure 3-tier cloud design directly into a hardened, high-availability local network topology.

---

## 🏗️ 1. Hypervisor and Virtual Machine Sizing

To ensure performance predictability and complete service isolation, we utilize a local Type-1 hypervisor (such as **Proxmox VE**, **VMware ESXi**, or **KVM**). The AWS-equivalent resources are distributed across three distinct virtual machines operating inside independent network segments.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PHYSICAL HYPERVISOR HOST                        │
│                                                                        │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐ │
│ │  VM-01: DMZ & Mgmt   │ │    VM-02: App Tier   │ │ VM-03: DB & AI   │ │
│ │ (4 vCPU, 8GB RAM)    │ │ (8 vCPU, 16GB RAM)   │ │ (16 vCPU, 64GB)  │ │
│ ├──────────────────────┤ ├──────────────────────┤ ├──────────────────┤ │
│ │ • BunkerWeb Proxy    │ │ • Spring Boot App    │ │ • PostgreSQL 17  │ │
│ │ • Gitea VCS / Runner │ │ • Vite-React Server  │ │ • Valkey Cache   │ │
│ │ • Semaphore & ARA    │ │ • Keycloak IAM       │ │ • Ollama & RAG   │ │
│ └──────────┬───────────┘ └──────────┬───────────┘ └────────┬─────────┘ │
└────────────┼────────────────────────┼──────────────────────┼───────────┘
             ▼                        ▼                      ▼
       [ VLAN 10 DMZ ]          [ VLAN 20 APP ]        [ VLAN 30 DB/AI ]
```

### Resource Sizing Matrix

| Virtual Machine | Logical Tier | Target Operating System | vCPU | RAM | Storage | Primary Services |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **VM-01** | Ingress, Management & VCS | Ubuntu 24.04 LTS (Hardened) | 4 | 8 GB | 150 GB SSD | BunkerWeb (Proxy), Gitea, Ansible Semaphore, Ansible ARA |
| **VM-02** | Secure Application Tier | Ubuntu 24.04 LTS (Hardened) | 8 | 16 GB | 200 GB SSD | Spring Boot (Backend), React Web, Keycloak (IAM) |
| **VM-03** | Sovereign DB & AI Tier | Ubuntu 24.04 LTS (Hardened) | 16 | 64 GB | 1 TB NVMe | PostgreSQL 17, Valkey Cache, Ollama, RAGFlow, Langfuse |

---

## 🔒 2. Multi-Tier VLAN and Network Isolation

Security is enforced at the hypervisor virtual switch layer. We configure three isolated virtual LANs (VLANs) that mirror the AWS Zero-Trust Subnet architecture. Direct routing is managed by a hardware firewall (e.g., pfSense, OPNsense, or Cisco ASA) with strict stateful ingress rules.

### Virtual Network Interfaces (VNIs) Mapping

1. **VLAN 10 (DMZ / External Ingress):**
   - **Subnet Range:** `10.10.10.0/24`
   - **Scope:** Public-facing virtual ports. Receives incoming HTTPS traffic from the corporate switch and routes it to BunkerWeb. No direct traffic is allowed from VLAN 10 to VLAN 30.
2. **VLAN 20 (Private Application Tier):**
   - **Subnet Range:** `10.10.20.0/24`
   - **Scope:** Secure app communication. Hosts VM-02. Only accepts traffic from BunkerWeb (VLAN 10) on designated application ports (e.g., `8080` for backend, `8443` for Keycloak).
3. **VLAN 30 (Isolated Database & AI Processing Tier):**
   - **Subnet Range:** `10.10.30.0/24`
   - **Scope:** Highest classification area. Hosts PostgreSQL, Valkey, and Ollama/RAGFlow. **Completely isolated from the DMZ.** Only accepts incoming connections from VLAN 20 (App Server) on port `5432` (Postgres) and `6379` (Valkey).

### Stateful Firewall Rule Matrix

| Source Network | Destination VM/Network | Allowed Destination Ports | Description / Business Justification |
| :--- | :--- | :--- | :--- |
| **Corporate LAN** | **VM-01 (VLAN 10)** | `80/tcp`, `443/tcp` | Public web traffic routing to BunkerWeb Edge Proxy. |
| **Corporate Admin CIDR** | **VM-01 (VLAN 10)** | `22/tcp`, `3000/tcp` | Whitelisted admin access to Gitea VCS and SSH. |
| **VM-01 (BunkerWeb)** | **VM-02 (VLAN 20)** | `8080/tcp`, `8443/tcp` | Edge proxy forwarding clean, decrypted traffic to Spring Boot and Keycloak. |
| **VM-02 (VLAN 20)** | **VM-03 (VLAN 30)** | `5432/tcp` | Spring Boot backend connecting to PostgreSQL database. |
| **VM-02 (VLAN 20)** | **VM-03 (VLAN 30)** | `6379/tcp` | Spring Boot backend caching session states in Valkey. |
| **VM-02 (VLAN 20)** | **VM-03 (VLAN 30)** | `11434/tcp`, `9300/tcp` | Spring Boot backend invoking Ollama LLM and Elasticsearch queries. |

---

## 🐳 3. Local Rootless Podman Network Mapping

Within each VM, containers do not communicate directly on the host's physical VNI. Instead, they operate inside an unprivileged virtual network managed natively by **Podman 5+**.

```
┌────────────────────────────────────────────────────────┐
│                      VM-03 (HOST)                      │
│                                                        │
│   ┌────────────────────────────────────────────────┐   │
│   │ Podman User-Space Network: skm_fabric_net      │   │
│   │ Subnet: 10.89.1.0/24                           │   │
│   ├────────────────────────────────────────────────┤   │
│   │  [PostgreSQL Container]  ◄───►  [Valkey Cache] │   │
│   │     (10.89.1.10)                 (10.89.1.20)  │   │
│   │                                                │   │
│   │  [Ollama AI Engine]      ◄───►  [RAGFlow App]  │   │
│   │     (10.89.1.30)                 (10.89.1.40)  │   │
│   └────────────────────────┬───────────────────────┘   │
└────────────────────────────┼───────────────────────────┘
                             ▼ (Exposed via User Ports)
                   Host Port Mapping (VLAN 30)
```

By defining unprivileged subnets inside Podman Quadlets, we ensure that:
- Containers remain completely decoupled from the host VM's local network stack.
- Dynamic DNS names (e.g. `postgresql.skm_fabric_net`) resolve cleanly within the user session using Podman's built-in DNS plugin.
- Port translation is handled safely via `PublishPort` definitions in systemd Quadlet files, keeping root privileges completely out of the runtime container flow.

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
