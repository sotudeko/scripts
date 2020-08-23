#!/bin/bash

image=$1
version=$2

nxrm3_image=sola.local:8882/${image}:${version}

scan_name=${image}${version}
rm -rf ${scan_name}
mkdir ${scan_name}

docker pull ${nxrm3_image}

./clair-scanner --ip host.docker.internal -r ./${scan_name}/clair-scanner-output.json ${nxrm3_image}

iqscan ${scan_name} ./${scan_name}


