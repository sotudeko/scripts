import json
import requests
import os
import os.path
from pprint import pprint
from multiprocessing import Pool
import getListOfApplications 

import sys
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ADMINUSER = sys.argv[1]
ADMINPASS = sys.argv[2]
nexusOrg = 'ReleaseAutomatedScan'

IQURL = ""


def get_json_report(id):
	#https://fusionnexusiq.fg.rbc.com/api/v2/reports/applications/19d3c29b54c44acb90a75bd71edc5df5
	r = requests.get('{}/api/v2/reports/applications/{}'.format(IQURL, id), auth=(ADMINUSER, ADMINPASS), verify=False)
	
	data = json.loads(r.text)
	
	urls = ""
	
	for i in data:
		urls = (i['reportDataUrl'])
		print (urls)

	return(urls)

	
def download_reports(url):
	r = requests.get('{}/{}'.format(IQURL,url), auth=(ADMINUSER, ADMINPASS), verify=False)
	
	try:
		data = json.loads(r.text)
	except:
		return None
	projectname = url.split('/')
	print(data['matchSummary'])
	with open('jsonReports/{}.{}.json'.format(sys.argv[3],projectname[3]), 'w') as f:
		json.dump(data, f)
		

def main():

	applicationData = getListOfApplications.main()

	try:
		os.makedirs('jsonReports')
	except OSError:
		pass	


	reports = []

	for app in applicationData:
		try:
			reports.append(applicationData[app]['reportUrl'])
			print (app)
		except:
			continue

	with Pool(5) as p:
		p.map(download_reports, reports)	


			
				
if __name__ == '__main__':
	main()
			
