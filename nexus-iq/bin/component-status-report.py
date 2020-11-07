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

# iqUrl = "http://localhost:8870"
# iquser = "admin"
# iqpwd = "admin123"

generateData = True
outputDir = './datafiles'

overRidesJsonFile = '{}/{}'.format(outputDir, 'overrides.json')
overRidesCsvFile = '{}/{}'.format(outputDir, 'overrides.csv')

appReportsJsonFile = '{}/{}'.format(outputDir, 'appreports.json')
appReportsUrlsCsvFile = '{}/{}'.format(outputDir, 'appreportsurls.csv')
appIssuesStatusCsvFile = '{}/{}'.format(outputDir, 'appissuesstatus.csv')

appPolicyViolationsCsvFile = '{}/{}'.format(outputDir, 'apppolicyviolations.csv')

statusSummaryCsvFile = '{}/{}'.format(outputDir, 'statussummary.csv')

overRidesDb = []
policyViolationsDb = []
secLicIssuesDb = []


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


def applicationHasOverride(applicationName):
	exists = False

	for o in overRidesDb:
		info = o.split(',')

		overrideApplicationName = info[0]
		overrideApplicationId = info[1]

		if overrideApplicationName == applicationName:
			exists = True
			break
	
	return exists


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])


def componentHasOverride(applicationName, packageUrl):
	exists = False

	for o in overRidesDb:
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


def getOverRidesData():
	# get security vulnerabilty override data
	statusCode, overrides = getNexusIqData('/api/v2/securityOverrides')

	if statusCode == 200:
		# Write the json data to file
		writeJsonFile(overRidesJsonFile, overrides)

		overrides = overrides['securityOverrides']

		# write also a summary csv file
		with open(overRidesCsvFile, 'w') as fd:
				fd.write("ApplicationName,ApplicationId,PackageUrl,ComponentHash,CVE,OverrideStatus,Comment,\n")
				for override in overrides:
					comment = override["comment"]
					referenceId = override["referenceId"]
					status = override["status"]
					ownerPublicId = override["owner"]["ownerPublicId"]
					ownerId = override["owner"]["ownerId"]

					for affectedComponent in override["currentlyAffectedComponents"]:
						packageUrl = affectedComponent["packageUrl"]
						proprietary = affectedComponent["proprietary"]
						thirdParty = affectedComponent["thirdParty"]
						componentHash = affectedComponent["hash"]

						line = ownerPublicId + "," + ownerId + "," + packageUrl +  "," + componentHash + "," + referenceId + "," + status + "," + comment + "\n"

						# store and also write to file 
						overRidesDb.append(line)
						fd.write(line)

	print(overRidesCsvFile)
	return statusCode



# def getSecurityScore(applicationName, hash, findCve):
# 	return 1, "none"
# 	print (secLicIssuesDb)
# 	for issue in secLicIssuesDb:
# 		cves = issue[3].split(';')
# 		licenseStatus = issue[4]
# 		licenseStatus = licenseStatus[:-1]
# 		cveScore = 0

# 		for c in cves:
# 			el = c.split(':')
# 			cve = el[0]
# 			status = el[1]
# 			score = el[2]

# 			if cve == findCve:
# 				cveScore = score

# 	return cveScore, licenseStatus


def getApplicationEvaluationReports():
    # get all application reports info
    statusCode, applicationEvaluations = getNexusIqData('/api/v2/reports/applications')

    if statusCode == 200:
         # Write the json data to file
        writeJsonFile(appReportsJsonFile, applicationEvaluations)

        # Get the Url of each report and write to CSV file
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


