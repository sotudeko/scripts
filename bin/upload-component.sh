#!/bin/bash

filename=$1
version=$2
repoId=$3

repo="staging-development"
packaging=`basename ${filename}`

groupId=teamB.demo
artifactId=webgoat

mvn deploy:deploy-file -DgroupId=${groupId} -DartifactId=${artifactId} -Dversion=${version} -DgeneratePom=true -Dpackaging=${packaging} -DrepositoryId=${repoId} -Durl=http://localhost:8081/repository/${repo} -Dfile=${filename}



