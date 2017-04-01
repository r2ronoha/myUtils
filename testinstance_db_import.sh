#!/bin/bash

buildhome="/c/Users/arturo/OneDrive/VenYa/SOURCES/DOCKER_CONTAINERS"
staginghome="$buildhome/STAGING"
domain="venya.es"
mongoport=27017
db="venya"
localmachine="34.252.180.8"
bkpdest="$buildhome/MongoDB/AWS_DB_BKP"
logfolder="$staginghome/log"
logfile="$logfolder/live_db_mirror.log"
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

option=`echo "$1" | tr '[:lower:]' '[:upper:]'`

while getopts ":rb" opt; do
	case "$opt" in
		b)
			echolog "backup live DB"
			# get domain name ip @'s
			echolog "Getting IP running Live instance for $domain"
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
			
			# Backup live MongoDB
			echolog ">> BACKING UP LIVE MONGO DB"	
			mongodump --host $instance --port $mongoport --db $db --out $bkpdest 2>&1 | tee -a $logfile
		;;
		r)
			echolog "Restore from live backup"
			# Restore MongoDB to staging DB
			echolog ">> RESTORE MONGO DB INTO STAGING DB"
			mongorestore --host $localmachine --port $mongoport $bkpdest 2>&1 | tee -a $logfile
		;;
		\?)
			echolog "unknow option $opt. Exit"
			return
	esac
done

echolog "Mirroring of Live Mongo DB to staging completed"
echolog "============================================================================="
echo "Logs available at $logfile"
echo "BYE"
