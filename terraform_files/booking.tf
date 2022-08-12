locals {
  booking_file_path = "${path.module}/../lambdas/booking.py"
  booking_zip_path = "${path.module}/../lambdas/booking.zip"
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
    },
    {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:ap-south-1:728747466273:*"
    },
    {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Effect" : "Allow",
        "Resource" : "${aws_cloudwatch_log_group.booking_function.arn}:*"
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

resource "aws_lambda_permission" "booking_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.booking_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.account.account_id}:${aws_api_gateway_rest_api.booking.id}/*/${aws_api_gateway_method.booking_method.http_method}${aws_api_gateway_resource.booking_resource.path}"
}

#output "booking_arn" {
#  value = aws_lambda_function.booking_lambda.arn
#}