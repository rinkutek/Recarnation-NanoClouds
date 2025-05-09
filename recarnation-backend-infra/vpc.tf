# Create a dedicated VPC
resource "aws_vpc" "recarnation_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "recarnation-vpc"
  }
}

# Create public subnets (required for Elastic Beanstalk)
resource "aws_subnet" "public" {
  count             = 2  # Minimum 2 for high availability
  vpc_id            = aws_vpc.recarnation_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "recarnation-public-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.recarnation_vpc.id
  cidr_block        = "10.0.${count.index + 3}.0/24" # e.g. 10.0.3.0/24, 10.0.4.0/24
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

# Internet Gateway for public subnets
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.recarnation_vpc.id
  tags = {
    Name = "recarnation-igw"
  }
}

# Route table for public subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.recarnation_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Data source to fetch available AZs
data "aws_availability_zones" "available" {
  state = "available"
}