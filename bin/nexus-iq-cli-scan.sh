#!/bin/bash

app=$1
sfile=$2

if [ $# -eq 3 ]; then
  stage=$3
else
  stage=build
fi

debug=
user=admin
passwd=admin123
#iqserver=http://192.168.99.100:30070
iqserver=http://localhost:8070

java -jar /opt/nxiq/nexus-iq-cli -r out.json -i ${app} -s ${iqserver} -a ${user}:${passwd} -t ${stage} ${sfile} ${debug}

