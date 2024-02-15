#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 0.1.0

#Imports
import argparse
import os
import subprocess
import sys

#Variables=
SHOWCOMMANDS= """multicommand.py command -f FILE [-s SEPARATOR]
    
Available Commands
    1. openssl
    2. testssl
    """

#Definitions
def showCommands():
    print("""MultiCommand. Execute several commands to multiple assets at once.
    Usage: multicommand.py command -f FILE [-s SEPARATOR]
    
    \tAvailable Commands
    1. openssl
    2. testssl
    """)
    sys.exit(0)

def openssl(ip, port):
    command="openssl s_client -showcerts -connect {ip}:{port} </dev/null | openssl_{ip}_{port}".format(ip=ip, port=port)
    print(command)
    subprocess.Popen(command, shell=False, check=True)
    return

def testssl(ip, port):
    command="testssl --color 2 -oA testssl_{ip}_{port} https://{ip}:{port}".format(ip=ip, port=port)
    subprocess.Popen(command, shell=False, check=True)
    return

#Argparse
parser = argparse.ArgumentParser(prog="multiCommand" ,description="Execute specific checks to multiple assets at once.", usage=SHOWCOMMANDS)
parser.add_argument("command", help="Command to execute.", nargs=1)
parser.add_argument("-f", "--file", dest="file", help="File containing the hosts and the ports where the command must be execute.", nargs=1, required=True)
parser.add_argument("-s", "--sep", dest="sep", help="Custom separator for the host-port file.", nargs=1, required=False, default=" ")
args = parser.parse_args()

#Main
if __name__ == '__main__':
    if not os.path.isfile(args.file[0]):
        print("File {file} not found".format(file=args.file[0]))
        sys.exit(0)
    else:
        with open(args.file[0],"r",encoding='utf-8') as file:
            for line in file:
                print(line)
                ip, port = line.rstrip("\r\n").split(args.sep[0])
                print(ip, port, sep=" -----> ")
                funct = globals()[args.command[0]]
                funct(ip, port)