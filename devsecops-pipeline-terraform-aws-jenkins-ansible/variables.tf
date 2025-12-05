variable "inbound_port_jenkins_ec2" {
  type        = list(any)
  default     = [22, 8080, 9000, 8090]
  description = "inbound port allow on jenkins node"
}

variable "inbound_port_jenkins_sonarqube" {
  type        = list(any)
  default     = [22, 9000]
  description = "inbound port allow on sonarqube instance"
}

variable "inbound_port_production_ec2" {
  type        = list(any)
  default     = [22, 8080, 80]
  description = "inbound port allow on production node"
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}

variable "ami" {
  type    = string
  default = "ami-0cf13cb849b11b451"
}

variable "key_name" {
  type    = string
  default = "kemane"
}

variable "availability_zone" {
  type    = list(string)
  default = ["eu-north-1a", "eu-north-1b", "eu-north-1c"]
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "subnet_cidrs" {
  type        = list(string)
  description = "list of all cidr for subnet"
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24", "10.0.4.0/24", "10.0.5.0/24"]
}

variable "target_application_port" {
  type    = string
  default = "80"
}

variable "db_name" {
  type    = string
  default = "wordpressdb"
}

variable "db_user" {
  type    = string
  default = "admin"
}

variable "db_password" {
  type    = string
  default = "Wordpress-AWS2Tier"
}
