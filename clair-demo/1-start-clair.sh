#!/bin/bash

docker run -p 5432:5432 -d --name db arminc/clair-db:2019-11-11

docker run -p 6060:6060 -p 6061:6061 --link db:postgres -d --name clair arminc/clair-local-scan:v2.0.8_0ed98e9ead65a51ba53f7cc53fa5e80c92169207

 