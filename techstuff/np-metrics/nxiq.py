import requests
import json
import pprint

def print(json):
	pprint.pprint(json)
	return

class Connection:
	def __init__(self, host, username, password):
		self.host = host
		self.username = username
		self.password = password


	def getData(self, api):
		url = "{}{}".format(self.host, api)

		req = requests.get(url, auth=(self.username, self.password), verify=False)

		if req.status_code == 200:
			res = req.json()
		else:
			res = "Error fetching data"

		return res

	def getHost(self):
		return self.host


	def getOrganizations(self):
		endpoint = '/api/v2/organizations'
		data = self.getData(endpoint)
		return data


	def getOrganizationId(self, orgName):
		data = self.getOrganizations()
		organizationId = ""

		organizations = data['organizations']

		for organization in organizations:
			oname = organization['name']
			oid = organization['id']

			if orgName == oname:
				organizationId = oid

		return organizationId


	def getApplications(self):
		endpoint = '/api/v2/applications'
		data = self.getData(endpoint)
		return data


	def getApplicationId(self, applicationName):
		data = self.getApplications()
		applicationId = ""

		applications = data['applications']

		for application in applications:
			appName = application['name']
			appId = application['id']
			orgId = application['organizationId']
			publicId = application['publicId']

			if appName == applicationName:
				applicationId = appId

		return applicationId

	def getPolicyId(self, policyName):
		endpoint = '/api/v2/policies'
		policyId = ""
		data = self.getData(endpoint)

		policies = data['policies']

		for policy in policies:
			pname = policy['name']
			pid = policy['id']

			if pname == policyName:
				policyId = pid
				
		return policyId


	def getPolicyViolations(self, policyId):
		endpoint = '/api/v2/policyViolations' + '?p=' + policyId
		data = self.getData(endpoint)
		return data

	
	def getApplicationReport(self, applicationId):
		endpoint = '/api/v2/reports/applications/' + applicationId
		data = self.getData(endpoint)
		return data


	def getApplicationReports(self):
		endpoint = '/api/v2/reports/applications'
		data = self.getData(endpoint)
		return data




