resource "aws_cloudwatch_log_group" "signup_function" {
  name              = "/aws/lambda/${aws_lambda_function.signup_lambda.function_name}"
  retention_in_days = 0
  lifecycle {
    prevent_destroy = false
  }
}
resource "aws_cloudwatch_log_group" "booking_his_function" {
  name              = "/aws/lambda/${aws_lambda_function.booking_his_lambda.function_name}"
  retention_in_days = 0
  lifecycle {
    prevent_destroy = false
  }
}
resource "aws_cloudwatch_log_group" "booking_function" {
  name              = "/aws/lambda/${aws_lambda_function.booking_lambda.function_name}"
  retention_in_days = 0
  lifecycle {
    prevent_destroy = false
  }
}
resource "aws_cloudwatch_log_group" "signin_function" {
  name              = "/aws/lambda/${aws_lambda_function.signin_lambda.function_name}"
  retention_in_days = 0
  lifecycle {
    prevent_destroy = false
  }
}

output "fghf" {
  value = aws_cloudwatch_log_group.booking_function.arn
}