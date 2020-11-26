#!/bin/bash

docker build -t webgoat-docker .  
docker images
docker tag 74749f2e7576 webgoat-docker:1.1

