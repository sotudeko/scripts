#!/bin/bash

repo=$1
tag=$2
groupId=$3
artifactId=$4
version=$5

curl -s -X POST -u admin:admin123 -H 'Content-Type: application/json' -H 'Accept: application/json' \
http://localhost:8081/service/rest/beta/tags/associate/${tag} \
-d repository=${repo} \
-d maven.groupId=${groupId} \
-d maven.artifactId=${artifactId} \
-d maven.baseVersion=${version}

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 
'http://localhost:8081/service/rest/beta/tags/associate/my-tag-2?repository=staging-dev&maven.groupId=WebGoat&maven.artifactId=WebGoat&maven.baseVersion=5.0'

curl -u admin:admin123 -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8081/service/rest/beta/tags/associate/my-tag-4?repository=staging-dev&maven.groupId=WebGoat&maven.artifactId=WebGoat&maven.baseVersion=5.0'
