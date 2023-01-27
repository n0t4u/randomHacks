#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 0.1.0

#imports
import argparse
import random
import string

#Argparse
parser= argparse.ArgumentParser(description="Custom dict generator to avoid bruteforce lock.")
parser.add_argument("-u", "--username", dest="username", help="Username to perform brute force",nargs=1, required="true")
parser.add_argument("-r", "--repetitions", dest="repetitions", help="Number of repetitions between random usernames",type=int, nargs=1, required="true")
parser.add_argument("-t", "--total", dest="total", help="Total length of the dictionary", type=int, nargs=1, required="true")
parser.add_argument("-o", "--output", dest="output", help="Output file", nargs=1)
args = parser.parse_args()

#Main
if __name__ == '__main__':
    dict = []
    uLen = len(args.username[0])
    for n in range(1,args.total[0]+1):
        if n % args.repetitions[0] == 0:
            randomUser = ''.join(random.choice(string.ascii_letters) for x in range(uLen))
            dict.append(randomUser)
        else:
            dict.append(args.username[0])
    if args.output:
        with open(args.output[0],"w",encoding="utf-8") as file:
            for line in dict:
                file.write(line+"\n")
    else:
        for line in dict:
            print(line)