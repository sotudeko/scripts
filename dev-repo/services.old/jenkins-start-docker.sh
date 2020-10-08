#!/bin/bash

docker run \
  --rm \
  -u root \
  -p 8089:8080 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$HOME":/home \
  jenkinsci/blueocean
  
