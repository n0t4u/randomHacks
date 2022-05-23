#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 1.1.1

#Notes
#Add remove unkown services

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
def parseData(file):
	try:
		file = open(file,"r", encoding="UTF-8")
		scan = file.read()
		file.close()
	except Exception as e:
		raise e
	else:
		for ipScan in re.findall(r'Host: [\d\.]+[ \(\)]+\tPorts:[\S ]+',scan,re.I):
			#print(ipScan)
			host, ports = ipScan.split("\t")
			ip =re.search(r'[\d\.]+',host)[0]
			ports = ports.split(":")[1]
			for port in re.sub(r'[\/]{1,}','/',ports).split('/,'):
				p = port.split("/")
				try:
					portData={
						"ip":ip,
						"port":p[0].lstrip(" "),
						"state":p[1],
						"protocol":p[2],
						"service":p[3],
						"version":p[4]
					}
				except Exception as e:
					portData={
						"ip":ip,
						"port":p[0].lstrip(" "),
						"state":p[1],
						"protocol":p[2],
						"service":p[3],
						"version":"-"
					}
				finally:
					data.append(portData)
			generateOutput(ip)
			data.clear()
		#print(data)
	return

def generateOutput(ip):
	if args.order:
		order= args.order[0].split(",")
	else:
		order= ["ip","port","protocol","state","service","version"]
	if args.print:
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
			for port in data:
				try:
					output= ";".join([port[order[0]],port[order[1]],port[order[2]],port[order[3]],port[order[4]],port[order[5]]])
					output = output+"\n"
					outputFile.write(output)
					#print(port[order[0]],port[order[1]],port[order[2]],port[order[3]],port[order[4]],port[order[5]], sep=";")
				except KeyError as e:
					print(colored("[Error] Unknown key %s.","red") %e, "Allowed values separated by comma: ip, port, protocol, state, service, version ")
					sys.exit(0)
		outputFile.close()
		print("Results successfully saved in %s" %outputFilename)
	return


#Argparse
parser= argparse.ArgumentParser()
parser.add_argument("file",help="nmap sV .gnmap file to parse",nargs=1)
parser.add_argument("-p","--print",dest="print", help="Print results instead of saving them into a file", action="store_true")
parser.add_argument("-o","--order",dest="order", help="Output specific order separated by commas. Example: ip,port,protocol,state,service,version", nargs=1)
#parser.add_argument("-u","--unknown",dest="unknown", help="Remove unknown services", action="store_true")
args = parser.parse_args()

#Main
if __name__ == '__main__':
	if os.path.splitext(args.file[0])[1] != ".gnmap":
		print(colored("[ERROR]","red")," .gnmap file required")
	else:
		parseData(args.file[0])
