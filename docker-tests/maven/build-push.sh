#!/bin/bash

tag=$1
version=$2

if [[ $# -ne 2 ]]; then
  echo "usage: $0 tag version-number"
	exit -1
fi

docker build -t sola.local:9002/${tag}:${version} .
docker push sola.local:9002/${tag}:${version} 


