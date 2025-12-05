resource "aws_vpc" "infrastructure_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = "true" #gives you an internal domain name
  enable_dns_hostnames = "true" #gives you an internal host name
  instance_tenancy     = "default"

  tags = {
    Name = "devops-pipeline-vpc"
  }
}

#It enables our vpc to connect to the internet
resource "aws_internet_gateway" "devops_pipeline_igw" {
  vpc_id = aws_vpc.infrastructure_vpc.id
  tags = {
    Name = "devops-pipeline-igw"
  }
}

#jenkins node public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.infrastructure_vpc.id
  cidr_block              = var.subnet_cidrs[0]
  map_public_ip_on_launch = "true" //it makes this a public subnet
  availability_zone       = var.availability_zone[0]
  tags = {
    Name = "Jenkins public subnet"
  }
}

resource "aws_subnet" "public_subnet_1_ecs" {
  vpc_id                  = aws_vpc.infrastructure_vpc.id
  cidr_block              = var.subnet_cidrs[1]
  map_public_ip_on_launch = "true" //it makes this a public subnet
  availability_zone       = var.availability_zone[1]
  tags = {
    Name = "ECS public subnet"
  }
}
resource "aws_subnet" "public_subnet_2_ecs" {
  vpc_id                  = aws_vpc.infrastructure_vpc.id
  cidr_block              = var.subnet_cidrs[2]
  map_public_ip_on_launch = "true" //it makes this a public subnet
  availability_zone       = var.availability_zone[2]
  tags = {
    Name = "ECS public subnet"
  }
}


#database read replica private subnet
resource "aws_subnet" "database_read_replica_private_subnet" {
  vpc_id                  = aws_vpc.infrastructure_vpc.id
  cidr_block              = var.subnet_cidrs[3]
  map_public_ip_on_launch = "false"
  availability_zone       = var.availability_zone[1]
  tags = {
    Name = "database read replica private subnet"
  }
}

#database private subnet
resource "aws_subnet" "database_private_subnet" {
  vpc_id                  = aws_vpc.infrastructure_vpc.id
  cidr_block              = var.subnet_cidrs[4]
  map_public_ip_on_launch = "false"
  availability_zone       = var.availability_zone[2]
  tags = {
    Name = "database private subnet"
  }
}
