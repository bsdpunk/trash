import sys
import requests
import json
import re
from pprint import pprint

def list_domains(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=domain.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)


def domain_resource_list(api_key, domain_id, resource_id=0):
    headers = {'content-type': 'application/json'}
    if resource_id == 0:
        endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=domain.resource.list&DomainID="+ domain_id
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text) 
    else:
        endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=domain.resource.list&DomainID="+ domain_id + "&ResourceID="+resource_id
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text) 
 
    return(json_data)


def domain_resource_create(api_key, domain_id, kind, name = None,target = None):
    headers = {'content-type': 'application/json'}
    if name is None:
        print("none")
    elif target is None:
        print("none")
    else:
        endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=domain.resource.create&DomainID=" +domain_id + "&Type=" + kind + "&Name=" + name +"&Target=" + target

    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)






#def ip_list(api_key, arguement=0):
#    headers = {'content-type': 'application/json'}
#    ip_addy = re.compile('(\d+|\d)\.(\d+|\d)\.(\d+|\d)\.(\d+|\d)')
#    lin_name = re.compile('linode(\d+)')
#    #print(arguement)
#    if(arguement == 0):
#        endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=linode.ip.list"
#        r = requests.get(endpoint, headers=headers)
#        json_data = json.loads(r.text) 
#
#    elif re.match(ip_addy, arguement) is not None:
#        print("not implimented yet")
#    elif re.match(lin_name, arguement) is not None:
#        p = re.match(lin_name, arguement)
#        lin_id = p.group(1)
#        #print(lin_id)
#        endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=linode.ip.list&LinodeID="+ lin_id
#        r = requests.get(endpoint, headers=headers)
#        json_data = json.loads(r.text)
#        #pprint(json_data)
#        json_data = json_data["DATA"][0]["IPADDRESS"]
#        
#        
#    return(json_data)
#
#def linode_create(api_key, dc_id, plan_id, pay_term_id=0):
#    headers = {'content-type': 'application/json'}
#    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=linode.create&DatacenterID="+ dc_id +"&PlanID=" +plan_id
#    r = requests.get(endpoint, headers=headers)
#    json_data = json.loads(r.text) 
#   
#    return(json_data)
#
#def linode_shutdown(api_key, numeric_lin_id):
#    headers = {'content-type': 'application/json'}
#    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=linode.shutdown&LinodeID="+ numeric_lin_id
#    r = requests.get(endpoint, headers=headers)
#    json_data = json.loads(r.text) 
#   
#    return(json_data)
