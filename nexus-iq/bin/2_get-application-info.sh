#!/bin/sh

appPublicId=$1

curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications?publicId=${appPublicId} | python -m json.tool

