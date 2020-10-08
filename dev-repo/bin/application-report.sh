#!/bin/bash

counter=0;

cd /opt/nxiq/sonatype-work/clm-server/report;

for apps in `ls`; do
    if [ -d ${apps} ]; then
        echo "moving into app directory $apps";
        cd $apps;
        counter=0;
        for i in `ls -t`; do
            if [ -d ${i} ]; then
                counter=$((counter + 1));
                echo "$i is a directory";
                if [ $counter = 1 ]; then
                    echo "most recent report directory, keep it";
                else
                    echo "older report directory, delete it";
                    echo rm -rf ${i};
                fi
            else
                echo "$i is a file";
            fi
        done;
        echo "moving out of the app directory $apps";
        cd ..;
    fi
done;


