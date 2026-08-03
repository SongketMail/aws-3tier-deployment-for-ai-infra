output "primary_endpoint_address" {
  description = "The primary connection endpoint address for the Valkey cluster"
  value       = aws_elasticache_replication_group.valkey.primary_endpoint_address
}

output "security_group_id" {
  description = "The ID of the security group assigned to the Valkey cluster"
  value       = aws_security_group.valkey_sg.id
}

output "subnet_group_name" {
  description = "The name of the subnet group assigned to the Valkey cluster"
  value       = aws_elasticache_subnet_group.valkey.name
}
