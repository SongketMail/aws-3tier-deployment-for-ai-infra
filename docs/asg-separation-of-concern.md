---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "Auto Scaling Groups (ASGs) & Separation of Concerns"
timestamp: 2026-08-05T21:48:38Z
topics: ["aws", "cloud", "architecture", "vpc", "alb", "asg", "rds", "ssl", "disaster-recovery", "efs", "postgresql", "gpu", "ragflow", "langfuse"]
---
# Auto Scaling Groups (ASGs) & Separation of Concerns

In a modern cloud-native architecture, managing complex applications requires balancing scalability, security, cost, and operational maintenance. This document explores the architectural rationale for using **Separation of Concerns (SoC)** via distinct Auto Scaling Groups (ASGs) and provides an exhaustive guide on how to handle shared storage (**Amazon S3**, **Amazon EFS**, or both) to enable seamless, stateless autoscaling.

---

## 1. Separation of Concerns (SoC) via Dedicated ASGs

Using a single, monolithic fleet of EC2 instances to run multiple, diverse components of your application (e.g., Frontend, Backend, and AI Processing Tiers) creates tight coupling, increases the blast radius of failures, and complicates scaling.

By defining **distinct Auto Scaling Groups** for each logical application tier (e.g., an ASG for Server 01: Nginx/Frontend, an ASG for Server 02: Backend + DMS, and an ASG for Server 03: RAGFlow + AI Processing), you achieve robust Separation of Concerns.

### Architectural Advantages of Multi-ASG Layouts

1. **Independent Elastic Scaling:**
   - **Different Resource Triggers:** Frontend layers scale based on network load or request counts, Backend layers scale based on CPU or memory, and AI layers (RAGFlow/LangFuse) scale based on custom metrics like GPU utilization or task queue length.
   - **Cost Optimization:** You don't need to scale expensive, heavy instances (e.g., Graviton `t4g.xlarge` with 16GB RAM) just because the simple web server/reverse proxy layer is experiencing high traffic. Only scale the specific layer under load.
2. **Blast Radius Limitation:**
   - If a memory leak or heavy computation in the AI tier (Server 03) crashes an instance, the Nginx web tier (Server 01) and the core Backend tier (Server 02) remain completely operational, allowing you to return graceful degraded responses to users.
3. **Least Privilege Security (IAM Roles & Security Groups):**
   - Each ASG is equipped with its own dedicated **IAM Instance Profile**. The Backend ASG can have permission to read from specific database parameter stores, whereas the AI ASG can have exclusive read/write access to S3 training buckets.
   - Security Groups can be strictly chained: the Frontend ASG security group only accepts traffic from the ALB; the Backend ASG security group only accepts traffic from the Frontend ASG; the Database and AI tiers are accessible only by the Backend ASG.
4. **Decoupled Deployments & Rolling Updates:**
   - Code updates to the RAGFlow AI stack can be rolled out as a rolling update to the AI ASG (via Instance Refresh) without causing a single millisecond of downtime or disruption to the core Backend and Frontend layers.

---

## 2. Statelessness: The Core Prerequisite of ASGs

The foundational rule of Auto Scaling is **statelessness**.
Because ASG instances are automatically launched, terminated, and replaced during scaling events (scale-out, scale-in, or health-check replacements), **no persistent state should ever reside directly on an instance's local root disk (EBS).**

If an application writes files (e.g., user profile pictures, uploaded documents for RAG processing, temporary cached AI model weights) directly to the local filesystem of an EC2 instance, those files will be:
- **Inaccessible** to other instances in the ASG (causing HTTP 404 errors when a load balancer routes subsequent requests to a different instance).
- **Permanently lost** when the specific instance scale-in or gets replaced due to a failed health check.

To solve this, you must decouple your compute tier (ASG) from your storage tier. This brings us to the core decision: **Amazon S3, Amazon EFS, or both?**

---

## 3. The Critical Role of AWS Application Load Balancer (ALB) for ASGs

While Auto Scaling Groups (ASGs) manage the lifecycle, elasticity, and count of compute instances, they cannot work in isolation. The **Application Load Balancer (ALB)** serves as the orchestrator and gateway, acting as the bridge between external incoming client traffic and the highly dynamic, ephemeral instances managed by the ASG.

### Key Architectural Advantages of the ALB-ASG Integration

#### 1. Abstraction of Ephemeral IP Addresses (Single Entry Point)
Instances inside an ASG are ephemeral by design. During auto-scaling scale-out/scale-in events, or when an instance is replaced due to an unhealthy status check, the instance is terminated and a new one is launched. This results in constantly changing, dynamic IP addresses.
* **The ALB Solution:** The ALB provides a single, high-availability DNS name (e.g., `production-alb-12345678.ap-southeast-5.elb.amazonaws.com`) mapped via Route53 alias records (e.g., `app.linuxmalaysia.com`). Clients only ever target the ALB, and the ALB automatically handles routing to the exact private IP addresses of the currently running ASG instances, abstracting all backend churn from the user.

