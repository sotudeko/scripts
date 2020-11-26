#!/usr/bin/env bash

version=$(grep jenkins /vagrant/installs/versions | cut -f2 -d':')

jenkins_rpm="jenkins-${version}.noarch.rpm"

cd /vagrant/packages
yum -y localinstall ${jenkins_rpm}
service jenkins start





