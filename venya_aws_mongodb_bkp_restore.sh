#!/bin/bash

buildhome="/c/Users/arturo/OneDrive/VenYa/SOURCES/DOCKER_CONTAINERS"
domain="venya.es"
mongoport=27017
db="venya"
bkpdest="$buildhome/MongoDB/AWS_DB_BKP"
logfolder="$bkpdest/log"
logfile="$logfolder/venya-mongodb-backup-restore.log"
maxlogsize=1 #Max size of log file in MB
maxlogunit="M"
noaccess="Could not access the MongoDB for bkp. Do you wish to continue? [Y/N] : "
wronginput="please enter a valide answer [Y/N] : "
instance=""

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
echolog() {
	echo "`date +%Y-%m-%d_%H:%M:%S` : $@" | tee -a $logfile
}

check_ip_running() {
	if [[ $# -ne 1 ]]; then 
		echolog "[check_ip_log] Missing IP to check. Exit..."
		exit 1
	fi

	ip=$1
	echolog "checking if $ip is the running instance"

	# check if telnet is installed to check access to DB. If not available use `mongo --quiet` to check access
	echo exit | telnet &> /dev/null
	if [[ $? -eq 0 ]]; then
		echolog "Using telnet to check access to the DB"
		if [[ `echo exit | telnet $ip $mongoport | grep -i "connected to $ip"` != "" ]]; then
			instance=$ip
		fi
	else
		echolog "Using \"mongo --quiet\" to check access to the DB"
		if [[ `mongo --quiet --host $ip --port $mongoport &> /dev/null; echo $?` -eq 0 ]]; then
			instance=$ip
		fi
	fi
	
}

rotate_log

if [[ $# -lt 1 || ( "$1" != "restore" && "$1" != "backup" ) ]]; then
	echo "please enter a valid option: \"$0 [backup/restore]\""
	exit 1
else
	option=`echo "$1" | tr '[:lower:]' '[:upper:]'`

	# get domain name ip @'s
	echolog "Getting IP running instance for $domain"
	if [[ `nslookup  venya.es | grep -A1 "Name.*$domain" | grep "^Addresses:"` == "" ]]; then
		for instip in `nslookup $domain | grep -A 1 "Name.*$domain" | grep Address | sed -e "s/ //g" | cut -d':' -f2`; do
			check_ip_running $instip
			if [[ "$instance" == "$instip" ]]; then 
				echolog "Found instance: $instance"
				break
			fi
		done
	else
		for instip in `nslookup $domain | grep -A3 "Addresses" | grep -v "^$" | sed -e "s/^[ \t]\{1,\}/:/g" -e "s/ //g" | cut -d':' -f2`; do 
			check_ip_running $instip
			if [[ "$instance" == "$instip" ]]; then 
				echolog "Found instance: $instance"
				break
			fi
		done
	fi

	echolog "DB instance running on $instance"
	case "$option" in
		'BACKUP')
			# Backup MongoDB
			echolog ">> BACKING UP MONGO DB"	
			mongodump --host $instance --port $mongoport --db $db --out $bkpdest 2>&1 | tee -a $logfile
		;;
		'RESTORE')
			# Restore MongoDB
			echolog ">> RESTORE MONGO DB"
			mongorestore --host $instance --port $mongoport $bkpdest 2>&1 | tee -a $logfile
		;;
		*)
			echolog "invalide option $option"
		;;
	esac
fi
echolog "$option of $domain Mongo DB completed"
echolog "============================================================================="
echo "Logs available at $logfile"
echo "BYE"
