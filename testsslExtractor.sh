#!/bin/bash

#Author: n0t4u
#Description: Easy testssl parser for several IPs

#TODO. Add IP and domain in output
#TODO. Clean path

#Colors
Green='\033[0;32m'	# Green
Red='\033[0;31m'	# Red
Blue='\033[1;34m'	# Bold blue
Bold='\033[1;39m'	# Bold white
ColorOff='\033[0m'	# Text Reset


declare -a vulns=('ROBOT' 'Secure Renegotiation' 'Secure Client_Initiated Renegotiation' 'CRIME' 'BREACH' 'POODLE' 'TLS_FALLBACK_SCSV' 'SWEET32' 'FREAK' 'DROWN' 'LOGJAM' 'BEAST' 'LUCKY13' 'Winshock' 'RC4')

if [ "$#" -lt 1 ]; then
	route="."
else
	route="${1}"
fi
if command -v testssl; then
	for vuln in "${vulns[@]}"; do
		echo -e "\n${Blue}${vuln}${ColorOff}"
		for file in $(ls ${route}/testssl_*.log); do
			domain=$(echo -e "${file}" | rev | cut -d '/' -f1 |rev|  sed 's/\(testssl_\|\.log\)//g';)
			ips=$(cat ${file} | grep -P '(?<=\-\-\>\> )[\d\.]{7,15}(?=:[\d]{1,5} [\S]* \<\<\-\-)' -o | uniq | sed ':a;N;$!ba;s/\n/, /g')
			echo -e "${ColorOff}${Bold}${domain}${ColorOff}\t (${ips})" 
			
			cat $file | grep -v Grade | grep -P "${vuln}";
		done
	done
fi
