# VPC Module Setup
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr                 = var.vpc_cidr
  environment              = var.environment
  public_subnet_cidrs      = var.public_subnet_cidrs
  private_app_subnet_cidrs = var.private_app_subnet_cidrs
  private_db_subnet_cidrs  = var.private_db_subnet_cidrs
  availability_zones       = var.availability_zones
}

# Security Groups Setup
module "security_groups" {
  source = "./modules/security_groups"

  vpc_id      = module.vpc.vpc_id
  environment = var.environment
  http_port   = var.http_port
  db_port     = var.db_port
}

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

# Auto Scaling Group (ASG) Setup
module "asg" {
  source = "./modules/asg"

  environment            = var.environment
  private_app_subnet_ids = module.vpc.private_app_subnet_ids
  asg_sg_id              = module.security_groups.asg_sg_id
  target_group_arn       = module.alb.target_group_arn
  min_size               = var.min_size
  max_size               = var.max_size
  desired_capacity       = var.desired_capacity
  instance_type          = var.instance_type
  ami_id                 = var.ami_id
}

# Relational Database Service (RDS) Setup
module "rds" {
  source = "./modules/rds"

  environment           = var.environment
  private_db_subnet_ids = module.vpc.private_db_subnet_ids
  db_sg_id              = module.security_groups.db_sg_id
  db_engine             = var.db_engine
  db_engine_version     = var.db_engine_version
  db_instance_class     = var.db_instance_class
  db_name               = var.db_name
  db_username           = var.db_username
  db_password           = var.db_password
  db_port               = var.db_port
}
