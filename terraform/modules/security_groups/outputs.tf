output "alb_sg_id" {
  description = "The ID of the ALB Security Group"
  value       = aws_security_group.alb_sg.id
}

output "asg_sg_id" {
  description = "The ID of the ASG Security Group"
  value       = aws_security_group.asg_sg.id
}

output "db_sg_id" {
  description = "The ID of the Database Security Group"
  value       = aws_security_group.db_sg.id
}
