#!/bin/bash

conan --version
conan remote list
conan remote remove conan-center
conan remote list
conan remote add conan-proxy http://localhost:8081/repository/conan-proxy/ false
conan remote list
rm -rfv ~/.conan
