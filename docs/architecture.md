# System Architecture

This document describes the high-availability 3-tier network topology, AWS component layouts, and routing architectures deployed by this Terraform project.

---

## Architectural Schematic

```
                      [ INTERNET ]
                           │
                           ▼
                     [ AWS WAFv2 ]   <-- (OWASP Top 10 + IP Rate Limiting)
                           │
                           ▼
             [ Application Load Balancer ]  <-- (Public Subnets)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      [ ASG EC2 Instance ]       [ ASG EC2 Instance ]  <-- (Private App Subnets)
             │                           │
             └─────────────┬─────────────┘
                           ▼
                 [ Multi-AZ RDS DB ]        <-- (Private Database Subnets)
```

---

## Network Isolation Layers

### 1. Presentation / Web Layer (Public Subnets)
- **Subnets:** `10.0.1.0/24` (AZ `ap-southeast-5a`) and `10.0.2.0/24` (AZ `ap-southeast-5b`).
- **Description:** Host public-facing services. This layer routes inbound internet traffic directly through the Internet Gateway (IGW).
- **Resources:**
  - **Application Load Balancer (ALB):** Terminates and routes incoming connections.
  - **NAT Gateways:** Deployed in each public subnet to provide highly resilient outbound internet access for private instances.
  - **AWS WAFv2 Web ACL:** Directly attached to the ALB to block bad actors at the edge.

### 2. Application Layer (Private Subnets)
- **Subnets:** `10.0.10.0/24` (AZ `ap-southeast-5a`) and `10.0.11.0/24` (AZ `ap-southeast-5b`).
- **Description:** Holds business and compute logic. Instances have no public IP addresses and cannot be accessed directly from the internet.
- **Resources:**
  - **Auto Scaling Group (ASG) EC2 Instances:** Hosts the application code (Nginx web service). Outbound requests (such as API calls or package updates) are routed securely through the Public Layer's NAT Gateways.

### 3. Database Layer (Isolated Private Subnets)
- **Subnets:** `10.0.20.0/24` (AZ `ap-southeast-5a`) and `10.0.21.0/24` (AZ `ap-southeast-5b`).
- **Description:** Dedicated to backend databases. Deeply isolated without any outbound route to the internet or NAT gateways, minimizing any data extraction surface.
- **Resources:**
  - **Multi-AZ RDS PostgreSQL Instance:** Running synchronously across multiple availability zones. Inbound access is strictly limited to PostgreSQL port `5432` from the Application Layer's security group.

---

## Routing Configuration

The architecture manages network traffic flow through three distinct route tables:

### Public Route Table
- Associated with public subnets.
- Routes all outbound traffic (`0.0.0.0/0`) to the **Internet Gateway (IGW)**.

### Private Application Route Table
- Associated with private application subnets.
- Routes all outbound traffic (`0.0.0.0/0`) to the respective **NAT Gateway** running in the corresponding public subnet, providing Multi-AZ internet redundancy.

### Database Route Table
- Associated with private database subnets.
- Contains only local VPC route entries (`10.0.0.0/16`), ensuring database traffic never traverses public routes or internet gateways.
