#!/bin/bash

home="/c/Users/arturo/OneDrive/Venya/SOURCES/DOCKER_CONTAINERS/STAGING"
mongodir="$home/MongoDB"
nodedir="$home/NODE_SERVER"
webdir="$home/APP_CLIENT_AWS"
DBIMPORT=/c/Users/arturo/OneDrive/Venya/scripts/staging_live_db_import.sh

echo ">> CLEANING EXISTING RUNNING ENVIRONMENT"
echo "--------------------------"
docker stop venya-web
docker rm venya-web
echo "============================================================"

echo ">> BUILDING WEB APP IMAGE"
echo "--------------------------"
cd $webdir
docker build -t r2ronoha/staging-venya-web-aws .
echo ">> STARTING WEB APP"
echo "--------------------------"
docker run -d --rm -p 80:5000 --name venya-web --link venya-node-server r2ronoha/staging-venya-web-aws
echo "============================================================"
sleep 5
docker ps
