#!/bin/bash

OLDIFS=$IFS

for file in `ls *.html`; do
	echo "## $file"
	echo "--------"
	cp -vp $file $file.ori
	rm $file.tmp
	IFS=''
	while read line; do
		if [[ `echo "$line" | grep "</head>" &> /dev/null; echo $?` -eq 0 ]]; then
			echo -e "\t<script type=\"text/javascript\" src=\"/static/common/languages.js\"></script>" >> $file.tmp
		fi
		echo "$line" >> $file.tmp
	done < $file
	echo "diff $file $file.tmp"
	diff $file $file.tmp
	mv $file.tmp $file
	echo "----------------"
done
IFS=$OLDIFS
