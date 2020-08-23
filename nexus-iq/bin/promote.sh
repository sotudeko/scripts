#!/bin/bash

appId=$1

curl -u admin:admin123 -X POST -H "Content-Type: application/json" -d@promote-data.json  "http://localhost:8070/api/v2/evaluation/applications/${appId}/promoteScan"

