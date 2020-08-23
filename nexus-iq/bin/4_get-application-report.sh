#!/bin/sh

# appPublicId=$1
# reportId=$2

# curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications/${appPublicId}/reports/${reportId} | python -m json.tool

#curl --silent -u admin:admin123 -X GET http://localhost:8070/api/v2/applications/webgoat-ci/reports/45d74e009e184c62aae25181abea4d3c

applicationName=$1
reportId=$2

iqhost=http://localhost:8070
dataReportUri=api/v2/applications
uiReportUri=ui/links/application

dataReport=${iqhost}/${dataReportUri}/${applicationName}/reports/${reportId}
uiReport=${iqhost}/${uiReportUri}/${applicationName}/report/${reportId}

curl --silent -u admin:admin123 -X GET ${dataReport} | python -m json.tool
