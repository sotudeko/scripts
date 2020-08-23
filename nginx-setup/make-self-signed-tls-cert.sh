#!/bin/bash

# https://support.sonatype.com/hc/en-us/articles/213465768-SSL-Certificate-Guide?_ga=2.159121658.1745357296.1567936651-791282984.1515494824

if [[ $# -ne 1 ]]; 
    then echo "$0 <hostname>"
    exit 1
fi

server_name=$1
keystore_file=keystore.jks
tmpdir=./tmp.$$
mkdir ${tmpdir} && cd ${tmpdir}

# delete existing key
# keytool -delete -alias ${server_name} -keystore keystore.jks -storepass password 

# Generate public private key pair using keytool
echo step 1
keytool -genkeypair -keystore ${keystore_file} -storepass password -alias ${server_name} \
 -keyalg RSA -keysize 2048 -validity 5000 -keypass password \
 -dname "CN=*.${server_name}, OU=Sonatype, O=Sonatype, L=London, ST=LOndon, C=GB" 
 #-ext "SAN=DNS:nexus.${server_name},DNS:clm.${server_name},DNS:repo.${server_name},DNS:www.${server_name}"
 # -> keystore.jks

# Convert Java specific keystore binary".jks" file to a widely compatible PKCS12 keystore ".p12" file
echo step 2
keytool -importkeystore -storepass password -srckeystore ${keystore_file} -destkeystore ${keystore_file} -deststoretype pkcs12
# -> keystore.jks

exit

# Generate PEM encoded public certificate file using keytool
echo step 3
keytool -exportcert -keystore ${keystore_file} -storepass password -alias ${server_name} -rfc > ${server_name}.cert
# -> server_name.cert 

# Extract a self signed X.509 certificate from the keystore
#keytool -export -alias jetty -keystore keystore.jks -rfc -file nexus.cer

# List and verify new keystore file contents
echo step 4
keytool -list -keystore ${keystore_file} -storepass password -storetype PKCS12

# Extract pem (certificate) from ".p12" keystore file ( this is same as step 2, but openssl spits out more verbose contents )
echo step 5
openssl pkcs12 -nokeys -in ${server_name}.p12 -out ${server_name}.pem
# -> ${server_name}.pem 

# Extract unencrypted private key file from ".p12" keystore file
echo step 6
openssl pkcs12 -nocerts -nodes -in ${server_name}.p12 -out ${server_name}.key
# -> ${server_name}.key

echo ${tmpdir}
