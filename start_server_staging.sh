#!/bin/bash

home="/c/Users/arturo/OneDrive/Venya/SOURCES/DOCKER_CONTAINERS/STAGING"
mongodir="$home/MongoDB"
nodedir="$home/NODE_SERVER"
webdir="$home/APP_CLIENT_AWS"
DBIMPORT=/c/Users/arturo/OneDrive/Venya/scripts/staging_live_db_import.sh

echo ">> CLEANING EXISTING RUNNING ENVIRONMENT"
echo "--------------------------"
docker stop venya-node-server
docker rm venya-node-server
echo "============================================================"

echo ">> BUILDING NODE SERVER IMAGE"
echo "--------------------------"
cd $nodedir
docker build -t r2ronoha/staging-venya-node-server-aws .
echo ">> STARTING NODE SERVER"
echo "--------------------------"
#docker run -d --rm -p 8888:8888 --name venya-node-server --link venya-mongodb r2ronoha/staging-venya-node-server-aws
docker run -d -p 8888:8888 --name venya-node-server --link venya-mongodb r2ronoha/staging-venya-node-server-aws
echo "============================================================"
sleep 5
docker ps
