import json
import requests
import os
import os.path
import sys
import csv
import shutil

iqUrl = sys.argv[1]
iquser = sys.argv[2]
iqpwd = sys.argv[3]

generateData = True
outputDir = './datafiles'

overRidesJsonFile = '{}/{}'.format(outputDir, 'overrides.json')
overRidesCsvFile = '{}/{}'.format(outputDir, 'overrides.csv')

appReportsJsonFile = '{}/{}'.format(outputDir, 'appreports.json')
appReportsUrlsCsvFile = '{}/{}'.format(outputDir, 'appreportsurls.csv')
appIssuesStatusCsvFile = '{}/{}'.format(outputDir, 'appissuesstatus.csv')
appPolicyViolationsCsvFile = '{}/{}'.format(outputDir, 'apppolicyviolations.csv')

policyViolationsDb = []
secLicIssuesDb = {}
overRidesDb = []


if len(sys.argv) > 4:
	generateData = False


def getNexusIqData(api):
    # access Nexus IQ API
    url = "{}{}" . format(iqUrl, api)
    req = requests.get(url, auth=(iquser, iqpwd), verify=False)

    if req.status_code == 200:
        data = req.json()
    else:
        data = 'Error fetching data'

    return req.status_code, data


def writeJsonFile(jsonFile, jsonData):
	with open(jsonFile, 'w') as fd:
			json.dump(jsonData, fd)

	print(jsonFile)

	return


def writeOverRidesCsvFile(overrides):

	components = overrides['securityOverrides']

	with open(overRidesCsvFile, 'w') as fd:
			fd.write("Application,Hash,PackageUrl,CVE,Status,Comment\n")
			for component in components:
				comment = component["comment"]
				referenceId = component["referenceId"]
				status = component["status"]
				ownerPublicId = component["owner"]["ownerPublicId"]
				ownerId = component["owner"]["ownerId"]

				for affectedComponent in component["currentlyAffectedComponents"]:
					packageUrl = affectedComponent["packageUrl"]
					proprietary = affectedComponent["proprietary"]
					thirdParty = affectedComponent["thirdParty"]
					hash = affectedComponent["hash"]

					line = ownerPublicId + "," + hash + "," + packageUrl +  "," + referenceId + "," + status + "," + comment + "\n"
					fd.write(line)

	print(overRidesCsvFile)

	return


def getOverRidesData():
    # get security vulnerabilty override data
    statusCode, data = getNexusIqData('/api/v2/securityOverrides')

    if statusCode == 200:
        # Write the json data to file
        writeJsonFile(overRidesJsonFile, data)

        # Extract relevant data and write to CSV file
        writeOverRidesCsvFile(data)
    else:
        print(str(statusCode) + ': ' + data + ' - Overrides')

    return statusCode


def getApplicationEvaluationReports():
    # get all application reports info
    statusCode, data = getNexusIqData('/api/v2/reports/applications')

    if statusCode == 200:
         # Write the json data to file
        writeJsonFile(appReportsJsonFile, data)

        # Get the Url of each report and write to CSV file
        writeAppReportUrlsCsvFile(data)
    else:
        print(str(statusCode) + ': ' + data + ' - Application Reports')

    return statusCode


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])


def writeAppReportUrlsCsvFile(applicationEvaluations):
	with open(appReportsUrlsCsvFile, 'w') as fd:
			for applicationEvaluation in applicationEvaluations:
				applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
				applicationReportUrl = applicationEvaluation["reportDataUrl"]

				line = applicationName + "," + applicationReportUrl + "\n"
				fd.write(line)

	print(appReportsUrlsCsvFile)
	return


