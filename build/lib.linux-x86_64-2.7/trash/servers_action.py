import sys
import requests
import json
import re
from pprint import pprint

def linode_list(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def linode_list_ip(api_key, arguement=0):
    headers = {'content-type': 'application/json'}
    ip_addy = re.compile('(\d+|\d)\.(\d+|\d)\.(\d+|\d)\.(\d+|\d)')
    lin_name = re.compile('(\d+)')
    #print(arguement)
    if(arguement == 0):
        endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.ip.list"
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text) 

    elif re.match(ip_addy, arguement) is not None:
        json_data = "not implimented yet"
    elif re.match(lin_name, arguement) is not None:
        p = re.match(lin_name, arguement)
        lin_id = p.group(1)
        #print(lin_id)
        endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.ip.list&LinodeID="+ lin_id
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text)
        #pprint(json_data)
        json_data = json_data["DATA"][0]["IPADDRESS"]
    else:
        json_data = "Invalid"   
        
    return(json_data)

def linode_create(api_key, dc_id, plan_id, pay_term_id=0):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.create&DatacenterID="+ dc_id +"&PlanID=" +plan_id
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def linode_disk_create(api_key, l_id, size, dst_id=0, root=0, label=0, formatt=0, ro=0):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.create&DatacenterID="+ dc_id +"&PlanID=" +plan_id
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def linode_disk_dist(api_key, l_id, dst_id, label, size, root, ssh_key=0):
    headers = {'content-type': 'application/json'}
    if ssh_key == 0:
        endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.disk.createfromdistribution&LinodeID="+ l_id +"&DistributionID=" +dst_id+"&Label="+label+"&Size="+size+"&rootPass="+root
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text) 
    else:
        json_data = "Invalid"
    return(json_data)

#def linode_config_create(api_key, l_id, k_id, label, size, root, ssh_key=0):
#    headers = {'content-type': 'application/json'}
#    if ssh_key == 0:
#        endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.disk.createfromdistribution&LinodeID="+ l_id +"&DistributionID=" +dst_id+"&Label="+label+"&Size="+size+"&rootPass="+root
#        r = requests.get(endpoint, headers=headers)
#        json_data = json.loads(r.text) 
#    else:
#        json_data = "Invalid"
#    return(json_data)

#def linode_disk_image(api_key, i_id, l_id, label, size, root, ssh_key=0):
#    headers = {'content-type': 'application/json'}
#    if ssh_key == 0:
#        endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.disk.createfromdistribution&i_id="+i_id+"&LinodeID="+ l_id+"&Label="+label+"&Size="+size+"&rootPass="+root
#
#        r = requests.get(endpoint, headers=headers)
#        json_data = json.loads(r.text) 
#    else:
#        json_data = "Invalid"
#    return(json_data)

def list_images(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=image.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)




def linode_shutdown(api_key, numeric_lin_id):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key["Linode-API-Key"] + "&api_action=linode.shutdown&LinodeID="+ numeric_lin_id
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)
