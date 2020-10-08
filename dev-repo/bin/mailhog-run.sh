#!/bin/bash

# Edit config.yml
# * Enable mail
# * Set SMTP port to 1025

# Check sent emails at http://localhost:8025/#

# https://github.com/mailhog/MailHog


docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

