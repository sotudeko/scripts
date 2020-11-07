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
# appPolicyViolationsJsonFile = '{}/{}'.format(outputDir, 'apppolicyviolations.json')

statusSummaryCsvFile = '{}/{}'.format(outputDir, 'statussummary.csv')

secLicIssuesDb = {}

policyViolationsDb = []
overRidesDataDb = []


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
			json.dump(jsonData, fd, indent=4)

	print(jsonFile)

	return


def getOverRidesData():
    # get security vulnerabilty override data
    statusCode, data = getNexusIqData('/api/v2/securityOverrides')

    if statusCode == 200:
        # Write the json data to file
        writeJsonFile(overRidesJsonFile, data)

        # Save the overrides data
        saveOverridesData(data)
    else:
        print(str(statusCode) + ': ' + data + ' - Overrides')

    return statusCode


def saveOverridesData(overrides):
	components = overrides['securityOverrides']

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

			line = ownerPublicId + "," + hash + "," + packageUrl +  "," + referenceId + "," + status + "," + comment

			# keep all data to write to file later
			overRidesDataDb.append(line)

	print (overRidesDataDb)
	return


def writeOverRidesCsvFile():

	with open(overRidesCsvFile, 'w') as fd:
			fd.write("Application,Hash,PackageUrl,CVE,Status,Comment,SecurityScore,LicenseStatus\n")
			for item in overRidesDataDb:
				items = item.split(',')

				ownerPublicId = items[0]
				hash = items[1]
				packageUrl = items[2]
				referenceId = items[3]
				status = items[4]
				comment = items[5]

				securityScore, licenseStatus = getSecurityScore(ownerPublicId, hash, referenceId)
				line = ownerPublicId + "," + hash + "," + packageUrl +  "," + referenceId + "," + status + "," + comment + "," + str(securityScore) + "," + licenseStatus + "\n"
				fd.write(line)

	print (overRidesCsvFile)
	return 200


def getSecurityScore(applicationName, hash, findCve):
	issue = secLicIssuesDb.get(applicationName + "-" + hash).split(',')
	
	cves = issue[3].split(';')
	licenseStatus = issue[4]
	licenseStatus = licenseStatus[:-1]
	cveScore = 0

	for c in cves:
		el = c.split(':')
		cve = el[0]
		status = el[1]
		score = el[2]

		if cve == findCve:
			cveScore = score

	return cveScore, licenseStatus


def getApplicationEvaluationReports():
    # get all application reports info
    statusCode, applicationEvaluations = getNexusIqData('/api/v2/reports/applications')

    if statusCode == 200:
         # Write the json data to file
        writeJsonFile(appReportsJsonFile, applicationEvaluations)

        # Get the Url of each report and write to CSV file
        # writeAppReportUrlsCsvFile(data)
        with open(appReportsUrlsCsvFile, 'w') as fd:
                for applicationEvaluation in applicationEvaluations:
                    applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
                    applicationReportUrl = applicationEvaluation["reportDataUrl"]
                    
                    # only write the details if the application has an override
                    if applicationHasOverride(applicationName):
                        line = applicationName + "," + applicationReportUrl + "\n"
                        fd.write(line)
    else:
        print(str(statusCode) + ': ' + applicationEvaluations + ' - Application Reports')

    print(appReportsUrlsCsvFile)
    return statusCode


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])


def writeAppReportUrlsCsvFile(applicationEvaluations):
	with open(appReportsUrlsCsvFile, 'w') as fd:
			for applicationEvaluation in applicationEvaluations:
				applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
				applicationReportUrl = applicationEvaluation["reportDataUrl"]

				# only write the details if the application has an override
				if applicationHasOverride(applicationName):
					line = applicationName + "," + applicationReportUrl + "\n"
					fd.write(line)

	print(appReportsUrlsCsvFile)
	return


