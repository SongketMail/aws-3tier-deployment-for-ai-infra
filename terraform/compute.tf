# Compute Infrastructure Modules (Auto Scaling Group, Standalone EC2, Bastion Jumphost)

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

# Standalone EC2 Instances Module Setup
module "standalone_ec2" {
  count  = var.enable_standalone_ec2 ? 1 : 0
  source = "./modules/standalone_ec2"

  environment            = var.environment
  vpc_id                 = module.vpc.vpc_id
  private_app_subnet_ids = module.vpc.private_app_subnet_ids
  alb_sg_id              = module.security_groups.alb_sg_id
  instance_type          = var.standalone_ec2_instance_type
  instance_count         = var.standalone_ec2_count
  ami_id                 = var.standalone_ec2_ami_id
  ubuntu_ami_filter_name = var.standalone_ubuntu_ami_filter_name
}

# Secure SSH Jumphost (Bastion) Setup (Conditional Setup)
module "jumphost" {
  count  = var.enable_jumphost ? 1 : 0
  source = "./modules/jumphost"

  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  instance_type     = var.jumphost_instance_type
  allowed_ssh_cidr  = var.jumphost_allowed_ssh_cidr
  jumphost_os       = var.jumphost_os
  ami_id            = var.jumphost_ami_id
  asg_sg_id         = module.security_groups.asg_sg_id
  standalone_sg_id  = try(module.standalone_ec2[0].security_group_id, "")
}
