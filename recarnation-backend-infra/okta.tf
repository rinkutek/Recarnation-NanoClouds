# okta.tf
resource "okta_app_oauth" "recarnation" {
  label          = "Recarnation Django App"
  type           = "web"
  grant_types    = ["authorization_code", "refresh_token"]
  redirect_uris  = [
    "https://${aws_cloudfront_distribution.recarnation_distribution.domain_name}/oauth/callback/okta/",
    "https://${aws_elastic_beanstalk_environment.recarnation_env.cname}/oauth/callback/okta/"
  ]
  response_types = ["code"]
  login_uri      = "https://${aws_cloudfront_distribution.recarnation_distribution.domain_name}/"
}

# For custom user profile properties (v4.0+)
resource "okta_user_schema_property" "custom_property" {
  index       = "customPropertyName"
  title       = "Custom Property"
  type        = "string"
  description = "Custom user attribute"
  master      = "PROFILE_MASTER" # Okta manages the attribute
  scope       = "SELF"           # Visible to user
  permissions = "READ_WRITE"     # Allow user to modify
}

# For app-specific attributes (v4.0+)
resource "okta_app_user_schema_property" "app_custom_property" {
  app_id      = okta_app_oauth.recarnation.id
  index       = "customPropertyName"
  title       = "Custom Property"
  type        = "string"
  description = "Custom user attribute"
  required    = false
}