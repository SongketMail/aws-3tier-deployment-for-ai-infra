terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Replace this block with your S3 & DynamoDB state backend config when deploying to production
  # backend "s3" {
  #   bucket         = "my-terraform-state-bucket"
  #   key            = "state/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "my-terraform-lock-table"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region
}
