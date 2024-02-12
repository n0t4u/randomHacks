#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Author: n0t4u

# TODO
# TODO. Remove modes. If no -r is set then use mode 1.

# Imports
import argparse
import os.path
import requests
import re
import sys
from tabulate import tabulate
import time
import urllib3

urllib3.disable_warnings()

# Variables
headers = {}
token = ""
tableHeaders = ["#", "Token", "Status Code", "Length"]
results = []


def curlRequest(session, route, method, data):
    try:
        if method == "POST":
            # https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw
            request = requests.Request("POST", route, headers=headers, data=data)
            req = request.prepare()
            print('{}\n{}\r\n{}\r\n\r\n{}'.format(
                '-----------START-----------',
                req.method + ' ' + req.url,
                '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
                req.body,
            ))
            response = session.send(req, allow_redirects=args.redirect, verify=False, timeout=args.timeout[0])
            #response = session.post(args.route[0], headers=headers, allow_redirects=args.redirect, verify=False, timeout=args.timeout[0], data=data)
        elif method == "GET":
            req = route + "?" + data
            response = session.get(req, headers=headers, allow_redirects=args.redirect, verify=False,
                                   timeout=args.timeout[0])
        else:
            print(method)
    except requests.exceptions.Timeout as timeout:
        print("Resquest to %s took to long. Consider increase timeout." % route)
        return False
    except requests.exceptions.TooManyRedirects as redirects:
        print("Too Many Redirects for %s" % route)
        return False
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(0)
    else:
        #print(response.status_code, response.headers, response.text, sep="\n")
        print(response.status_code, response.headers, sep="\n")
        return response.status_code, len(response.text), response.text


def getToken(response):
    if re.search(args.regex[0], response):
        token = re.search(args.regex[0], response)[0]
        token = re.split(r'=', token, 1)[1]
        token = re.sub(r'(\"|\')', '', token)
        return token
    else:
        return False


def modeOne():
    if args.dict:
        if not os.path.isfile(args.dict[0]):
            print("Could not find the provided dictionary file (%s)" % args.dict[0])
            sys.exit(1)
        # startExecution()
        with open(args.dict[0], "r", encoding="utf-8") as dictionary:
            for line in dictionary:
                data = re.sub(r'%%FUZZ%%', line.rstrip("\n"), args.args)
                data = re.sub(r'%%CSRF%%', token, data)
                # print(data)
                status, length, response = curlRequest(session, args.route[0], args.method, data)
                token = getToken(response)
                if token:
                    results.append([token, status, length])
                    print("The token obtained is %s" % token)
                else:
                    results.append(["--", status, length])
                    print("No token was obtained with the provided Regular Expression. Quitting...")
                    break
                time.sleep(args.sleep[0] / 1000)
        printTable()

    else:
        # startExecution()
        status, length, response = curlRequest(session, args.route[0], args.method, args.args)
        token = getToken(response)
        if token:
            print("The token obtained is %s." % token)
        else:
            print("No token was obtained with the provided Regular Expression.")
        # stopExecution()
    return


def modeTwo():
    if args.dict:
        if not os.path.isfile(args.dict[0]):
            print("Could not find the provided dictionary file (%s)" % args.dict[0])
            sys.exit(1)
        # startExecution()
        with open(args.dict[0], "r", encoding="utf-8") as dictionary:
            for line in dictionary:
                status, length, response = curlRequest(session, args.request[0], args.method, data=None)
                token = getToken(response)
                if not token:
                    print("No token was obtained with the provided Regular Expression. Quitting...")
                    results.append([token, status, length])
                    print("The token obtained is %s" % token)
                    break
                else:
                    data = re.sub(r'%%FUZZ%%', line.rstrip("\n"), args.args)
                    data = re.sub(r'%%CSRF%%', token, data)
                    # print(data)
                    status, length, response = curlRequest(session, args.route[0], args.method, data)
                    results.append([token, status, length])
                    print("The token obtained is %s" % token)
                    time.sleep(args.sleep[0] / 1000)
        printTable()
    else:
        # startExecution()
        status, length, response = curlRequest(session, args.request[0], args.method, args.args)
        token = getToken(response)
        if token:
            print("The token obtained is %s." % token)
        else:
            print("No token was obtained with the provided Regular Expression.")
        # stopExecution()
    return


def startExecution():
    print("[*] TokenBruteforce started '%s' command at %s." % (
    " ".join(sys.argv[:]).lstrip(" "), time.strftime("%a, %d %b %Y %H:%M:%S")))
    return


def stopExecution():
    print("[*] TokenBruteforce finished '%s' command at %s." % (
    " ".join(sys.argv[:]).lstrip(" "), time.strftime("%a, %d %b %Y %H:%M:%S")))
    return


def printTable():
    print(tabulate(results, headers=tableHeaders, tablefmt="simple", showindex="always"))
    return


# Argparse
parser = argparse.ArgumentParser(
    description="Python bruteforce tool for requests with CRSF token.\nModes:\n\t» Mode 1. The application returns to the same web page when the data provided is incorrect.\n\t» Mode 2. The application returns to another page whether the result is possitive or not.")
parser.add_argument("mode", help="Mode of execution.", type=int, nargs=1, choices=[1, 2])
parser.add_argument("route", help="Request URL.", nargs=1)
parser.add_argument("args",
                    help="Data to send in the request. Valid formats: username=admin&password=$$FUZZ$$&token=$$CRSF$$ or {'username':'admin','password':'$$FUZZ$$','token':'$$CRSF$$'}.")
parser.add_argument("-t", "--token", dest="token", help="Initial token for the first request", nargs=1)
parser.add_argument("-R", "--regex", dest="regex", help="Regular expression to extract the CSRF token", nargs=1, required="true")
parser.add_argument("-r", "--request", dest="request", help="GET request to obtain the CSRF token in mode 2.", nargs=1)
parser.add_argument("-d", "--dictionary", dest="dict", help="Dictionary to perform the bruteforce", nargs=1)
# Miscellaneous
parser.add_argument("-s", "--sleep", dest="sleep", help="Sleeping time , in milliseconds, between requests.", type=int,
                    nargs=1, default=[0])
parser.add_argument("-T", "--timeout", dest="timeout", help="Set timeout for slow websites (sec).", nargs=1, type=int,
                    default=[10])
# Options from curl
parser.add_argument("-X", "--method", dest="method", help="Request method to use (by default POST).", nargs=1,
                    choices=["POST", "GET", "PUT", "PATCH"], default="POST")
parser.add_argument("-L", "--location", dest="redirect", help="Allow redirections", action='store_true')
parser.add_argument("-H", "--header", dest="headers", help="Request headers separated by commas", nargs=1)

parser.add_argument("-o", "--output", dest="output", help="Output file", nargs=1)
args = parser.parse_args()

# Main
if __name__ == "__main__":
    # Setup
    session = requests.session()
    session.max_redirects = 5
    if not re.search(r'^https?://[\S]+\.[\S]{2,}', args.route[0]):
        print("The URL provided is not valid. Example: https://github.com/n0t4u")
        sys.exit(1)
    if args.headers:
        for header in args.headers[0].split(","):
            key, value = header.split(":", 1)
            headers[key.strip(" ")] = value.strip(" ")
    print(args.regex[0])
    print(args.method)
    print(args.redirect)
    token = args.token[0] if args.token else ""
    if args.mode[0] == 1:
        modeOne()
    elif args.mode[0] == 2:
        modeTwo()
    sys.exit(0)
