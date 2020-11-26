#!/bin/bash

curl -v -u admin:admin123 -X POST 'http://localhost:8081/service/rest/v1/components?repository=mvn-releases' -F maven2.groupId=org.test -F maven2.artifactId=webwolf -F maven2.version=1.1 -F maven2.asset1=@../scan-artifacts/java/webwolf-8.0.0.M21.jar -F maven2.asset1.extension=jar -F maven2.generate-pom=true


