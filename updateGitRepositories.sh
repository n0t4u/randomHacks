#!/usr/bin/env bash

# Author: n0t4u
# Version: 1.0
# Description: Update your Git repositories to last version.

#Colors
Green='\033[0;32m'      # Green
Red='\033[0;31m'        # Red
Blue='\033[0;34m'       # Blue
Bold='\033[1m'          # Bold
ColorOff='\033[0m'      # Text Reset

check_privs(){
        if [[ whoami -ne "root" ]]; then
                echo -e "${Red}This script is supposed to be run with sudo privileges${ColorOff}"
                exit 0
        fi
}

update_repositories() {
        cd /opt/
        for folder in *; do
                if [[ -d "/opt/${folder}/.git" ]]; then
                        echo -e "${Green}[»] Updating ${folder} ${ColorOff}"
                        cd "/opt/${folder}/"; sudo git pull
                        if [ $? -eq 130 ]; then
                                trap_ctrlc
                        fi
                fi
        done
}

trap_ctrlc() {
        echo -e "${Red}[X] CTRL+C signal detected. Aborting updates...${ColorOff}"
        exit 1
}

# Main
trap trap_ctrlc SIGINT SIGTERM
check_privs
update_repositories
exit 0
