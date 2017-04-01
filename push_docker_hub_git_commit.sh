#!/bin/bash

if [ $# -lt 1 ]; then
	echo "[`date +%Y-%m-%d_%H:%M:%S`] You need to provide a message for the git commit"
	exit 1
fi

message=$1
basedir="/c/Users/arturo/OneDrive/Venya/SOURCES/DOCKER_CONTAINERS"
cd $basedir

echo "[`date +%Y-%m-%d_%H:%M:%S`] docker push r2ronoha/venya-mongodb-aws"
docker push r2ronoha/venya-mongodb-aws

echo "[`date +%Y-%m-%d_%H:%M:%S`] docker push r2ronoha/venya-node-server-aws"
docker push r2ronoha/venya-node-server-aws

echo "[`date +%Y-%m-%d_%H:%M:%S`] docker push r2ronoha/venya-web-aws"
docker push r2ronoha/venya-web-aws

echo "[`date +%Y-%m-%d_%H:%M:%S`] adding folders to git (NODE_SERVER, APP_CLIENT_AWS/, MongoDB/mongoDB.cfg, MongoDB/Dockerfile"
echo "git add NODE_SERVER/"
git add NODE_SERVER/
echo "git add APP_CLIENT_AWS/"
git add APP_CLIENT_AWS/
echo "git add MongoDB/mongod.cfg"
git add MongoDB/mongod.cfg
echo "git add MongoDB/Dockerfile*"
git add MongoDB/Dockerfile*
echo "git commit -m \"$message\""
git commit -m "$message"
echo "git push origin master"
git push origin master

echo "[`date +%Y-%m-%d_%H:%M:%S`] Push to Docker HUB and GIT HUB COMPLETED"
