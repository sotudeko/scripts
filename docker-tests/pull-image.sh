#!/bin/bash

tag=$1
version=$2

if [[ $# -ne 1 ]]; then
  echo "usage: $0 tag [version-number]"
	exit -1
fi

if [[ $# -eq 1 ]]; then
  version=latest
fi

docker pull sola.local:9001/${tag}:${version} 

