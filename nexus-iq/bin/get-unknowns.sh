#!/bin/bash

curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications?publicId=simple-app | python -m json.tool
curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/reports/applications/f88b403ec839417a8054743e492e1169 | python -m json.tool
curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications/simple-app/reports/d2536952932640d7b7871f74b07ff735| python -m json.tool
