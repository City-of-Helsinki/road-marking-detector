terraform {
  backend "s3" {
    encrypt         = "true"
    region          = "us-east-1"
    bucket          = "integrify-hel-pedestor-terraform-state-dev"
    key             = "us-east-1/dev/terraform.tfstate"
    dynamodb_table  = "hel-pedestor-terraform-state-lock-dev"
  }
}
