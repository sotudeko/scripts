#!/bin/bash

server=http://localhost:8080
user=solao
passwd=solao

jobfile=$1
jobname=$jobfile

cd job_configs

for jobfile in `ls -1 *.xml`
do
 echo Processing "$jobfile"
 jobname="${jobfile%.*}"
 java -jar ~/Downloads/jenkins-cli.jar -s $server -auth $user:$passwd create-job $jobname < $jobfile
done
