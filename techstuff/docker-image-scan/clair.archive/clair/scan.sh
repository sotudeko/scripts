
image=$1
docker run --net=docker_scanning --rm --name=scanner --link=clair:clair -v "`pwd`:/tmp" -v '/var/run/docker.sock:/var/run/docker.sock'  objectiflibre/clair-scanner --clair="http://clair:6060" --ip="scanner" -r /tmp/centos-clair.json -t Medium ${image}

