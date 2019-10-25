#!/usr/bin/python3

# This script is meant to facilitate the creation of a new Gitlab repository for a publication.
# To this end, it
# * forks numapde-template into a new Gitlab repository with a specified name (shortTitle), 
# * assigns the new repository to a Gitlab namespace different from the default numade/sandbox if desired (namespace)
# * creates a new README.md from the template README.md.in by substitution.

# The Gitlab API access token is obtained from the environment variable NUMAPDE_GITLAB_TOKEN.

import requests
import json
import argparse
import sys
import time
import os

# Specify the Gitlab server
gitlabServer = os.environ.get('NUMAPDE_GITLAB_SERVER', None)
if gitlabServer is None:
    print('Please set the NUMAPDE_GITLAB_SERVER variable.')
    sys.exit(1)

# Specify the URL format to access the Gitlab project API
urlFormat = 'https://' + gitlabServer + '/api/v4/projects/%(projectId)d'

# Specify the default name space 
# namespace = 'numapde/sandbox'
namespace = 'numapde/Publications'

# Set the repository id for the template to be forked
# https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/numapde-template
templateId = 5326 

# Define some status codes according to https://docs.gitlab.com/ee/api/README.html#status-codes
POST_OK = 201
PUT_OK = 200
GET_OK = PUT_OK

# Provide the command line arguments to the parser
parser = argparse.ArgumentParser(description = 'This script forks the numapde Gitlab template repository for a new publication and provides an initial README.md.')
parser.add_argument('longTitle', metavar = 'longTitle', help = 'long publication title')
parser.add_argument('shortTitle', metavar = 'shortTitle', help = 'short publication title')
parser.add_argument('--namespace', metavar = 'namespace', help = 'Gitlab namespace with default %s.' % namespace, nargs = '?', default = namespace)
args = parser.parse_args()

# Get the API access token from the environment variable NUMAPDE_GITLAB_TOKEN
privateToken = os.environ.get('NUMAPDE_GITLAB_TOKEN', None)
if privateToken is None:
    print('Please set the NUMAPDE_GITLAB_TOKEN variable to your personal Gitlab access token.')
    sys.exit(1)

# Set the long title
longTitle = args.longTitle

# Replace spaces by hyphens in the short title
shortTitle = args.shortTitle
shortTitle = shortTitle.replace(' ','-')

# Set the namespace
namespace = args.namespace

# Define the common header for all API operations
headers = {'Private-Token': privateToken} 

# Prepare the fork action URL
url = urlFormat %{'projectId': templateId} + '/fork'

# Assemble the URL payload for the fork request
# 'name' corresponds to 'Project name' in the 'new project' web interface.
# 'path' corresponds to 'Project slug' in the 'new project' web interface.
payload = {'namespace': namespace, 'name': longTitle, 'id': templateId, 'path': shortTitle}
# print(payload)

# Submit the fork request
# TODO: Make this output more verbose and anticipate the name of the target repository URL
print('Requesting the Gitlab server to fork %s.' % url)
r = requests.post(url, headers = headers, data = payload)
# print(r.text)
if(r.status_code != POST_OK):
    print('Something went wrong during forking. The status code is %d and the result text is %s.' % (r.status_code, r.text))
    sys.exit(1)

# Extract the project information into a dictionary 
newProject = json.loads(r.text) 
newId = newProject['id'] 
newUrl = urlFormat %{'projectId': newId}


# Allow the Gitlab server to create the project
# TODO: check if the project is ready after each pause
print('Waiting some seconds to allow Gitlab to create the project...')
time.sleep(5)


# Update (empty) the project description
newDescription = '' 

# Assemble the URL payload for the project description update request
payload = {'id': newId, 'description': newDescription}

# Submit the commit request
rDescription = requests.put(newUrl, headers = headers, data = payload)
# print(rDescription)
if(rDescription.status_code != PUT_OK):
    print('Updating project description failed. The result text is: ' + rDescription.text)
    sys.exit(1)


# Prepare the new README.md
# https://docs.gitlab.com/ee/api/repository_files.html 
# Prepare the URL for the README.md file in the new repository
# TODO: do this url-encoding in the right way..
readmeUrl = newUrl + '/repository/files/README%2Emd'

# Get path to README.md.in, relative to the directory from where the present script is located
readmePath = os.path.dirname(os.path.abspath(__file__)) + '/../README.md.in'
print('Using template %s.' % readmePath)

# Read the template README.md.in
with open(readmePath) as file:
    readme = file.read()

# Get SSH and HTTP URLs to new project
sshURLToRepo = newProject['ssh_url_to_repo']
httpURLToRepo = newProject['http_url_to_repo']

# Prepare the new README.md file by string substitution
readme = readme % {'PUBLICATION_TITLE': longTitle, 'HTTP_URL_TO_REPO': httpURLToRepo, 'SSH_URL_TO_REPO': sshURLToRepo}

# Assemble the URL payload for the README.md commit request
payload = {'file_path': 'README%2Emd', 'branch': 'master', 'content': readme, 'commit_message': '%s auto-generates README.md' % sys.argv[0]}

# Submit the commit request
rReadme = requests.put(readmeUrl, headers = headers, data = payload)
# print(rReadme)
if(rReadme.status_code != PUT_OK):
    print('Commiting README.md failed. The result text is: ' + rReadme.text)
    sys.exit(1)


# Print a success message
print('Clone the new repository using\n  git clone --recurse-submodules %s' % sshURLToRepo)
print('Then update the submodules via\n  bin/numapde-submodules-update.sh')

