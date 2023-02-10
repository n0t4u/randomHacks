#!/usr/bin/env bash

#Author: n0t4u
#Description: Bash script to automatically perform banner grabbing and highlight which assets and ports responds to any command injected. It does not perform any further checks, they must be done manually later.

#Colors
Green='\033[0;32m'        # Green
Red='\033[0;31m'          # Red
Blue='\033[1;34m'         # Bold blue
ColorOff='\033[0m'       # Text Reset

declare -a commands=("helo" "hello" "help" "info" "?" "GET" "POST" "HEAD" "login" "user" "id")
timeout=1
#IFS=' '
positives=()


helpBanner() {
	echo -e "bannergrabber.sh\nUsage:\t bannergrabber.sh <PORT_SCAN> [<TIMEOUT>]"
}

bannerGrabber() {
	#read -a words <<< "$line"
	#echo "${words[0]} ${words[1]}"
	for command in "${commands[@]}"; do
		echo "${command}"
		res="$(echo "${command}" | nc -w $timeout $1 2>&1)"
		#read $res
		#if [[ $res == *"refused"* ]]; then
		if [[ $res =~ "Connection refused" ]]; then
		#if $(echo "${res}" | grep -i -o -P "Connection refused"); then
			echo "${1} - Connection refused"
			break
		elif [[ -n $res ]];then
			echo -e "${Green}[»] ${ColorOff}${Blue}${1}${ColorOff} returned some content for ${Blue}${command}${ColorOff} command. Further manual testing is required for this port."
			positives+=("${1}")
			break
		else
			echo "${res}"
		fi
	done
	return
}

results() {
	echo -e "[*] Open ports with response."
	for port in "${positives[@]}"; do
		echo -e "${port}" # | tee -a bannerGrabber:out.txt
		echo "${port}" >> bannerGrabber_out.txt
	done
}

trap_ctrlc() {
	echo -e "${Red}[X] CTRL+C signal detected. Ending banner grabbing...${ColorOff}"
	results
	exit 4
}

trap "trap_ctrlc" SIGINT #2
if [[ "$#" -lt 1 || "$#" -gt 3 ]]; then
	echo -e "${Red}[X] Unrecognized number of params.${ColorOff}"
	helpBanner
elif [[ "$#" -eq 2 ]]; then
	timeout=$2
else
	# shellcheck disable=SC2162
	while read line; do
		bannerGrabber "${line}"
	done < "${1}"

fi
exit 0
