#!/bin/bash

container_ip=localhost
license_file=/vagrant/packages/sonatype-nexus-firewall-lifecycle-2017.lic

curl --fail -s -u 'admin:admin123' -F file=@$license_file http://${container_ip}:8070/rest/product/license >/dev/null

