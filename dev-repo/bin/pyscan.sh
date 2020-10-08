#!/bin/bash

app=$1
sfile=$2
user=admin
passwd=admin123

java -jar /opt/nexus-iq/nexus-iq-cli -D zip=whl -i ${app} -s http://localhost:8070 -a ${user}:${passwd} -t build ${sfile}
