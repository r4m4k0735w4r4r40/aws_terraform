resource "aws_dynamodb_table" "tickets_data-table" {
  name           = "ticket_data"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "ticket_id"

  attribute {
    name = "ticket_id"
    type = "S"
  }
}

output "tickets_table_arn" {
  value = aws_dynamodb_table.tickets_data-table.arn
}