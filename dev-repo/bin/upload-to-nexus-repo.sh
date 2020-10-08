#!/bin/bash

uploadfile=my-package-1.0.1.jar
curl -v -u admin:admin123 --upload-file ${uploadfile} http://localhost:8081/repository/maven-releases/com/example/my-package/1.0.1/my-package-1.0.1.jar