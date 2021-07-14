#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 1.0

#imports
import argparse
import re
import subprocess

#Lists
openports=[]

#Functions
def parseData(f):
	with open(f,"r",encoding="iso-8859-1") as file:
		ip=""
		ports=""
		for line in file:
			if re.search(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}',line):
				if ip and ports:
					openports.append([ip,ports.rstrip(",")])
				ports=""
				ip = re.search(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}',line)[0]
				print(ip)
			elif re.search(r'[\d]{1,5}\/tcp',line):
				port = re.search(r'[\d]{1,5}',line)[0]
				print (port)
				ports=ports+ port+","

	print(openports)

def executeNmap():
	for d in openports:
		command="sudo nmap -sV -p %s -oA nmap_%s %s" %(d[1],d[0],d[0])
		print(command)
		subprocess.call(command, shell=True)

#Argparse
parser= argparse.ArgumentParser()
parser.add_argument("file",help="Furious output file to parse",nargs=1)
args = parser.parse_args()

#Main
if __name__ == '__main__':
	parseData(args.file[0])
	executeNmap()