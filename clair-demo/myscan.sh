#!/bin/bash

docker run -p 5432:5432 -d --name db arminc/clair-db:2019-11-11

docker run -p 6060:6060 -p 6061:6061 --link db:postgres -d --name clair arminc/clair-local-scan:v2.0.8_0ed98e9ead65a51ba53f7cc53fa5e80c92169207

git clone https://github.com/sonatype-nexus-community/struts2-rce

cd ./struts2-rce
mvn clean package

cd ./struts2-rce
docker build -t hackable .

docker images | grep hackable
docker tag f8721e73eddb sola.local:8881/hackable:1.1
docker push sola.local:8881/hackable:1.1

docker save -o ./scanfiles/output.tar hackable
./clair-scanner --ip host.docker.internal -r ./scanfiles/clair-scanner-output.json hackable:latest

iqscan appname ./scanfiles
