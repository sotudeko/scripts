#!/usr/bin/env bash

yum -y install wget
yum -y install ansible
yum -y install git-all
yum -y install maven
yum -y install python-devel 
yum -y install openldap-devel
yum -y install gcc openssl-devel bzip2-devel

sudo yum install yum-utils device-mapper-persistent-data lvm2
   25  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   26  sudo yum install docker-ce
   27  sudo systemctl start docker
   28  docker run --name my-openldap-container --detach osixia/openldap:1.2.1
   29  sudo docker run --name my-openldap-container --detach osixia/openldap:1.2.1
   30  ansible-playbook ldap.yml 
   31  docker ps
   32  sudo docker ps
   33  history








