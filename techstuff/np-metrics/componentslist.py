import nxiq

host = 'http://localhost:8070'
user = 'admin'
passwd = 'admin123'
conn = nxiq.Connection(host, user, passwd) 

def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])

def fmtDate(dateStr):
    d = dateStr.split('.')[0]
    d = d.replace('T', ' ')
    return d

def toFile(applicationReports):

	with open('applicationreportlinks.csv', 'w') as fd:
			fd.write("ApplicationName,Url\n")
			for report in applicationReports:
				dataUrl = report["reportDataUrl"]
				applicationName = getApplicationName(dataUrl)
				line = applicationName + "," + dataUrl + "\n"
				fd.write(line)
	
	print('applicationreportlinks.csv')
	return


def getDataUrl(applicationReports):
	for report in applicationReports:
		dataUrl = report["reportDataUrl"]
		applicationName = getApplicationName(dataUrl)
		reportDataUrl = "{}/{}".format(conn.getHost(), dataUrl)
		components = conn.getData('/' + dataUrl)
		listComponents(applicationName, components)


def listComponents(applicationName, data):
	components = data['components']
	for component in components:
		packageUrl = component['packageUrl']
		# licenses = component['licenseData']['effectiveLicenses']
		security = component['securityData']['securityIssues']
		line = "{},{}".format(applicationName, packageUrl)
		print(line)



def main():
	ar = conn.getApplicationReports()
	toFile(ar)
	getDataUrl(ar)


if __name__ == "__main__":
	main()