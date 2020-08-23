!#/bin/bash

curl -i -X POST -u admin:admin123 -H 'Content-Type: application/json' -d @./tag.json http://localhost:8081/service/rest/beta/tags
