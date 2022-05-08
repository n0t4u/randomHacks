#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 1.0.3

#Notes
#Add columns order option
#Add remove unkown services
#Add support for several IPs in the same file


#imports
import argparse
from termcolor import colored
import os
import re
import subprocess
import sys


#Variables
data=[]

#Functions
def getIP(f):
	with open(f,"r",encoding="iso-8859-1") as file:
		for line in file:
			#print(line)
			if re.search(r'Host:[ ]*[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}',line):
				ip = re.search(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}',line)[0]
				#print(ip)
				return ip

def parseData(file,ip):
	command= "cat %s | grep -o -P '[\d]+\/open\/[\S]+\/\/([\S]+[\/]+)?([\S ]+[\/]+)?' | sed 's/[\/]\{1,\}/\t/g' | sed 's/\t, /\\n/g'" %file
	proc= subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
	parsedData= proc.stdout.read().decode("UTF-8")
	#print(parsedData)
	for line in parsedData.rstrip("\n").split("\n"):
		l = line.split("\t")
		print(l)
		try:
			portData={
				"ip":ip,
				"port":l[0],
				"state":l[1],
				"protocol":l[2],
				"service":l[3],
				"version":l[4]
			}
		except Exception as e:
			portData={
				"ip":ip,
				"port":l[0],
				"state":l[1],
				"protocol":l[2],
				"service":l[3],
				"version":"-"
			}
		else:
			data.append(portData)



def generateOutput(ip):
	if args.order:
		order= args.order[0].split(",")
	else:
		order= [ip,port,protocol,status,service,version]
	print(order)
	if args.print:
		print("print")
		for port in data:
			try:
				print(port[order[0]],port[order[1]],port[order[2]],port[order[3]],port[order[4]],port[order[5]], sep="\t")
				#print(port[order[0]],port[order[1]],port[order[2]],port[order[3]],port[order[4]],port[order[5]], sep=",")
			except KeyError as e:
				print(colored("[Error] Unknown key %s.","red") %e, "Allowed values separated by comma: ip, port, protocol, state, service, version ")
				sys.exit(0)
		#for line in parsedData.rstrip("\n").split("\n"):
		#	print(ip,line,sep="\t")
	else:
		outputFilename="nmap_parsed_open_ports_%s.txt" %ip
		with open(outputFilename,"w",encoding="UTF-8") as outputFile:
			for line in parsedData.rstrip("\n").split("\n"):
				#print(ip,line)
				dataline= "%s\t%s\n" %(ip,line)
				outputFile.write(dataline) 
		outputFile.close()
	return


#Argparse
parser= argparse.ArgumentParser()
parser.add_argument("file",help="nmap sV .gnmap file to parse",nargs=1)
parser.add_argument("-p","--print",dest="print", help="Print results instead of saving them into a file", action="store_true")
parser.add_argument("-o","--order",dest="order", help="Output specific order separated by commas. Example: ip,port,protocol,state,service,version", nargs=1)
args = parser.parse_args()

#Main
if __name__ == '__main__':
	if os.path.splitext(args.file[0])[1] != ".gnmap":
		print(colored("[ERROR]","red")," .gnmap file required")
	else:
		#print(args.file[0])
		ip =getIP(args.file[0])
		parseData(args.file[0],ip)
		#print(data)
		generateOutput(ip)