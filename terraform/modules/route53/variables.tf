variable "environment" {
  description = "Environment name (e.g., development, production)"
  type        = string
}

variable "domain_name" {
  description = "The root domain name (e.g., example.com)"
  type        = string
}

variable "subdomain" {
  description = "The subdomain to point to the ALB (e.g., app). If empty, points to the root domain."
  type        = string
  default     = ""
}

variable "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer"
  type        = string
}

variable "alb_zone_id" {
  description = "The Canonical Hosted Zone ID of the Application Load Balancer"
  type        = string
}
