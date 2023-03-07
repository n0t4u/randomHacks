#!/usr/bin/env python3

# DNSResolver
# Author: n0t4u
# Description:  Automatic DNS resolution tool for several domains.

#Imports
import argparse
import subprocess
import re

#Functions
def checkIP(domain):
    try:
        command = "dig +short @8.8.8.8 %s" % domain
        c = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        ip = c.communicate()[0]
        ip = ip.decode('utf-8').strip("\n")
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)
        if args.ip and ip:
            [print(ip_aux) for ip_aux in ip]
        else:
            dirs = " ".join(ip)
            print(domain, dirs)
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        raise e

#Argparse
parser = argparse.ArgumentParser(description="DNS Resolver.")
parser.add_argument("-f", "--file", dest="file", help="URL file.", nargs=1, required=True)
parser.add_argument("--ip", dest="ip", help="Show IP only. ", action="store_true")
args = parser.parse_args()

#Main
if __name__ == "__main__":
    if args.file:
        with open(args.file[0], "r", encoding="utf-8") as f:
            try:
                for line in f:
                    url = re.sub(r'https?:\/\/', '', line)
                    url = url.rstrip("\n")
                    checkIP(url)
            except Exception as e:
                raise e
