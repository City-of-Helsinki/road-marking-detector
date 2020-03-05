#!/bin/bash

source ./terraform-utils.sh

ec2_public_ip=$(terraform_get aws_eip.server[0].public_ip)
ssh -i instance-private.key ubuntu@$ec2_public_ip "$@"
