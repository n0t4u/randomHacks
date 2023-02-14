#!/usr/bin/env bash

#nmapScans
#Author: n0t4u
#Description: Bash script that executes a full ports scan, parse the results and performs a second scan with version option only to the open ports.

#Colors
Green='\033[0;32m'        # Green
Red='\033[0;31m'          # Red
Blue='\033[0;34m'         # Blue
ColorOff='\033[0m'       # Text Reset

#Default options
options="-sT -T3 -Pn -n -v --open"
scanned=()

nmap() {
	echo -e "${Blue}[*] Nmap basic scan to ${1} with options ${2}${ColorOff}"
	echo "${1} ${2}"
	sudo sh -c "nmap ${2} -p- -oA nmap_p_${1} ${1}"
	sudo chown "$USER":"$USER" nmap_p_"${1}".*
}

getOpenPorts() {
	ports=$(grep -P -o "[\d]+\/open\/[\S]+\/\/([\S]+[\/]{3,})?" nmap_p_"$1".gnmap | cut -d "/" -f 1 | sed ':a;N;$!ba;s/\n/,/g')
	echo "${ports}"
}

nmapsV() {
	echo -e "${Blue}[*] Nmap version scan to ${1} and ports ${2} with options ${3}${ColorOff}"
	echo "${1} ${3}"
	sudo sh -c "nmap ${3} -sV -sC -p ${2} -oA nmap_sV_${1} ${1}"
	sudo chown "$USER":"$USER" nmap_sV_"${1}".*
	scanned+=("${1}")
}

trap_ctrlc() {
	echo -e "${Red}[X] CTRL+C signal detected. Aborting port scanning...${ColorOff}"
	echo -e "Assets fully scanned:\n"
	for asset in "${scanned[@]}"; do
		echo "${asset}"
	done
	exit 4
}

#Main
trap trap_ctrlc SIGINT SIGTERM #2

if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
	echo -e "${Red}[x] Only two arguments can be provided: File/IP and scan options (optional)${ColorOff}"
	exit 1
elif [ "$#" -eq 2 ]; then
	options=$2
fi
echo -e "${Blue}Options${ColorOff}\t$2"
if [[ -f $1 ]]; then
	echo -e "${Blue}File${ColorOff}\t$1"
	while read -r ip; do
		nmap "${ip}" "${options}"
		openPorts=$(getOpenPorts "${ip}")
		if [[ -z "${openPorts}" ]]; then
			echo -e "${ip} has no open ports."
			scanned+=("${ip}")
		else
			nmapsV "${ip}" "${openPorts}" "${options}"
		fi
	done < "$1"
else
	echo -e "${Blue}IP${ColorOff}\t$1"
	nmap "${1}" "${options}"
	openPorts=$(getOpenPorts "$1")
	if [[ -z "${openPorts}" ]]; then
		echo -e "${1} has no open ports."
	else
		#echo -e "${openPorts}"
		nmapsV "${1}" "${openPorts}" "${options}"
	fi
fi

echo -e "${Green}Script finished sucessfully${ColorOff}"
exit 0