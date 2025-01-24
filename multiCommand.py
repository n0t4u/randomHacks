#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 0.2.1

#Imports
import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event

#Variables

STOP= Event()
SHOWCOMMANDS= """multicommand.py command -f FILE [-s SEPARATOR]

Available Commands
	1. openssl
	2. ssh_audit
	3. sslscan
	4. terrapin
	5. testssl
	"""

#Definitions
def showCommands():
	print("""MultiCommand. Execute several commands to multiple assets at once.
	Usage: {command}
	""").format(command=SHOWCOMMANDS)
	sys.exit(0)

def openssl(ip, port):
	#command="openssl s_client -showcerts -connect {ip}:{port} </dev/null &> openssl_{ip}_{port}".format(ip=ip, port=port)
	command="openssl s_client -showcerts -connect {ip}:{port} </dev/null".format(ip=ip, port=port)
	outputFilename= "openssl_{ip}_{port}".format(ip=ip, port=port)
	output= subprocess.run(command, shell=True,capture_output=True,text=True)
	with open(outputFilename,"w") as file:
		file.write(output.stdout)
	return

#Not tested yet
def ssh_audit(ip,port):
	command="ssh-audit --port={port} {ip}".format(ip=ip, port=port)
	outputFilename= "ssh-audit_{ip}_{port}".format(ip=ip,port=port)
	output= subprocess.run(command,shell=True, capture_output=True,text=True)
	with open(outputFilename,"w") as file:
		file.write(output.stdout)
	return

def sslscan(ip,port):
	command="sslscan --show-ciphers {ip}:{port}".format(ip=ip, port=port)
	outputFilename= "sslscan_{ip}_{port}".format(ip=ip,port=port)
	output= subprocess.run(command,shell=True, capture_output=True,text=True)
	with open(outputFilename,"w") as file:
		file.write(output.stdout)
	return

def terrapin(ip,port):
	command="Terrapin-Scanner --connect {ip}:{port} | tee terrapin_{ip}_{port}".format(ip=ip, port=port)
	subprocess.run(command,shell=True)
	return

def testssl(ip, port):
	command="testssl --color 2 --warnings off --quiet -s -p -U -P -oA testssl_{ip}_{port} https://{ip}:{port} ".format(ip=ip, port=port)
	res = subprocess.run(command, shell=True,capture_output=True)
	return res

def executeCommand(line):
	if STOP.is_set():
		return
	else:
		funct = globals()[args.command[0]]
		ip, port = line.rstrip("\r\n").split(args.sep[0])
		print("[»] {command} -----> {ip}:{port}".format(command=args.command[0],ip=ip,port=port))
		funct(ip,port)
	return

def processFile(file,maxThreads):
	try:
		tasks = []
		
		with open(file,"r",encoding='utf-8') as file:
			lines = [line.strip() for line in file if line.strip()]

			with ThreadPoolExecutor(maxThreads) as executor:
				for line in lines:
					
					futures = {executor.submit(executeCommand,line)}
				for future in as_completed(futures):
					print("[*]Completed!")
	except KeyboardInterrupt:
		STOP.set()
		print("\nCTRL+C detected!")
		stopExecution = "[*] %s execution finished at %s." % (args.command[0].capitalize(), time.strftime("%a, %d %b %Y %H:%M:%S"))
		print(stopExecution)
		sys.exit(0)
	

#Argparse
parser = argparse.ArgumentParser(prog="multiCommand" ,description="Execute specific checks to multiple assets at once.", usage=SHOWCOMMANDS)
parser.add_argument("command", help="Command to execute.", nargs=1)
parser.add_argument("-f", "--file", dest="file", help="File containing the hosts and the ports where the command must be execute.", nargs=1, required=True)
parser.add_argument("-s", "--sep", dest="sep", help="Custom separator for the host-port file.", nargs=1, required=False, default=" ")
parser.add_argument("-t", "--threads", dest="threads", help="Number of concurrent threads", type=int, required=False, default=4)
args = parser.parse_args()

#Main
if __name__ == '__main__':
	if not os.path.isfile(args.file[0]):
		print("File {file} not found".format(file=args.file[0]))
		sys.exit(0)
	else:
		startExecution = "[*] %s execution started at %s." % (args.command[0].capitalize(), time.strftime("%a, %d %b %Y %H:%M:%S"))
		print(startExecution)
		processFile(args.file[0],args.threads)
		stopExecution = "[*] %s execution finished at %s." % (args.command[0].capitalize(), time.strftime("%a, %d %b %Y %H:%M:%S"))
		print(stopExecution)