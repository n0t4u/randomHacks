#!/bin/bash

#Author: n0t4u
#Description: Easy testssl parser for several IPs

#TODO. Clean path

#Colors
Green='\033[0;32m'	# Green
Red='\033[0;31m'	# Red
Blue='\033[1;34m'	# Bold blue
Bold='\033[1;39m'	# Bold white
ColorOff='\033[0m'	# Text Reset

declare -a protocols=('SSLv2' 'SSLv3' 'TLS 1 ' 'TLS 1.1' 'TLS 1.2' 'TLS 1.3')
declare -a ciphers=('LOW: 64 Bit + DES, RC[2,4], MD5' 'Triple DES Ciphers / IDEA' 'Obsoleted CBC ciphers' 'Strong encryption (AEAD ciphers) with no FS' 'Strong encryption (AEAD ciphers) with no FS')
declare FS='TLS 1.2 sig_algs offered'
declare -a vulns=('ROBOT' 'Secure Renegotiation' 'Secure Client_Initiated Renegotiation' 'CRIME' 'BREACH' 'POODLE' 'TLS_FALLBACK_SCSV' 'SWEET32' 'FREAK' 'DROWN' 'LOGJAM' 'BEAST' 'LUCKY13' 'Winshock' 'RC4')

echo -e "${Green}TESTSSL parser.\nUsage ./testsslExtractor.sh [--filter FILTER] [PATH]${ColorOff}\n"
if [ "$#" -lt 1 ]; then
	route="."
else
	if { [[ "${1}" = "-f" ]] || [[ "${1}" = "--filter" ]]; } && [[ -n "${2}" ]]; then
		if [[ -n "${3}" ]]; then
			route="${3}"
		else
			route="."
		fi
		for file in $(ls "${route}"/testssl_*.log); do
			domain=$(echo -e "${file}" | rev | cut -d '/' -f1 |rev|  sed 's/\(testssl_\|\.log\)//g';)
			ips=$(cat "${file}" | grep -P '(?<=\-\-\>\> )[\d\.]{7,15}(?=:[\d]{1,5} [\S]* \<\<\-\-)' -o | uniq | sed ':a;N;$!ba;s/\n/, /g')
			echo -e "${ColorOff}${Bold}${domain}${ColorOff}\t (${ips})"
			grep -P "${2}" "${file}"
		done
		exit
	else
		route="${1}"
	fi
fi
if command -v testssl; then
	for prot in "${protocols[@]}"; do
		echo -e "\n${Blue}${prot}${ColorOff}"
		for file in $(ls "${route}"/testssl_*.log); do
			domain=$(echo -e "${file}" | rev | cut -d '/' -f1 |rev|  sed 's/\(testssl_\|\.log\)//g';)
			ips=$(cat "${file}" | grep -P '(?<=\-\-\>\> )[\d\.]{7,15}(?=:[\d]{1,5} [\S]* \<\<\-\-)' -o | uniq | sed ':a;N;$!ba;s/\n/, /g')
			echo -e "${ColorOff}${Bold}${domain}${ColorOff}\t (${ips})"
			grep "Testing protocols" -A 10 "${file}" | grep -i -P "${prot}"
		done
	done
	for cipher in "${ciphers[@]}"; do
		echo -e "\n${Blue}${cipher}${ColorOff}"
		for file in $(ls "${route}"/testssl_*.log); do
			domain=$(echo -e "${file}" | rev | cut -d '/' -f1 |rev|  sed 's/\(testssl_\|\.log\)//g';)
			ips=$(cat "${file}" | grep -P '(?<=\-\-\>\> )[\d\.]{7,15}(?=:[\d]{1,5} [\S]* \<\<\-\-)' -o | uniq | sed ':a;N;$!ba;s/\n/, /g')
			echo -e "${ColorOff}${Bold}${domain}${ColorOff}\t (${ips})"
			grep "Testing cipher categories" -A 10 "${file}" | grep -P "${cipher}"
		done
	done
	echo -e "\n${Blue}Forward Secrecy"
	for file in $(ls "${route}"/testssl_*.log); do
		domain=$(echo -e "${file}" | rev | cut -d '/' -f1 |rev|  sed 's/\(testssl_\|\.log\)//g';)
		ips=$(cat "${file}" | grep -P '(?<=\-\-\>\> )[\d\.]{7,15}(?=:[\d]{1,5} [\S]* \<\<\-\-)' -o | uniq | sed ':a;N;$!ba;s/\n/, /g')
		echo -e "${ColorOff}${Bold}${domain}${ColorOff}\t (${ips})"
		grep "${FS}" "${file}"
	done
	for vuln in "${vulns[@]}"; do
		echo -e "\n${Blue}${vuln}${ColorOff}"
		for file in $(ls "${route}"/testssl_*.log); do
			domain=$(echo -e "${file}" | rev | cut -d '/' -f1 |rev|  sed 's/\(testssl_\|\.log\)//g';)
			ips=$(cat "${file}" | grep -P '(?<=\-\-\>\> )[\d\.]{7,15}(?=:[\d]{1,5} [\S]* \<\<\-\-)' -o | uniq | sed ':a;N;$!ba;s/\n/, /g')
			echo -e "${ColorOff}${Bold}${domain}${ColorOff}\t (${ips})" 
			if [ "${vuln}" == "RC4" ]; then
				grep -v Grade "${file}" | grep -P "${vuln}" | grep "CVE-2013-2566";
			else
				grep -v Grade "${file}" | grep -P "${vuln}";
			fi
		done
	done
fi
