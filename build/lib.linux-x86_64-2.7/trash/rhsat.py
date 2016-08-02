import sys
import json
import re
from pprint import pprint

def sat_list_users(key):
    luser = key["client"].user.list_users(key["key"])
    #pprint(luser)
    data = {}
    for user in luser:
        alter = {'login': user.get('login'), 'login_uc': user.get('login_uc'), 'name': user.get('name'), 'email': user.get('email')}
        data[user.get('login')]=alter
        
    json_data = data
   
    return(json_data)

def sat_get_api_call(key):
    api = key["client"].api.getApiCallList(key["key"])
    #pprint(luser)
    data = api
    #for api_calls in api:
        #alter = {'name': api_calls.get('name'), 'parameters': api_calls.get('parameters'), 'exceptions': api_calls.get('exceptions'), 'return': api_calls.get('return')}
        #data[user.get('login')]=alter
        
    json_data = data
   
    return(json_data)

def sat_get_version(key):
    api = key["client"].api.getVersion()
    #pprint(luser)
    data = api
    #for api_calls in api:
        #alter = {'name': api_calls.get('name'), 'parameters': api_calls.get('parameters'), 'exceptions': api_calls.get('exceptions'), 'return': api_calls.get('return')}
        #data[user.get('login')]=alter
        
    json_data = data
   
    return(json_data)

def sat_system_version(key):
    api = key["client"].api.systemVersion()
    #pprint(luser)
    data = api
    #for api_calls in api:
        #alter = {'name': api_calls.get('name'), 'parameters': api_calls.get('parameters'), 'exceptions': api_calls.get('exceptions'), 'return': api_calls.get('return')}
        #data[user.get('login')]=alter
        
    json_data = data
   
    return(json_data)


def sat_list_all_groups(key):
    groups = key["client"].systemgroup.listAllGroups(key["key"])
    #pprint(luser)
    data = groups
    #for user in luser:
     #   alter = {'login': user.get('login'), 'login_uc': user.get('login_uc'), 'name': user.get('name'), 'email': user.get('email')}
     #   data[user.get('login')]=alter
        
    json_data = data
   
    return(json_data)



def sat_list_active_systems(key):
    systems = key["client"].system.listActiveSystems(key["key"])
    data = systems
        
    json_data = data
   
    return(json_data)

def sat_list_groups(key, server):
    groups = key["client"].system.listGroups(key["key"], server)
    data = groups
        
    json_data = data
   
    return(json_data)

def sat_system_group_audit(key):
    newkey = key["key"] 
    systems = key["client"].system.listActiveSystems(key["key"])
    data = {}
    
    for s in systems:
        #print(s)
        #print(s.get('id'))    
        groups = key["client"].system.listGroups(newkey, s.get('id'))
        #print(groups)
        #print(s.get('name')) 
        i = 0
        data[str(s.get('name'))]={}
        for g in groups:
            if g.get('subscribed') == 1:
            #print(s.get('name'))
                data[str(s.get('name'))][i]=g.get('system_group_name')
                i = i + 1

    json_data = data

    return(json_data)


def sat_list_systems(key, sys_groups):
    groups = key["client"].systemgroup.listSystems(key["key"], sys_groups)
    #pprint(luser)
    data = {}
    for w in groups:
        alter = {'id': w.get('id'), 'release': w.get('release'), 'hostname': w.get('hostname')}
        data[w.get('id')]=alter
        
    json_data = data
   
    return(json_data)


