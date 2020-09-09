#!/bin/bash

period=$1
inputfile=${1}.json

#curl -u admin:admin123 -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d@sm.json  "http://localhost:8070/api/v2/reports/metrics"

#curl -u admin:admin123 -X POST -H "Accept: text/csv" -H "Content-Type: application/json" -d@${inputfile}  "http://localhost:8070/api/v2/reports/metrics"

#curl -n -X POST -H "Accept: text/csv" -H "Content-Type: application/json" -d@${inputfile}  "http://localhost:8070/api/v2/reports/metrics"
curl -n -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d@${inputfile}  "http://localhost:8070/api/v2/reports/metrics"

