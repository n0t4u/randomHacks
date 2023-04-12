#!/usr/bin/env bash

#nmapScans
#Author: n0t4u
#Description: Bash script that executes a full ports scan, parse the results and performs a second scan with version option only to the open ports.

#Colors
Green='\033[0;32m'	# Green
Red='\033[0;31m'	# Red
Blue='\033[0;34m'	# Blue
Bold='\033[1m'		# Bold
ColorOff='\033[0m'	# Text Reset

#Default options
options="-sT -T3 -Pn -n -v --open"
scanned=()
resume=false
user=""

help_banner() {
	echo -e """${Blue}${Bold}============================================

		nmapScans.sh

===========================(This is n0t4u)==${ColorOff}

${Bold}Usage:${ColorOff} ./nmapScans.sh <FILE/IP> [scan_options] [--resume]

${Bold}Example:${ColorOff} ./nmapScans.sh 192.168.1.200 '-sS -T2 -Pn --reason'

${Bold}Current default scan options:${ColorOff} ${options}"""
}

nmap() {
	echo -e "${Blue}[*] Nmap basic scan to ${1} with options ${2}${ColorOff}"
	echo "${1} ${2}"
	sudo sh -c "nmap ${2} -p- -oA nmap_p_${1} ${1}"
	if [ $? -eq 130 ]; then
		trap_ctrlc
	else
		sudo chown "${user}":"${user}" nmap_p_"${1}".*
	fi
}

getOpenPorts() {
	ports=$(grep -P -o "[\d]+\/open\/[\S]+\/\/([\S]+[\/]{3,})?" nmap_p_"$1".gnmap | cut -d "/" -f 1 | sed ':a;N;$!ba;s/\n/,/g')
	echo "${ports}"
}

nmapsV() {
	echo -e "${Blue}[*] Nmap version scan to ${1} and ports ${2} with options ${3}${ColorOff}"
	echo "${1} ${3}"
	sudo sh -c "nmap ${3} -sV -sC -p ${2} -oA nmap_sV_${1} ${1} " # --allports --version-all
	if [ $? -eq 130 ]; then
		trap_ctrlc
	else
		scanned+=("${1}")
		sudo chown "${user}":"${user}" nmap_sV_"${1}".*
	fi
}

writeLog(){
	for asset in "${scanned[@]}"; do
		echo "${asset}" >> ./.nmapScans.log
	done
}

trap_ctrlc() {
	echo -e "${Red}[X] CTRL+C signal detected. Aborting port scanning...${ColorOff}"
	echo "${#scanned}"
	if [ ${#scanned} -eq 0 ]; then
		echo -e "Any assets were fully scanned"
	else
		echo -e "Assets fully scanned:\n"
		for asset in "${scanned[@]}"; do
			echo "${asset}"
			echo "${asset}" >> ./.nmapScans.log
		done
	fi
	exit 4
}

#Main
trap trap_ctrlc SIGINT SIGTERM #2
echo "Current user: $USER"
user=$(who a mi | awk '{print $1}')

if [ "$#" -lt 1 ] || [ "$#" -gt 4 ]; then
	help_banner
	exit 1
elif [ "$#" -eq 3 ]; then
	if [ "$3" = "--resume" ] && [ -f ./.nmapScans.log ]; then
		resume=true
	else
		echo -e "${Red}Wrong arguments provided. Run nmapScan.sh --help for usage.${ColorOff}"
	fi
	options=$2
	echo "" > ./.nmapScans.log
elif [ "$#" -eq 2 ]; then
	if [ "$2" = "--resume" ]; then
		if [ -f ./.nmapScans.log ]; then
			resume=true
			echo true
		fi
	else
		options=$2
		echo "" > ./.nmapScans.log
	fi
fi
touch ./.nmapScans.log
echo -e "${Blue}Options${ColorOff}\t${options}"
if [[ -f $1 ]]; then
	echo -e "${Blue}File${ColorOff}\t$1"
	while read -r ip; do
		if [ "${resume}" = true ] && [ $(grep -c "${ip}" ./.nmapScans.log) -ne 0 ];then
			echo -e "${Green}${ip} already scanned. Skipped.${ColorOff}"
			continue
		else
			nmap "${ip}" "${options}"
			if [ $? -ne 130 ]; then
				openPorts=$(getOpenPorts "${ip}")
				if [[ -z "${openPorts}" ]]; then
					echo -e "${ip} has no open ports."
					scanned+=("${ip}")
				else
					nmapsV "${ip}" "${openPorts}" "${options}"
				fi
			fi
		fi
	done < "$1"
else
	if [ $1 = "--help" ] || [ $1 = "-h" ]; then
		help_banner
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
fi
writeLog
echo -e "${Green}\nScript finished sucessfully${ColorOff}"
exit 0
