#!/bin/bash

printf "Get Component\n"

downloadPath=$1
artefactName=`basename ${downloadPath}`

endpoint=/service/rest/v1/components
host=localhost:8081

curl -o ${artefactName} ${downloadPath}

