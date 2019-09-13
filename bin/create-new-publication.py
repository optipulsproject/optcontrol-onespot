#!/usr/bin/python3

import requests
import json
import argparse
import sys
import time
import os

#the format a url which accesses the gitlab project api
urlFormat='https://gitlab.hrz.tu-chemnitz.de/api/v4/projects/%(projectId)d'
#status codes according to https://docs.gitlab.com/ee/api/README.html#status-codes
POST_OK=201
PUT_OK=200
GET_OK=PUT_OK

#provide the command line arguments to the parser
parser=argparse.ArgumentParser(description='prepare fork for new publication and provide an initial README.md')
parser.add_argument('pubTitle', metavar='title', help='publication title')
parser.add_argument('--pubPath', metavar='path', help='path in gitlab. The default path is constructed from the title by replacing spaces with minus.', nargs='?', default=None)
parser.add_argument('--login-token', metavar='token', help='the private token for login', nargs='?', default=None) #, type=basestring)

args=parser.parse_args()

#prefer the token from commandline
if args.login_token:
    privateToken = args.login_token
else:
    privateToken = os.environ['NUMAPDE_GITLAB_TOKEN']

pubTitle=args.pubTitle
pubPath=pubTitle.replace(' ','-')
if(args.pubPath):
    pubPath=args.pubPath

#url="https://gitlab.hrz.tu-chemnitz.de/api/v4/projects"

#define the common headerfor all operations
headers={'Private-Token' : privateToken} 

#fork the template
templateId=5326 #TODO: request the id from the name
#sandboxId=2576
url=urlFormat %{'projectId':templateId}+'/fork'
#print(url)
payload={'namespace':'numapde/sandbox','name':pubTitle,'id':templateId, 'path' : pubPath}
print(payload)

r=requests.post(url, headers=headers, data=payload)
print(r.text)
if(r.status_code != POST_OK):
    print('something went wrong during forking. got status code %d and result text %s' % (r.status_code, r.text))
    sys.exit(1)

#prepare the new README.md
#https://docs.gitlab.com/ee/api/repository_files.html 
newProject=json.loads(r.text) # extract the project information into a dictionary
newId=newProject['id'] 
#TODO: check if the project is ready after each pause
print('wait some seconds and let gitlab create the project')
time.sleep(5)
url=urlFormat %{'projectId' : newId}
#TODO: do this url-encoding in the right way..
url=url+'/repository/files/README%2Emd'
with open('README.md.in') as file:
    readme = file.read()
ssh_url_to_repo=newProject['ssh_url_to_repo']
#prepare the new readme file
readme=readme % { 'PUBLICATION_TITLE' : pubTitle, 'http_url_to_repo' : newProject['http_url_to_repo'], 'ssh_url_to_repo' : ssh_url_to_repo}
#call the gitlab api
payload={'file_path':'README%2Emd', 'branch' : 'master', 'content' : readme, 'commit_message' : 'replace the readme with title and project information'}
rReadme=requests.put(url, headers=headers, data=payload)
if(rReadme.status_code != PUT_OK):
    print("the readme update did not work, got error response: "+rReadme.text)
    sys.exit(1)
#print('response after readme update: '+rReadme.text)
print("created new repository at "+ssh_url_to_repo)
