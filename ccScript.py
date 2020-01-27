import requests
import urllib3
import json
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## User Variables to modify.
cvpNode = '192.168.255.51'
cvpUsername = 'admin'
cvpPassword = 'Arista'
##

"""
Simple change-control script to use for scheduling.

To run:
python ccScript.py <args>
eg: python ccScript.py --ccid=656f730a-20D8ZwR41 --start

Arguments:
--ccid = change control identifier. Can find by inspecting the URL while in
a change control. Ex: /change-control?ccId=656f730a-20D8ZwR41 - use everything
after 'ccId=', so ccid should be 656f730a-20D8ZwR41
--start = start change control, generates no useful output.
"""

#Requests info for CVP API
server = 'https://'+cvpNode
connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
requests.packages.urllib3.disable_warnings()
session = requests.Session()

def parseArgs():
   parser = argparse.ArgumentParser( description='Change-Control Kickstart' )
   parser.add_argument('--ccid', help='Enter the Change Control id.', type=str)
   parser.add_argument('--start', help='Starts Change Control.', action='store_true')
   args = parser.parse_args()
   return args

# CVP API Functions
def login(url_prefix, username, password):
    authdata = {"userId": username, "password": password}
    headers.pop('APP_SESSION_ID', None)
    response = session.post(url_prefix+'/web/login/authenticate.do', data=json.dumps(authdata),
                            headers=headers, timeout=connect_timeout,
                            verify=False)
    cookies = response.cookies
    headers['APP_SESSION_ID'] = response.json()['sessionId']
    if response.json()['sessionId']:
        return response.json()['sessionId']

def logout(url_prefix):
    response = session.post(url_prefix+'/cvpservice/login/logout.do')
    return response.json()

def start_cc(url_prefix,ccID):
    tempData = json.dumps({'cc_id': ccID})
    response = session.post(url_prefix+'/api/v3/services/ccapi.ChangeControl/Start', data=tempData)
    return response.json()

options = parseArgs()
if options.ccid:
    ccID = options.ccid
else:
    print 'Please enter a change control identifier with --ccid (changecontrolid).'
    exit()
login(server,cvpUsername,cvpPassword)
if options.start:
    output = start_cc(server,ccID)
print output
logout(server)
