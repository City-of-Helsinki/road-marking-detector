#!/bin/bash

filter_string() {
  echo $(echo $1|tr '[:upper:]' '[:lower:]'|sed -e 's/[^a-z0-9\-]/-/g')
}

terraform_get() {
  echo $(echo "$1"|terraform console|grep -v "state lock.")
}

AWS_ACCESS_KEY_ID=$(terraform_get var.aws_access_key)
AWS_SECRET_ACCESS_KEY=$(terraform_get var.aws_secret_key)
REGION=$(terraform_get var.aws_region)
ENV=$(terraform_get var.environment)
PROJECT=$(terraform_get var.project)
COMPANY=$(terraform_get var.company)
BUCKET=$(filter_string "$COMPANY")-$(filter_string "$PROJECT")-terraform-state-${ENV}

if [ $(echo $BUCKET|wc -c) -gt 63 ]; then
  echo "Bucket name ($BUCKET) can't be longer than 63 characters (S3 limit)."
  exit 1
fi

DYNAMODB_TABLE=$(filter_string "$PROJECT")-terraform-state-lock-$(filter_string "$ENV")

aws s3api head-bucket --bucket $BUCKET --region $REGION > /dev/null 2>&1
if [ "$?" != "0" ]; then
  echo "Creating S3 bucket $BUCKET in region $REGION"
  aws s3 mb s3://$BUCKET --region $REGION

  if [ "$?" != "0" ]; then
    echo "Failed to create bucket $BUCKET as it may already exist. Please choose a different name and try again."
    exit 1
  fi

  aws s3api put-bucket-versioning \
    --bucket $BUCKET \
    --versioning-configuration Status=Enabled
  if [ "$?" != "0" ]; then
    echo "WARNING: Failed to enable bucket versioning can not be enabled. Risk of losing state data. Please check and enable it manually."
  fi
fi

aws dynamodb describe-table --table-name $DYNAMODB_TABLE --region $REGION &> /dev/null
if [ "$?" != "0" ]; then
  echo "Creating DynamoDB table $DYNAMODB_TABLE for terraform file state locking"
  aws dynamodb create-table \
    --table-name $DYNAMODB_TABLE \
    --region $REGION \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

  if [ "$?" != "0" ]; then
    echo "Failed to create DynamoDB table."
    exit 1
  fi
fi

cat > backend.tf <<EOT
  terraform {
    backend "s3" {
      encrypt         = "true"
      region          = "$REGION"
      bucket          = "$BUCKET"
      key             = "${REGION}/${ENV}/terraform.tfstate"
      dynamodb_table  = "$DYNAMODB_TABLE"
    }
  }
EOT

terraform init \
  -backend-config="access_key=$AWS_ACCESS_KEY_ID" \
  -backend-config="secret_key=$AWS_SECRET_ACCESS_KEY"
