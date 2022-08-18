locals {
  booking_his_file_path = "${path.module}/../lambdas/booking_history.py"
  booking_his__zip_path = "${path.module}/../lambdas/booking_history.zip"
}

resource "aws_iam_role_policy" "booking_role_policy" {
  policy =  <<EOF
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
            "Resource": "arn:aws:logs:ap-south-1:${local.account_id}:*"
    },
    {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Effect" : "Allow",
        "Resource" : "${aws_cloudwatch_log_group.booking_his_function.arn}:*"
      }
  ]
}
EOF
  role   = aws_iam_role.booking_history_role.id
}

resource "aws_iam_role" "booking_history_role" {
  name = "booking_history_role"
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

data "archive_file" "booking_history_zip" {
  output_path = local.booking_his__zip_path
  source_file = local.booking_his_file_path
  type        = "zip"
}

resource "aws_lambda_function" "booking_his_lambda" {
  filename = local.booking_his__zip_path
  function_name = "booking_his_lambda"
  role          = aws_iam_role.booking_history_role.arn
  handler = "booking_history.lambda_handler"

  source_code_hash = data.archive_file.booking_history_zip.output_base64sha256

  runtime = "python3.8"
}

resource "aws_lambda_permission" "booking_his_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.booking_his_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.account.account_id}:${aws_api_gateway_rest_api.booking.id}/*/${aws_api_gateway_method.booking_his_method.http_method}${aws_api_gateway_resource.booking_his_resource.path}"
}