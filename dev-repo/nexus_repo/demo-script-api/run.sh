#!/bin/bash

scriptname=$1

if [[ -z "${scriptname}" ]]; then
curl -v -X POST -u admin:admin123 --header "Content-Type: text/plain" "http://localhost:8081/service/rest/v1/script/${scriptname}/run"
else
curl -v -X POST -u admin:admin123 --header "Content-Type: text/plain" -d @${scriptname}.json "http://localhost:8081/service/rest/v1/script/${scriptname}/run"
fi