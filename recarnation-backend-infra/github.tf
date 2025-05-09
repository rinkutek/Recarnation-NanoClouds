# github.tf
resource "okta_app_oauth" "github_sso" {
  label        = "GitHub SSO"
  type         = "browser"
  grant_types  = ["authorization_code"]
  redirect_uris = [
    "https://github.com/sessions/oauth/authorize"
  ]
  response_types = ["code"]
}

resource "okta_idp_social" "github" {
    scopes         = ["user:email"] 
  type          = "GITHUB"
  protocol_type = "OAUTH2"
  name          = "GitHub"
  client_id     = var.github_client_id
  client_secret = var.github_client_secret
}

variable "github_client_id" {
  description = "GitHub OAuth App Client ID"
  type        = string
}

variable "github_client_secret" {
  description = "GitHub OAuth App Client Secret"
  type        = string
  sensitive   = true
}