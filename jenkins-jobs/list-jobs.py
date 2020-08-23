import sys

from jenkins import Jenkins

j = Jenkins(url='http://sola.local:8080', username='solao', password='a480305b97fdc9575aabde3717b96ea5')

w = j.get_whoami()

print(w)

jobs = j.get_all_jobs()

for j in jobs:
  # print(j['name'] + ' --> ' + j['fullname'])
  print(j['fullname'])






