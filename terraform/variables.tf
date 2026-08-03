variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "ap-southeast-5"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_app_subnet_cidrs" {
  description = "List of CIDR blocks for private app subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "private_db_subnet_cidrs" {
  description = "List of CIDR blocks for private database subnets"
  type        = list(string)
  default     = ["10.0.20.0/24", "10.0.21.0/24"]
}

variable "availability_zones" {
  description = "Availability Zones to deploy subnets"
  type        = list(string)
  default     = ["ap-southeast-5a", "ap-southeast-5b"]
}

variable "http_port" {
  description = "Port to expose the application"
  type        = number
  default     = 80
}

variable "db_port" {
  description = "Port to connect to the database"
  type        = number
  default     = 5432
}

variable "db_engine" {
  description = "RDS engine (e.g., mysql, postgres)"
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "RDS engine version"
  type        = string
  default     = "16"
}

variable "db_instance_class" {
  description = "RDS instance size (e.g., 'db.t4g.micro' for testing, 'db.m6g.large' [2 vCPU, 8GB] for baseline production, or 'db.m6g.xlarge' [4 vCPU, 16GB] to match developer specifications)"
  type        = string
  default     = "db.t4g.micro"
}

variable "db_name" {
  description = "The database name"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "The database administrator username"
  type        = string
  default     = "dbadmin"
}

variable "db_password" {
  description = "The database administrator password"
  type        = string
  sensitive   = true
}

variable "instance_type" {
  description = "Instance type for ASG instances (e.g., 't4g.medium' [2 vCPU, 4GB] for baseline, or 't4g.xlarge' [4 vCPU, 16GB] / 'm6g.xlarge' [4 vCPU, 16GB] to match developer specifications)"
  type        = string
  default     = "t4g.micro"
}

variable "ami_id" {
  description = "AMI ID to use for the launch template in ap-southeast-5"
  type        = string
  default     = ""
}

variable "min_size" {
  description = "Minimum size of the ASG"
  type        = number
  default     = 2
}

variable "max_size" {
  description = "Maximum size of the ASG"
  type        = number
  default     = 6
}

variable "desired_capacity" {
  description = "Desired size of the ASG"
  type        = number
  default     = 2
}

variable "waf_rate_limit" {
  description = "WAF IP rate limit value (requests per 5 minutes)"
  type        = number
  default     = 2000
}
