# rds.tf
resource "aws_db_instance" "recarnation_db" {
  identifier           = "recarnation-db"
  engine               = "postgres"
  engine_version       = "15.7" # Free tier supported version
  instance_class       = "db.t3.micro" # Free tier eligible
  allocated_storage    = 20 # GB (free tier up to 20GB)
  storage_type         = "gp2"
  db_name              = "recarnation"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.recarnation_subnet_group.name
}

resource "aws_db_subnet_group" "recarnation_subnet_group" {
  name       = "recarnation-db-subnet-group"
  subnet_ids = [aws_subnet.private[0].id, aws_subnet.private[1].id] # Use private subnets for RDS

  tags = {
    Name = "Recarnation DB Subnet Group"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "recarnation-rds-sg"
  description = "Allow access to RDS from Elastic Beanstalk"
  vpc_id      = aws_vpc.recarnation_vpc.id # Must match EB's VPC

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.jenkins_sg.id] # Reference EB's SG
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "recarnation-rds-sg"
  }
}


variable "db_username" {
  description = "RDS master username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "RDS master password"
  type        = string
  sensitive   = true             # Optional: hides password in output
  default     = "temp_password"  # Default value (change this!)
}