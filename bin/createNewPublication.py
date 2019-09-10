#!/usr/bin/python3

import requests
import json
import argparse
import sys
import time

parser=argparse.ArgumentParser(description='prepare fork for new publication')
parser.add_argument('login_token', metavar='token', help='the private token for login') #, type=basestring)
parser.add_argument('pubTitle', metavar='title', help='publication title')
parser.add_argument('pubPath', metavar='path', help='path in gitlab. The default path is constructed from the title by replacing spaces with minus.', nargs='?', default=None)

args=parser.parse_args()
privateToken = args.login_token
pubTitle=args.pubTitle
pubPath=pubTitle.replace(' ','-')
if(args.pubPath):
    pubPath=args.pubPath

url="https://gitlab.hrz.tu-chemnitz.de/api/v4/projects"
headers={'Private-Token' : privateToken} 
#print(headers)

#payload={'simple':True, 'owned' : True, 'membership': True}
#r=requests.get(url, headers=headers, data=payload)
##print(r.text)
#asData=json.loads(r.text)
#print(len(asData))
##print(asData[0])
#for d in asData:
#    print(d['namespace'])


#url='https://gitlab.hrz.tu-chemnitz.de/api/v4/projects'
#payload={'name':'myTestProject'}
#r=requests.post(url, headers=headers, data=payload)
#print(r.text)
#print(r.status_code)

#fork the template
templateId=5326
#sandboxId=2576
urlFormat='https://gitlab.hrz.tu-chemnitz.de/api/v4/projects/%(projectId)d'
url=urlFormat %{'projectId':templateId}+'/fork'
#print(url)
payload={'namespace':'numapde/sandbox','name':pubTitle,'id':templateId, 'path' : pubPath}
print(payload)

r=requests.post(url, headers=headers, data=payload)
print(r.text)
if(r.status_code != 201):
    print('something went wrong during forking. got status code %d and result text %s' % (r.status_code, r.text))
    sys.exit(1)

#prepare the new README.md
#https://docs.gitlab.com/ee/api/repository_files.html 
newProject=json.loads(r.text)
newId=newProject['id']
#TODO: check if the project is ready after each pause
print('wait some seconds and let gitlab create the project')
time.sleep(5)
url=urlFormat %{'projectId' : newId}
#TODO: do this url-encoding in the right way..
url=url+'/repository/files/README%2Emd'
with open('README.md.in') as file:
    readme = file.read()
readme=readme % { 'PUBLICATION_TITLE' : pubTitle, 'http_url_to_repo' : newProject['http_url_to_repo'], 'ssh_url_to_repo' : newProject['ssh_url_to_repo']}
payload={'file_path':'README%2Emd', 'branch' : 'master', 'content' : readme, 'commit_message' : 'replace the readme with title and project information'}
rReadme=requests.put(url, headers=headers, data=payload)
if(rReadme.status_code != 200):
    print("the readme update did not work, got response: "+rReadme.text)
    sys.exit(1)
print('response after readme update: '+rReadme.text)
