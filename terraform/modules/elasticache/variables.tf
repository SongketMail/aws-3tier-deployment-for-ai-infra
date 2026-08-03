variable "environment" {
  description = "Environment name (e.g., production, dev, staging)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "private_db_subnet_ids" {
  description = "List of private subnet IDs for database/cache layers"
  type        = list(string)
}

variable "asg_sg_id" {
  description = "The security group ID of the application Auto Scaling Group instances"
  type        = string
}

variable "standalone_sg_id" {
  description = "The security group ID of standalone developer/staging instances (optional)"
  type        = string
  default     = ""
}

variable "node_type" {
  description = "The instance class for the Valkey cache nodes (e.g., cache.t4g.micro)"
  type        = string
  default     = "cache.t4g.micro"
}

variable "num_cache_clusters" {
  description = "Number of cache clusters (nodes) in the replication group"
  type        = number
  default     = 1
}

variable "engine_version" {
  description = "The version number of the Valkey engine"
  type        = string
  default     = "7.2"
}

variable "parameter_group_name" {
  description = "The name of the parameter group to associate with this cache cluster"
  type        = string
  default     = "default.valkey7"
}
