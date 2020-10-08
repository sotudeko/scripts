#!/bin/bash

cd /Users/sotudeko/Development/awx/installer
ansible-playbook -i inventory -e docker_registry_password=password install.yml

#docker ps
#docker logs -f awx_task

