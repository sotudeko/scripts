#!/bin/bash

curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' \
-F maven2.asset1=WebGoat-5.4.3.war \
-F maven2.groupId=WebGoat \
-F maven2.artifactId=WebGoat \
-F maven2.version=5.4.3 \
-F maven2.generate-pom=true \
-F maven2.packaging=war \
-F maven2.tag=my-test-tag \
http://localhost:8081/service/rest/beta/components?repository=staging-dev