def writePolicyViolationsCsvFile():
	with open(appPolicyViolationsCsvFile, 'w') as fd:
			fd.write('ApplicationName,Hash,PackageUrl,PolicyName,PolicyId,Waived\n')
			fd.close()

    # read the app report urls file
	with open(appReportsUrlsCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			for row in r:
				applicationName = row[0]
				url = row[1]

                # append the policy violations for this application report to the output csvfile
				policyViolations(applicationName, url)

	print(appPolicyViolationsCsvFile)

	return 200


def policyViolations(applicationName, url):

    # we want the policy violations
	policyReportDataUrl = url.replace('/raw', '/policy')
	statusCode, policyReportData = getNexusIqData('/' + policyReportDataUrl)

	if not statusCode == 200:
		print(str(statusCode) + ': ' + policyReportData + ' - ' + policyReportDataUrl)
		return statusCode

	components = policyReportData["components"]
	application = policyReportData["application"]
	counts = policyReportData["counts"]
	reportTime = policyReportData["reportTime"]
	initiator = policyReportData["initiator"]

    #  write the data
	with open(appPolicyViolationsCsvFile, 'a') as fd:
			for component in components:
				hash = component["hash"]
				packageUrl  = component["packageUrl"]

				if not packageUrl:
					packageUrl = "none"

				if not outputFormat(packageUrl):
					continue

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
					line = applicationName + "," + hash + "," + packageUrl + "," + policyName + "," + policyId + "," + str(waived) + "\n"

					# store in database and also write to file
					policyViolationsDb.append(line)
					fd.write(line)
	return


def outputFormat(purl):
	if ":a-name/" in purl or ":npm/" in purl:
		return True
	else:
		return False


def writeSecLicIssuesCsvFile():
	with open(appIssuesStatusCsvFile, 'w') as fd:
			fd.write('ApplicationName,Hash,PackageUrl,Issues,LicenceStatus\n')
			fd.close()

    # read the app report urls file
	with open(appReportsUrlsCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			for row in r:
				applicationName = row[0]
				url = row[1]

                # append the security/license issues and status for the application report to the output csvfile
				secLicIssues(applicationName, url)

	print(appIssuesStatusCsvFile)

	return 200


def secLicIssues(applicationName, url):

    # get the report raw data
	statusCode, rawData = getNexusIqData('/' + url)

	if not statusCode == 200:
		print(str(statusCode) + ': ' + rawData + ' - ' + url)
		return	
        
	components = rawData["components"]

    # write the data
	with open(appIssuesStatusCsvFile, 'a') as fd:
			for component in components:
				hash = component["hash"]
				packageUrl  = component["packageUrl"]

				licenseData = component["licenseData"]
				if licenseData:
					licenseStatus = licenseData["status"]
				else:
					licenseStatus = 'none'

				if not packageUrl:
					packageUrl = "none"

				if not outputFormat(packageUrl):
					continue

				if type(component["securityData"]) is dict:
					securityIssues = component["securityData"]["securityIssues"]

					if len(securityIssues) > 0:
						issues = ""
						for securityIssue in securityIssues:
							issues += securityIssue["reference"] + ":" + securityIssue["status"] + ":" + str(securityIssue["severity"]) + ";"
						issues = issues[:-1]

						#if securityIssue["status"] != 'Open':
						key = applicationName + "-" + hash
						line = applicationName + "," + hash + "," + packageUrl + "," + issues + "," + licenseStatus + "\n"

						# store in db and also write to file
						secLicIssuesDb[key] = line
						fd.write(line)
				#else:
					#line = applicationName + "," + hash + "," + packageUrl + "," + 'no security issues' + "\n"
					#fd.write(line)
					
	return


def loadPolicyViolationsByReport():
	with open(appPolicyViolationsCsvFile, 'r') as fd:
		for line in fd.readlines():
				policyViolationsDb.append(line)

	return


def componentMapper():
	with open(overRidesCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			lineCount = 0
			for row in r:
				if lineCount == 0:
					lineCount += 1
				else:
					lineCount += 1

					# Hash,PackageUrl,CVE,Status
					line = '{}:{}:{}:{}:{}'.format(row[0], row[1], row[2], row[3], row[4])

					print (line)
					findHash(row[1])

	return


def findHash(hash):

	#if "model" in dict:

	for i in policyViolationsDb:

		# remove newline
		i = i[:-1]
		
		# search and print if we find matching hash
		if hash in i:
			print('  ' + i)

	return


def main():

    if generateData:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        if not getApplicationEvaluationReports() == 200:		
            sys.exit(-1)

        if not writePolicyViolationsCsvFile() == 200:
            sys.exit(-1)

        if not writeSecLicIssuesCsvFile() == 200:
            sys.exit(-1)

        if not getOverRidesData() == 200:
            sys.exit(-1)

    # analyse
    componentMapper()


if __name__ == '__main__':
	main()
