resource "aws_iam_role_policy" "signup_policy" {
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
    },
    {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Effect" : "Allow",
        "Resource" : "${aws_cloudwatch_log_group.signup_function.arn}"
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
        "Resource" : "${aws_cloudwatch_log_group.signup_function.arn}:*"
      }
  ]
}
EOF
  role   = aws_iam_role.signup_role.id
}

resource "aws_iam_role" "signup_role" {
  name = "signup_role"
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

data "archive_file" "signup_zip_file" {
  type        = "zip"
  source_file = "${path.module}/../lambdas/sign_up.py"
  output_path = "${path.module}/../lambdas/sign_up.zip"
}

resource "aws_lambda_function" "signup_lambda" {
  filename = "${path.module}/../lambdas/sign_up.zip"
  function_name = "signup_lambda"
  role          = aws_iam_role.signup_role.arn
  handler = "sign_up.lambda_handler"

  source_code_hash = filebase64sha256("${path.module}/../lambdas/sign_up.py")

  runtime = "python3.8"
}

resource "aws_lambda_permission" "signup_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.signup_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.account.account_id}:${aws_api_gateway_rest_api.booking.id}/*/${aws_api_gateway_method.signup_method.http_method}${aws_api_gateway_resource.signup_resource.path}"
}

#output "signup_arn" {
#  value = aws_lambda_function.signup_lambda.arn
#}