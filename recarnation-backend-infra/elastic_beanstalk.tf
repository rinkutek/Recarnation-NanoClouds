# elastic_beanstalk.tf - WORKING VERSION
resource "aws_elastic_beanstalk_application" "recarnation" {
  name        = "recarnation-app"
  description = "Recarnation Django application"
}

data "aws_elastic_beanstalk_solution_stack" "python" {
  most_recent = true
  name_regex  = "^64bit Amazon Linux 2.* running Python 3.11" # More stable than AL2023
}

resource "aws_elastic_beanstalk_environment" "recarnation_env" {
  name                = "recarnation-env"
  application         = aws_elastic_beanstalk_application.recarnation.name
  solution_stack_name = data.aws_elastic_beanstalk_solution_stack.python.name
  tier                = "WebServer"

  # VPC Configuration (Required)
  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = aws_vpc.recarnation_vpc.id
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", [aws_subnet.public[0].id, aws_subnet.public[1].id])
  }

  # IAM & Security (Required)
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.eb_sg.id
  }

  # Environment Type
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance" 
  }

  # Instance Configuration
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.medium"
  }

  # Django Settings
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DJANGO_SETTINGS_MODULE"
    value     = "recarnation.settings.production"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_URL"
    value     = "postgres://${var.db_username}:${var.db_password}@${aws_db_instance.recarnation_db.endpoint}/${aws_db_instance.recarnation_db.db_name}"
  }
}

resource "aws_security_group" "eb_sg" {
  name        = "recarnation-eb-sg"
  description = "Allow inbound access to Elastic Beanstalk"
  vpc_id      = aws_vpc.recarnation_vpc.id # Must specify VPC

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}