import sys

from jenkins import Jenkins

j = Jenkins(url='http://sola.local:8080', username='solao', password='a480305b97fdc9575aabde3717b96ea5')

job = j.get_job_config('Route-To-Live/WebGoat-Build')

print(job)