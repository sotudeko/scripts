import sys
import os
import re
from jenkins import Jenkins

jk = Jenkins(url='http://sola.local:8080', username='solao', password='a480305b97fdc9575aabde3717b96ea5')

with open('jobs.lst') as f:
    jobs_list = f.read().splitlines()

for f in jobs_list:
  print(f)
  jk.delete_job(f)

