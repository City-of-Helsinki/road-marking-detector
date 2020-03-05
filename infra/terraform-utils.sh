#!/bin/bash

set -e

if ! echo true | terraform console|grep -v "state lock." &> /dev/null; then
  echo "Terraform has not been initialized properly"
  exit 1
fi

terraform_get() {
  echo $(echo "$1"|terraform console|grep -v "state lock.")
}
