#!/bin/bash

repo=$1
tag=$2

#curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8081/service/rest/beta/staging/move/staging-test?tag=jenkins-WebGoat-Example-Staging-Demo-33'

curl -u admin:admin123 -X POST --header "Content-Type: application/json" --header "Accept: application/json" "http://localhost:8081/service/rest/beta/staging/move/${repo}?tag=${tag}"

