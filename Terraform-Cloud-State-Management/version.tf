terraform {
  required_version = "~> 1.13.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.14.1"
    }
    random = {
      source = "hashicorp/random"
    }
    archive = {
      source = "hashicorp/archive"
    }
  }

  ## Use for CLI-Driven and local terraform operations
  # cloud { 

  #   organization = "amanpathak-devops" 

  #   workspaces { 
  #     name = "demo-cli-driven-aws-workspace" 
  #   } 
  # } 

  cloud {}

}