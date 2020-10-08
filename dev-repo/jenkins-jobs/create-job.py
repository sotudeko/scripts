import sys

from jenkins import Jenkins

j = Jenkins(url='http://sola.local:8080', username='solao', password='a480305b97fdc9575aabde3717b96ea5')

f = open('job.xml','r')

config_xml = f.read()

job = j.create_job('Route-To-Live/WebGoat-Build-2', config_xml)

print(job)