terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state-buckets-1"
    key    = "tf_state"
    region = "ap-south-1"
    shared_credentials_file = ""
  }
}

provider "aws" {
  region = "ap-south-1"
}