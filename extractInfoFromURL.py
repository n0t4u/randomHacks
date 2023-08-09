#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Author: n0t4u

# Imports
import argparse
from termcolor import colored
import logging
import requests
import re
import sys
import urllib3
from urllib.parse import urlparse

urllib3.disable_warnings()

#Variables
headers = {}
routes = []
forms = []
versions = []
comments = []
response = ""
responseHeaders = {}

#Constants
securityHeaders = [
	"X-Frame-Options",
	"X-Content-Type-Options",
    "Referrer-Policy",
    "Content-Type",
    "Strict-Transport-Security",
	"Content-Security-Policy",
    "Access-Control-Allow-Origin",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy",
	"Permissions-Policy"
]
deprecatedSecurityHeaders = [
    "X-XSS-Protection",
    "Expect-CT",
    "Feature-Policy",
]
versionHeaders = [
    "Server",
    "X-Powered-By",
    "X-AspNet-Version",
    "X-AspNetMvc-Version",
    "X-DNS-Prefetch-Control"
]

cacheHeaders = [
    "Cache-Control",
    "Expires"
]

#Functions
def sendRequest(session, method, url):
    try:
        # https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw
        request = requests.Request(method, url, headers=headers, data=None)
        req = request.prepare()
        logging.info('{}\n{}\r\n{}\r\n\r\n{}\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
            '-----------STOP------------'
        ))
        response = session.send(req, allow_redirects=args.redirect, verify=False, timeout=args.timeout[0])
    except requests.exceptions.Timeout as timeout:
        print('Resquest to %s took to long. Consider increase timeout.' % url)
        logging.info(timeout)
        return False
    except requests.exceptions.TooManyRedirects as redirects:
        print('Too Many Redirects for %s' % url)
        logging.info(redirects)
        return False
    except requests.exceptions.RequestException as err:
        print('Error while sending request. For more information use de Debug option.')
        logging.info(err)
        sys.exit(0)
    else:
        logging.info(response.status_code, response.headers)
        return response.status_code, response.headers, response.text


def getSecurityHeaders():
    print(colored('\n[»] Security headers','blue'))
    for header in securityHeaders:
        if header in responseHeaders:
            print(header.ljust(30,' '), colored(responseHeaders[header],'green'))
        else:
            print(header.ljust(30,' '),colored('None','red'))
    print('[*] Note that some headers only applies for CORS')
    print(colored('[»] Deprecated security headers','blue'))
    for header in deprecatedSecurityHeaders:
        if header in responseHeaders:
            print(header.ljust(30,' '), colored(responseHeaders[header],'red'))
        else:
            print(header.ljust(30,' '), colored('None','green'))
    print(colored('[»] Version headers','blue'))
    for header in versionHeaders:
        if header in responseHeaders:
            print(header.ljust(30,' '), responseHeaders[header])
        else:
            print(header.ljust(30,' '),'None')
    print(colored('[»] Cache headers','blue'))
    for header in cacheHeaders:
        if header in responseHeaders:
            print(header.ljust(30,' '), colored(responseHeaders[header],'green'))
        else:
            print(header.ljust(30,' '), colored('None','red'))
    print('[*] These headers have been obtained from the OWASP Security Headers Project. For more information about these headers and its implementation, please refer to:\nhttps://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html')
    return


def getRoutes():
    getForms()
    return


def getForms():
    #Remove Enter, tabs and multi spaces to find all forms in the page
    minResponse = re.sub('(\n|\t| {2,}(?= ))','',response)
    #minResponse = re.sub('</form>','</form>\n',minResponse)
    minResponse = re.sub(r'<form','\n<form',minResponse)
    #print(minResponse)
    formsTags = re.findall('< ?form[\S ]+</form>',minResponse)
    logging.info('Obtained {} forms'.format(len(formsTags)))
    for find in formsTags:
        #print("\n"+find)
        findFormTag = re.split(r'>',find,1)[0]
        #print(findFormTag)
        name = re.search(r'(?<=name=["\'])[\S]+(?=["\'])', findFormTag)
        method = re.search(r'(?<=method=["\'])[\S]+(?=["\'])', findFormTag)
        action = re.search(r'(?<=action=["\'])[\S ]+(?=["\']>?)', findFormTag)
        enctype = re.search(r'(?<=enctype=["\'])[\S]+(?=["\']>?)', findFormTag)
        if enctype and findFormTag[enctype.start():enctype.end()] == 'multipart/form-data':
            print("Possible file upload. Reason: multipart/form-data form")
            inputValues = None #TODO. Extract form inputs
        else:
            inputValues = getInputValues(find,format=args.format)
        formInfo = dict(name=findFormTag[name.start():name.end()], method=findFormTag[method.start():method.end()], action=findFormTag[action.start():action.end()], inputs=inputValues)
        forms.append(formInfo)
        #logging.info(print(formInfo))
    print(colored('\n[»] Forms detected','blue'))
    for form in forms:
        print('{}\t{}://{}{}\t{}'.format(form['method'].upper(), url.scheme, url.netloc, re.sub(' ', '%20', form['action']), form['inputs']))
    return


