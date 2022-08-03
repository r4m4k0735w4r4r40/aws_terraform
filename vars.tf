variable "region" {
  default = "ap-south-1"
}

data "aws_caller_identity" "account" {}