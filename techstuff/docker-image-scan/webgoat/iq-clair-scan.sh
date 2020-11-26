#!/bin/bash

#docker run -p 5432:5432 -d --name db arminc/clair-db:2019-11-11
 
#docker run -p 6060:6060 -p 6061:6061 --link db:postgres -d --name clair arminc/clair-local-scan:v2.0.8_0ed98e9ead65a51ba53f7cc53fa5e80c92169207
 
#docker pull vulnerables/web-dvwa
 
#docker run -it --rm --name clair-scanner -p 9279:9279 -v ~/tmp/clair-scanner-output:/clair-scanner-output -v /var/run/docker.sock:/var/run/docker.sock ovotech/clair-scanner:06-11-2019 clair-scanner --ip=host.docker.internal -c http://host.docker.internal:6060 -r /clair-scanner-output/clair-scanner-output.json vulnerables/web-dvwa

docker pull sola.local:8882/webgoat-docker:1.0

docker run -it --rm --name clair-scanner -p 9279:9279 -v ~/tmp/clair-scanner-output:/clair-scanner-output -v /var/run/docker.sock:/var/run/docker.sock ovotech/clair-scanner:06-11-2019 clair-scanner --ip=host.docker.internal -c http://host.docker.internal:6060 -r /clair-scanner-output/clair-scanner-output.json sola.local:8882/webgoat-docker:1.0
