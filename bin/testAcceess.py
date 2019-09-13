#!/usr/bin/python3

import requests
import json
import argparse
import sys
import time

url="https://gitlab.hrz.tu-chemnitz.de/oauth/token"
payload={'grant_type' : 'password', 'username' : 'andna--tu-chemnitz.de'} #@gitlab.hrz.tu-chemnitz.de
r=requests.post(url, data=payload)
print(r.status_code)
print(r.text)
authData=json.loads(r.text)

#headers={'Authorization' : " ".join([authData['token_type'],authData['access_token']])}
#payload={'simple':True, 'owned' : True, 'membership': True}
#r=requests.get(url, headers=headers, data=payload)
#print(r.text)
