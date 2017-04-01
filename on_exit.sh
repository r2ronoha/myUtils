#!/bin/bash

scriptsdir="/c/Users/arturo/OneDrive/VenYa/scripts"
dbbackup="venya_aws_mongodb_bkp_restore.sh"
venyaStagingStart="start_venya_staging.sh"

buildhome="/c/Users/arturo/OneDrive/VenYa/SOURCES/DOCKER_CONTAINERS"
db="venya"
bkpdest="$buildhome/MongoDB/AWS_DB_BKP"
logfolder="$bkpdest/log"

# check if the latest backup file is older than 24h. if so backup, if not, skip
lastFile=`ls -rt $bkpdest/$db | tail -1`

if [[ `docker ps &> /dev/null; echo $?` -eq 0 ]]; then
	if test "`find $bkpdest/$db/$lastFile -mmin +$((24*60))`"; then
		echo ""
		echo "WARNING: DB backup is older than 24h. Backing up"
		echo "-----------------------------------------------------"
		$scriptsdir/$dbbackup backup
	else
		echo ""
		echo "** Backup is still recent. Nothing to do **"
		echo ""
	fi
	
	if [[ `docker images | grep "none" &> /dev/null; echo $?` -eq 0 ]]; then
		echo ""
		echo "WARNING: removing empty images"
		docker rmi -f $(docker images | grep "none" | awk '{print $3}')
	else
		echo ""
		echo "** no old images to remove **"
		echo ""
	fi	
else
	echo ""
	echo "!!! WARNING !!! COULD NOT ACCESS DOCKER ENVIRONMENT. SKIPPING DOCKER ENV CLEANING AND SET UP"
	echo ""
fi
