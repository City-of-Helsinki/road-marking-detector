data "aws_ami" "ubuntu-18_04-ml" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["*Deep Learning AMI (Ubuntu 18.04) Version 26.0*"]
  }
}

data "aws_availability_zones" "available" {}
