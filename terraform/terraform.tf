terraform {
  backend "s3" {
    encrypt = true
    bucket  = "052937280793-tfstate"
    profile = "terraform"
    region  = "us-east-1"
  }
  required_version = ">=1.3.8"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.54.0"
    }
  }
}

provider "aws" {
  profile = "terraform"
  region  = "us-east-1"
}
