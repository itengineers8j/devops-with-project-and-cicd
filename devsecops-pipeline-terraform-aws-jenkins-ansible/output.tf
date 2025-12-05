output "jenkins_public_ip" {
  value = aws_instance.jenkins_instance.public_ip
}

output "jenkins_bucket" {
  value = aws_s3_bucket.jenkins_bucket.bucket
}

output "aws_ecr_repository" {
  value = aws_ecr_repository.ecr.repository_url
}

