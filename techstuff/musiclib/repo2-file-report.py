#!/usr/bin/env python

import os
import os.path, time
import subprocess

nexus2_storage_directory = '/opt/nxrm2/sonatype-work/nexus/storage/'  # DO incl trailing slash
repo2_id = ""
#repo2_id = "releases-repo"

full_path_length = len(nexus2_storage_directory) + len(repo2_id)

for base, dirs, files in os.walk(str(nexus2_storage_directory) + str(repo2_id)):
    # print base
    # print dirs
    # print files

    for file in files:
        if file[:1] != '.':
            if base[(full_path_length+1):(full_path_length+2)] != '.': # ignore hidden directories
                full_path = str(base) + '/' + str(file)

                if str(full_path[-3:]) not in ("pom", "md5", "sha1", "xml"):
                    statinfo = os.stat(full_path)

                    # print full_path
                    print file
                    print "Size: %d" % (statinfo.st_size)
                    print("Created: %s" % time.ctime(os.path.getctime(full_path)))
                    print("Last modified: %s" % time.ctime(os.path.getmtime(full_path)))
                    print ""

                   


