#!/bin/bash

docker run --name mynginx -P -d nginx

# docker run \
# 	--rm \
# 	--name mynginx2 \
# 	-v /var/www:/usr/share/nginx/html:ro \
# 	-v /var/lib/etc/nginx/conf:/etc/nginx:ro \
# 	-P \
# 	-d nginx 