def getInputValues(text, format):
    if format == "json":
        values = {}
        inputs = re.split(r'<input',text)[1:]
        for input in inputs:
            inputName = re.search(r'(?<=name=["\'])[\S]+(?=["\'])', input)
            inputValue = re.search(r'(?<=value=["\'])[\S]+(?=["\'])', input)
            if inputName and inputValue:
                values[input[inputName.start():inputName.end()]]=input[inputValue.start():inputValue.end()]
            elif inputName:
                values[input[inputName.start():inputName.end()]]='VALUE'
            else:
                logging.info('TODO. JSON form not completed.\n{}'.format(text))
        return values
    else:
        values = ""
        inputs = re.split(r'<input',text)[1:]
        for input in inputs:
            inputName = re.search(r'(?<=name=["\'])[\S]+(?=["\'])', input)
            inputValue = re.search(r'(?<=value=["\'])[\S]+(?=["\'])', input)
            if inputName and inputValue:
                values = '{}{}={}&'.format(values,input[inputName.start():inputName.end()],input[inputValue.start():inputValue.end()])
            elif inputName:
                values = '{}{}=VALUE&'.format(values, input[inputName.start():inputName.end()])
            else:
                logging.info('TODO. Normal form not completed.\n{}'.format(text))
        return values[:-1]


def getResources():
    return


def getVersions():
    return


def getComments():
    return


#Argparse
parser = argparse.ArgumentParser(description='Extract relevant information from a given URL')
parser.add_argument('url', help='URL to request and extract the information', action='store', nargs=1)
parser.add_argument('-r', '--routes', dest='routes', help='Extract routes, forms and resources', action='store_true')
parser.add_argument('-v', '--versions', dest='versions', help='Extract web technology versions', action='store_true')
parser.add_argument('-c', '--comments', dest='comments', help='Extract comments from source code', action='store_true')
parser.add_argument('-s', '--security-headers', dest='secHeaders', help='Extract the security headers', action='store_true')
parser.add_argument('-a', '--all', dest='all', help='Extract all', action='store_true')
#Misc options
parser.add_argument('-T', '--timeout', dest='timeout', help='Set timeout for slow websites (sec).', nargs=1, type=int, default=[10])
parser.add_argument('-d','--debug', dest='debug', help='Enable debug mode', action='store_true')
parser.add_argument('--format', dest='format',help='Format for form values. Options: normal (default),json', choices=['normal','json'], default='normal')
#Options from curl
parser.add_argument('-X', '--method', dest='method', help='Request method to use (by default POST).', nargs=1,
                    choices=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'], default='GET')
parser.add_argument('-L', '--location', dest='redirect', help='Allow redirections', action='store_true')
parser.add_argument('-H', '--headers', dest='headers', help='Request headers separated by commas', nargs=1)
#Output options
parser.add_argument('-o', '--output', dest='output', help='Output file', nargs=1)
args = parser.parse_args()



#Main
if __name__ == '__main__':
    if args.debug:
        logging.basicConfig(level=logging.INFO)
    session = requests.session()
    session.max_redirects = 5
    if args.headers:
        for header in args.headers[0].split(','):
            key, value = header.split(':', 1)
            headers[key.strip(' ')] = value.strip(' ')
        logging.info("Using the following headers:\n{}".format(headers))
    url = urlparse(args.url[0])
    print('Extracting information from {}'.format(args.url[0]))
    statusCode, responseHeaders, response = sendRequest(session, args.method, args.url[0])

    if args.all:
        getSecurityHeaders()
        getRoutes()
        #getVersions()
        #getComments()
    else:
        if args.secHeaders():
            getSecurityHeaders()
        if args.routes:
            getRoutes()
        if args.versions:
            getVersions()
        if args.comments:
            getComments()

    if args.output:
        with open(args.output[0],'w', encoding='utf-8') as file:
            file.write('TODO')