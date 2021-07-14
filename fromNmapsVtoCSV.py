#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 1.0

#imports
import argparse
import os
import re
import subprocess

#Data
outputFilename="nmap_parsed_open_ports.txt"

#Functions
def getIP(f):
	with open(f,"r",encoding="iso-8859-1") as file:
		for line in file:
			#print(line)
			if re.search(r'Host:[ ]*[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}',line):
				ip = re.search(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}',line)[0]
				print(ip)
				return ip

def parseData(file,ip):
	command= "cat %s | grep -o -P '[\d]+\/open\/[\S]+\/\/([\S]+[\/]+)?([\S ]+[\/]+)?' | sed 's/[\/]\{1,\}/ /g' | sed 's/ , /\\n/g'" %file
	proc= subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
	parsedData= proc.stdout.read().decode("UTF-8")
	#print(parsedData)
	with open(outputFilename,"a+",encoding="UTF-8") as outputFile:
		for line in parsedData.rstrip("\n").split("\n"):
			#print(ip,line)
			dataline= "%s %s\n" %(ip,line)
			outputFile.write(dataline) 
	outputFile.close()


#Argparse
parser= argparse.ArgumentParser()
parser.add_argument("file",help="nmap sV .gnmap file to parse",nargs=1)
args = parser.parse_args()

#Main
if __name__ == '__main__':
	if os.path.splitext(args.file[0])[1] != ".gnmap":
		print("[ERROR] gnmap file required")
	else:
		print(args.file[0])
		ip =getIP(args.file[0])
		parseData(args.file[0],ip)
