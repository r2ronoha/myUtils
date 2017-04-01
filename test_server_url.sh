#!/bin/bash

staging_server="192.168.99.100"
live_server="venya.es"
port=8888


urlparams=""

while getopts ":lst:r:u:p:-:" opt; do
	case $opt in
		-)
			case $OPTARG in
				request)
					target="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					;;
				target)
					target="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					;;
				action)
					action="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}action=${action}&"
					;;
				customerid)
					customerid="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}customerid=$customerid&"
					;;
				providerid)
					providerid="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}providerid=${providerid}&"
					;;
				sessionid)
					sessionid="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}sessionid=${sessionid}&"
					;;
				appointmentid)
					appointmentid="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}appointmentid=${appointmentid}&"
					;;
				username)
					username="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}username=${username}&"
					;;
				password)
					password="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}password=${password}&"
					;;
				id)
					id="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					urlparams="${urlparams}id=${id}&"
					;;
				ip)
					staging_server="${!OPTIND}"
					OPTIND=$((OPTIND + 1))
					;;
			esac
			;;
		t)
			target=$OPTARG
			;;
		r)
			target=$OPTARG
			;;
		l)
			venyaUrl="http://$live_server:$port"
			;;
		u)
			urlparams="${urlparams}username=${OPTARG}&"
			;;
		p)
			urlparams="${urlparams}password=${OPTARG}&"
			;;
		:)
			echo "option -$OPTARG requires an argument"
			exit 1
			;;
	esac
done
venyaUrl="http://$staging_server:$port"
urlparams=`echo $urlparams | sed -e "s/\\\\\\&$//g"`
url="${venyaUrl}/${target}?${urlparams}"
echo "url: $url"
curl $url
