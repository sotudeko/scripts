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

outputdir = './datafiles'

policyviolationsJsonfile = '{}/policyviolations.json'.format(outputdir)
policyviolationsCsvfile = '{}/policyviolations.csv'.format(outputdir)

overridesJsonfile = '{}/overrides.json'.format(outputdir)
overridesCsvfile = '{}/overrides.csv'.format(outputdir)

reportsJsonfile = '{}/applicationreports.json'.format(outputdir)
reportsUrlsCsvfile = '{}/applicationreporturls.csv'.format(outputdir)

rawComponentsDataByReportCsvfile = '{}/rawcomponentsdatabyreport.csv'.format(outputdir)
policyViolationsByReportCsvfile = '{}/policyviolationsbyreport.csv'.format(outputdir)

outputdir = './datafiles'




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


def writePolicyviolationsCsvFile(policyViolations):

	applicationViolations = policyViolations['applicationViolations']

	with open(policyviolationsCsvfile, 'w') as fd:
			fd.write("Hash,PackageUrl,PolicyName,CVE,ApplicationName,OpenTime,Stage\n")
			for applicationViolation in applicationViolations:
				applicationPublicId = applicationViolation["application"]["publicId"]

				policyViolations = applicationViolation["policyViolations"]
				for policyViolation in policyViolations:
					stage = policyViolation["stageId"]
					openTime = policyViolation["openTime"]
					policyName = policyViolation["policyName"]
					policyViolationId = policyViolation["policyViolationId"]
					packageUrl = policyViolation["component"]["packageUrl"]
					hash = policyViolation["component"]["hash"]
					proprietary = policyViolation["component"]["proprietary"]

					constraintViolations = policyViolation["constraintViolations"]

					for constraintViolation in constraintViolations:
						values = ""

						reasons = constraintViolation["reasons"]
						for reason in reasons:
							v = getCVEValue(reason["reference"])
							values += v+":"
						
						values = values[:-1]
						line = hash + "," + packageUrl + "," + policyName + "," + values + "," + applicationPublicId + "," + openTime + "," + stage + "\n"

						fd.write(line)

	print(policyviolationsCsvfile)
	return


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
	# with open(rawComponentsDataByReportCsvfile, 'w') as fd:
	# 		fd.write('ApplicationName,Hash,PackageUrl,Issues\n')
	# 		fd.close()

	# with open(policyViolationsByReportCsvfile, 'w') as fd:
	# 		fd.write('ApplicationName,Hash,PackageUrl,PolicyName,Waived\n')
	# 		fd.close()

	with open(reportsUrlsCsvfile, 'w') as fd:
			for applicationEvaluation in applicationEvaluations:
				applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
				applicationReportUrl = applicationEvaluation["reportDataUrl"]

				line = applicationName + "," + applicationReportUrl + "\n"
				fd.write(line)

				# rawData = getNexusIqData('/' + applicationReportUrl)
				# writeRawComponentsDataByReport(applicationName, rawData)

				# policyReportDataUrl = applicationReportUrl.replace('/raw', '/policy')
				# policyReportData = getNexusIqData('/' + policyReportDataUrl)
				# writePolicyViolationsByReport(applicationName, policyReportData)

 
	print(reportsUrlsCsvfile)

	return


def writeReportsCsv(applicationEvaluations):
	with open(rawComponentsDataByReportCsvfile, 'w') as fd:	
			fd.write('ApplicationName,Hash,PackageUrl,Issues\n')
			fd.close()

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



def componentMapper():

	with open(overridesCsvfile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			lineCount = 0
			for row in r:
				if lineCount == 0:
					lineCount += 1
				else:
					lineCount += 1
					hash = row[0]
					print (hash)

def main():

	if os.path.exists(outputdir) and os.path.isdir(outputdir):
		shutil.rmtree(outputdir)

	os.mkdir(outputdir)

	# overrides

	overrides = getNexusIqData('/api/v2/securityOverrides')
	writeJsonfile(overridesJsonfile, overrides)
	writeOverridesCsvfile(overrides)

	# policy violations

	policies = getNexusIqData('/api/v2/policies')
	policyIds = getPolicyIds(policies)
	policyViolations = getNexusIqData("/api/v2/policyViolations?" + policyIds)

	writeJsonfile(policyviolationsJsonfile, policyViolations)
	writePolicyviolationsCsvFile(policyViolations)

	# application reports

	applicationEvaluations = getNexusIqData('/api/v2/reports/applications')
	writeJsonfile(reportsJsonfile, applicationEvaluations)
	writeReportsUrls(applicationEvaluations)
	writeReportsCsv(applicationEvaluations)

	# policy violations by report

	# analyse

	#componentMapper()


if __name__ == '__main__':
	main()
