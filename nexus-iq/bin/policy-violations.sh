#!/bin/bash

policyId=$1

curl -u admin:admin123 -X GET http://localhost:8070/api/v2/policyViolations?p=${policyId} | python -m json.tool


