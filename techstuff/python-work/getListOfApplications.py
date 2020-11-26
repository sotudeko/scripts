import requests
import sys
import json
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ADMINUSER = sys.argv[1]
ADMINPASS = sys.argv[2]

appcodeIgnoreList = ['MRK0']

appCodeDownload = sys.argv[3]

IQURL = ""

def getListOfReports(listOfApplications):
	#/api/v2/reports/applications
	r = requests.get('{}/api/v2/reports/applications'.format(IQURL), auth=(ADMINUSER, ADMINPASS), verify=False)

	data = json.loads(r.text)

	reportList = []

	for row in data:
		applicationName = row['reportDataUrl'].split('/')[3]
		if applicationName in listOfApplications:
			listOfApplications[applicationName]['reportUrl'] = row['reportDataUrl']

	return listOfApplications

def organizationsJson():
    #/api/v2/organizations
    r = requests.get('{}/api/v2/organizations'.format(IQURL), auth=(ADMINUSER, ADMINPASS), verify=False)
    return(json.loads(r.text))

def getOrgId(orgJson, orgName):
    for row in orgJson['organizations']:
        if row['name'] == orgName:
            return row['id']

def getInternalTag(orgJson):
	nexusIQTags = {}

	for row in orgJson['organizations']:
		if row['id'] == 'ROOT_ORGANIZATION_ID':
			for tag in row['tags']:
				nexusIQTags[tag['name']] = tag['id']

	return nexusIQTags

def getListOfApplications(orgId, nexusTags, appCodeOrgId):
	#/api/v2/reports/applications/
	r = requests.get('{}/api/v2/applications/'.format(IQURL), auth=(ADMINUSER, ADMINPASS), verify=False)
	data = json.loads(r.text)	
	nexusApplicationData = {}


	for row in data['applications']:
		internalFlag = False
		retiredFlag = False
		vendorFlag = False
		prodNotUsedFlag = False

		# reportDownloadFlag = False

		if row['organizationId'] == appCodeOrgId:
			print (row)
		elif row['organizationId'] == orgId and row['name'][0:4] in appCodeDownload:
			print (row)
		else:
			continue

		

	
		for tag in row['applicationTags']:
			if tag['tagId'] == nexusTags['Internal']:
				internalFlag = True
			if tag['tagId'] == nexusTags['Retired Component']:
				retiredFlag = True
			if tag['tagId'] == nexusTags['Vendor']:
				vendorFlag = True
			if tag['tagId'] == nexusTags['Prod Not Used']:
				prodNotUsedFlag = True

		nexusApplicationData[row['publicId']] = {'applicationId': row['id'], 'internalTag': internalFlag, 'retiredTag': retiredFlag, 'vendorTag': vendorFlag, 'prodNotUsedTag': prodNotUsedFlag}

	return(nexusApplicationData)


def main():
	nexusOrg = 'ReleaseAutomatedScan'
	orgJson = organizationsJson()
	orgId = getOrgId(orgJson, nexusOrg)
	nexusIQTags = getInternalTag(orgJson)

	appCodeOrgId = getOrgId(orgJson, appCodeDownload)

	listOfApplications = getListOfApplications(orgId, nexusIQTags, appCodeOrgId)
	listOfReports = getListOfReports(listOfApplications)

	return listOfReports

if __name__ == "__main__":
	myList = main()
	print (myList)