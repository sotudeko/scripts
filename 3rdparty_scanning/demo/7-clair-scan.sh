#!/bin/bash

./clair-scanner --ip host.docker.internal -r ./scanfiles/clair-scanner-output.json hackable:latest

