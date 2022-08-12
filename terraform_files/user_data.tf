resource "aws_dynamodb_table" "user_data-table" {
  name           = "users_data"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "user_name"

  attribute {
    name = "user_name"
    type = "S"
  }
}