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
    "Permissions-Policy",
    "Access-Control-Allow-Origin",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy"
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
    getResources()
    getLinks()
    return


def getForms():
    #Remove Enter, tabs and multi spaces to find all forms in the page
    minResponse = re.sub('(\r|\n|\t| {2,}(?= ))','',response)
    #minResponse = re.sub('</form>','</form>\n',minResponse)
    minResponse = re.sub(r'<form','\n<form',minResponse)
    formsTags = re.findall(r'< ?form[\S ]+</form>',minResponse)
    logging.info('Obtained {} forms'.format(len(formsTags)))
    for find in formsTags:
        findFormTag = re.split(r'>',find,1)[0]
        name = re.search(r'((?<=name=["\'])|(?<=id=["\']))\S+(?=["\'])', findFormTag)
        if name is None:
            name = "-"
        else:
            name = findFormTag[name.start():name.end()]
        method = re.search(r'(?<=method=["\'])\S+(?=["\'])', findFormTag)
        if method is None:
            method = "-"
        else:
            method = findFormTag[method.start():method.end()]
        action = re.search(r'(?<=action=["\'])[^"\']+(?=["\']>?)', findFormTag)
        if action is None:
            action = "-"
        else:
            action = findFormTag[action.start():action.end()]
        enctype = re.search(r'(?<=enctype=["\'])\S+(?=["\']>?)', findFormTag)
        if enctype and findFormTag[enctype.start():enctype.end()] == 'multipart/form-data':
            print("Possible file upload. Reason: multipart/form-data form")
            inputValues = None #TODO. Extract form inputs
        else:
            inputValues = getInputValues(find,format=args.format)
        #formInfo = dict(name=findFormTag[name.start():name.end()], method=findFormTag[method.start():method.end()], action=findFormTag[action.start():action.end()], inputs=inputValues)
        formInfo = dict(name=name, method=method, action=action, enctype=enctype, inputs=inputValues)
        forms.append(formInfo)
        #logging.info(print(formInfo))
    print(colored('\n[»] Forms detected','blue'))
    for form in forms:
        if action == "-":
            print('{}\t{}://{}\t\t{}'.format(form['method'].upper(), url.scheme, url.netloc, form['inputs']))
        else:
            #If the action has the complete URL, remove the scheme and the domain.
            if re.search('^https?://', form['action'], re.I):
                form['action'] = '/{}'.format(form['action'].split('/',3)[-1])
            if form['method'] == "GET":
                print('{}\t{}://{}{}?{}'.format(form['method'].upper(), url.scheme, url.netloc, re.sub(' ', '%20', form['action']), form['inputs']))
            else:
                print('{}\t{}://{}{}\t{}'.format(form['method'].upper(), url.scheme, url.netloc, re.sub(' ', '%20', form['action']), form['inputs']))

    return


def getInputValues(text, format):
    #TODO. Get value input types and replace {{VALUE}} with its type
    #TODO. Add * when detecting forms with hidden values
    if format == "json":
        values = {}
        inputs = re.split(r'<input',text)[1:]
        for input in inputs:
            inputName = re.search(r'(?<=name=["\'])[\S]+(?=["\'])', input)
            inputValue = re.search(r'(?<=value=["\'])[\S]+(?=["\'])', input)
            if inputName and inputValue:
                values[input[inputName.start():inputName.end()]]=input[inputValue.start():inputValue.end()]
            elif inputName:
                values[input[inputName.start():inputName.end()]]='{{VALUE}}'
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
                values = '{}{}={{{{VALUE}}}}&'.format(values, input[inputName.start():inputName.end()])
            else:
                logging.info('TODO. Normal form not completed.\n{}'.format(text))
        return values[:-1]


def getResources():
    minResponse = re.sub('(\r|\n|\t| {2,})', ' ', response)
    print(colored('\n[»] Style Resources', 'blue'))
    cssMinResponse = re.sub(r'<link','\n<link',minResponse)
    cssMinResponse = re.sub(r'>', '>\n', cssMinResponse)
    cssLinks = re.findall(r'<link[\S ]+href=[\'"](?P<link>https?://[^\'"]+)',cssMinResponse)
    for cssLink in cssLinks:
        print(cssLink)
    print(colored('\n[»] JavaScript Libraries', 'blue'))
    jsMinResponse = re.sub(r'<script>','\n<script>',minResponse)
    jsMinResponse = re.sub(r'</script>', '</script>\n',jsMinResponse)
    javascriptSrcs = re.findall(r'<script[\S ]+src=[\'"](?P<script>https?://[^\'"]+)[\S ]+</script>',jsMinResponse) #
    for javascriptSrc in javascriptSrcs:
        print(javascriptSrc)
    return


