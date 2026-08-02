output "asg_id" {
  description = "The ID of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.id
}

output "asg_name" {
  description = "The name of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.name
}

output "asg_arn" {
  description = "The ARN of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.arn
}
