import sys
import re

from jenkins import Jenkins

jk = Jenkins(url='http://sola.local:8080', username='solao', password='a480305b97fdc9575aabde3717b96ea5')

jobs = jk.get_all_jobs()

for j in jobs:
  job_name = j['fullname']
  print (job_name)

  job_config = jk.get_job_config(job_name)

  job_name = re.sub('/','__', job_name)

  of = 'job_configs/' + job_name + '.xml'

  f = open(of,'w')
  f.write(job_config)
  f.close()











