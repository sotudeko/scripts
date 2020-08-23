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
	with open("successmetrics.json", 'wb') as fd:
            for chunk in req.iter_content(chunk_size=128):
                fd.write(chunk)

def main():
	get_metrics()

				
if __name__ == '__main__':
	main()
