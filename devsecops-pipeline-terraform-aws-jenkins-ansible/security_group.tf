#Create a security  group for Jenkins node to allow traffic on port 22 and 8080
resource "aws_security_group" "jenkins-sg" {
  name        = "jenkins-sg"
  description = "Security from who allow inbound traffic on port 22 and 8080"
  vpc_id      = aws_vpc.infrastructure_vpc.id

  # dynamic block who create two rules to allow inbound traffic on port 22 and 8080
  dynamic "ingress" {
    for_each = var.inbound_port_jenkins_ec2
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}


#Create a security  group for database to allow traffic on port 3306 and from ec2 production security group
resource "aws_security_group" "sonarqube-sg" {
  name        = "sonarqube-sg"
  description = "security  group for sonarqube server"
  vpc_id      = aws_vpc.infrastructure_vpc.id

  dynamic "ingress" {
    for_each = var.inbound_port_jenkins_sonarqube
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# resource "aws_security_group" "database-sg" {
#   name        = "database-sg"
#   description = "security  group for database to allow traffic on port 3306 and from ec2 production security group"
#   vpc_id      = aws_vpc.infrastructure_vpc.id

#   ingress {
#     description = "Allow traffic from port 3306 and from ec2 production security group"
#     from_port   = 3306
#     to_port     = 3306
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = -1
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }