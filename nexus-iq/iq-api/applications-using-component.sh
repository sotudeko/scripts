#¡/bin/bash

groupId=org.so
artifactId=wolf
version=1.2
type=jar

#curl -u admin:admin123 -X GET -H "Content-Type: application/json" "http://localhost:8070/api/v2/search/component?stageId=build&packageUrl=pkg:maven/commons-beanutils/commons-beanutils@1.6?type=jar"

curl -s -u admin:admin123 -X GET -H "Content-Type: application/json" "http://localhost:8070/api/v2/search/component?stageId=build&packageUrl=pkg:maven/${groupId}/${artifactId}@${version}?type=${type}" | python -m json.tool



