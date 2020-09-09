#!/bin/bash

iqurl=http://localhost:8070
iquser=admin
iqpasswd=admin123
periodfile=${1}.json

outputfile=${1}-data.json

curl -u ${iquser}:${iqpasswd} -X POST -H "Accept: application/json" -H "Content-Type: application/json" -o ${outputfile} -d@${periodfile} ${iqurl}/api/v2/reports/metrics 

echo "Created file ${outputfile}"


