#!/bin/bash

printf "Listing Components\n"

repository=$1

endpoint=/service/rest/v1/components
host=localhost:8081

url=http://${host}${endpoint}

curl -u admin:admin123 -X GET ${url}?repository=${repository}





