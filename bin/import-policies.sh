#!/bin/bash

policies=$1

curl -u admin:admin123 -H 'Cookie: CLM-CSRF-TOKEN=x' -H "Content-Type: multipart/form-data" -F "file=@${policies};type=application/json" -F "X-CSRF-TOKEN=x"  http://localhost:8070/rest/policy/organization/ROOT_ORGANIZATION_ID/import

