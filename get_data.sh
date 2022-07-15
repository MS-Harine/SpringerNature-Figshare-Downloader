#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 file1 file2"
	echo "  - file1 : List of filenames"
	echo "  - file2 : List of links"

	exit -1
fi

if [ ! -d download ]; then
	mkdir download
fi

for i in $(seq $(( $(cat $2 | wc -l) + 1 )) )
do
	file_name=$(sed -n "${i}p" < $1)
	file_link=$(sed -n "${i}p" < $2)
	
	echo "Download ${i}th file"
	wget -O download/$file_name $file_link
done
