---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Enterprise Percona Server for PostgreSQL 17 on On-Premises"
timestamp: 2026-08-09T15:00:00Z
topics: ["onprem", "virtualization", "patroni", "etcd", "percona", "postgresql", "high-availability", "pgbackrest", "haproxy", "pgbouncer"]
---
<div class="arch-badge arch-badge-strategic">
  <strong>[STRATEGIC FINANCIAL]</strong> — Sovereignty, Compliance & Infrastructure Cost Control
</div>
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — Security Hardening & Platform Engineers
</div>

# 🐘 Enterprise Percona Server for PostgreSQL 17 On-Premises Setup

This guide details the high-availability (HA), enterprise-grade onsite on-premises deployment of **Percona Server for PostgreSQL 17**. It details the architectural design, clustering mechanisms, and step-by-step configurations required to achieve a resilient database platform matching or exceeding AWS RDS PostgreSQL Multi-AZ capabilities, completely isolated from external networks.

---

## 1. Executive Summary & Binary Compatibility

[Percona Server for PostgreSQL 17](https://docs.percona.com/postgresql/17/postgresql-server.html) is an enterprise-ready, open-source, binary-compatible drop-in replacement for upstream PostgreSQL 17. Because it functions identically to upstream PostgreSQL, it guarantees seamless, zero-risk migrations between the two platforms.

In addition to upstream core functionality, Percona Server introduces critical enterprise features out of the box, including:
* **Storage Manager (SMGR) API exposure:** Unlocks advanced custom storage manager integration for third-party extensions.
* **WAL Read/Write API exposure:** Enables specialized hooks into write-ahead logging.
* **`pg_tde` extension compatibility:** Allows data-at-rest encryption (Transparent Data Encryption), covering index-level and Write-Ahead Logging (WAL) encryption natively without performance degradation.
* **`pg_stat_monitor` integration:** Provides advanced query-level telemetry tracking, chronological execution plan analysis, and client metadata tracking.

---

## 2. High Availability Clustering Architecture (Patroni & etcd)

To achieve enterprise-grade resilience, we implement a highly available cluster with **Patroni** as the template/cluster management orchestrator and **etcd** as the Distributed Consensus Store (DCS). A minimum of three nodes are deployed to prevent "split-brain" scenarios and maintain quorum.

```
                           ┌─────────────────────────────────┐
                           │      BunkerWeb / Edge Proxy     │
                           └────────────────┬────────────────┘
                                            │
                                            ▼
                           ┌─────────────────────────────────┐
                           │      HAProxy Load Balancer      │
                           │   (Port 5000: Write / 5001: Read)│
                           └────────────────┬────────────────┘
                                            │
                                            │ Port 6432 (PgBouncer Pooler)
                                            ▼
                           ┌─────────────────────────────────┐
                           │    PgBouncer Connection Pooler  │
                           └────────────────┬────────────────┘
                                            │
                 ┌──────────────────────────┼──────────────────────────┐
                 │                          │                          │
                 ▼ (Write Port 5432)        ▼ (Read-Only Port 5432)    ▼ (Read-Only Port 5432)
┌───────────────────────────────┐ ┌───────────────────────────────┐ ┌───────────────────────────────┐
│     VM-03-A (Primary Node)    │ │    VM-03-B (Replica Node 1)   │ │    VM-03-C (Replica Node 2)   │
│                               │ │                               │ │                               │
│  ┌─────────────────────────┐  │ │  ┌─────────────────────────┐  │ │  ┌─────────────────────────┐  │
│  │  Percona PG v17 (R/W)   ├─┼─┼─> Percona PG v17 (R-Only) │  │ │  Percona PG v17 (R-Only) │  │
│  └───────────┬─────────────┘  │ │  └───────────┬─────────────┘  │ │  └───────────┬─────────────┘  │
│  ┌───────────▼─────────────┐  │ │  ┌───────────▼─────────────┐  │ │  ┌───────────▼─────────────┐  │
│  │   Patroni Agent         │  │ │  │   Patroni Agent         │  │ │  │   Patroni Agent         │  │
│  └───────────┬─────────────┘  │ │  └───────────┬─────────────┘  │ │  └───────────┬─────────────┘  │
│  ┌───────────▼─────────────┐  │ │  ┌───────────▼─────────────┐  │ │  ┌───────────▼─────────────┐  │
│  │   etcd Consensus Node   │  │ │  │   etcd Consensus Node   │  │ │  │   etcd Consensus Node   │  │
│  └───────────┬─────────────┘  │ │  └───────────┬─────────────┘  │ │  └───────────┬─────────────┘  │
└──────────────┼────────────────┘ └──────────────┼────────────────┘ └──────────────┼────────────────┘
               │                                 │                                 │
               └─────────────────┬───────────────┴─────────────────────────────────┘
                                 │
                                 │ WAL Archiving & Compressed Backups
                                 ▼
               ┌──────────────────────────────────────────────────┐
               │              pg_backrest Streamer                │
               └─────────────────────────┬────────────────────────┘
                                         ▼
               ┌──────────────────────────────────────────────────┐
               │            On-Premises Dedicated NAS             │
               └──────────────────────────────────────────────────┘
```

### Component Roles
1. **Patroni:** A Python-based clustering manager that configures, boots, and monitors Percona Server. It interfaces with `etcd` to maintain cluster state, dynamically configuring PostgreSQL streaming replication and triggering automated failovers when a primary goes offline.
2. **etcd:** A distributed, reliable key-value store used as the Distributed Consensus Store (DCS). It tracks node health, holds the master/leader lock key, and coordinates configuration changes across the database cluster.
3. **HAProxy:** Acts as the entrypoint load balancer, exposing a single stable entrypoint. It queries Patroni's HTTP API (port `8008`) to identify the current healthy primary node (`/primary` health check) and standby nodes (`/replica` health check), routing queries dynamically.
4. **PgBouncer:** Lightweight connection pooler deployed on top of PostgreSQL to handle thousands of concurrent application connections, minimizing memory consumption.
5. **pg_backrest:** An enterprise-grade, block-level backup utility executing compressed, parallel backups directly to our local on-premises network-attached storage (NAS).

---

## 3. High-Fidelity Configuration Blueprints

Deploying this stack within our unprivileged rootless container context requires detailed Quadlets and custom configurations on **VM-03**.

### A. The DCS Consensus Engine: `etcd.container`
Deploy `etcd` inside an unprivileged container namespace on each of the three database virtual machines to form a resilient quorum.

```ini
# /home/songket/.config/containers/systemd/etcd.container
[Container]
ContainerName=etcd_node
Image=quay.io/coreos/etcd:v3.5.12
PublishPort=2379:2379
PublishPort=2380:2380
Volume=/var/srv/etcd/data:/etcd-data:Z
UserNS=keep-id:uid=2001,gid=2001
Environment=ETCD_NAME=etcd-01
Environment=ETCD_INITIAL_LISTEN_PEER_URLS=http://0.0.0.0:2380
Environment=ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379
Environment=ETCD_INITIAL_ADVERTISE_PEER_URLS=http://10.10.30.11:2380
Environment=ETCD_ADVERTISE_CLIENT_URLS=http://10.10.30.11:2379
Environment=ETCD_INITIAL_CLUSTER=etcd-01=http://10.10.30.11:2380,etcd-02=http://10.10.30.12:2380,etcd-03=http://10.10.30.13:2380
Environment=ETCD_INITIAL_CLUSTER_TOKEN=etcd-songket-token
Environment=ETCD_INITIAL_CLUSTER_STATE=new

[Service]
Restart=always
```

### B. The Patroni Orchestrated Percona Server: `patroni-percona.container`
Patroni is packaged inside a custom image containing Percona Server for PostgreSQL 17, `pg_backrest`, and Patroni binaries.

```ini
# /home/songket/.config/containers/systemd/patroni-percona.container
[Container]
ContainerName=patroni_postgresql
Image=docker.io/percona/percona-postgresql-patroni:17
PublishPort=5432:5432
PublishPort=8008:8008
Volume=/var/srv/postgresql/data:/var/lib/postgresql/data:Z
Volume=/var/srv/postgresql/config:/etc/patroni:Z
UserNS=keep-id:uid=2001,gid=2001
Environment=PATRONI_CONFIGURATION_FILE=/etc/patroni/patroni.yml

[Service]
Restart=always
```

#### The Cluster Orchestration File: `patroni.yml`
```yaml
# /var/srv/postgresql/config/patroni.yml
scope: songket-cluster
namespace: /service
name: pg-node-01

etcd3:
  hosts:
    - 10.10.30.11:2379
    - 10.10.30.12:2379
    - 10.10.30.13:2379

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.10.30.11:8008

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        shared_buffers: 16GB
        work_mem: 64MB
        maintenance_work_mem: 2GB
        max_connections: 500
        shared_preload_libraries: 'pg_stat_statements,pg_stat_monitor,pg_tde'
        archive_mode: "on"
        archive_command: "pgbackrest --stanza=songket-db archive-push %p"

  init:
    pg_hba:
      - host replication replicator 10.10.30.0/24 md5
      - host all all 0.0.0.0/0 md5

  users:
    admin:
      password: SecureMasterPassword123
      options:
        - superuser
        - createdb

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.10.30.11:5432
  data_dir: /var/lib/postgresql/data/songket-cluster
  bin_dir: /usr/lib/postgresql/17/bin
  pgpass: /home/songket/.pgpass
  authentication:
    replication:
      username: replicator
      password: SecureReplicationPassword123
    superuser:
      username: postgres
      password: SecurePostgresPassword123

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
  nosync: false
```

### C. Traffic Routing Layer: `haproxy.container`
Exposes the single VIP entrypoint for application compute nodes, dynamically selecting active primaries or passive replicas using Patroni's HTTP endpoint.

```ini
# /home/songket/.config/containers/systemd/haproxy.container
[Container]
ContainerName=haproxy_loadbalancer
Image=docker.io/library/haproxy:2.8
PublishPort=5000:5000
PublishPort=5001:5001
Volume=/var/srv/haproxy/config:/usr/local/etc/haproxy:Z
UserNS=keep-id:uid=2001,gid=2001

[Service]
Restart=always
```

#### Routing Configuration: `haproxy.cfg`
```haproxy
# /var/srv/haproxy/config/haproxy.cfg
global
    maxconn 4096

defaults
    mode tcp
    timeout connect 5s
    timeout client 30m
    timeout server 30m

# Port 5000: Write-only routing to the active primary node
frontend write_pool
    bind 0.0.0.0:5000
    default_backend primary_pg_cluster

backend primary_pg_cluster
    option httpchk GET /primary
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server pg-node-01 10.10.30.11:5432 maxconn 500 check port 8008
    server pg-node-02 10.10.30.12:5432 maxconn 500 check port 8008
    server pg-node-03 10.10.30.13:5432 maxconn 500 check port 8008

# Port 5001: Read-only load-balanced routing to replica standby nodes
frontend read_pool
    bind 0.0.0.0:5001
    default_backend standby_pg_cluster

backend standby_pg_cluster
    balance roundrobin
    option httpchk GET /replica
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
    server pg-node-01 10.10.30.11:5432 maxconn 500 check port 8008
    server pg-node-02 10.10.30.12:5432 maxconn 500 check port 8008
    server pg-node-03 10.10.30.13:5432 maxconn 500 check port 8008
```

---

## 4. Disaster Recovery & pg_backrest On-Premises Strategy

To achieve a **Zero-Data-Loss RPO** and match the backup standard of Amazon RDS, we utilize **pg_backrest**. pg_backrest performs point-in-time recovery (PITR) by continuously streaming Write-Ahead Logs (WAL) and executing compressed, parallel backups.

### The Backup Configuration: `pgbackrest.conf`
```ini
# /etc/pgbackrest/pgbackrest.conf
[global]
repo1-path=/mnt/nas/pgbackrest
repo1-retention-full=4
repo1-retention-diff=6
process-max=4
log-level-console=info
log-level-file=detail
compress-type=lz4
compress-level=3

[songket-db]
pg1-path=/var/lib/postgresql/data/songket-cluster
pg1-user=postgres
```

### Automated Backup Pipeline Playbook
Backup scheduling is automated on-premises via standard crontab or Ansible task schedulers:

```bash
# Full Backup every Sunday at 01:00 AM local time (MYT)
00 01 * * 0 podman exec patroni_postgresql pgbackrest --stanza=songket-db --type=full backup

# Incremental Backup every daily at 01:00 AM MYT
00 01 * * 1-6 podman exec patroni_postgresql pgbackrest --stanza=songket-db --type=incr backup
```

---

## 5. Security & Isolation Controls

Operating an enterprise database on-premises demands rigid logical boundaries and hardening steps conforming with **Bank Negara Malaysia guidelines** and the **Malaysian Personal Data Protection Act (PDPA) 2010**:

1. **VLAN Segmentation:** The database VMs (VLAN 30) are blocked from communicating with the outer DMZ (VLAN 10). Incoming connections must originate strictly from VLAN 20 (Application servers VM-02) or dedicated database replica IPs.
2. **mTLS Encryption:** All inter-node cluster replication traffic (PostgreSQL streaming) and consensus coordination (Patroni-to-etcd) are encrypted using locally generated, self-signed CA certificates mapped inside the unprivileged container volumes.
3. **Transparent Data Encryption (TDE):** Utilizing Percona's unique **`pg_tde`** extension, all Write-Ahead Logs (WAL) and data block pages are encrypted on disk. This protects customer personal identifiable information (PII) from physical disk theft or hypervisor compromises.

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
