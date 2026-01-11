output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.app_logs.name
}

output "cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.app_logs.arn
}

output "s3_bucket_name" {
  description = "Name of the S3 data bucket"
  value       = aws_s3_bucket.data_bucket.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 data bucket"
  value       = aws_s3_bucket.data_bucket.arn
}

output "app_role_arn" {
  description = "ARN of the IAM role for the application"
  value       = aws_iam_role.app_role.arn
}

output "app_role_name" {
  description = "Name of the IAM role for the application"
  value       = aws_iam_role.app_role.name
}
