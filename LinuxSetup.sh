#!/bin/bash

#Author: n0t4u
#Version: 0.1.3
#Description: Automatic installation of hacking tools on Kali

#Source: https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Reset
ColorOff='\033[0m'       # Text Reset

#Setup
sudo apt update
sudo apt upgrade -y

#Python3 and PIP3
echo -e "${Blue}[*] Installing python3 and pip3${ColorOff}"
sudo apt install python3.10 -y
sudo apt install python3-pip -y

#git
echo -e "${Blue}[*] Installing git${ColorOff}"
sudo apt install git -y

#Go
echo -e "${Blue}[*] Installing go and dependecies (BETA)${ColorOff}"
sudo apt-get install curl golang-go git mercurial make binutils bison gcc build-essential -y
go version

#ZSH
#apt install zsh zsh-syntax-highlighting thefuck fonts-powerline zsh-autosuggestions
#sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

#SublimeText 3
echo -e "${Blue}[*] Installing Sublime Text${ColorOff}"
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text -y

#SecLists
echo -e "${Blue}[*] Downloading dictionaries from SecLists${ColorOff}"
git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists

#Dig and Nslookup
echo -e "${Blue}[*] Installing dnsutils (dig, nslookup)${ColorOff}"
sudo apt install dnsutils -y

#CherryTree
echo -e "${Blue}[*] Installing CherryTree${ColorOff}"
sudo apt install cherrytree -y

#Terminator
echo -e "${Blue}[*] Installing Terminator${ColorOff}"
sudo apt install terminator -y

#Nuclei
echo -e "${Blue}[*] Installing nuclei${ColorOff}"
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
sudo ln -s $HOME/go/bin/nuclei /usr/bin/nuclei

#Interactsh
echo -e "${Blue}[*] Installing interactsh${ColorOff}"
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
sudo ln -s $HOME/go/bin/interactsh-client /usr/bin/interactsh

#Testssl.sh
echo -e "${Blue}[*] Installing testssl${ColorOff}"
git clone https://github.com/drwetter/testssl.sh.git /opt/testssl.sh
sudo ln -s /opt/testssl.sh/testssl.sh /usr/bin/testssl

#SSLScan
echo -e "${Blue}[*] Installing SSLScan${ColorOff}"
sudo apt install sslscan

#Onesixtyone (SNMP)
echo -e "${Blue}[*] Installing onesixtyone${ColorOff}"
git clone https://github.com/trailofbits/onesixtyone.git /opt/onesixtyone
gcc -o onesixtyone /opt/onesixtyone/onesixtyone.c

#DRAMFe
echo -e "${Blue}[*] Installing DRAFMe${ColorOff}"
git clone https://github.com/n0t4u/DRAFMe.git /opt/DRAFMe
sudo ln -s /opt/DRAFMe.py /usr/bin/DRAFMe

#EasyAndroidStaticAnalysis
echo -e "${Blue}[*] Installing EasyAndroidStaticAnalysis${ColorOff}"
git clone https://github.com/n0t4u/easyAndroidStaticAnalysis /opt/easyAndroidStaticAnalysis
sudo ln -s /opt/easyAndroidStaticAnalysis.sh /usr/bin/easa

#wafw00f
echo -e "${Blue}[*] Installing wafw00f${ColorOff}"
python3 -m pip install wafw00f
#sudo git clone https://github.com/EnableSecurity/wafw00f.git /opt/wafw00f
#python /opt/wafw00f/setup.py install

#httpx
echo -e "${Blue}[*] Installing httpx${ColorOff}"
git clone https://github.com/projectdiscovery/httpx /opt/httpx
sudo ln -s $/opt/httpx /usr/bin/httpx

#Dirb
echo -e "${Blue}[*] Installing dirb${ColorOff}"
sudo apt install dirb -y

#Gobuster
echo -e "${Blue}[*] Installing gobuster${ColorOff}"
sudo apt install gobuster -y

#Sublist3r
echo -e "${Blue}[*] Installing sublist3r${ColorOff}"
sudo git clone https://github.com/aboul3la/Sublist3r.git /opt/Sublist3r
sudo ln -s $/opt/Sublist3r /usr/bin/Sublist3r

#Subfinder
echo -e "${Blue}[*] Installing subfinder${ColorOff}"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

#Arjun
echo -e "${Blue}[*] Installing arjun${ColorOff}"
sudo python3 -m pip install arjun

#ikeforce
#echo -e "${Blue}[*] Installing ikeforce${ColorOff}"
sudo python3 -m pip install pyip pycrypto pyopenssl
sudo git clone https://github.com/SpiderLabs/ikeforce.git /opt/ikeforce
sudo ln -s /opt/ikeforce/ikeforce.py /usr/bin/ikeforce

#ike-trans
echo -e "${Blue}[*] Installing ike-trans${ColorOff}"
sudo git clone https://github.com/actuated/ike-trans /opt/ike-trans
sudo ln -s /opt/ike-trans.sh /usr/bin/ike-trans

#dnsrecon
echo -e "${Blue}[*] Installing dnsrecon${ColorOff}"
sudo git clone https://github.com/darkoperator/dnsrecon.git /opt/dnsrecon
sudo python3 -m pip install -r /opt/dnsrecon/requirements.txt
sudo ln -s /opt/dnsrecon/dnsrecon.py /usr/bin/dnsrecon

#domain_analyzer
echo -e "${Blue}[*] Installing domain_analyzer${ColorOff}"
sudo git clone https://github.com/eldraco/domain_analyzer.git /opt/domain_analyzer
sudo ln -s /opt/domain_analyzer /usr/bin/domain_analyzer

#ffuf
echo -e "${Blue}[*] Installing ffuf${ColorOff}"
git clone https://github.com/ffuf/ffuf.git /opt/ffuf
go get /opt/ffuf/
go build /opt/ffuf/

#dnsmasq
echo -e "${Blue}[*] Installing dnsmasq${ColorOff}"
sudo apt install dnsmasq -y

#Mobile Tools
#MobSF
echo -e "${Blue}[*] Installing MobSF${ColorOff}"
sudo apt install python3-dev python3-venv python3-pip build-essential libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev wkhtmltopdf -y
sudo git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF.git /opt/MobSF
sudo /opt/MobSF/setup.sh
echo "Execute ./run.sh 127.0.0.1:8000"

#Frida tools
echo -e "${Blue}[*] Installing Frida Tools${ColorOff}"
sudo python3 -m pip install frida-tools

