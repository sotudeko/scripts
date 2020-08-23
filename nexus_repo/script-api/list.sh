#/bin/bash

curl -s -u admin:admin123 -X GET http://localhost:8081/service/rest/v1/script | grep '"name"' | cut -f4 -d'"' 
