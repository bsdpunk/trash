import sys
import requests
import json
from pprint import pprint

def avail_datacenters(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.datacenters"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)


def avail_distributions(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.distributions"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def avail_plans(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.linodeplans"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def avail_stackscripts(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.stackscripts"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)


#def avail_kernels(api_key, option):
#    if(option)
#    headers = {'content-type': 'application/json'}
#    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.kernels"
#    r = requests.get(endpoint, headers=headers)
#    json_data = json.loads(r.text) 
#    return(json_data)
