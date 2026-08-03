variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "private_app_subnet_ids" {
  description = "List of private application subnet IDs to deploy the instances into"
  type        = list(string)
}

variable "alb_sg_id" {
  description = "The security group ID of the Application Load Balancer"
  type        = string
}

variable "instance_type" {
  description = "Instance type for standalone instances (typically Graviton, e.g., t4g.micro or t4g.medium)"
  type        = string
  default     = "t4g.micro"
}

variable "ami_id" {
  description = "Optional specific AMI ID to override the dynamic search"
  type        = string
  default     = ""
}

variable "ubuntu_ami_filter_name" {
  description = "Search filter pattern for the Ubuntu AMI name (allows switching between 24.04 and 26.04)"
  type        = string
  default     = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-*-server-*"
}

variable "instance_count" {
  description = "Number of standalone EC2 instances to provision"
  type        = number
  default     = 1
}
