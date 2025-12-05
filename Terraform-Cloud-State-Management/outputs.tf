output "lambda_function_name" {
  value = aws_lambda_function.demo_lambda.function_name
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "bucket_name" {
  value = aws_s3_bucket.demo_bucket.bucket
}
