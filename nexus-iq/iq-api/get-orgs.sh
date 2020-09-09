#!/bin/bash

curl -u admin:admin123 -X GET 'http://localhost:8070/api/v2/organizations' | python -m json.tool