def getLinks():
    minResponse = re.sub('(\r|\n|\t| {2,})', ' ', response)
    print(colored('\n[»] Links', 'blue'))
    linkMinResponse = re.sub(r'<a','\n<a',minResponse)
    links = re.findall(r'<a[\S ]+href=[\'"](?P<link>[^\'"]+)[\S ]+>', linkMinResponse)
    for link in links:
        if re.search(r'^https?://',link):
            print(link)
        elif re.search(r'^[#?]',link):
            print('{}{}'.format(args.url[0],link))
        elif re.search(r'/',link):
            print('{}://{}{}'.format(url.scheme,url.hostname,link))
        elif re.search(r'(tel:|mailto:)',link):
            print(link)
        #else:
            #print("NO {}".format(link))

def getVersions():
    print(colored('\n[»] Versions detected', 'blue'))
    for header in versionHeaders:
        if header in responseHeaders:
            print('{}\t Reason: Server response header \'{}: {}\''.format(colored(responseHeaders[header], 'red'), header, responseHeaders[header]))
    return


def getComments():
    print(colored('\n[»] Comments in source code', 'blue'))
    lineComments = re.findall(r'(^//[\S ]+|(?<=[ \t])//[\S ]+)',response)
    print(colored('\t[»] One-line comments', 'blue'))
    for lineComment in lineComments:
        print(re.sub(r'^[\s]*// *','',lineComment))
    minResponse = re.sub(r'(\r|\n|\t| {2,}(?= ))', '', response)
    minResponse = re.sub(r'<!--','\n<!--',minResponse)
    minResponse = re.sub(r'-->','-->\n',minResponse)
    comments = re.findall(r'<!--.*-->',minResponse)
    #TODO. Add the line number of the comments.
    print(colored('\t[»] Block comments', 'blue'))
    for comment in comments:
        print(re.sub(r'(^<!-- *| *-->$)','',comment))
    minResponse = re.sub(r'/\*','\n/*',minResponse)
    minResponse = re.sub(r'\*/','*/\n',minResponse)
    javaScriptBlockComments = re.findall(r'/\*.*\*/',minResponse)
    print(colored('\t[»] JavaScript comments', 'blue'))
    for blockComment in javaScriptBlockComments:
        print(re.sub(r'(^/\*[ \*]*|[ \*]*\*/$)','',blockComment))
    return

#Argparse
parser = argparse.ArgumentParser(description='Extract relevant information from a given URL')
parser.add_argument('url', help='URL to request and extract the information', action='store', nargs=1)
#Misc options
parser.add_argument('-T', '--timeout', dest='timeout', help='Set timeout for slow websites (sec).', nargs=1, type=int, default=[10])
verbose = parser.add_mutually_exclusive_group()
verbose.add_argument('-i', '--info', dest='info', help='Show more information', action='store_true')
verbose.add_argument('-d', '--debug', dest='debug', help='Enable debug mode', action='store_true')
parser.add_argument('--format', dest='format',help='Format for form values. Options: normal (default),json', choices=['normal','json'], default='normal')
#Options from curl
parser.add_argument('-X', '--method', dest='method', help='Request method to use (by default GET).', nargs=1,
                    choices=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'], default='GET')
parser.add_argument('--data', dest='data', help='Data for POST,PUT,DELETE and PATCH methods', nargs=1)
parser.add_argument('-L', '--location', dest='redirect', help='Allow redirections', action='store_true')
parser.add_argument('-H', '--headers', dest='headers', help='Request headers separated by commas', nargs=1)
#Output options
parser.add_argument('-o', '--output', dest='output', help='Output file', nargs=1)
args = parser.parse_args()



#Main
if __name__ == '__main__':
    if args.info:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif args.debug:
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    session = requests.session()
    session.max_redirects = 5
    if args.headers:
        for header in args.headers[0].split(','):
            key, value = header.split(':', 1)
            headers[key.strip(' ')] = value.strip(' ')
        logging.info("Using the following headers:\n{}".format(headers))
    try:
        url = urlparse(args.url[0])
        print('Extracting information from {}'.format(args.url[0]))
    except Exception as e:
        print(e)
    else:
        if args.method != 'GET' and not args.data:
            parser.error('--data option is required with {} method. If the request does not use any data, send " "'.format(args.method))
            exit()
        else:
            statusCode, responseHeaders, response = sendRequest(session, args.method, args.url[0])

    getSecurityHeaders()
    getRoutes()
    getVersions()
    getComments()

    if args.output:
        with open(args.output[0],'w', encoding='utf-8') as file:
            file.write('TODO')
