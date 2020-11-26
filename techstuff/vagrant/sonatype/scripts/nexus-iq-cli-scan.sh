#!/bin/bash

sfile=$1
app=$2

JAR_FILE=nexus-iq-cli-1.45.0-01.jar

java -jar /opt/nexus-iq-cli/${JAR_FILE} -i ${app} -s http://localhost:8070 -a admin:admin123 -t build ${sfile}


