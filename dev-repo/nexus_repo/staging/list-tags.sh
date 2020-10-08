#!/bin/bash

curl -s -X GET --user admin:admin123 http://localhost:8081/service/rest/v1/tags | python -m json.tool
