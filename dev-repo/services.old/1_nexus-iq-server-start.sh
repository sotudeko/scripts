#!/bin/bash

cd /opt/nxiq
java -jar nexus-iq-server server config.yml
echo http://localhost:8070
