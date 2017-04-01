#!/bin/bash

if [[ $# -lt 1 ]]; then
	echo "usage $0 <id>"
	exit 1
else 
	id=$1
fi
curl http://192.168.99.100:8888/updateSetting?action=update\&type=customer\&id=$id\&field=sessionid\&newvalue=closed
