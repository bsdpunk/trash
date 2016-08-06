import sys
import requests
import json
from pprint import pprint

def nodebal_list(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=nodebalancer.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def nodebal_node_list(api_key, config_id):
    headers = {'content-type': 'application/json'}
    print(config_id)    
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=nodebalancer.node.list&ConfigID="+ config_id
    print(endpoint)
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def nodebal_config_list(api_key, node_bal_id):
    headers = {'content-type': 'application/json'}
    #print(config_id)    
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=nodebalancer.config.list&NodeBalancerId="+node_bal_id
    #print(endpoint)
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def nodebal_create(api_key, dc_id):
    headers = {'content-type': 'application/json'}
    #print(config_id)    
    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=nodebalancer.create&DatacenterId="+dc_id
    #print(endpoint)
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)


#def avail_distributions(api_key):
#    headers = {'content-type': 'application/json'}
#    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.distributions"
#    r = requests.get(endpoint, headers=headers)
#    json_data = json.loads(r.text) 
   
#    return(json_data)

#def avail_kernels(api_key, option):
#    if(option)
#    headers = {'content-type': 'application/json'}
#    endpoint = "https://api.linode.com/?api_key=" + api_key['Linode-API-Key'] + "&api_action=avail.kernels"
#    r = requests.get(endpoint, headers=headers)
#    json_data = json.loads(r.text) 
   
#    return(json_data)
