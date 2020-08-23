#!/bin/bash

docker run  -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin123 -e DB_VENDOR=h2 -p 8180:8080 jboss/keycloak

