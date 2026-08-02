output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "alb_dns_name" {
  description = "The public-facing DNS name of the Application Load Balancer protected by WAF"
  value       = module.alb.alb_dns_name
}

output "rds_endpoint" {
  description = "The connection endpoint for the private RDS database"
  value       = module.rds.db_instance_endpoint
}

output "asg_name" {
  description = "The name of the application Auto Scaling Group"
  value       = module.asg.asg_name
}

output "waf_web_acl_arn" {
  description = "The ARN of the protecting WAFv2 Web ACL"
  value       = module.waf.web_acl_arn
}
