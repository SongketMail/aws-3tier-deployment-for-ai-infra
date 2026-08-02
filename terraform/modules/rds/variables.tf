variable "environment" {
  description = "Environment name"
  type        = string
}

variable "private_db_subnet_ids" {
  description = "List of private subnets for database RDS subnet group"
  type        = list(string)
}

variable "db_sg_id" {
  description = "The ID of the DB Security Group"
  type        = string
}

variable "db_engine" {
  description = "The database engine (e.g., mysql, postgres, aurora-mysql)"
  type        = string
  default     = "mysql"
}

variable "db_engine_version" {
  description = "The database engine version"
  type        = string
  default     = "8.0.35"
}

variable "db_instance_class" {
  description = "The instance type of the RDS database"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "The upper limit for storage autoscaling (GB)"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
  default     = "mydb"
}

variable "db_username" {
  description = "Username for the master DB user"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Password for the master DB user"
  type        = string
  sensitive   = true
}

variable "multi_az" {
  description = "Specifies if the RDS instance is multi-AZ"
  type        = bool
  default     = true
}

variable "db_port" {
  description = "Database connection port"
  type        = number
  default     = 3306
}
