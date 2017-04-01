#!/bin/bash

if [[ $# -ne 2 ]]; then
	echo "usage $0 <username> <password>"
	exit 1
else 
	username=$1
	password=$2
fi
venyaurl="http://192.168.99.100:8888"
curl $venyaurl/updateSetting?action=update\&type=customer\&id=$(curl $venyaurl/getCustomer?action=login\&username=$username\&password=$password | awk -F'"id":"' '{print $2}' | cut -d'"' -f1)\&field=sessionid\&newvalue=closed
