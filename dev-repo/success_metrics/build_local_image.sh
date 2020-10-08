#!/bin/bash

version=latest
iq_url=http://sola.local:8070

#git clone <repo>
#cd repo

#== Build image for executive and table reports script

#docker build -f Dockerfile -t iq_success_metrics:${version} .

#== Run the application to create the JSON file

#mkdir /tmp/output

#docker run --name iq_success_metrics --rm -it -v /tmp/output:/usr/src/app/output iq_success_metrics:${version} success_metrics.py -u ${iq_url} -a admin:admin123

#== Run the application to produce the executive report

docker run --name iq_success_metrics --rm -it -v /tmp/output:/usr/src/app/output iq_success_metrics:${version} reports.py -f /usr/src/app/output/successmetrics.json -e

#== Run the application to produce the tables report

docker run --name iq_success_metrics --rm -it -v /tmp/output:/usr/src/app/output iq_success_metrics:${version} reports.py -f /usr/src/app/output/successmetrics.json -t



