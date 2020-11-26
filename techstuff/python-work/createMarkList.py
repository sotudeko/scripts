import glob
import argparse
import getpass
import json
from pprint import pprint
import csv

totalHashValue = []

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


def goThroughReport(reportPath, cvesInScope):
	with open(reportPath, 'r') as report:
		test = json.loads(report.read())

	newlist = []

	for row in test['components']:
		hashValue = row['hash']
		
		if row['securityData'] is not None and len(row['securityData']['securityIssues']) > 0:
			for issue in row['securityData']['securityIssues']:
				if issue['reference'] in cvesInScope:
					# component, hashValue, reference, status, source, comment
					# newlist.append('componentPlaceHolder,{},{},NOT_APPLICABLE,{},not applicable'.format(hashValue,issue['reference'],issue['source']))
					newlist.append(['componentPlaceHolder',hashValue,issue['reference'],'NOT_APPLICABLE',issue['source'],'not applicable'])
					# print (reportPath)

	return newlist


	

def main():
	args = setup()
	listOfReports = glob.glob('./jsonReports/{}*'.format(args.appcode))

	cvesInScope = open('cvelist/{}_cves.txt'.format(args.appcode)).read().split('\n')

	totalListOfVulns = []
	
	for report in listOfReports:

		newlist = goThroughReport(report, cvesInScope)

		for row in newlist:
			totalListOfVulns.append(row)

	header = ['component','hashValue','reference','status','source','comment']

	# totalListOfVulns = set(totalListOfVulns)

	totalListOfVulns = [list(x) for x in set(tuple(x) for x in totalListOfVulns)]


	with open('marklists/{}_Mark.csv'.format(args.appcode), 'w') as markListFile:
		csvWriter = csv.writer(markListFile)

		csvWriter.writerow(header)
		
		for row in totalListOfVulns:
			csvWriter.writerow(row)



if __name__ == "__main__":
	main()