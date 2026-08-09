---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Persistent EFS Storage & GitLab CI/CD"
timestamp: 2026-08-09T14:00:00Z
topics: ["devops", "engineering", "runbook", "efs", "gitlab", "nginx"]
---
<div class="arch-badge arch-badge-devops">
  <strong>[DEVOPS EXECUTION]</strong> — Systems Engineers & SREs
</div>

# 🛠️ Persistent EFS Storage & GitLab CI/CD

This runbook details how to configure **Amazon EFS (Elastic File System)** shared persistent storage, mount it on Auto Scaling Groups (ASG) and standalone instances, tune Nginx performance, and integrate shared storage with **GitLab CI/CD pipelines**.

---

## 💾 1. Mounting Amazon EFS on Boot

To share AI model weights, static media, and application configurations across multiple compute nodes in our private subnets, we mount Amazon EFS natively via standard NFSv4 parameters.

### 🛠️ Shell Mount Script (user_data.sh)
The script below automates EFS directory provisioning and updates `/etc/fstab` to ensure mounts persist across instance reboots:

```bash
#!/usr/bin/env bash
# Location: scripts/user_data.sh

# Strict error handling
set -Eeuo pipefail

EFS_ID="fs-0123456789abcdef0" # Replace with target EFS ID from OpenTofu outputs
MOUNT_POINT="/var/www/shared"
REGION="ap-southeast-5"

echo "Installing NFS client utilities..."
sudo apt-get update -y
sudo apt-get install -y nfs-common binutils

echo "Creating persistent mount point..."
sudo mkdir -p "${MOUNT_POINT}"

echo "Mounting Amazon EFS filesystem..."
# Mount utilizing standard recommended NFS options
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport "${EFS_ID}.efs.${REGION}.amazonaws.com:/" "${MOUNT_POINT}"

echo "Adding EFS to /etc/fstab for boot persistence..."
echo "${EFS_ID}.efs.${REGION}.amazonaws.com:/ /var/www/shared nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0" | sudo tee -a /etc/fstab

echo "Verifying active mount..."
df -h | grep "${MOUNT_POINT}"
```

---

## ⚡ 2. Nginx Metadata Performance Tuning

Mounting a network-attached filesystem like EFS introduces file metadata lookup latency. To prevent Nginx from stalling while serving files from the shared EFS directories, SREs must configure metadata caching inside Nginx:

```nginx
# Location: /etc/nginx/nginx.conf
http {
    # Cache open file descriptors, size, and modifications
    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    server {
        listen 80;
        server_name secure-app.songketmail.github.io;

        location /assets/ {
            root /var/www/shared;
            expires 7d;
            add_header Cache-Control "public, no-transform";
        }
    }
}
```

---

## 🔄 3. GitLab CI/CD Shared Storage Integration

Our GitLab CI/CD runner is deployed on a dedicated standalone instance and mounts the same persistent EFS volume. When developers commit new AI models or frontend static builds, the pipeline builds the assets and copies them directly into the EFS mount, making them immediately available across all private Auto Scaling nodes!

```yaml
# Location: .gitlab-ci.yml
stages:
  - build
  - deploy

build_assets:
  stage: build
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/

deploy_to_efs:
  stage: deploy
  script:
    - echo "Deploying compiled artifacts to persistent shared EFS mount..."
    - cp -r dist/* /var/www/shared/assets/
    - echo "Assets deployed successfully!"
  only:
    - main
```

---

*Deep State of Mind (DSOM) | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
