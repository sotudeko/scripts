#!/bin/bash

applicationName=$1
reportId=$2
curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications/${applicationName}/reports/${reportId} | python -m json.tool



