#!/bin/bash

####################################################################
# Author Arturo Noha
# v1, February 2017
# Script to build the venya images for AWS and push then to AWS
####################################################################

scriptname=$0
buildhome="/c/Users/arturo/OneDrive/VenYa/SOURCES/DOCKER_CONTAINERS"
DBBACKUP=./venya_aws_mongodb_bkp_restore.sh
JSON_PARSE="python read_json.py"

domain="venya.es"
mongoport=27017
db="venya"

awsregion="eu-west-1"

awsrepository="027674624948.dkr.ecr.eu-west-1.amazonaws.com"
dockerrepository="r2ronoha"
mongodir="$buildhome/MongoDB"
mongoimage="venya-mongodb-aws"
nodedir="$buildhome/NODE_SERVER"
nodeimage="venya-node-server-aws"
appdir="$buildhome/APP_CLIENT_AWS"
appimage="venya-web-aws"

bkpdest="$buildhome/MongoDB/AWS_DB_BKP"
noaccess="Could not access the MongoDB for bkp. Do you wish to continue? [Y/N] : "
wronginput="please enter a valide answer [Y/N] : "
logdir="$buildhome/logs"
logfile="$logdir/venya_aws_build.log"

githome="$buildhome"
gitsources=('NODE_SERVER/' 'APP_CLIENT_AWS/' 'MongoDB/mongoDB.cfg' 'MongoDB/Dockerfile')

echolog() {
	echo "`date +%Y-%m-%d_%H:%M:%S` : $@" | tee -a $logfile
}

rotate_log() {
	#archive log if bigger than max log size
	if [[ -f $logfile ]]; then
		logsize=`ls -sh $logfile | sed -e "s/^[ \t]\{1,\}//g" | cut -d' ' -f1`
		logsizenum=`ls -s $logfile | sed -e "s/^[ \t]\{1,\}//g" | cut -d' ' -f1`
		if [[ `echo "$logsize" | grep "$maxlogunit$" &> /dev/null; echo $?` -eq 0 && $logsizenum -gt $maxlogsize ]]; then
			TIMESTAMP=`date +%Y%m%d%H%M%S`
			echolog "Max log size reached. Archiving to $logfile.$TIMESTAMP" | tee -a $logfile
			mv $logfile $logfile.$TIMESTAMP
		fi
	fi
}

build_push() {
	# build the image and push it to AWS and Docker HUB
	if [[ $# -ne 2 ]]; then
		echolog "Wrong syntax. USAGE: build_push <build_directory> <image_name>"
		exit 1
	fi

	dir=$1
	image=$2

	echolog "BUILDING $image from $dir"
	echolog "---------------------"
	sleep 3
	cd $dir
	echolog "Building $dockerrepository/$image"
	docker build -t $dockerrepository/$image . 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"

	echolog "Tagging $awsrepository/$image:latest"
	docker tag $dockerrepository/$image:latest $awsrepository/$image:latest 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"

	echolog "Pushing $awsrepository/$image:latest to AWS"
	docker push $awsrepository/$image:latest 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"

	echolog "Pushing $dockerrepository/$image to Docker HUB"
	docker push $dockerrepository/$image 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"
}

git_commit() {
	gitmessage="$scriptname `date +%Y-%m-%d_%H%M%S`"

	if [[ $# -gt 1 ]]; then
		githome=$1
		if [[ $# -gt 2 ]]; then 
			gitmessage=$2
		fi
	fi

	cd $githome
	for gitsource in "${gitsources[@]}"; do
		echolog "Adding $gitsource to the git git build"
		git add $gitsource 2>&1 | tee -a $logdir
	done

	echolog "Commiting \"$gitmessage\""
	git commit -m "$gitmessage" 2>&1 | tee -a $logdir
	echolog "Pushing build to Git HUB"
	git push origin master 2>&1 | tee -a $logdir
}

if [[ $# -lt 1 ]]; then
	echo "Usage: $0 <config file (json/conf)> [options]"
	exit 1
else
	conf_file=$1
fi

if [[ ! -f $conf_file ]]; then
	echolog "[ERROR] Could not find configuration file \"$conf\""
	echolog "EXIT"
	echolog "============================================================"
	exit 1
fi
echolog "#############################################################################"
echolog "START OF BUILD"
echolog "------------------------------------------------"
echolog "Copying configuration file to temporary conf file"

if [[ `echo $conf_file | grep ".json$" &> /dev/null; echo $?` -eq 0 ]]; then
	#echo "JSON"
	$JSON_PARSE $conf_file > tmp.conf
else
	#echo "config file"
	cat $conf_file > tmp.conf
fi
echolog "Reading parameters from $conf_file"
while read -r line; do
	if [[ `echo "$line" | grep "^[^=]\{1,\}=.\{1,\}" &> /dev/null; echo $?` -eq 0 ]]; then
		#echo "[DEBUG] processing line: \"$line\""
		key=`echo "$line" | cut -d'=' -f1`
		value=`echo "$line" | cut -d'=' -f2 | sed -e 's/^"\|"$//g'`
		#echo "[DEBUG] value = $value"
		export $key="$value"
	#else
		#echo "[DEBUG] SKIP \"$line\""
	fi
done < tmp.conf
#exit 0

echolog "Getting login to AWS region $awsregion"
getlogin=`aws ecr get-login --region $awsregion`
echolog "Login in to AWS"
$getlogin 2>&1 | tee -a $logfile
if [[ $? -ne 0 ]]; then
	echolog "Failed to access AWS region $awsregion."
	echolog "EXIT"
	exit 1
fi
#exit 0

$DBBACKUP backup
build_push $mongodir $mongoimage
build_push $nodedir $nodeimage
build_push $appdir $appimage
git_commit $githome

echolog "BUILD AND PUSH COMPLETED. Restart of the AWS task required"

read -p "*** Would you like to restore the DB? [Y/N] : " input
choice=`echo $input | tr '[:upper:]' '[:lower:]'`

while [[ "$choice" != "y" && "$choice" != "n" ]]
do
	read -p "$wronginput" input
	choice=`echo $input | tr '[:upper:]' '[:lower:]'`
done

if [ $choice == "y" ]; then
	$DBBACKUP restore
fi

echolog "==============================================================================="
echo "LOGS AVAILABLE at $logfile"
echo "BYE"
