#!/bin/bash


source ./terraform-utils.sh

ec2_dns=$(terraform_get aws_eip.server[0].public_dns)
open http://${ec2_dns}:8080
