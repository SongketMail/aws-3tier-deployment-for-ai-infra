output "hosted_zone_id" {
  description = "The ID of the Route 53 Hosted Zone"
  value       = aws_route53_zone.main.zone_id
}

output "name_servers" {
  description = "The list of Name Servers assigned to the Hosted Zone"
  value       = aws_route53_zone.main.name_servers
}

output "fqdn" {
  description = "The Fully Qualified Domain Name pointing to the ALB"
  value       = aws_route53_record.alb_alias.fqdn
}
