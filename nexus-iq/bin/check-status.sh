#!/bin/bash

appId=$1
scanId=$2

curl -u admin:admin123 -X GET http://localhost:8070/api/v2/evaluation/applications/${appId}/status/${scanId} | python -m json.tool


