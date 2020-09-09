#¡/bin/bash

curl -u admin:admin123 -X GET "http://localhost:8070/api/v2/search/component?stageId=build&componentIdentifier=%7B%22format%22%3A%22maven%22%2C%22coordinates%22%3A%7B%22groupId%22%3A%22commons-beanutils%22%2C%22artifactId%22%3A%22*%22%2C%22version%22%3A%22*%22%2C%22extension%22%3A%22*%22%2C%22classifier%22%3A%22*%22%7D%7D" | python -m json.tool | grep applicationName
