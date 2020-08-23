#!/bin/bash

#docker pull cmorenoserrano/iq_success_metrics:latest

#rm -rf /tmp/sm_output

#docker run --name iq_success_metrics --rm -it -v /tmp/sm_output:/usr/src/app/output cmorenoserrano/iq_success_metrics:latest success_metrics.py -u 'http://sola.local:8070' -a admin:admin123 -s 50 -r

#docker run --name iq_success_metrics --rm -it -v /tmp/sm_output:/usr/src/app/output cmorenoserrano/iq_success_metrics:latest reports.py -f /usr/src/app/output/successmetrics.json -e

#docker run --name iq_success_metrics --rm -it -v /tmp/sm_output:/usr/src/app/output cmorenoserrano/iq_success_metrics:latest reports.py -f /usr/src/app/output/successmetrics.json -r

docker run --name iq-success-metrics --rm -it -v /tmp/sm_output:/usr/src/app/output sonatypecommunity/iq-success-metrics:latest success_metrics.py -u http://sola.local:8070 -a admin:admin123 -s 50 -r