def getPolicyViolationsForOverrideApplications():
	# get the policy violations for each override application 

	with open(appPolicyViolationsCsvFile, 'w') as fd:
			fd.write('ApplicationName,ApplicationId,PackageUrl,PolicyName,PolicyId,PolicyThreatCategory,PolicyThreatLevel,PolicyViolationId,Waived\n')
			fd.close()

    # read the app report urls file (it contains on applications with overrides)
	with open(appReportsUrlsCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			for row in r:
				applicationName = row[0]
				url = row[1]

                # append the policy violations for this application report to the output csvfile
				writePolicyViolations(applicationName, url)

	print(appPolicyViolationsCsvFile)
	return 200


def writePolicyViolations(applicationName, url):

    # we want the policy violations
	policyReportDataUrl = url.replace('/raw', '/policy')
	statusCode, policyReportData = getNexusIqData('/' + policyReportDataUrl)

	if not statusCode == 200:
		print(str(statusCode) + ': ' + policyReportData + ' - ' + policyReportDataUrl)
		return statusCode

	components = policyReportData["components"]
	applicationId = policyReportData["application"]["id"]
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

				# write only if it is format we need
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
						line = applicationName + "," + applicationId + "," + packageUrl + "," + policyName + "," + policyId + "," + policyThreatCategory + "," + str(policyThreatLevel) + "," + policyViolationId + "," + str(waived) + "\n"

						# store and also write to file 
						policyViolationsDb.append(line)
						fd.write(line)
	return


def getSecLicIssuesForOverrideApplications():
	with open(appIssuesStatusCsvFile, 'w') as fd:
			fd.write('ApplicationName,ComponentHash,PackageUrl,CVE,ThreatLevel,VulnStatus,LicenceStatus\n')
			fd.close()

    # read the app report urls file (it contains on applications with overrides)
	with open(appReportsUrlsCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			for row in r:
				applicationName = row[0]
				url = row[1]

                # append the security/license issues and status for the application report to the output csvfile
				writeSecLicIssues(applicationName, url)

	print(appIssuesStatusCsvFile)
	return 200


def writeSecLicIssues(applicationName, url):

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

				# write only if it is format we need
				if not outputFormat(packageUrl):
					continue

				# write only if this component has an override
				if not componentHasOverride(applicationName, packageUrl):
					continue

				if type(component["securityData"]) is dict:
					securityIssues = component["securityData"]["securityIssues"]

					if len(securityIssues) > 0:
						for securityIssue in securityIssues:
							line = applicationName + "," + hash + "," + packageUrl + "," + securityIssue["reference"] + "," + str(securityIssue["severity"]) + "," + securityIssue["status"] + "," + licenseStatus + "\n"
							fd.write(line)
	
	return


def getPolicyViolationDetails():

	with open(appPolicyViolationsCsvFile) as csvfile:
			r = csv.reader(csvfile, delimiter=',')
			lineCount = 0
			for row in r:
				if lineCount == 0:
					lineCount += 1
				else:
					lineCount += 1

					#ApplicationName,ApplicationId,PackageUrl,PolicyName,PolicyId,PolicyThreatCategory,PolicyThreatLevel,PolicyViolationId,Waived
					applicationName = row[0]
					applicationId = row[1]
					policyId = row[4]
					policyViolationId = row[7]

					statusCode, info = getPolicyViolationData(applicationId, policyId, policyViolationId)
					
	return


def getPolicyViolationData(applicationId, policyId, policyViolationId):
	# get policy violation data

	data = {}
	statusCode, pvd = getNexusIqData('/api/v2/policyViolations?p=' + policyId)

	if statusCode == 200:
		applicationsViolations = pvd["applicationViolations"]

		for application in applicationsViolations:
			pvApplicationId = application["application"]["id"]

			# look for the application we need
			if pvApplicationId == applicationId:
				
				for policyViolation in application["policyViolations"]:
					pvPolicyViolationId = policyViolation["policyViolationId"]

					# look for the policy violation we need
					if pvPolicyViolationId == policyViolationId:
						data["policyId"] = policyViolation["policyId"]
						data["policyName"] = policyViolation["policyName"]
						data["policyViolationId"] = policyViolation["policyViolationId"]
						data["stageId"] = policyViolation["stageId"]
						data["threatLevel"] = policyViolation["threatLevel"]
						data["packageUrl"] = policyViolation["component"]["packageUrl"]
						break
	
	return statusCode, data


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

        if not getPolicyViolationsForOverrideApplications() == 200:
            sys.exit(-1)

        if not getSecLicIssuesForOverrideApplications() == 200:
            sys.exit(-1)

    # summary report
    #makeStatusSummary()


if __name__ == '__main__':
	main()
