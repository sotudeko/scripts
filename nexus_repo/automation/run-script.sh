#!/bin/bash

name=$1
datafile=$2

userid=admin
passwd=admin123
repoUrl="http://localhost:8081/service/rest/v1/script"

printf "Running Integration API Script $name\n\n"

curl -v -X POST -u ${userid}:${passwd} --header "Content-Type: text/plain" -d @$datafile "${repoUrl}/${name}/run"
