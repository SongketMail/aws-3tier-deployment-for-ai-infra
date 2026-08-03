# Route 53 Public Hosted Zone for Custom Domain Management
resource "aws_route53_zone" "main" {
  name = var.domain_name

  tags = {
    Name        = "${var.environment}-hosted-zone"
    Environment = var.environment
  }
}

# Route 53 Alias Record pointing to the Application Load Balancer
resource "aws_route53_record" "alb_alias" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.subdomain != "" ? "${var.subdomain}.${var.domain_name}" : var.domain_name
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}
