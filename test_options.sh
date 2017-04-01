#!/bin/bash

usage() { echo "usage: $0 [-i <image-name>] [-a]" 1>&2; exit 1; }

while getopts ":i:a:" opt; do
	case "${opt}" in
		i)
			image=${OPTARG}
			( $image != "" ) || usage
			echo "building image $image"
			;;
		a)
			echo "full build"
			;;
		*)
			usage
			;;
	esac
done
