resource "aws_route_table" "infrastructure_route_table" {
  vpc_id = aws_vpc.infrastructure_vpc.id

  route {
    //associated subnet can reach everywhere
    cidr_block = "0.0.0.0/0"
    //CRT uses this IGW to reach internet
    gateway_id = aws_internet_gateway.devops_pipeline_igw.id
  }

}

# attach jenkins subnet to an internet gateway
resource "aws_route_table_association" "route-jenkins-subnet-to-igw" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.infrastructure_route_table.id
}

# attach jenkins subnet to an internet gateway
resource "aws_route_table_association" "route-ec2-1-subnet-to-igw" {
  subnet_id      = aws_subnet.public_subnet_1_ecs.id
  route_table_id = aws_route_table.infrastructure_route_table.id
}

# attach jenkins subnet to an internet gateway
resource "aws_route_table_association" "route-ec2-2-subnet-to-igw" {
  subnet_id      = aws_subnet.public_subnet_2_ecs.id
  route_table_id = aws_route_table.infrastructure_route_table.id
}
