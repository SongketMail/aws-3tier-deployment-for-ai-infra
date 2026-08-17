# Main OpenTofu Infrastructure Entrypoint
# Network Foundations & Core Security Groups

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
