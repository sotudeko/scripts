
docker network create docker_scanning
docker run -p 5432:5432 -d --net=docker_scanning --name db arminc/clair-db
docker run -p 6060:6060  --net=docker_scanning --link db:postgres -d --name clair arminc/clair-local-scan

