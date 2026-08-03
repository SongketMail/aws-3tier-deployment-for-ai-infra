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

output "standalone_ec2_instance_ids" {
  description = "The IDs of the generated standalone EC2 instances"
  value       = try(module.standalone_ec2[0].instance_ids, [])
}

output "standalone_ec2_private_ips" {
  description = "The private IP addresses assigned to the standalone EC2 instances"
  value       = try(module.standalone_ec2[0].private_ips, [])
}

output "standalone_ec2_security_group_id" {
  description = "The security group ID assigned to the standalone instances"
  value       = try(module.standalone_ec2[0].security_group_id, "")
}

output "route53_hosted_zone_id" {
  description = "The Route 53 Hosted Zone ID"
  value       = try(module.route53[0].hosted_zone_id, "")
}

output "route53_name_servers" {
  description = "The list of Name Servers assigned to the Route 53 Hosted Zone"
  value       = try(module.route53[0].name_servers, [])
}

output "route53_fqdn" {
  description = "The FQDN created in Route 53 pointing to the ALB"
  value       = try(module.route53[0].fqdn, "")
}
