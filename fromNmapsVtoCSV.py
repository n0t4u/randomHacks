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
	except IOError:
		print(colored("[Error] File %s doesn't exist." %file,"red"))
	except Exception as e:
		raise e
	else:
		for ipScan in re.findall(r'Host: [\d\.]+ ?\(?[\S]*\)?\tPorts:[\S ]+',scan,re.I):
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
					try:
						portData={
							"ip":ip,
							"port":p[0].lstrip(" "),
							"state":p[1],
							"protocol":p[2],
							"service":p[3],
							"version":"-"
						}
					except Exception as e2:
						portData={
							"ip":ip,
							"port":p[0].lstrip(" "),
							"state":p[1],
							"protocol":p[2],
							"service":"unknown",
							"version":"-"
						}
				finally:
					data.append(portData)
			generateOutput(ip)
			data.clear()
	return

def generateOutput(ip):
	if args.order:
		order= args.order[0].split(",")
	else:
		order= ["ip","port","protocol","state","service","version"]
	if args.print:
		#print(*order, sep="\t")
		for port in data:
			try:
				#print(port[order[0]],port[order[1]],port[order[2]],port[order[3]],port[order[4]],port[order[5]], sep="\t")
				for o in order:
					print(port[o], end="\t")
				print()
			except KeyError as e:
				print(colored("[Error] Unknown key %s.","red") %e, "Allowed values separated by comma: ip, port, protocol, state, service, version ")
				sys.exit(0)
	else:
		outputFilename="nmap_parsed_open_ports_%s.txt" %ip
		with open(outputFilename,"w",encoding="UTF-8") as outputFile:
			header = ";".join(order) + "\n"
			outputFile.write(header)
			for port in data:
				try:
					outputOrdered = []
					for o in order:
						outputOrdered.append(port[o])
					output = ";".join(outputOrdered) + "\n"
					#output= ";".join([port[order[0]],port[order[1]],port[order[2]],port[order[3]],port[order[4]],port[order[5]]])
					#output = output+"\n"
					outputFile.write(output)
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
