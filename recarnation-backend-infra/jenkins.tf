# jenkins.tf - Fixed Version
data "http" "my_ip" {
  url = "https://api.ipify.org" # More reliable than ifconfig.me
}

locals {
  my_ip = chomp(data.http.my_ip.response_body) # Use response_body instead of deprecated body
}

resource "aws_instance" "jenkins" {
  ami           = "ami-0c7217cdde317cfec" # Amazon Linux 2023 AMI
  instance_type = "t3.large"
  key_name      = aws_key_pair.jenkins_key.key_name
  subnet_id     = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.jenkins_sg.id]

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  tags = {
    Name = "Jenkins-Server"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install java-openjdk11 -y
              sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
              sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
              sudo yum install jenkins -y
              sudo systemctl enable jenkins
              sudo systemctl start jenkins
              EOF
}

resource "aws_security_group" "jenkins_sg" {
  name        = "jenkins-sg"
  description = "Allow restricted access to Jenkins"
  vpc_id      = aws_vpc.recarnation_vpc.id

  # SSH access only from your IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${local.my_ip}/32"]
  }

  # Jenkins UI access
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["${local.my_ip}/32"] # Restrict to your IP
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "jenkins_key" {
  key_name   = "jenkins-key-${substr(sha256(timestamp()), 0, 8)}"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_eip" "jenkins_eip" {
  instance = aws_instance.jenkins.id
  domain   = "vpc" # Replace deprecated 'vpc = true'
  tags = {
    Name = "Jenkins-EIP"
  }
}