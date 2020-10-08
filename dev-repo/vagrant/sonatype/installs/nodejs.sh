#!/bin/bash

yum -y groupinstall 'Development Tools'
curl --silent --location https://rpm.nodesource.com/setup_9.x | sudo bash -
yum -y install nodejs

