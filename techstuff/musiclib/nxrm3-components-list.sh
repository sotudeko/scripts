#!/bin/bash

repo=$1
port=$2

url='localhost'
user=admin
passwd=admin123

uri=http://${url}:${port}/service/rest/v1/components

timestamp=$(date +'%d%m%Y-%H%M%S')
outputDir=/var/tmp/nxrm3-components/${timestamp}
mkdir -p ${outputDir}

outfile="${outputDir}/${url}_${port}"

outfile_json="${outfile}.json"
outfile_ids="${outfile}.ids.txt"

echo "get list of components from repository ${repo} at ${url}:${port}..."

curl -s -u ${user}:${passwd} -o ${outfile_json} -X GET "${uri}?repository=${repo}"

echo "--> ${outfile_json}"

grep id ${outfile_json} | cut -d'"' -f4 > ${outfile_ids}

numberOfComponents=$(wc -l < ${outfile_ids} | tr -d ' ')

echo "--> ${outfile_ids}"

echo "number of components: ${numberOfComponents}"

echo "get components..."

#curl -s -u ${user}:${passwd} -X GET "${uri}/${componentId}



