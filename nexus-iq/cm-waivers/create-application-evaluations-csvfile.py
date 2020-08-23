import json
import requests
import os
import os.path
import sys

iqurl = sys.argv[1]
iquser = sys.argv[2]
iqpwd = sys.argv[3]


def get_metrics():
	req = requests.get('{}/api/v2/reports/applications'.format(iqurl), auth=(iquser, iqpwd), verify=False)
	
	if req.status_code == 200:
		res = req.json()
	else:
		res = "Error fetching data"

	return res


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])


def writeToCsvFile(applicationEvaluations):

	with open('applicationevaluations.csv', 'w') as fd:
			fd.write("ApplicationName,EvaluationDate,Stage\n")
			for applicationEvaluation in applicationEvaluations:
				stage = applicationEvaluation["stage"]
				evaluationDate = applicationEvaluation["evaluationDate"]
				applicationId = applicationEvaluation["applicationId"]
				applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
				line = applicationName + "," + evaluationDate + "," + stage + "\n"
				fd.write(line)
	
	print('applicationevaluations.json')
	return


def main():
	applicationEvaluations = get_metrics()

	with open("applicationevaluations.json", 'w') as fd:
    		json.dump(applicationEvaluations, fd)
	

	writeToCsvFile(applicationEvaluations)
	print('applicationevaluations.csv')


				
if __name__ == '__main__':
	main()
