locals {
  is_arm64        = length(regexall("^[a-z]+[0-9]g\\.", var.instance_type)) > 0
  selected_ami_id = var.ami_id != "" ? var.ami_id : one(data.aws_ami.ubuntu_canonical[*].id)
}

# Fetch Canonical Ubuntu Server AMI based on the architecture
data "aws_ami" "ubuntu_canonical" {
  count       = var.ami_id == "" ? 1 : 0
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = [var.ubuntu_ami_filter_name]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = [local.is_arm64 ? "arm64" : "x86_64"]
  }
}

# Standalone Instance Custom Security Group
resource "aws_security_group" "standalone_sg" {
  name        = "${var.environment}-standalone-ec2-sg"
  description = "Security group for standalone application/developer instances"
  vpc_id      = var.vpc_id

  # Inbound HTTP from the ALB SG for web-facing test applications
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [var.alb_sg_id]
  }

  # Inbound HTTPS from the ALB SG for secure test applications
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [var.alb_sg_id]
  }

  # Allow all outbound to NAT Gateway for package updates and auditing
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-standalone-ec2-sg"
    Environment = var.environment
  }
}

# IAM Role for Standalone EC2 Instance to integrate with Systems Manager (SSM)
resource "aws_iam_role" "standalone_role" {
  name = "${var.environment}-standalone-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach SSM Policy for secure shell administration and remote patches
resource "aws_iam_role_policy_attachment" "ssm_policy" {
  role       = aws_iam_role.standalone_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "standalone_profile" {
  name = "${var.environment}-standalone-ec2-profile"
  role = aws_iam_role.standalone_role.name
}

# Standalone EC2 Instances
resource "aws_instance" "standalone" {
  count         = var.instance_count
  ami           = local.selected_ami_id
  instance_type = var.instance_type

  subnet_id = var.private_app_subnet_ids[count.index % length(var.private_app_subnet_ids)]

  vpc_security_group_ids = [aws_security_group.standalone_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.standalone_profile.name

  # Enable detailed monitoring for staging audit compatibility
  monitoring = true

  # Tag specifications for proper compliance
  tags = {
    Name        = "${var.environment}-standalone-instance-${count.index + 1}"
    Environment = var.environment
    OS          = "Ubuntu-26.04-LTS"
    Hardened    = "ASIMP-Compliant"
  }

  # Bootstrapping user data for testing
  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get upgrade -y
              apt-get install -y nginx
              systemctl enable --now nginx
              echo "<h1>Standalone Developer Server ${count.index + 1} | ASIMP Hardened | Ubuntu 26.04 LTS</h1>" > /var/www/html/index.html
              EOF

  lifecycle {
    ignore_changes = [ami]
  }
}
