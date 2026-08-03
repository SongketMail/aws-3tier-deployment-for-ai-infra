output "jumphost_public_ip" {
  description = "The static Elastic IP address assigned to the Jumphost"
  value       = aws_eip.jumphost_eip.public_ip
}

output "jumphost_private_ip" {
  description = "The private IP address of the Jumphost"
  value       = aws_instance.jumphost.private_ip
}

output "security_group_id" {
  description = "The security group ID assigned to the Jumphost"
  value       = aws_security_group.jumphost_sg.id
}

output "instance_id" {
  description = "The ID of the Jumphost EC2 instance"
  value       = aws_instance.jumphost.id
}
