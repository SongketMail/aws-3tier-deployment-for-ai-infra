# Security Groups Module

This module defines stateful firewall rules (Security Groups) that isolate each layer of the 3-Tier topology, strictly adhering to the **Zero-Trust Network Principle**.

---

## Firewall Rulesets

### Presentation Layer: ALB Security Group (`alb_sg`)
- **Ingress:** Accepts inbound public traffic on:
  - Port `80` (HTTP) from any IPv4 or IPv6 address (`0.0.0.0/0`, `::/0`).
  - Port `443` (HTTPS) from any IPv4 or IPv6 address (`0.0.0.0/0`, `::/0`).
- **Egress:** Allows outbound connections to any destination (`0.0.0.0/0`) to route filtered requests.

### Application Layer: ASG/EC2 Security Group (`asg_sg`)
- **Ingress:** Accepts traffic **strictly** from the ALB Security Group on the application HTTP port (`80`). No direct internet access is permitted.
- **Egress:** Allows outbound connections to any destination (`0.0.0.0/0`) to allow instances to perform updates or retrieve application packages.

### Database Layer: RDS Security Group (`db_sg`)
- **Ingress:** Accepts traffic **strictly** from the ASG/EC2 Security Group on the database port (`5432` for PostgreSQL / `3306` for MySQL). No other traffic is allowed.
- **Egress:** Blocked to restrict exfiltration.

---

## Inputs and Outputs

For a detailed list of all input parameters and output values, please refer to the module's inline documentation at `terraform/modules/security_groups/README.md`.
