import csv
import argparse
import getpass
import requests
import json

IQURL = ""

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

def get_applist(args):

	SIDEBARURL = '{}/rest/sidebar'.format(IQURL)

	r = requests.get(SIDEBARURL, auth=(args.user, args.password), verify=False)

	sidebarList = json.loads(r.text)

	return sidebarList 

def get_tailoredlist(args, sideBarJson):

	appList = []

	for line in sideBarJson['organizations']:
		if line['name'] == 'ReleaseAutomatedScan':
			for row in line['applications']:
				if row['publicId'][:4] == args.appcode:
					appList.append(row['publicId'])
		elif line['name'] == args.appcode:
			for row in line['applications']:
				appList.append(row['publicId'])

	return appList

def dropAppList(appcode, appList):
	with open('applists/{}_applist.csv'.format( appcode), 'w') as f:
		writer = csv.writer(f)
		for row in appList:
			writer.writerow([row])

def main():
	args = setup()
	sideBarJson = get_applist(args)
	appList = get_tailoredlist(args, sideBarJson)

	dropAppList (args.appcode, appList)

if __name__ == "__main__":
	main()
