#!/bin/bash

artifact_name=demo-package-1.0.2.jar

gid=com.example
art=demo-package
ver=1.0.2

mvn deploy:deploy-file \
	-DgroupId=${gid} \
	-DartifactId=${art} \
	-Dversion=${ver} \
	-DgeneratePom=true \
	-Dpackaging=jar \
	-DrepositoryId=nexus \
	-Durl=http://localhost:8081/repository/maven-releases \
	-Dfile=target/${artifact_name} \
	-s /Users/sotudeko/.m2/.settings.xml

#mvn deploy:deploy-file -DgroupId=${gid} -DartifactId=${art} -Dversion=${ver}-SNAPSHOT -DgeneratePom=true -Dpackaging=jar -DrepositoryId=nexus -Durl=http://localhost:8081/repository/maven-snapshots -Dfile=target/${artifact_name}-SNAPSHOT.jar
