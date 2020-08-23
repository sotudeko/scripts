#¡/bin/bash

groudId=tomcat
artifactId=tomcat-util
version=5.5.23
extension=jar

groudId=org.demo
artifactId=gzip
version=1.0
extension=zip

#curl -u admin:admin123 -X POST -H "Content-Type: application/json" -d '{"components":[{"hash": null,"componentIdentifier": {"format":"maven","coordinates": {"artifactId":"tomcat-util","extension":"jar","groupId":"tomcat","version":"5.5.23"}}}]}' 'http://localhost:8070/api/v2/components/details' | python -m json.tool

#curl -u admin:admin123 -X POST -H "Content-Type: application/json" -d '{"components":[{"hash": "ed3c2b07d1b16ec11440","componentIdentifier": {"format":"maven","coordinates": {"artifactId":"commons-beanutils","extension":"jar","groupId":"commons-beanutils","version":"1.6"}}}]}' 'http://localhost:8070/api/v2/components/details' | python -m json.tool

#curl -u admin:admin123 -X POST -H "Content-Type: application/json" -d '{"components":[{"hash": null,"componentIdentifier": {"format":"maven","coordinates": {"artifactId":"commons-beanutils","extension":"jar","groupId":"commons-beanutils","version":"1.6"}}}]}' 'http://localhost:8070/api/v2/components/details' | python -m json.tool

#curl -u admin:admin123 -X POST -H "Content-Type: application/json" -d '{"components":[{"hash": null,"componentIdentifier": {"format":"maven","coordinates": {"artifactId":"commons-beanutils","extension":"jar","groupId":"commons-beanutils","version":"1.6"}}}]}' 'http://localhost:8070/api/v2/components/details' | python -m json.tool

curl -u admin:admin123 -X GET -H "Content-Type: application/json" "http://localhost:8070/api/v2/search/component?stageId=build&packageUrl=pkg:maven/commons-beanutils/commons-beanutils@1.6?type=jar"


