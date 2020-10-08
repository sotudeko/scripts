#!/bin/bash

docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog

## config.yml

#mail:
  # hostname: "127.0.0.1"
  # systemEmail: sotudeko@sonatype.com
  # port: 1025

# access mail at http://localhost:8025



