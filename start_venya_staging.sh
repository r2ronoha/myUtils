#!/bin/bash

home="/c/Users/arturo/OneDrive/Venya/SOURCES/DOCKER_CONTAINERS/STAGING"
mongodir="$home/MongoDB"
nodedir="$home/NODE_SERVER"
webdir="$home/APP_CLIENT_AWS"
DBIMPORT=/c/Users/arturo/OneDrive/Venya/scripts/staging_live_db_import.sh

echo ">> CLEANING EXISTING RUNNING ENVIRONMENT"
echo "--------------------------"
docker stop venya-mongodb venya-node-server venya-web
docker rm venya-mongodb venya-node-server venya-web
echo "============================================================"

echo ">> BUILDING MONGO IMAGE"
echo "--------------------------"
cd $mongodir
docker build -t r2ronoha/staging-venya-mongodb-aws .
echo ">> STARTING MONGODB"
echo "--------------------------"
docker run -d --rm -p 27017:27017 --name venya-mongodb r2ronoha/staging-venya-mongodb-aws
sleep 5

while getopts ":rb" opt; do
	case $opt in
		b)
			echo ">> BACKUP LIVE DB"
			$DBIMPORT -b
			#sleep 2
			echo "============================================================"
			;;
		r)
			echo ">> RESTORE LIVE DB"
			$DBIMPORT -r
			#sleep 2
			echo "============================================================"
			;;
		\?)
			echo "invalid option"
			;;
	esac
done

echo ">> BUILDING NODE SERVER IMAGE"
echo "--------------------------"
cd $nodedir
docker build -t r2ronoha/staging-venya-node-server-aws .
echo ">> STARTING NODE SERVER"
echo "--------------------------"
docker run -d -p 8888:8888 --name venya-node-server --link venya-mongodb r2ronoha/staging-venya-node-server-aws
sleep 2
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
