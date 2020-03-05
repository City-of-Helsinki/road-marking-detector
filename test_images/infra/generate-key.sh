#!/bin/bash

if [ ! -f ./instance-private.key ] || [ ! -f ./instance-public.key ]; then
  [ -f ./instance-private.key ] && chmod +w ./instance-private.key
  if ! which ssh-keygen > /dev/null; then
    echo "ssh-keygen is not found in your PATH"
    exit 1
  else
    echo y | ssh-keygen -b 2048 -t rsa -f ./instance-private.key -q -N "" -C "instance"
    mv ./instance-private.key.pub ./instance-public.key
  fi
  chmod 400 ./instance-private.key
fi
