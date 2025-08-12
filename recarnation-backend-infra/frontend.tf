# frontend.tf
resource "aws_s3_bucket" "recarnation_frontend" {
  bucket = "recarnation-frontend-${random_id.bucket_suffix.hex}"

#   # Disable ACLs and use bucket policy
#   object_ownership = "BucketOwnerEnforced" # Recommended for static websites
}

# Modern ACL alternative (works pre-version 4.0)
resource "aws_s3_bucket_ownership_controls" "frontend_owner" {
  bucket = aws_s3_bucket.recarnation_frontend.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "frontend_access" {
  bucket = aws_s3_bucket.recarnation_frontend.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "frontend_policy" {
  depends_on = [
    aws_s3_bucket_public_access_block.frontend_access
  ]

  bucket = aws_s3_bucket.recarnation_frontend.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.recarnation_frontend.arn}/*"
    }]
  })
}

resource "aws_cloudfront_distribution" "recarnation_distribution" {
  origin {
    domain_name = aws_s3_bucket.recarnation_frontend.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.recarnation_frontend.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.recarnation_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.recarnation_frontend.id}"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

resource "aws_cloudfront_origin_access_identity" "recarnation_oai" {
  comment = "OAI for Recarnation frontend"
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}