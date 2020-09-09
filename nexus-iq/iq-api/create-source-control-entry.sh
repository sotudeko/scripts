#!/bin/bash

iqUrl=http://localhost:8070
gitRepo=http://github.com/sotudeko/webgoat2
username=admin
passwd=admin123

tok=73b9cd98e6f5d08a6e905e991cf427b9bbde0e75
appId=a1ba6ad8f05445a0ae5b79f9316a9d95

# curl -u ${username}:${passwd} \
# -d "{\"applicationId\": \"${appId}\", \"repositoryUrl\": \"${gitRepo}\", \"token\": \"${tok}\"}" \
# -H "Content-Type: application/json" \
# -X POST ${iqUrl}/api/v2/sourceControl/${appId}

curl -s -u ${username}:${passwd} ${iqUrl}/api/v2/sourceControl/${appId} | python -m json.tool