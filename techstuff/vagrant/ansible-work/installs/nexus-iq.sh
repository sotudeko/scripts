#!/usr/bin/env bash

version=$(grep nexus_iq /vagrant/installs/versions | cut -f2 -d':')

nexus_iq_version=${version}

tools_dir="/opt/sonatype"
iq_server_dir=${tools_dir}/nexus-iq-server

if [[ ! -d ${iq_server_dir} ]]; then
    mkdir -p ${iq_server_dir}
    tar xvzf /vagrant/packages/nexus-iq-server-${nexus_iq_version}-bundle.tar.gz -C ${iq_server_dir} 
    sudo cp /vagrant/scripts/nexus-iq-server ${iq_server_dir}
    sudo ln -s ${iq_server_dir}/nexus-iq-server /etc/init.d/nexus-iq-server
    cd /etc/init.d
    sudo chkconfig --add nexus-iq-server
    sudo chkconfig --levels 345 nexus-iq-server on
    sudo service nexus-iq-server start
else
    echo "Nexus IQ Server is running"
fi