def writePolicyViolationsCsvFile():
	# get the policy violations for each application that has an override

	with open(appPolicyViolationsCsvFile, 'w') as fd:
			fd.write('ApplicationName,ApplicationId,PackageUrl,PolicyName,PolicyId,PolicyThreatCategory,PolicyThreatLevel,PolicyViolationId,Waived\n')
			fd.close()

    # read the app report urls file
	with open(appReportsUrlsCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			for row in r:
				applicationName = row[0]
				url = row[1]

                # append the policy violations for this application report to the output csvfile
				# only if it has an override
				if applicationHasOverride(applicationName):
					policyViolations(applicationName, url)

	print(appPolicyViolationsCsvFile)
	return 200

def applicationHasOverride(applicationName):
	exists = False

	for o in overRidesDataDb:
		info = o.split(',')
		overrideApplication = info[0]
		if overrideApplication == applicationName:
			exists = True
			break
	
	return exists


def policyViolations(applicationName, url):

    # we want the policy violations
	policyReportDataUrl = url.replace('/raw', '/policy')
	statusCode, policyReportData = getNexusIqData('/' + policyReportDataUrl)

	if not statusCode == 200:
		print(str(statusCode) + ': ' + policyReportData + ' - ' + policyReportDataUrl)
		return statusCode

	# writeJsonFile(outputDir + "/apppolicyviolations-" + applicationName + ".json", policyReportData)

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

				# write only if needed format - we want a-name's only
				if not outputFormat(packageUrl):
					continue

				# write only if this component has an override
				if not componentHasOverride(applicationName, packageUrl):
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
					policyThreatLevel = violation['policyThreatLevel']
					policyViolationId = violation['policyViolationId']

					# Only write if above threat level threshold
					if policyThreatLevel >= 7:
						line = applicationName + "," + hash + "," + packageUrl + "," + policyName + "," + policyId + "," + policyThreatCategory + "," + str(policyThreatLevel) + "," + policyViolationId + "," + str(waived) + "\n"

						# store in database and also write to file 
						policyViolationsDb.append(line)
						fd.write(line)
	return


def componentHasOverride(applicationName, packageUrl):
	exists = False

	for o in overRidesDataDb:
		info = o.split(',')
		overrideApplication = info[0]
		overridePackageUrl = info[2]

		if overrideApplication == applicationName and overridePackageUrl == packageUrl:
			exists = True
			break
	
	return exists


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
					
	return


def makeStatusSummary():

	with open(statusSummaryCsvFile, 'w') as fd:
			fd.write('Application,Hash,PackageUrl,PolicyName,PolicyId,Waived,CVE,SecurityScore,VulnStatus,LicenseStatus,Comment\n')
			fd.close()

	with open(overRidesCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			lineCount = 0
			for row in r:
				if lineCount == 0:
					lineCount += 1
				else:
					lineCount += 1

					# Application,Hash,PackageUrl,CVE,Status,Comment,SecurityScore,LicenseStatus 
					line = '{}:{}:{}:{}:{}:{}:{}'.format(row[0], row[1], row[2], row[3], row[4], row[6], row[7])
					headline = '{},{},{},{},{}'.format(row[3], row[6], row[4], row[7], row[5])
					findHash(row[1], headline)

	print(statusSummaryCsvFile)
	return


def findHash(hash, headline):

	with open(statusSummaryCsvFile, 'a') as fd:
		for i in policyViolationsDb:

			# remove newline
			i = i[:-1]
			
			# search and print if we find matching hash
			if hash in i:
				line = i + "," + headline + "\n"
				fd.write(line)

	return


def main():

    if generateData:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        if not getOverRidesData() == 200:
            sys.exit(-1)

        if not getApplicationEvaluationReports() == 200:		
            sys.exit(-1)

        if not writePolicyViolationsCsvFile() == 200:
            sys.exit(-1)

        if not writeSecLicIssuesCsvFile() == 200:
            sys.exit(-1)

        if not writeOverRidesCsvFile() == 200:
            sys.exit(-1)

    # summary report
    makeStatusSummary()


if __name__ == '__main__':
	main()
