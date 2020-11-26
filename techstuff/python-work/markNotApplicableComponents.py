import sys
import argparse
import getpass
import requests
import urllib3
import json
import csv
from time import sleep
from multiprocessing import Pool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

IQURL = ""

URL = '{}/assets/index.html'.format(IQURL)
NOTAPPLICURL = '{}/rest/securityVulnerabilityOverride/application/{}'
APPLICATIONLISTFILE = 'applists/{}_applist.csv'
MARKEDLISTFILE = 'marklists/{}_Mark.csv'

def setup():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-A",
		"--appcode",
		required=True,
		dest="appcode",
		type=str,
		help="The appcode you want to mark"
	)

	parser.add_argument(
		"-U",
		"--user",
		required=True,
		dest="user",
		type=str,
		help="Your username"
	)

	parser.add_argument(
		"-P",
		"--password",
		required=False,
		dest="password",
		type=str,
		help="Your password"
	)

	args = parser.parse_args()

	args.password = args.password or getpass.getpass('Enter your password: ')

	return args

def get_session(args):
	client = requests.Session()
	client.auth = (args.user, args.password)
	client.get(URL, verify=False)  # sets cookie
	
	return client

def get_appcode_list(appcode):
	appcodelist = []

	with open(APPLICATIONLISTFILE.format(appcode), newline='') as f:
		reader = csv.reader(f)
		appcodelist = [item for sublist in reader for item in sublist]

	return appcodelist

def get_mark_list(appcode):

	with open(MARKEDLISTFILE.format(appcode), newline='', encoding='utf-8-sig') as f:
		reader = csv.DictReader(f)
		markedList = list(reader)

	return markedList
	
def mark_vuln_status(client, app, hashValue, referenceId, source, status, comment):
	# hash of the component
	# hashValue = ''
	
	# The CVE or SONATYPE value
	# referenceId = ''

	# CVE or SONATYPE
	# source = '' 	

	# status from Nexus IQ:
	# 	OPEN 
	# 	NOT_APPLICABLE 
	# 	ACKNOWLEDGED
	#	CONFIRMED
	# status = ''

	# Whatever comment you want to make
	# comment = ''

	headers = {
		'Accept': "application/json, text/plain, */*",
		'Content-Type': "application/json;charset=UTF-8",
		'Referer': "https://fusionnexusiq.fg.rbc.com/assets/index.html",
		'Origin': 'https://fusionnexusiq.fg.rbc.com',
		'Upgrade-Insecure-Requests': "1",
		'X-CSRF-TOKEN': client.cookies['CLM-CSRF-TOKEN']
	}
	DATA = {"hash":hashValue,"referenceId":referenceId,"source":source,"status":status,"comment":comment}
	DATA = json.dumps(DATA)
	try:
		r = client.put(NOTAPPLICURL.format(IQURL,app), verify=False, data=DATA, headers=headers)
		print (r.text)
		print (r.status_code)
		if r.status_code == 200:
			print ("successfully marked as {}".format(hashValue))
	except Exception as e:
		print (e)
	
def getReportId(app, client):

	r = client.get('https://fusionnexusiq.fg.rbc.com/api/v2/applications?publicId={}'.format(app), verify=False)
	applicationId = json.loads(r.text)['applications'][0]['id']

	r = client.get('https://fusionnexusiq.fg.rbc.com/api/v2/reports/applications/{}'.format(applicationId), verify=False)

	reportIds = []

	try:
		for row in json.loads(r.text):
			reportHtmlUrl = row['reportHtmlUrl']
			reportId = reportHtmlUrl.split('/')[-1]
			reportIds.append(reportId)
	except Exception as e:
		print (e)
		return None


	return reportIds

def reEvaluatePolicy(app, reportId, client):
	# https://fusionnexusiq.fg.rbc.com/assets/index.html#/reports/{}/{} app reportId
	headers = { 
		'Accept': "application/json, text/plain, */*",
		'Content-Type': "application/json;charset=UTF-8",
		'Referer': "https://fusionnexusiq.fg.rbc.com/assets/index.html",
		'Origin': 'https://fusionnexusiq.fg.rbc.com',
		'Upgrade-Insecure-Requests': "1",
		'X-CSRF-TOKEN': client.cookies['CLM-CSRF-TOKEN']
	}

	r = client.post('https://fusionnexusiq.fg.rbc.com/rest/report/{}/{}/reevaluatePolicy'.format(app, reportId), verify=False, headers=headers)

	print (r.text)

def marking_vuln_status(app):
	tobemarked = get_mark_list(args.appcode)

	for mark in tobemarked:
		mark_vuln_status(client, app, mark['hashValue'], mark['reference'], mark['source'], mark['status'], mark['comment'])
		
	reportIds = getReportId(app, client)
	# eg. https://fusionnexusiq.fg.rbc.com/rest/report/XPU0.srdr_timeseries_producer.release/f2712fc7665b465aaaeb9aefdc46c058/reevaluatePolicy
	for reportId in reportIds:
		reEvaluatePolicy(app, reportId, client)

if __name__ == '__main__':

	args = setup()
	client = get_session(args)
	appcodelist = get_appcode_list(args.appcode)

	# tobemarked = get_mark_list(args.appcode)
	
	for row in appcodelist:
		marking_vuln_status(row)
	#with Pool(5) as p:
		#sleep(1)
		#p.map(marking_vuln_status, appcodelist)	

	# for app in appcodelist:
	# 	for mark in tobemarked:
	# 		mark_vuln_status(client, app, mark['hashValue'], mark['reference'], mark['source'], mark['status'], mark['comment'])
		
	# 	reportId = getReportId(app, client)
	# 	# eg. https://fusionnexusiq.fg.rbc.com/rest/report/XPU0.srdr_timeseries_producer.release/f2712fc7665b465aaaeb9aefdc46c058/reevaluatePolicy
	# 	if reportId is not None:
	# 		reEvaluatePolicy(app, reportId, client)

