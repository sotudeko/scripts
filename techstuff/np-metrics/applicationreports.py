import nxiq

host = 'http://localhost:8070'
user = 'admin'
passwd = 'admin123'


def getApplicationName(urlPath):
	l = urlPath.split('/')
	return(l[3])

def fmtDate(dateStr):
    d = dateStr.split('.')[0]
    d = d.replace('T', ' ')
    return d

def toFile(applicationReports):

	with open('applicationreports.csv', 'w') as fd:
			fd.write("ApplicationName,ReportDate,Stage\n")
			for report in applicationReports:
				stage = report["stage"]
				reportDate = fmtDate(report["evaluationDate"])
				applicationId = report["applicationId"]
				applicationName = getApplicationName(report["reportDataUrl"])
				line = applicationName + "," + reportDate + "," + stage + "\n"
				fd.write(line)
	
	print('applicationreports.csv')
	return


def main():

    conn = nxiq.Connection(host, user, passwd) 
    ar = conn.getApplicationReports()
    toFile(ar)


if __name__ == "__main__":
	main()