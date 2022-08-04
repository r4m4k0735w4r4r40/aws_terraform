terraform {
  backend "s3" {
    bucket = "my-terraforms-state-bucket"
    key    = "tf_state"
    region = "ap-south-1"
  }
}