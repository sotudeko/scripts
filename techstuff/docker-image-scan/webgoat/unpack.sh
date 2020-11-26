#!/bin/bash

application_name=$1
image_name=$2

docker save -o ${application_name}.tar ${image_name}

