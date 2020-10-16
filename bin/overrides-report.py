import json
import requests
import os
import os.path
import sys
import csv
import shutil

iqurl = sys.argv[1]
iquser = sys.argv[2]
iqpwd = sys.argv[3]
md = ""


if len(sys.argv) > 4:
	md = sys.argv[4]

overridesJsonfile = 'overrides.json'
overridesCsvfile = 'overrides.csv'

reportsJsonfile = 'applicationreports.json'
reportsUrlsCsvfile = 'applicationreporturls.csv'

rawComponentsDataByReportCsvfile = 'rawcomponentsdatabyreport.csv'
rawData = []

policyViolationsByReportCsvfile = 'policyviolationsbyreport.csv'
policyViolations = []

def getNexusIqData(api):
	url = "{}{}" . format(iqurl, api)
	# print (url)

	req = requests.get(url, auth=(iquser, iqpwd), verify=False)

	if req.status_code == 200:
		res = req.json()
	else:
		res = "Error fetching data"

	return res


def getCVEValue(d):
	cve = "none"

	if type(d) is dict:
		cve = d["value"]

	return(cve)


def getPolicyIds(data):
	policyIds = ""
	policies = data['policies']

	for policy in policies:
		name = policy["name"]
		id = policy["id"]

		if name == "Security-Critical" or name == "Security-High" or name == "Security-Medium" or name == "Security-Malicious" or name == "License-Banned" or name == "License-None" or name == "License-Copyleft":
			policyIds += "p=" + id + "&"

	result = policyIds.rstrip('&')

	return result


def writeOverridesCsvfile(overrides):

	components = overrides['securityOverrides']

	with open(overridesCsvfile, 'w') as fd:
			fd.write("Hash,PackageUrl,CVE,Status\n")
			for component in components:
				comment = component["comment"]
				referenceId = component["referenceId"]
				status = component["status"]

				for affectedComponent in component["currentlyAffectedComponents"]:
					packageUrl = affectedComponent["packageUrl"]
					proprietary = affectedComponent["proprietary"]
					thirdParty = affectedComponent["thirdParty"]
					hash = affectedComponent["hash"]

				line = hash + "," + packageUrl +  "," + referenceId + "," + status + "," + "\n"
				fd.write(line)

	print(overridesCsvfile)

	return


def writeJsonfile(jsonFile, jsonData):
	with open(jsonFile, 'w') as fd:
			json.dump(jsonData, fd)

	print(jsonFile)

	return


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])


def writeReportsUrls(applicationEvaluations):
	with open(reportsUrlsCsvfile, 'w') as fd:
			for applicationEvaluation in applicationEvaluations:
				applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
				applicationReportUrl = applicationEvaluation["reportDataUrl"]

				line = applicationName + "," + applicationReportUrl + "\n"
				fd.write(line)

	print(reportsUrlsCsvfile)

	return


def writeReportsCsv(applicationEvaluations):
	with open(policyViolationsByReportCsvfile, 'w') as fd:
			fd.write('ApplicationName,Hash,PackageUrl,PolicyName,Waived\n')
			fd.close()
	
	with open(reportsUrlsCsvfile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			lineCount = 0
			for row in r:
				applicationName = row[0]
				url = row[1]

				writeRawComponentsDataByReport(applicationName, url)
				writePolicyViolationsByReport(applicationName, url)

	print(policyViolationsByReportCsvfile)
	print(rawComponentsDataByReportCsvfile)
	
	return


def writeRawComponentsDataByReport(applicationName, url):
	rawData = getNexusIqData('/' + url)

	components = rawData["components"]

	with open(rawComponentsDataByReportCsvfile, 'a') as fd:
			for component in components:
				hash = component["hash"]
				packageUrl  = component["packageUrl"]

				if not packageUrl:
					packageUrl = "none"

				if type(component["securityData"]) is dict:
					securityIssues = component["securityData"]["securityIssues"]

					if len(securityIssues) > 0:
						issues = ""
						for securityIssue in securityIssues:
							issues += securityIssue["reference"] + ":" + securityIssue["status"] + ";"
						issues = issues[:-1]
				
						if securityIssue["status"] != 'Open':
							line = applicationName + "," + hash + "," + packageUrl + "," + issues + "\n"
							fd.write(line)
				else:
					line = applicationName + "," + hash + "," + packageUrl + "," + 'no security issues' + "\n"
					#fd.write(line)


	return


def writePolicyViolationsByReport(applicationName, url):
	policyReportDataUrl = url.replace('/raw', '/policy')
	policyReportData = getNexusIqData('/' + policyReportDataUrl)

	components = policyReportData["components"]
	application = policyReportData["application"]
	counts = policyReportData["counts"]
	reportTime = policyReportData["reportTime"]
	initiator = policyReportData["initiator"]

	with open(policyViolationsByReportCsvfile, 'a') as fd:
			for component in components:
				hash = component["hash"]
				packageUrl  = component["packageUrl"]

				if not packageUrl:
					packageUrl = "none"

				policyName = ""
				waived = ""

				violations = component['violations']

				for violation in violations:
					policyName = violation['policyName']
					policyId = violation['policyId']
					waived = violation['waived']
					grandfathered = violation['grandfathered']
					policyThreatCategory = violation['policyThreatCategory']
					policyViolationId = violation['policyViolationId']
					line = applicationName + "," + hash + "," + packageUrl + "," + policyName + "," + str(waived) + "\n"
					fd.write(line)

	return



def loadPolicyViolationsByReport():
	with open(policyViolationsByReportCsvfile, 'r') as fd:
		for line in fd.readlines():
				policyViolations.append(line)

	return


def componentMapper():
	with open(overridesCsvfile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			lineCount = 0
			for row in r:
				if lineCount == 0:
					lineCount += 1
				else:
					lineCount += 1
					line = '{}:{}:{}:{}'.format(row[0], row[1], row[2], row[3])
					print (line)

					findHash(row[0])

	return


def findHash(hash):
	for i in policyViolations:
		i = i[:-1]

		if hash in i:
			print('  ' + i)

	return




def main():

	if md == 'data':

		# overrides
		overrides = getNexusIqData('/api/v2/securityOverrides')
		writeJsonfile(overridesJsonfile, overrides)
		writeOverridesCsvfile(overrides)

		# report data
		applicationEvaluations = getNexusIqData('/api/v2/reports/applications')
		writeJsonfile(reportsJsonfile, applicationEvaluations)
		writeReportsUrls(applicationEvaluations)
		writeReportsCsv(applicationEvaluations)

	# analyse
	loadPolicyViolationsByReport()
	componentMapper()


if __name__ == '__main__':
	main()
