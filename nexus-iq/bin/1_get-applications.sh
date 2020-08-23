#!/bin/sh

curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications | python -m json.tool

