#!/bin/bash

source ./terraform-utils.sh

aws_access_key=$(terraform_get var.aws_access_key)
aws_secret_key=$(terraform_get var.aws_secret_key)
aws_region=$(terraform_get var.aws_region)
ec2_id=$(terraform_get aws_instance.server[0].id)

AWS_ACCESS_KEY_ID=$aws_access_key \
AWS_SECRET_ACCESS_KEY=$aws_secret_key \
AWS_DEFAULT_REGION=$aws_region \
aws ec2 stop-instances \
  --instance-ids $ec2_id
