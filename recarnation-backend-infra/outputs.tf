# outputs.tf
output "elastic_beanstalk_url" {
  value = aws_elastic_beanstalk_environment.recarnation_env.cname
}

output "frontend_url" {
  value = aws_cloudfront_distribution.recarnation_distribution.domain_name
}

output "database_endpoint" {
  value = aws_db_instance.recarnation_db.endpoint
}

output "jenkins_public_ip" {
  value = aws_instance.jenkins.public_ip
}

output "okta_client_id" {
  value = okta_app_oauth.recarnation.client_id
}

output "okta_client_secret" {
  value     = okta_app_oauth.recarnation.client_secret
  sensitive = true
}