#### 2. Dynamic Target Registration and Connection Draining (Zero Packet Loss)
As the ASG scales, instances come and go dynamically.
* **Target Registration:** When a new instance launches in the ASG, the ASG automatically registers its IP address with the associated ALB **Target Group** (`target_group_arns`). Once the instance passes initial health checks, the ALB starts sending traffic to it.
* **Connection Draining (Deregistration Delay):** When the ASG scales in or triggers a rolling update, instances are not terminated abruptly. The ALB initiates a **Deregistration Delay** (connection draining) period. During this time, the ALB stops routing *new* client requests to the deregistering instance, but allows active, in-flight HTTP requests to finish processing. Once all in-flight connections are complete or the timeout is reached, the instance is safely terminated with zero client-side aborted requests.

#### 3. Active Health-Check Monitoring and Auto-Healing Delegation
By default, an ASG only monitors hardware-level EC2 Status Checks (hypervisor status, CPU hardware, host power). If your application layer (e.g., your Spring Boot application, Nginx, or RAGFlow) hangs, deadlocks, runs out of memory, or crashes, the VM still appears "running" and the basic EC2 check passes.
* **The ALB Solution:** By setting the ASG's `health_check_type` to **"ELB"** (Elastic Load Balancing), you delegate the auto-healing logic to the ALB.
* **How it works:** The ALB continuously probes the application’s web port (e.g., checking `/` or `/health`) at configured intervals. If the application on a specific instance fails to respond with a successful HTTP code (e.g. returns 500, or times out) for the configured `unhealthy_threshold`, the ALB flags the instance as unhealthy and stops routing traffic to it. The ASG detects this unhealthy status and automatically terminates the failed instance, launching a fresh, healthy one in its place.

#### 4. SSL/TLS Termination and Offloading
Managing SSL/TLS certificates and handling the cryptographic overhead of encrypting and decrypting HTTPS connections at individual EC2 instances is computationally expensive and operationally complex.
* **The ALB Solution:** The ALB integrates natively with **AWS Certificate Manager (ACM)**, allowing SSL certificates to be terminated directly at the load balancer level. Traffic is decrypted at the ALB and forwarded securely via private subnets to the ASG instances. This offloads cryptographic workloads from the EC2 instances, freeing up 100% of their CPU resources to focus on executing application logic, database operations, or resource-heavy AI RAG model inference.

#### 5. Security Group Chaining and Network Isolation
For enterprise security, compute instances running backend APIs and AI tools should never be exposed directly to the public internet.
* **The ALB Solution:** Using the ALB, we place our ASG instances inside **fully private subnets** without public IP addresses.
* **Security Group Chaining:** We configure the ASG Security Group to only accept inbound traffic on the application port (e.g., Port 80, 5000, or 8000) from the specific **ALB Security Group**. All direct public access is physically blocked at the network boundary, forcing all traffic to pass through the ALB's centralized, inspected, and controlled entry point.

#### 6. Host-Based and Path-Based Routing (Powering SoC)
Instead of provisioning separate expensive load balancers for each tier of our architecture, a single shared Application Load Balancer can orchestrate routing rules to separate, specialized target groups.
* **The ALB Solution:** We can define listener rules on a single ALB to direct traffic dynamically:
  - Traffic to `app.linuxmalaysia.com/` is routed to the **Nginx/Frontend ASG Target Group**.
  - Traffic to `app.linuxmalaysia.com/api/*` is routed to the **Backend ASG Target Group**.
  - Traffic to `app.linuxmalaysia.com/rag/*` is routed to the **AI RAGFlow ASG Target Group**.
This single-ALB multi-ASG integration allows us to keep our layers decoupled, scale each tier independently, and enforce strict Separation of Concerns while maintaining a lean and highly cost-optimized infrastructure.

---

## 4. Storage Guide: Amazon S3 vs. Amazon EFS

To handle data across auto-scaling instances, AWS offers two primary shared storage options. Understanding when to use each—or combining them in a hybrid layout—is critical to a high-performing architecture.

### Option A: Amazon S3 (Simple Storage Service)
Amazon S3 is a highly durable, virtually infinite, secure, and cost-effective **object storage service** designed for cloud-native applications.

* **How it works:** Files (objects) are accessed and manipulated directly via HTTP/HTTPS REST API calls (typically using AWS SDKs or the AWS CLI) rather than traditional filesystem commands (like `open()`, `write()`, or `seek()`).
* **Best suited for:**
  - Modern, stateless, cloud-native applications.
  - User-facing uploads (e.g., images, PDFs, videos).
  - Raw data source files before they are ingested, chunked, and embedded into vector databases by AI services like RAGFlow.
  - Long-term backups, application logs, and database snapshots.
