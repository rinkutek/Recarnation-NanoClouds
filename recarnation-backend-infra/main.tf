# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    okta = {
      source  = "okta/okta"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Using us-east-1 for maximum free tier availability
}

provider "okta" {
  org_name  = "dev-10693315" # Replace with your Okta org name
  base_url  = "okta.com"      # Update if using a different Okta domain
  api_token = var.okta_api_token
}

variable "okta_api_token" {
  description = "Okta API token"
  type        = string
  sensitive   = true
}