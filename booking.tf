locals {
  booking_file_path = "${path.module}/lambdas/booking.py"
  booking_zip_path = "${path.module}/lambdas/booking.zip"
}

resource "aws_iam_role_policy" "booking_policy" {
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1659016280205",
      "Action": [
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem",
        "dynamodb:DeleteItem",
        "dynamodb:GetItem",
        "dynamodb:GetRecords",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:UpdateItem",
        "dynamodb:UpdateTable"
      ],
      "Effect": "Allow",
      "Resource": "${aws_dynamodb_table.tickets_data-table.arn}"
    }
  ]
}
EOF
  role   = aws_iam_role.booking_role.id
}
resource "aws_iam_role" "booking_role" {
  name = "booking_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "archive_file" "booking_zip_file" {
  type        = "zip"
  source_file = local.booking_file_path
  output_path = local.booking_zip_path
}

resource "aws_lambda_function" "booking_lambda" {
  filename = local.booking_zip_path
  function_name = "booking_lambda"
  role          = aws_iam_role.booking_role.arn
  handler = "booking.lambda_handler"

  source_code_hash = filebase64sha256(local.booking_file_path)

  runtime = "python3.8"
}

output "booking_arn" {
  value = aws_lambda_function.booking_lambda.arn
}