* **Pros:**
  - **Incredible Scalability:** Handles millions of concurrent requests effortlessly.
  - **Unmatched Durability:** Designed for 99.999999999% (11 9s) of durability.
  - **Low Cost:** Very inexpensive compared to standard filesystems ($0.023 per GB/month for standard, even lower for intelligent tiering/infrequent access).
  - **Global Delivery Integration:** Seamlessly integrates with Amazon CloudFront CDN for global low-latency asset delivery.
* **Cons:**
  - **Non-POSIX Compliant:** You cannot "mount" S3 as a traditional directory and perform standard file writes/appends in legacy code without utility layers (like Mountpoint for Amazon S3), which have limitations on write patterns.

### Option B: Amazon EFS (Elastic File System)
Amazon EFS is a fully-managed, serverless, POSIX-compliant **network filesystem (NFSv4)** designed to be mounted concurrently by hundreds of EC2 instances across multiple Availability Zones.

* **How it works:** EFS is mounted over the network (port 2049) to a local directory on your EC2 instances. To the operating system, it looks and behaves exactly like a standard local directory.
* **Best suited for:**
  - Legacy or commercial off-the-shelf (COTS) software that expects a standard filesystem path (e.g., `/var/www/uploads` or `/opt/app/data`) and cannot easily be modified to use an AWS SDK.
  - Shared directories requiring low-latency read-write concurrency across multiple compute instances simultaneously.
  - **AI Model Cache:** Sharing large pre-trained AI models or embedding files (e.g., Hugging Face model caches, SentenceTransformers weights) across your RAGFlow/AI ASG instances. Mounting EFS prevents instances from having to download multi-gigabyte files from S3 or external hubs during a scale-out bootstrap, significantly accelerating launch speed.
* **Pros:**
  - **POSIX Compliant:** Supports full directory structures, file permissions (UID/GID), and standard file system tools (`tar`, `gzip`, `grep`).
  - **Elastic Capacity:** Scales automatically up to petabytes without manual provisioning; you only pay for what you use.
  - **Multi-AZ Availability:** Built-in replication across multiple AZs.
* **Cons:**
  - **Higher Cost:** Significantly more expensive than S3 ($0.30 per GB/month for standard SSD storage, though lifecycle policies can tier unused data to lower-cost tiers).
  - **I/O Overhead:** Network filesystem overhead means file read/write latencies are higher than local SSDs (EBS) or highly-optimized API calls.

---

## 5. Architectural Comparison Table

| Feature | Amazon S3 (Object Storage) | Amazon EFS (Network File System) |
| :--- | :--- | :--- |
| **Primary Protocol** | HTTP / HTTPS (REST API) | NFSv4 (TCP Port 2049) |
| **POSIX Support** | No (requires custom SDK or client) | Yes (standard directory, file permissions, file locking) |
| **Scalability** | Virtually infinite; high concurrent request throughput | Automatic capacity scaling; scales throughput with size |
| **Typical Ingress Cost** | Free inbound; $0.023/GB/month (Standard) | $0.30/GB/month (Standard Storage) |
| **Access Latency** | Tens of milliseconds | Single-digit milliseconds (metadata operations can be slower) |
| **Direct Web Serving** | Yes (via CloudFront / S3 Public endpoints) | No (must traverse an EC2 instance/web server) |
| **Mounting on EC2** | Direct SDK integration preferred (or Mountpoint utility) | Standard Linux `mount` command via `amazon-efs-utils` |
| **Best AWS ASG Case** | Storing user uploads, large datasets, and logs | Shared AI model weight caches, shared configuration directories |

---

## 6. The Verdict: Do we need EFS, S3, or Both?

For most modern AWS architectures utilizing Auto Scaling Groups, **using Both in a hybrid design is the industry best practice.** They are not mutually exclusive, but rather complementary.

Here is the architectural distribution for our secure 3-tier layout:

```
                            ┌──────────────────────────────────────┐
                            │    Application Load Balancer (ALB)   │
                            └──────────────────┬───────────────────┘
                                               │
               ┌───────────────────────────────┴──────────────────────────────┐
               ▼                                                              ▼
 ┌───────────────────────────┐                                  ┌───────────────────────────┐
 │   ASG Tier 2: Backend     │                                  │     ASG Tier 3: AI Stack  │
 │  (Stateless Compute)      │                                  │   (RAGFlow + LangFuse)    │
 └─────────────┬─────────────┘                                  └─────────────┬─────────────┘
               │                                                              │
               │ (SDK API Read/Write)                                         │ (Mount /mnt/efs)
               ▼                                                              ▼
 ┌───────────────────────────┐                                  ┌───────────────────────────┐
 │     Amazon S3 Bucket      │                                  │  Amazon EFS File System   │
 │                           │                                  │                           │
 │ • Static Assets           │                                  │ • AI Model Weight Cache   │
 │ • User Document Uploads   │                                  │ • Shared App Configs      │
 │ • System Logs & Backups   │                                  │ • POSIX Temp File Storage │
 └───────────────────────────┘                                  └───────────────────────────┘
```

