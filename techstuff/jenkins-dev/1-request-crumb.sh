#!/bin/bash

curl -v -X GET http://sola.local:8080/crumbIssuer/api/json --user solao:solao | python -m json.tool



