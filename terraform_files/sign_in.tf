locals {
  file_path = "${path.module}/lambdas/sign_in.py"
  zip_path = "${path.module}/lambdas/sign_in.zip"
}

resource "aws_iam_role_policy" "signin_policy" {
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
      "Resource": "${aws_dynamodb_table.user_data-table.arn}"
    }
  ]
}
EOF
  role   = aws_iam_role.signin_role.id
}
resource "aws_iam_role" "signin_role" {
  name = "signin_role"
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

data "archive_file" "signin_zip_file" {
  type        = "zip"
  source_file = local.file_path
  output_path = local.zip_path
}

resource "aws_lambda_function" "signin_lambda" {
  filename = local.zip_path
  function_name = "signin_lambda"
  role          = aws_iam_role.signin_role.arn
  handler = "sign_in.lambda_handler"

  source_code_hash = filebase64sha256(local.file_path)

  runtime = "python3.8"
}

resource "aws_lambda_permission" "signin_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.signin_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.account.account_id}:${aws_api_gateway_rest_api.booking.id}/*/${aws_api_gateway_method.signin_method.http_method}${aws_api_gateway_resource.signin_resource.path}"
}

#output "signin_arn" {
#  value = aws_lambda_function.signin_lambda.arn
#}