variable "environment" {
  description = "Environment name (e.g., dev, production)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs in the VPC"
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance size for the Jumphost (Graviton-compatible default)"
  type        = string
  default     = "t4g.micro"
}

variable "allowed_ssh_cidr" {
  description = "IP CIDR allowed to connect to the Jumphost (e.g., Cyberjaya office public IP)"
  type        = string
  default     = "103.188.0.0/16"
}

variable "jumphost_os" {
  description = "The OS to deploy for the Jumphost ('ubuntu' or 'amazon-linux-2023')"
  type        = string
  default     = "ubuntu"
}

variable "ami_id" {
  description = "Optional specific AMI ID override for the Jumphost"
  type        = string
  default     = ""
}

variable "ubuntu_ami_filter_name" {
  description = "The search pattern name for the Ubuntu AMI"
  type        = string
  default     = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-*-server-*"
}

variable "asg_sg_id" {
  description = "The Security Group ID of the Auto Scaling Group instances"
  type        = string
}

variable "standalone_sg_id" {
  description = "Optional Security Group ID of the Standalone EC2 instances"
  type        = string
  default     = ""
}
