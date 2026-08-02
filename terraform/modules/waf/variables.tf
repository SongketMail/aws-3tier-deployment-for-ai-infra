variable "environment" {
  description = "Environment name"
  type        = string
}

variable "alb_arn" {
  description = "The ARN of the ALB to associate with WAF"
  type        = string
}

variable "rate_limit" {
  description = "The limit on requests from a single IP in a 5-minute period"
  type        = number
  default     = 1000
}