### When to use S3 for Auto Scaling:
- **Stateless Web Files:** All user uploads (e.g., PDFs sent to the DMS or RAG system) must be directed immediately to an Amazon S3 Bucket. When a user uploads a document, the Backend API processes it, writes the raw file to S3, and records the metadata (such as the S3 Object URL) in the **RDS PostgreSQL Database**.
- **Scale-Out Safety:** When a new instance boots up inside the ASG, it doesn't need to copy legacy user data. It simply calls S3 URLs on demand.

### When to use EFS for Auto Scaling:
- **Accelerating Scale-Out (The Bootstrapping Problem):** If your RAGFlow AI service requires a 4GB language model to process requests, downloading this model from S3 or Hugging Face during a scale-out operation can take several minutes. This severely delays your auto-scaling response. By storing the model weights inside a shared EFS directory (mounted as `/mnt/models`), any newly launched AI instance can read the models instantly from EFS, reducing scaling boot times from 10 minutes to under 60 seconds.
- **Shared Working Workspace:** If multiple nodes in the AI ASG must cooperate on batch processing files and require immediate POSIX write access.

---

## 7. Implementation and Configuration Guide

To implement EFS and S3 storage within your Auto Scaling Groups, configure the following AWS parameters.

### 7.1 Configuring S3 Integration for ASGs

To allow instances in your ASG to read and write to an S3 bucket securely:

1. **Do NOT use static AWS Access Keys.** Instead, attach an IAM Policy to your ASG instance role:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "s3:GetObject",
                   "s3:PutObject",
                   "s3:ListBucket"
               ],
               "Resource": [
                   "arn:aws:s3:::my-application-storage-bucket",
                   "arn:aws:s3:::my-application-storage-bucket/*"
               ]
           }
       ]
   }
   ```
2. **Launch Template User Data Integration:**
   In your launch template, you can download startup assets or configurations using the AWS CLI:
   ```bash
   #!/bin/bash
   # Update and install AWS CLI
   dnf update -y
   dnf install -y awscli

   # Download environment secrets or application configuration from S3
   mkdir -p /etc/myapp
   aws s3 cp s3://my-application-storage-bucket/config/config.json /etc/myapp/config.json
   ```

---

### 7.2 Configuring EFS Integration for ASGs

To mount an EFS volume automatically on launch across multiple AZs:

1. **Security Group Configuration:**
   - Create an **EFS Security Group** (`sg-efs`).
   - Allow **Inbound TCP Port 2049 (NFS)** from your **ASG Security Group** (`sg-asg`).
2. **Deploy Mount Targets:**
   - In your OpenTofu/Terraform code, deploy EFS Mount Targets (`aws_efs_mount_target`) in **each private application subnet** within your VPC.
3. **Launch Template User Data Mounting:**
   Use the following script within your ASG's Launch Template `user_data` to install dependencies and mount EFS securely using TLS:
   ```bash
   #!/bin/bash
   # Install EFS mounting utilities (standard in Amazon Linux 2023)
   dnf install -y amazon-efs-utils

   # Define EFS Target Directory
   MOUNT_DIR="/mnt/efs"
   mkdir -p $MOUNT_DIR

   # Mount using EFS File System ID (Enable TLS for encryption in-transit)
   # Replace fs-xxxxxx with your actual EFS ID
   mount -t efs -o tls fs-xxxxxx:/ $MOUNT_DIR

   # Ensure the mount is persistent across potential reboots
   echo "fs-xxxxxx:/ /mnt/efs efs _netdev,tls,defaults 0 0" >> /etc/fstab
   ```

---

## 8. Cost-Optimization Best Practices

When leveraging S3 and EFS alongside ASGs, implement these practices to minimize operational costs:

1. **EFS Lifecycle Management:** Set EFS Lifecycle policies to automatically move files that haven't been accessed in 14 or 30 days to **EFS Infrequent Access (IA)** or **EFS Archive**. This can reduce EFS storage costs by up to 90%.
2. **S3 Intelligent-Tiering:** Enable S3 Intelligent-Tiering on your buckets. This automatically moves files between frequent, infrequent, and archive access tiers based on real-time usage patterns, without any performance overhead or administrative management.
3. **Mountpoint for Amazon S3:** For large read-heavy file access patterns (like streaming static training datasets to AI nodes), evaluate AWS's official `Mountpoint for Amazon S3` as a high-throughput, lower-cost alternative to mounting EFS.
