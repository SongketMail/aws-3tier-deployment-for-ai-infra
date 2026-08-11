---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "On-Premises Infrastructure with Ansible"
timestamp: 2026-08-09T15:00:00Z
topics: ["onprem", "virtualization", "ansible", "fqcn", "gitea", "ara", "semaphore"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>
<div class="arch-badge arch-badge-security">
  <strong>[SECURITY & COMPLIANCE]</strong> — Infrastructure Audit & SecOps Teams
</div>

# 🤖 On-Premises Infrastructure Management with Ansible

This guide establishes the automation standards for configuring our local host VMs and deploying containerized applications. It details our symmetric privilege separation, Fully Qualified Collection Names (FQCN) guidelines, and our local self-hosted CI/CD pipeline integrated with **Gitea**, **Ansible Semaphore**, and **Ansible ARA**.

---

## 🛡️ 1. Symmetric Privilege Separation Strategy

To enforce the principle of least privilege, our Ansible playbooks separate global administrative server configuration from unprivileged container operations.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      SYMMETRIC PRIVILEGE PIPELINE                      │
│                                                                        │
│ ┌──────────────────────┐ become: yes                                   │
│ │ 1. Rootful Hardening │ ──► Installs Podman, enables sysctl tuning,   │
│ │      (Root Sudo)     │     creates user songket (UID 2001)           │
│ └──────────────────────┘                                               │
│                                                                        │
│ ┌──────────────────────┐ become_user: songket                          │
│ │  2. Rootless Deploy  │ ──► Templates systemd Quadlet files, reloads   │
│ │     (User Space)     │     user daemon, restarts rootless pod services│
│ └──────────────────────┘                                               │
└────────────────────────────────────────────────────────────────────────┘
```

Below is a production playbook template displaying this symmetric separation:

```yaml
---
# Location: playbooks/deploy_onprem_services.yml
- name: Phase 1 - Rootful Host Hardening and Environment Prep
  hosts: onprem_servers
  become: yes
  vars:
    songket_user: "songket"
    songket_uid: 2001

  tasks:
    - name: Ensure podman and systemd utilities are installed
      ansible.builtin.apt:
        name:
          - podman
          - dbus-user-session
          - python3-pip
        state: present
        update_cache: yes

    - name: Create non-root service group
      ansible.builtin.group:
        name: "{{ songket_user }}"
        gid: "{{ songket_uid }}"
        state: present

    - name: Create non-root service account
      ansible.builtin.user:
        name: "{{ songket_user }}"
        uid: "{{ songket_uid }}"
        group: "{{ songket_user }}"
        shell: /bin/bash
        state: present

    - name: Enable systemd lingering for service user
      ansible.builtin.command:
        cmd: "loginctl enable-linger {{ songket_user }}"
        creates: "/var/lib/systemd/linger/{{ songket_user }}"

- name: Phase 2 - Rootless Application Deployment (Unprivileged)
  hosts: onprem_servers
  become: yes
  become_user: songket
  vars:
    songket_uid: 2001

  tasks:
    - name: Create user-level systemd Quadlet directory
      ansible.builtin.file:
        path: "/home/songket/.config/containers/systemd"
        state: directory
        owner: songket
        group: songket
        mode: '0755'

    - name: Deploy application container Quadlet specification
      ansible.builtin.template:
        src: "templates/emailserver.container.j2"
        dest: "/home/songket/.config/containers/systemd/emailserver.container"
        owner: songket
        group: songket
        mode: '0644'
      register: quadlet_config

    - name: Reload user-level systemd daemon and apply changes
      ansible.builtin.systemd_service:
        daemon_reload: yes
        scope: user
        name: emailserver.service
        state: restarted
        enabled: yes
      environment:
        XDG_RUNTIME_DIR: "/run/user/{{ songket_uid }}"
        DBUS_SESSION_BUS_ADDRESS: "unix:path=/run/user/{{ songket_uid }}/bus"
      when: quadlet_config.changed
```

---

## 🛠️ 2. Core Ansible Engine Optimization (`ansible.cfg`)

For rapid execution over complex multi-VLAN architectures, our baseline `ansible.cfg` configures low-level network and logging overrides:

- **SSH Pipelining:** Enabled under `[ssh_connection]` to execute multiple modules sequentially without reclaiming SSH sessions, reducing task latency by over **60%**.
- **YAML Callback:** Configured as `stdout_callback = yaml` to render structured, human-readable console outputs.

```ini
# Location: ansible.cfg
[defaults]
inventory = ./inventory/hosts.ini
stdout_callback = yaml
callbacks_enabled = ansible.posix.profile_tasks, ara_default
host_key_checking = False

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
```

---

## 🔗 3. Self-Hosted Deployment Pipeline Orchestration

To avoid external network calls, our entire delivery workflow is integrated using local self-hosted open-source software tools:

```
 ┌──────────────┐          ┌─────────────────────┐          ┌─────────────┐
 │  Local Gitea │  ──────► │  Ansible Semaphore  │  ──────► │ Ansible ARA │
 │ (VCS & Push) │ (Webhook)│ (Task Execution UI) │ (Callback)│ (Audit Log) │
 └──────────────┘          └─────────────────────┘          └─────────────┘
```

### A. Private Version Control Server: **Gitea**
- **Role:** Private Git server deployed in a local rootless container on VM-01.
- **Workflow:** Stores infrastructure-as-code repositories containing Ansible playbooks, roles, inventory configurations, and Quadlet templates.
- **Trigger:** Configured with a Gitea Git hook that invokes a secure HTTP webhook on Ansible Semaphore when modifications are pushed to the `main` branch.

### B. Lightweight Web Orchestrator: **Ansible Semaphore**
- **Role:** A responsive, lightweight, open-source web interface that serves as a direct alternative to AWX/Ansible Tower.
- **Workflow:**
  - Retrieves SSH deployment keys from a secure local credential store.
  - Automatically pulls the verified Ansible playbooks from Gitea.
  - Executes playbooks across target host VMs (`VM-01`, `VM-02`, `VM-03`) using role-based access control (RBAC).
  - Renders real-time play logs to administrators and security auditors.

### C. Compliance Auditor & Recorder: **Ansible ARA**
- **Role:** Record Ansible executions transparently into a private database, serving a beautiful searchable Web UI (`ara-web`).
- **Configuration:** Integrated as a callback plugin inside `ansible.cfg` (via `callbacks_enabled = ara_default`).
- **Workflow:**
  - Records the exact parameters of every task executed.
  - Logs environment variables, target hosts, success/failure parameters, and file changes.
  - Provides compliance teams with high-fidelity, permanent visual audits of all configuration actions, eliminating "configuration drift" troubleshooting overhead.

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
