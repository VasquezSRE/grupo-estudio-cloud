#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <ALB_URL>"
  exit 1
fi

while true; do
  curl -s $1 > /dev/null
  echo "Request sent to $1"
  sleep 0.1
done
