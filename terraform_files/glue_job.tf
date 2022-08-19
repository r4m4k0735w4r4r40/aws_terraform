locals {
  glue_job_file_path = "${path.module}/../glues/glue_job-1.py"
}
resource "aws_iam_role" "glue_assume_role" {
  name = "glue_iam_role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}
resource "aws_iam_role_policy" "glue_role_policy" {
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
  role   = aws_iam_role.glue_assume_role.id
}
resource "aws_glue_job" "example" {
  glue_version = "3.0"
  name     = "Terraform_glue"
  role_arn = aws_iam_role.glue_assume_role.arn
  default_arguments = {
    "--job-language": "python",
    "--TempDir": "s3://${aws_s3_object.glue_job.bucket}/temporary"
    "--enable-spark-ui": true,
    "--job-bookmark-option": "job-bookmark-enable",
    "--enable-metrics": true,
    "--enable-job-insights": true,
    "--enable-glue-datacatalog": true,
    "--spark-event-logs-path": "s3://${aws_s3_object.glue_job.bucket}/sparkHistoryLogs/"
  }

  command {
    script_location = "s3://${aws_s3_object.glue_job.bucket}/${aws_s3_object.glue_job.key}"
  }
}
resource "aws_s3_object" "glue_job" {
  bucket = "aws-glue-assets-131069340413-ap-south-1"
  key    = "scripts/terraform_glue_job1.py"
  source = local.glue_job_file_path
  source_hash = filemd5(local.glue_job_file_path)
}
resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "glue-table-1"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "customerid"

  attribute {
    name = "customerid"
    type = "N"
  }
}