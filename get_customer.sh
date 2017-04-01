#!/bin/bash

if [[ $# -lt 2 ]]; then
	echo "usage $0 <username> <password>"
	exit 1
else 
	username=$1
	password=$2
fi

server_ip="192.168.99.100"
if [[ $# -eq 3 ]]; then
	server_ip=$3
fi
curl http://$server_ip:8888/getCustomer?action=login\&type=customer\&username=$username\&password=$password
