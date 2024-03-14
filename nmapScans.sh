#!/usr/bin/env bash

#nmapScans
#Author: n0t4u
#Description: Bash script that executes a custom port scan, parse the results and performs a second versions scan only to the open ports.

#Colors
Green='\033[0;32m'	# Green
Red='\033[0;31m'	# Red
Blue='\033[0;34m'	# Blue
Cyan='\033[36m'		# Cyan
Bold='\033[1m'		# Bold
ColorOff='\033[0m'	# Text Reset

#Default options
options="-p- -sT -T3 -Pn -n -v --open --reason"
versionAux="-sV -sC"
versionOptions="" #Do not complete
subName=""
scanned=()
resume=false
user=$(logname)

help_banner() {
	echo -e """
${Blue}${Bold}============================================

		nmapScans.sh

===========================(This is n0t4u)==${ColorOff}

${Bold}Usage:${ColorOff} ./nmapScans.sh <FILE/IP> [scan_options] [--resume]
${Bold}Example:${ColorOff} ./nmapScans.sh 192.168.1.200 '-sS -T2 -Pn --reason'

${Bold}Current default scan options:${ColorOff} ${options}
${Bold}Current version scan options:${ColorOff} $(echo "${options}" | sed "s/-p\(-\| \?[0-9,\-]\+\)/${versionAux}/g")
"""
}

setup () {
	if [[ "${options}" =~ -oA ]]; then
		options=$(echo "${options}" | sed "s/ -oA [^[:space:]]\+//g")
	fi
		if [[ "${options}" =~ -sV ]]; then
		options=$(echo "${options}" | sed "s/ -sV//g")
	fi
	case " ${options}" in #Added a space to achieve regex
		[[:graph:][:space:]]*-sT[[:graph:][:space:]]*) subName="sT";;
		[[:graph:][:space:]]*-sS[[:graph:][:space:]]*) subName="sS";;
		[[:graph:][:space:]]*-sU[[:graph:][:space:]]*) subName="sU";;
		[[:graph:][:space:]]*-sP[[:graph:][:space:]]*) subName="sP";;
		[[:graph:][:space:]]*-sX[[:graph:][:space:]]*) subName="sX";;
		[[:graph:][:space:]]*-sY[[:graph:][:space:]]*) subName="sY";;
		[[:graph:][:space:]]*-sA[[:graph:][:space:]]*) subName="sA";;
		[[:graph:][:space:]]*-sN[[:graph:][:space:]]*) subName="sN";;
		[[:graph:][:space:]]*-sM[[:graph:][:space:]]*) subName="sM";;
	esac

	if [[ "${options}" =~ -p- ]]; then
		subName+="_p"
	elif [[ "${options}" =~ -p[[:space:]]?([[:digit:]]+-[[:digit:]]+) ]]; then
		#echo "MATCH: ${BASH_REMATCH[1]}"
		subName+="_${BASH_REMATCH[1]}"
	elif [[ "${options}" =~ -p[[:space:]]?([[:digit:],-]+) ]]; then
		#echo "MATCH: ${BASH_REMATCH[1]}"
		subName+="_range"
	else
		echo -e "${Red}[ERROR]${ColorOff} Condition not matched"
	fi

	touch ./.nmapScans.log
	echo "${options}" >> ./.nmapScans.log
	sudo chown "${user}":"${user}" ./.nmapScans.log
}

nmap() {
	echo -e "${Blue}[$(date '+%Y-%m-%d %H:%M:%S')] Nmap basic scan to ${1} with options ${2}${ColorOff}"
	sudo sh -c "nmap ${2} -oA nmap_${subName}_${1} ${1}"
	echo -e "${Blue}[$(date '+%Y-%m-%d %H:%M:%S')] Nmap basic scan saved to nmap_${subName}_${1}${ColorOff}"
	if [ $? -eq 130 ]; then
		trap_ctrlc
	else
		sudo chown "${user}":"${user}" nmap_"${subName}"_"${1}".*
	fi
}

getOpenPorts() {
	ports=$(grep -P -o "[\d]+\/open\/[\S]+\/\/([\S]+[\/]{3,})?" nmap_"${subName}"_"${1}".gnmap | cut -d "/" -f 1 | sed ':a;N;$!ba;s/\n/,/g')
	echo "${ports}"
}

nmapsV() {
	echo -e "${Blue}[$(date '+%Y-%m-%d %H:%M:%S')] Nmap version scan to ${1} and ports ${2} with options ${3}${ColorOff}"
	sudo sh -c "nmap ${3} -p ${2} -oA nmap_sV_${subName}_${1} ${1} " # --allports --version-all
	echo -e "${Blue}[$(date '+%Y-%m-%d %H:%M:%S')] Nmap version scan saved to nmap_sV_${subName}_${1}${ColorOff}"
	if [ $? -eq 130 ]; then
		trap_ctrlc
	else
		scanned+=("${1}")
		sudo chown "${user}":"${user}" "nmap_sV_${subName}_${1}".*
	fi
}

writeLog(){
	for asset in "${scanned[@]}"; do
		echo "${asset}" >> ./.nmapScans.log
	done
}

trap_ctrlc() {
	echo -e "${Red}[X] CTRL+C signal detected. Aborting port scanning...${ColorOff}"
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
elif [ "$#" -eq 2 ]; then
	if [ "$2" = "--resume" ]; then
		if [ -f ./.nmapScans.log ]; then
			resume=true
		fi
	else
		options=$2

	fi
fi
setup
versionOptions=$(echo "${options}" | sed "s/-p\(-\| \?[0-9,\-]\+\)/${versionAux}/g")
#versionOptions= echo "${options}//-p(-|[0-9,\-]+)/${versionAux}"
echo -e "${Blue}Basic scan options${ColorOff}\t${options}\n${Blue}Version scan options${ColorOff}\t${versionOptions}"

if [[ -f $1 ]]; then
	echo -e "${Blue}File${ColorOff}\t$1"
	while read -r ip; do
		if [ "${resume}" = true ] && [ $(grep -c "${ip}" ./.nmapScans.log) -ne 0 ];then
			echo -e "${Green}${ip} already scanned. Skipped.${ColorOff}"
			continue
		else
			echo -e "\n${Cyan}${ip}${ColorOff}"
			nmap "${ip}" "${options}"
			if [ $? -ne 130 ]; then
				openPorts=$(getOpenPorts "${ip}")
				if [[ -z "${openPorts}" ]]; then
					echo -e "${Green}${ip} has no open ports.${ColorOff}"
					scanned+=("${ip}")
				else
					echo "${ip} ${openPorts} ${versionOptions}"
					nmapsV "${ip}" "${openPorts}" "${versionOptions}"
				fi
			fi
		fi
	done < "$1"
else
	if [ "${1}" = "--help" ] || [ "${1}" = "-h" ]; then
		help_banner
	else
		echo -e "\n${Cyan}${1}${ColorOff}"
		nmap "${1}" "${options}"
		openPorts=$(getOpenPorts "$1")
		if [[ -z "${openPorts}" ]]; then
			echo -e "${Green}${1} has no open ports.${ColorOff}"
			scanned+=("${1}")
		else
			nmapsV "${1}" "${openPorts}" "${versionOptions}"
		fi
	fi
fi
writeLog
echo -e "${Green}\nScript finished sucessfully${ColorOff}"
exit 0
