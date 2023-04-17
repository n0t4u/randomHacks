#!/usr/bin/env bash

#Author: n0t4u
#Description: Bash script to automatically perform banner grabbing and highlight which assets and ports responds to any command injected. It does not perform any further checks, they must be done manually later.

#Colors
Green='\033[0;32m'	# Green
Red='\033[0;31m'	# Red
Blue='\033[1;34m'	# Bold blue
Bold='\033[1;39m'	# Bold white
ColorOff='\033[0m'	# Text Reset

declare -a commands=("helo" "hello" "help" "info" "?" "GET" "POST" "HEAD" "login" "user" "id")
timeout=1
newline=false #Just for beauty output
#IFS=' '
positives=()


helpBanner() {
	echo -e "bannergrabber.sh\nUsage:\t bannergrabber.sh <PORT_SCAN> [<TIMEOUT>]"
}

bannerGrabber() {
	for command in "${commands[@]}"; do
		#For UDP netcat, use -u option
		res=$(echo "${command}"| nc -w $timeout $1 2>&1)
		if [[ $res =~ "Connection refused" ]]; then
		#if $(echo "${res}" | grep -i -o -P "Connection refused"); then
			echo "${1} - Connection refused"
			break
		elif [[ -n $res ]];then
			if [ "${newline}" = true  ]; then
				echo -e "\n"
			fi
			echo -e "${Green}[»] ${ColorOff}${Blue}${1}${ColorOff} returned some content for ${Blue}${command}${ColorOff} command."
			positives+=("${1}")
			newline=false
			break
		else
			echo -ne "${Bold}.${ColorOff}"
			newline=true
		fi
	done
	return
}

results() {
	if [ "${newline}" = true  ]; then
		echo -e "\n"
	fi
	echo -e "${Green}[*] Open ports with response. Further manual testing is required for these ports.${ColorOff}"
	for port in "${positives[@]}"; do
		echo -e "${port}" # | tee -a bannerGrabber:out.txt
		echo "${port}" >> bannerGrabber_out.txt
	done
	echo -e "Results saved in bannerGrabber_out.txt"
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
fi
# shellcheck disable=SC2162
while read line; do
	bannerGrabber "${line}"
done < "${1}"
results
exit 0
