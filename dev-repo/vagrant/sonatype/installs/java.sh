#!/usr/bin/env bash

version=$(grep java /vagrant/installs/versions | cut -f2 -d':')

javafile_name="jdk-${version}-linux-x64.rpm"

javafile_url="http://download.oracle.com/otn-pub/java/jdk/8u162-b12/0da788060d494f5095bf8624735fa2f1"

cd /vagrant/packages

if [[ ! -f "./${javafile_name}" && -x "/usr/bin/wget" ]]; then
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "${javafile_url}/${javafile_name}"
fi

yum -y localinstall ${javafile_name}



