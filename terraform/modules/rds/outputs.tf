output "db_instance_endpoint" {
  description = "The connection endpoint of the RDS Database"
  value       = aws_db_instance.main.endpoint
}

output "db_instance_address" {
  description = "The hostname of the RDS Database"
  value       = aws_db_instance.main.address
}

output "db_instance_id" {
  description = "The ID of the RDS Instance"
  value       = aws_db_instance.main.id
}
