variable "company" {
  description = "Name of the company"
  default     = "Integrify"
}

variable "project" {
  description = "Name of the project"
  default     = "hel-pedestor"
}

variable "environment" {
  description = "Name of the environment"
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "AWS access key"
}

variable "aws_secret_key" {
  description = "AWS sercret key"
}

variable "ec2_server_port" {
  description = "Notebook port"
  default     = 8080
}

variable "ec2_instance_count" {
  description = "Number of instances"
  default     = 1
}

variable "ec2_instance_type" {
  description = "Type of EC2 instance"
  default     = "p3.2xlarge"
}

variable "vpc_cidr" {
  description = "CIDR for the main VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDRs for public subnets"
  type        = list(string)
  default = [
    "10.0.1.0/24"
  ]
}

variable "private_subnet_cidrs" {
  description = "CIDR for private subnet"
  type        = list(string)
  default = [
    "10.0.3.0/24"
  ]
}
