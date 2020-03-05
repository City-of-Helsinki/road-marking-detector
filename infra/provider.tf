terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version    = "2.31.0"
}

provider "null" {
  version = "2.1.2"
}

provider "archive" {
  version = "1.3.0"
}

provider "template" {
  version = "2.1.2"
}

provider "local" {
  version = "1.4.0"
}
