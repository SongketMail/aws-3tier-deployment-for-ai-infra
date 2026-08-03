output "instance_ids" {
  description = "The IDs of the standalone EC2 instances"
  value       = aws_instance.standalone[*].id
}

output "private_ips" {
  description = "The private IP addresses assigned to the standalone instances"
  value       = aws_instance.standalone[*].private_ip
}

output "security_group_id" {
  description = "The security group ID assigned to the standalone instances"
  value       = aws_security_group.standalone_sg.id
}
