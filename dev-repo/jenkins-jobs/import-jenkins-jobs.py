import sys
import os
import re
from jenkins import Jenkins

jk = Jenkins(url='http://sola.local:8080', username='solao', password='a480305b97fdc9575aabde3717b96ea5')

config_dir = 'job_configs'

dir_list = os.listdir(config_dir)

folders = []
jobs = []

for f in dir_list:
   fn = config_dir + '/' + f

   fdescr = open(fn,'r')
   config_xml = fdescr.read()

   f = re.sub('__', '/', f)
   f = re.sub('.xml', '', f)

   if "com.cloudbees.hudson.plugins.folder.Folder" in config_xml:
     #print (f + ": is a folder")
     folders.append(f)
   else:
     #print (f + ": is a job")
     jobs.append(f)

for folder in folders:
    folder_name = 'zz_' + folder
    print ('creating folder: ' + folder_name)
    jk.create_folder(folder_name)

for job in jobs:
    job_name = 'zz_' + job
    print(job_name)
    jk.create_job(job_name, config_xml)

