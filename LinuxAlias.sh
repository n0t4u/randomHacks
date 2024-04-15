#!/usr/bin/env bash

# Alias and functions for Linux Shell

#Colors
Green='\033[0;32m'        # Green
Red='\033[0;31m'          # Red
Blue='\033[1;34m'         # Bold blue
ColorOff='\033[0m'       # Text Reset

declare -a alias=('cd..="cd .."'
'mobsf="/opt/MobSF/run.sh 127.0.0.1:8000"'
'nessus="sudo systemctl start nessusd.service"'
'nmapParser="python3 /opt/randomHacks/fromNmapsVtoCSV.py"'
'nmapScan="/opt/randomHacks/nmapScans.sh"'
'manageProject="python3 /opt/manageProject/project.py"'
'DNSResolver="python3 /opt/randomHacks/DNSResolver.py"'
)

declare -a functions=('back() {pathChange=""; for n in {1..$1}; do pathChange+="../" ;done; cd "${pathChange}";}'
'mkcd(){mkdir -p "${1}"; cd "${1}";}'
'secListsSearch() {for file in $(find /opt/SecLists -name "*${1}*" -type f); do wc -l $file; done;}')

shellFile=""

if [ "$SHELL" = "/usr/bin/zsh" ];then
	shellFile="${HOME}/.zshrc"
elif [ "$SHELL" = "/usr/bin/bash" ];then
	shellFile="${HOME}/.bashrc"
fi

echo -e "${Blue}[*] Including alias on ${shellFile}${ColorOff}"
echo '#Custom Aliases' #>> $HOME/.zshrc
IFS='='
for aka in "${alias[@]}";do
	read -a name <<< "$aka"
	if [[ -z $(grep -i -P "^alias ${name[0]}" ${shellFile}) ]]; then
		echo "alias ${aka}" >> ${shellFile}
		echo -e "${Green}[»]${ColorOff} ${name[0]} alias added"
	else
		echo -e "${Red}[x]${ColorOff} Alias ${name[0]} already in file. Skipping"
	fi
done
IFS='('
for f in "${functions[@]}"; do
	read -a name <<< "$f"
	if [[ -z $(grep -i -P "^${name[0]}" ${shellFile}) ]]; then
		echo "${f}" >> ${shellFile}
		echo -e "${Green}[»]${ColorOff} ${name[0]} function added"
	else
		echo -e "${Red}[x]${ColorOff} Function ${name[0]} already in file. Skipping"
	fi
done
