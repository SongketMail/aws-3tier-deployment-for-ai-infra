# Fetch latest Amazon Linux 2023 AMI for x86_64
data "aws_ssm_parameter" "al2023_x86_64" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# Fetch latest Amazon Linux 2023 AMI for arm64
data "aws_ssm_parameter" "al2023_arm64" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64"
}

locals {
  # If instance type starts with t4g, m6g, c6g, r6g, etc. (typically Graviton), select arm64.
  is_arm64        = length(regexall("^[a-z]+[0-9]g\\.", var.instance_type)) > 0
  default_ami_id  = local.is_arm64 ? data.aws_ssm_parameter.al2023_arm64.value : data.aws_ssm_parameter.al2023_x86_64.value
  selected_ami_id = var.ami_id != "" ? var.ami_id : local.default_ami_id
}

# IAM Role for EC2 Instance to integrate with systems or read configurations if needed
resource "aws_iam_role" "instance_role" {
  name = "${var.environment}-asg-instance-role"

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

# Attach AWS SSM Policy for remote management/troubleshooting
resource "aws_iam_role_policy_attachment" "ssm_policy" {
  role       = aws_iam_role.instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "instance_profile" {
  name = "${var.environment}-asg-instance-profile"
  role = aws_iam_role.instance_role.name
}

# Launch Template
resource "aws_launch_template" "main" {
  name_prefix   = "${var.environment}-launch-template-"
  image_id      = local.selected_ami_id
  instance_type = var.instance_type

  iam_instance_profile {
    arn = aws_iam_instance_profile.instance_profile.arn
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  network_interfaces {
    associate_public_ip_address = false
    security_groups             = [var.asg_sg_id]
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y nginx
              systemctl enable --now nginx
              echo "<h1>3-Tier Architecture Active | AWS Malaysia (ap-southeast-5) | Host: \$(hostname -f) | Env: ${var.environment}</h1>" > /usr/share/nginx/html/index.html
              EOF
  )

  monitoring {
    enabled = true
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "${var.environment}-asg-instance"
      Environment = var.environment
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name_prefix         = "${var.environment}-asg-"
  vpc_zone_identifier = var.private_app_subnet_ids

  target_group_arns         = [var.target_group_arn]
  health_check_type         = "ELB"
  health_check_grace_period = 300

  min_size         = var.min_size
  max_size         = var.max_size
  desired_capacity = var.desired_capacity

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }

  force_delete = true

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
    }
    triggers = ["tag"]
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [desired_capacity]
  }
}

# Scale Out (Up) Policy based on CPU
resource "aws_autoscaling_policy" "scale_out" {
  name                   = "${var.environment}-asg-scale-out"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

# Scale In (Down) Policy based on CPU
resource "aws_autoscaling_policy" "scale_in" {
  name                   = "${var.environment}-asg-scale-in"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

# CPU Metric Alarm for Scale Out (High CPU > 70%)
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.environment}-asg-high-cpu"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 70

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.main.name
  }

  alarm_actions = [aws_autoscaling_policy.scale_out.arn]
}

# CPU Metric Alarm for Scale In (Low CPU < 30%)
resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "${var.environment}-asg-low-cpu"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 30

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.main.name
  }

  alarm_actions = [aws_autoscaling_policy.scale_in.arn]
}
