resource "aws_instance" "jenkins_instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.jenkins-sg.id]
  key_name               = var.key_name
  user_data              = file("install_script_jenkins_instance.sh")
  iam_instance_profile   = aws_iam_instance_profile.ec2_jenkins_instance_profile.name # access to s3 bucket

  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "jenkins"
  }
}

resource "aws_instance" "sonarqube_server" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.sonarqube-sg.id]
  key_name               = var.key_name
  user_data              = file("install_script_sonarqube.sh")

  tags = {
    Name = "Sonarqube"
  }
}

#Create S3 bucket for your application Artifacts not open to the public
resource "aws_s3_bucket" "jenkins_bucket" {
  bucket = "jenkins-bucket-for-artifact-devsecops-pipeline"
  tags = {
    description = "Private bucket to hold Jenkins artifacts"
    name        = "jenkins_bucket"
  }
}

# resource "aws_db_subnet_group" "database_subnet" {
#   name       = "db subnet"
#   subnet_ids = [aws_subnet.database_private_subnet.id, aws_subnet.database_read_replica_private_subnet.id]
# }

# resource "aws_db_instance" "rds_master" {
#   identifier              = "master-rds-instance"
#   allocated_storage       = 10
#   engine                  = "mysql"
#   engine_version          = "5.7.37"
#   instance_class          = "db.t3.micro"
#   db_name                 = "db_assiduite"
#   username                = var.db_user
#   password                = var.db_password
#   backup_retention_period = 7
#   multi_az                = false
#   availability_zone       = var.availability_zone[2]
#   db_subnet_group_name    = aws_db_subnet_group.database_subnet.id
#   skip_final_snapshot     = true
#   vpc_security_group_ids  = [aws_security_group.database-sg.id]
#   storage_encrypted       = true

#   tags = {
#     Name = "my-rds-master"
#   }
# }

resource "aws_ecr_repository" "ecr" {
  name                 = "assiduite"
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "KMS"
  }
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = {
    "Name" = "ecr_repo"
  }
}
