---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Open-Source On-Premise Stack Specs"
timestamp: 2026-08-09T15:00:00Z
topics: ["onprem", "virtualization", "podman", "bunkerweb", "postgres", "valkey", "keycloak", "ollama", "ragflow", "langfuse"]
---
<div class="arch-badge arch-badge-strategic">
  <strong>[STRATEGIC FINANCIAL]</strong> — Cost Savings & Open-Source Sovereignty
</div>
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>

# 📦 Open-Source Containerized Stack Specifications

This guide provides a comprehensive comparison and high-fidelity container specification mapping our enterprise **AWS Secure 3-Tier Architecture** directly to its corresponding open-source, on-premises alternatives. All alternatives are packaged as rootless containers, operating under unprivileged user contexts and orchestrated natively via systemd Quadlets.

---

## 1. AWS-Native vs. On-Premises Open-Source Mapping Matrix

The table below outlines our transition framework, mapping cloud-managed services to self-hosted, sovereign container implementations.

| AWS Core Component | On-Premises Open-Source Alternative | Host Location | Deployment Context | Security & Operational Controls |
| :--- | :--- | :--- | :--- | :--- |
| **AWS ALB & WAFv2** | **BunkerWeb Edge Proxy** (Nginx-based) | VM-01 (DMZ) | Rootless Quadlet Container | Built-in ModSecurity WAF rules, automated local Let's Encrypt / CA SSL, rate-limiting, and web administrative GUI. |
| **AWS ASG Compute** | **Spring Boot 3.5.12 JVM + React 19** | VM-02 (App) | Rootless Quadlet Pod (`skm_pod`) | Hardened Ubuntu host running unprivileged JVM, SSM-equivalent terminal logging, and structured systemd metrics. |
| **Amazon RDS PostgreSQL** | **PostgreSQL 17 + pgvector** | VM-03 (DB/AI) | Rootless Quadlet Container | Volume storage mapped to physical NVMe disks, restricted VLAN 30 port access, and cron-scheduled automated backup dumps. |
| **ElastiCache Valkey** | **Valkey 7.x / 8.0** (Open Source) | VM-03 (DB/AI) | Rootless Quadlet Container | In-memory session store restricted to VLAN 20/30 ingress with forced password authentication. |
| **Amazon Bedrock & GPUs** | **Ollama** (Local Inference Model Engine) | VM-03 (DB/AI) | Rootless GPU-Passthrough Container | Secure offline execution of Qwen3 LLM and embedding models. Zero foreign network transfer. |
| **Amazon Cognito** | **Keycloak** or **Authentik** | VM-02 (App) | Rootless Quadlet Container | Managed OAuth 2.0, OpenID Connect (OIDC), active JWT generation, credential hashing, and user directory management. |
| **RAG Engine & Metrics** | **RAGFlow + Langfuse** | VM-03 (DB/AI) | Rootless Container Multi-Pod | Local OCR, semantic parsing, vector ingestion, and LLM telemetry tracking. |
| **AWS Security Hub** | **Wazuh SIEM Manager** | VM-01 (Mgmt) | Native VM / Standalone Container | Log aggregation, host configuration audits (ASIMP), and rootkit detection across all VMs. |

---

## 🛡️ 2. Architectural Deep-Dive & Quadlet Blueprints

### A. Presentation Layer Proxy: **BunkerWeb**
To replace the combined traffic filtering and TLS termination of AWS ALB and WAFv2, we utilize **BunkerWeb**. BunkerWeb is a hardened, open-source web application firewall (WAF) and reverse proxy based on Nginx.

```ini
# /home/songket/.config/containers/systemd/bunkerweb.container
[Container]
ContainerName=bunkerweb
Image=docker.io/bunkerity/bunkerweb:1.5.8
PublishPort=80:8080
PublishPort=443:8443
Volume=/var/srv/bunkerweb/data:/data:Z
Volume=/var/srv/bunkerweb/config:/etc/bunkerweb:Z
Environment=LISTEN_HTTP_PORT=8080
Environment=LISTEN_HTTPS_PORT=8443
Environment=USE_REVERSE_PROXY=yes
Environment=REVERSE_PROXY_URLS=/api/* http://10.10.20.10:8080/api/
Environment=AUTO_LETS_ENCRYPT=yes
Environment=BAD_IPS_FILTER=yes
Environment=LIMIT_REQ=yes
UserNS=keep-id:uid=2001,gid=2001

[Service]
Restart=always
```

### B. Relational Database Layer: **PostgreSQL 17**
To replicate the reliability of Amazon RDS, we run PostgreSQL 17 with the `pgvector` extension. To match the High-Availability and disaster recovery of RDS, we implement a local cron-based backup script.

```ini
# /home/songket/.config/containers/systemd/postgresql.container
[Container]
ContainerName=postgresql_db
Image=docker.io/pgvector/pgvector:0.7.0-pg17
Volume=/var/srv/postgresql/data:/var/lib/postgresql/data:Z
Environment=POSTGRES_DB=songket_db
Environment=POSTGRES_USER=songket_admin
Environment=POSTGRES_PASSWORD=SecureMasterPassword123
PublishPort=5432:5432
UserNS=keep-id:uid=2001,gid=2001

[Service]
Restart=always
```

#### 💾 The RDS-Equivalent Automated Backup Cron Script
To protect against database corruption on-premises, a local shell script is scheduled on `VM-03` via a systemd timer (or standard cron):

```bash
#!/bin/bash
# Location: /var/srv/postgresql/scripts/backup_db.sh
BACKUP_DIR="/var/srv/postgresql/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/songket_db_${TIMESTAMP}.sql.gz"

# Run pg_dump inside the unprivileged container context
podman exec postgresql_db pg_dump -U songket_admin songket_db | gzip > "${BACKUP_FILE}"

# Enforce a 30-day retention policy
find "${BACKUP_DIR}" -name "songket_db_*.sql.gz" -mtime +30 -exec rm {} \;

# Replicate the backup file to the local network-attached storage (NAS) on VLAN 30
rsync -az "${BACKUP_DIR}/" user@10.10.30.200:/mnt/nas/postgresql_backups/
```

### C. Caching Layer: **Valkey 7/8**
Valkey is deployed locally as an unprivileged, high-performance in-memory key-value cache container, providing the same session management, rate-limiting, and counter mechanisms as Amazon ElastiCache.

```ini
# /home/songket/.config/containers/systemd/valkey.container
[Container]
ContainerName=valkey_cache
Image=docker.io/valkey/valkey:8.0.0
PublishPort=6379:6379
Volume=/var/srv/valkey/data:/data:Z
UserNS=keep-id:uid=2001,gid=2001

[Service]
Restart=always
ExecStart=valkey-server --requirepass MasterValkeyPass123 --protected-mode no
```

### D. Identity & Access Layer: **Keycloak**
To replace Amazon Cognito, we deploy Keycloak inside `VM-02`. Keycloak manages the user directory, coordinates authentication tokens, signs JWT keys for Spring Boot verification, and handles OAuth 2.0 RBAC flows natively.

```ini
# /home/songket/.config/containers/systemd/keycloak.container
[Container]
ContainerName=keycloak_iam
Image=quay.io/keycloak/keycloak:24.0.5
PublishPort=8443:8443
Volume=/var/srv/keycloak/data:/opt/keycloak/data:Z
Environment=KEYCLOAK_ADMIN=admin
Environment=KEYCLOAK_ADMIN_PASSWORD=SecureAdminPassword123
Environment=KC_DB=postgres
Environment=KC_DB_URL=jdbc:postgresql://10.10.30.10:5432/songket_db
Environment=KC_DB_USERNAME=songket_admin
Environment=KC_DB_PASSWORD=SecureMasterPassword123
UserNS=keep-id:uid=2001,gid=2001

[Service]
Restart=always
ExecStart=kc.sh start-dev --http-port 8080 --https-port 8443
```

---

## 🧠 3. Sovereign local AI Processing (Ollama & RAGFlow)

Rather than calling external LLM APIs (like Amazon Bedrock or OpenAI) which sends sensitive corporate and personal data over public networks, VM-03 executes AI inferencing and retrieval locally:

1. **Ollama:** Serves as the localized inference host. It mounts NVIDIA host GPU devices (using `--device nvidia.com/gpu=all` or equivalent Podman parameters) to execute **Qwen3 (Qwen2.5-Instruct)** LLM and dense embedding indexing sweeps.
2. **RAGFlow:** Mounts local folders containing enterprise documentation, parses them semantically using specialized unprivileged OCR and parser engines, and ingests vector structures natively into the PostgreSQL `pgvector` database.
3. **Langfuse:** Captures local Spring Boot LLM transaction traces, mapping operational latency and execution cost metrics cleanly to a local database.

This complete network-isolated lifecycle guarantees absolute compliance with both PDPA data transit restrictions and the highest level of corporate IP protection.

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
