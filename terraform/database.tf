# Database & Caching Infrastructure Modules (RDS PostgreSQL, ElastiCache Valkey)

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

# ElastiCache Valkey Setup (Conditional Setup)
module "elasticache_valkey" {
  count  = var.enable_elasticache_valkey ? 1 : 0
  source = "./modules/elasticache"

  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  private_db_subnet_ids = module.vpc.private_db_subnet_ids
  asg_sg_id             = module.security_groups.asg_sg_id
  standalone_sg_id      = try(module.standalone_ec2[0].security_group_id, "")
  node_type             = var.valkey_node_type
  num_cache_clusters    = var.valkey_num_cache_clusters
  engine_version        = var.valkey_engine_version
  parameter_group_name  = var.valkey_parameter_group_name
}
