#!/bin/bash

jobname="Route-to-Live"
jenkins_crumb=dfab49d8f2e4fad470129cd21a75ce94

curl -X POST http://sola.local:8080/job/Route-To-Live/job/WebGoat-Build/buildWithParameters -H "Jenkins-Crumb: ${jenkins_crumb}" --user solao:solao --data-urlencode json='{"parameter": [{"BUILD_VERSION":"3.4.4"}]}'

#curl -X POST http://localhost:8080/job/${jobname}/build -H "Jenkins-Crumb: ${jenkins_crumb}" --user solao:solao --data-urlencode json='{"parameter": [{"build_version":"3.4.4"}]}'




