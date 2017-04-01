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

awsloginpwd="$buildhome/aws.tok"
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
gitmessage=""

echolog() {
	echo "`date +%Y-%m-%d_%H:%M:%S` : $@" | tee -a $logfile
}

aws_login() {
	loginexpired=false
	echolog "checking if credentials are still valid"
	if [[ -f $awsloginpwd ]]; then
		awspwd=`cat $awsloginpwd`
		if [[ `docker login -u AWS -p $awspwd -e none https://$awsrepository &> /dev/null; echo $?` -ne 0 ]]; then
			echolog "login to aws expired. Renewing it."
			loginexpired=true
		fi
	else
		echolog "credentials not available. Getting new ones"
		loginexpired=true
	fi

	if [[ $loginexpired ]]; then
		aws ecr get-login --region $awsregion | awk -F "-p " '{print $2}' | cut -d' ' -f1 > $awsloginpwd
		if [[ $? -ne 0 ]]; then
			echolog "ERROR: FAILED to get AWS Credentials. Abort"
			exit 1
		fi
		awspwd=`cat $awsloginpwd`
		docker login -u AWS -p $awspwd -e none https://$awsrepository 2>&1 | tee -a $logfile
		if [[ $? -ne 0 ]]; then
			echolog "ERROR: FAILED to login to AWS. Abort"
			exit 1
		fi
	fi
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

parse_file() {
	if [[ $# -ne 1 ]]; then
		echolog "Wrong syntax. USAGE: parse_file <conf_file>"
		exit 1
	fi

	myconf_file=$1

	echolog "Copying configuration file to temporary conf file"
	if [[ `echo $myconf_file | grep ".json$" &> /dev/null; echo $?` -eq 0 ]]; then
		#echo "JSON"
		$JSON_PARSE $myconf_file > tmp.conf
	else
		#echo "config file"
		cat $myconf_file > tmp.conf
	fi
	echolog "Reading parameters from $myconf_file"
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
}

#build_push() {
#}
full_build_push(){
	if [[ $# -lt 1 || $(($# % 2)) -ne 0 ]]; then
		echolog "Wrong syntax. USAGE: full_build_push <build_directory1 image_name1> [build_directory2 image_name2 [...]]"
	exit 1
	fi
	n=1
	#for image_info in $@
	while (( "$#" ))
	do
		if [[ $((n % 2)) -eq 1 ]]; then
			dir=$1
			n=$(($n + 1))
		else
			image=$1
			n=$(($n + 1))

			echo "dir=$dir --- image=$image"
			if [[ ! -d $dir ]]; then
				echolog "Folder $dir for image $image does not exist. Skipping..."
			else
				build_image $dir $image
				push_aws_image $image
				push_hub_image $image
			fi
		fi
	shift
	done
	#git_commit
}

build_image() {
	if [[ $# -ne 2 ]]; then
		echolog "Wrong syntax. USAGE: build_image <build_directory> <image_name>"
		exit 1
	fi

	mydir=$1
	myimage=$2

	echolog "BUILDING $myimage from $mydir"
	echolog "---------------------"
	sleep 3
	cd $mydir
	echolog "Building $dockerrepository/$myimage"
	#docker build -t $dockerrepository/$image . 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"
}

push_aws_image() {
	if [[ $# -ne 1 ]]; then
		echolog "Wrong syntax. USAGE: push_aws_image <image_name>"
		exit 1
	fi

	myimage=$1

	aws_login

	echolog "Tagging $awsrepository/$myimage:latest"
	#docker tag $dockerrepository/$myimage:latest $awsrepository/$myimage:latest 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"

	echolog "Pushing $awsrepository/$myimage:latest to AWS"
	#docker push $awsrepository/$myimage:latest 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"
}

push_hub_image(){
	if [[ $# -ne 1 ]]; then
		echolog "Wrong syntax. USAGE: push_hub_image <image_name>"
		exit 1
	fi

	myimage=$1

	echolog "Pushing $dockerrepository/$myimage to Docker HUB"
	#docker push $dockerrepository/$myimage 2>&1 | tee -a $logfile
	echolog "--------------------------------------------"
}

git_commit() {
	if [[ $gitmessage == "" ]]; then
		gitmessage="$scriptname `date +%Y-%m-%d_%H%M%S`"
		echolog "No MESSAGE for GIT COMMIT provided. Setting it to automated $gitmessage"
	fi

	if [[ $# -gt 1 ]]; then
		githome=$1
		if [[ $# -gt 2 ]]; then 
			gitmessage=$2
		fi
	fi

	cd $githome
	for gitsource in "${gitsources[@]}"; do
		echolog "Adding $gitsource to the git git build"
		git add $gitsource 2>&1 | tee -a $logfile
	done

	echolog "Commiting \"$gitmessage\""
	git commit -m "$gitmessage" 2>&1 | tee -a $logfile
	echolog "Pushing build to Git HUB"
	git push origin master 2>&1 | tee -a $logfile
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

## Available functions
# echolog() - aws_login() - rotate_log() - parse_file() - full_build_push()- build_image() - push_aws_image() - push_hub_image()- git_commit()

while getopts ":f:" opt; do
	case $opt in
		f)
			full_build_push $mongodir $mongoimage $nodedir $nodeimage $appdir $appimage
			;;
		\?)
			## Build options menu
			echolog "unknown option $opt."
			;;
	esac
done

echolog "#############################################################################"
echolog "START OF BUILD"
echolog "------------------------------------------------"

#parse_file $conf_file

#aws_login

full_build_push $mongodir $mongoimage $nodedir $nodeimage $appdir $appimage
#$DBBACKUP backup
#build_push $mongodir $mongoimage
#build_push $nodedir $nodeimage
#build_push $appdir $appimage
#git_commit $githome

#echolog "BUILD AND PUSH COMPLETED. Restart of the AWS task required"
#
#read -p "*** Would you like to restore the DB? [Y/N] : " input
#choice=`echo $input | tr '[:upper:]' '[:lower:]'`
#
#while [[ "$choice" != "y" && "$choice" != "n" ]]
#do
#	read -p "$wronginput" input
#	choice=`echo $input | tr '[:upper:]' '[:lower:]'`
#done
#
#if [ $choice == "y" ]; then
#	$DBBACKUP restore
#fi

echolog "==============================================================================="
echo "LOGS AVAILABLE at $logfile"
echo "BYE"
