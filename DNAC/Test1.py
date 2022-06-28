
import requests
#import prettytable
from requests.auth import HTTPBasicAuth
import os
import sys
from Authentication import auth

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)




#import env_lab

#DNAC_URL = env_lab.DNA_CENTER["host"]
#DNAC_USER = env_lab.DNA_CENTER["username"]
#DNAC_PASS = env_lab.DNA_CENTER["password"]

DNAC_URL = "10.8.11.100"
DNAC_USER = "admin"
DNAC_PASS = "Cisco123!"

def get_network_hierarchy():
    """
    Building out function to reitrieve network hierarchy with sites/buildings/floors 
    """
    token = auth.get_auth_token(DNAC_URL, DNAC_USER, DNAC_PASS)
    url = "https://{}/dna/intent/api/v1/site".format(DNAC_URL)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
    site_list = resp.json()
    #print_device_list(site_list)
    #print(type(site_list))
    #print(site_list)

    #for site in site_list['response']:
    #    print(site.get('name') + ": ", end = '')
    #    for addInfo in site['additionalInfo']:
    #        area_type = addInfo.get('attributes').get('type')
    #        print(site.get('name'), ": ", area_type)

    for site in site_list['response']:
        print(site.get('name') + ": " + site.get('id'))

def create_site():
    token = auth.get_auth_token()
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    hdr['__runsync'] = 'true'
    hdr['__runsynctimeout'] = '30'
    url = "https://{}/dna/intent/api/v1/site".format(DNAC_URL)
       
    site_area = {
    "type": "area",
    "site": {
        "area": {
            "name": "Zizkov",
            "parentName": "Test"
            }
        }
    }   
    resp = requests.post(url, headers=hdr, json=site_area, verify=False)

if __name__ == "__main__":
    #create_site()
    get_network_hierarchy()