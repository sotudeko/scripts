#!/bin/bash

docker images | grep hackable
docker tag f8721e73eddb sola.local:8881/hackable:1.1
docker push sola.local:8881/hackable:1.1

