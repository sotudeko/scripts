import json
import requests
import os
import os.path
import sys

iqurl = sys.argv[1]
iquser = sys.argv[2]
iqpwd = sys.argv[3]


def getNexusIqData(api):
	url = "{}{}" . format(iqurl, api)

	req = requests.get(url, auth=(iquser, iqpwd), verify=False)

	if req.status_code == 200:
		res = req.json()
	else:
		res = "Error fetching data"

	return res


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])


def writeJsonToFile(applicationEvaluations, fileName):
    with open(fileName, 'w', encoding='utf-8') as fd:
        json.dump(applicationEvaluations, fd, ensure_ascii=False, indent=4)

    print(fileName)
    
    return


def writeEvaluationInfo(applicationEvaluations):

    with open('applicationcomponents.csv', 'w') as fd:
        fd.write("ApplicationName,Evaluation Date, Stage, PackageUrl,CVEs\n")

        for applicationEvaluation in applicationEvaluations:

            stage = applicationEvaluation["stage"]
            evaluationDate = applicationEvaluation["evaluationDate"]
            applicationName = getApplicationName(applicationEvaluation["reportDataUrl"])
            reportDataUrl = applicationEvaluation["reportDataUrl"]

            evaluationData = getNexusIqData("/" + reportDataUrl)

            dComponents = evaluationData["components"]

            for component in dComponents:
                packageUrl = component["packageUrl"]
                securityData = component["securityData"]

                if packageUrl != None:
                    cves = ""
                    for securityIssue in securityData["securityIssues"]:
                        cves = securityIssue["reference"] + "," + cves
        
                    line = applicationName + "," + evaluationDate + "," + stage + "," + packageUrl + "," + cves +"\n"
                    fd.write(line)

    return


def main():

	applicationEvaluations = getNexusIqData('/api/v2/reports/applications')
    
    writeJsonToFile(applicationEvaluations, "applicationevaluations.json")

	writeEvaluationInfo(applicationEvaluations)

	print('evaluationInfo.csv')
	

				
if __name__ == '__main__':
	main()
