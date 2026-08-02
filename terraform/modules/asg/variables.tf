variable "environment" {
  description = "Environment name"
  type        = string
}

variable "private_app_subnet_ids" {
  description = "List of IDs of private subnets for application servers"
  type        = list(string)
}

variable "asg_sg_id" {
  description = "The ID of the ASG Security Group"
  type        = string
}

variable "target_group_arn" {
  description = "The ARN of the ALB Target Group"
  type        = string
}

variable "ami_id" {
  description = "AMI ID to use for the launch template"
  type        = string
  default     = "" # Will default to SSM parameter for latest Amazon Linux 2023 if not provided
}

variable "instance_type" {
  description = "Instance type for ASG instances"
  type        = string
  default     = "t3.micro"
}

variable "min_size" {
  description = "Minimum size of the ASG"
  type        = number
  default     = 2
}

variable "max_size" {
  description = "Maximum size of the ASG"
  type        = number
  default     = 5
}

variable "desired_capacity" {
  description = "Desired capacity of the ASG"
  type        = number
  default     = 2
}
