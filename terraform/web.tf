# Web Routing, Edge Security & DNS Modules (ALB, WAF, Route 53)

# Application Load Balancer (ALB) Setup
module "alb" {
  source = "./modules/alb"

  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  alb_sg_id         = module.security_groups.alb_sg_id
  http_port         = var.http_port
}

# Web Application Firewall (WAF) Setup
module "waf" {
  source = "./modules/waf"

  environment = var.environment
  alb_arn     = module.alb.alb_arn
  rate_limit  = var.waf_rate_limit
}

# Route 53 Module Setup (Conditional Setup)
module "route53" {
  count  = var.enable_route53 ? 1 : 0
  source = "./modules/route53"

  environment  = var.environment
  domain_name  = var.domain_name
  subdomain    = var.subdomain
  alb_dns_name = module.alb.alb_dns_name
  alb_zone_id  = module.alb.alb_zone_id
}
