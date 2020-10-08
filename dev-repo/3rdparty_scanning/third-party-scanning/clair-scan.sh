#!/bin/bash

image=vulnerables/web-dvwa
image=alpine:3.5

docker run -it --rm --name clair-scanner -p 9279:9279 -v ~/tmp/clair-scanner-output:/clair-scanner-output -v /var/run/docker.sock:/var/run/docker.sock ovotech/clair-scanner:06-11-2019 clair-scanner --ip=192.168.1.25 -c http://192.168.1.12:6060 -r /clair-scanner-output/clair-scanner-output.json ${image}
