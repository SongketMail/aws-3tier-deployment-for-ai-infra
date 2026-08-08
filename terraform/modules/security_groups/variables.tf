variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "http_port" {
  description = "HTTP Port"
  type        = number
  default     = 80
}

variable "db_port" {
  description = "Database connection port"
  type        = number
  default     = 5432 # Default for PostgreSQL
}
