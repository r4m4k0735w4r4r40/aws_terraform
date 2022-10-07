resource "aws_sqs_queue" "terraform_queue" {
  name                      = "terraform-example-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}
output "queue_url" {
  value = "${aws_sqs_queue.terraform_queue.url}"
}
resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.terraform_queue.arn
  function_name    = aws_lambda_function.test_lambda.arn
}
locals {
  test_file_path = "${path.module}/../lambdas/test_lamba.py"
  test_zip_path = "${path.module}/../lambdas/test_lamba.zip"
}
data "archive_file" "test_zip_file" {
  type        = "zip"
  source_file = local.test_file_path
  output_path = local.test_zip_path
}
resource "aws_lambda_function" "test_lambda" {
  filename         = local.test_zip_path
  function_name    = "test_lamba"
  role             = aws_iam_role.booking_role.arn
  handler          = "test_lamb.lambda_handler"
  source_code_hash = data.archive_file.test_zip_file.output_base64sha256
  runtime = "python3.8"
}