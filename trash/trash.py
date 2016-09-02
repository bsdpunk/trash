from __future__ import print_function
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import xmlrpclib
import ssl
import re
import readline
import threading
import sys
#import requests
import json
import os
from pprint import pprint
import signal,random, getpass
import urlparse, argparse
import pkg_resources
#Counters and Toggles
import readline
import codecs
import unicodedata
import readline
import rlcompleter
import rhsat, ucommands
import random, shlex, atexit
import platform, time, calendar
import vmutils
import pyVim, pyVmomi
#linosh libraries
#import oneshot
import servers_action, domain, lin_utility, node_balance 
from pyVim.connect import SmartConnect, Disconnect
import dock_containers

arg_count = 0
no_auth = 0
database_count = 0
ddb_count = 0
hist_toggle = 0
prompt_r = 0


        
#For tab completion
COMMANDS = sorted(['dock-events','dock-containers','esx-destroy-vm','esx-create-from-ova','esx-create-from-ovf','list-images','linode-disk-dist','domain-resource-list','domain-resource-create','list-domains','linode-shutdown', 'avail-stackscripts','avail-plans','linode-create','nodebal-create', 'nodebal-config-list','nodebal-node-list','nodebal-list', 'linode-list','linode-list-ip', 'avail-datacenters', 'avail-distributions','esx-vm-device-info', 'esx-list-datastores',  'esx-check-tools', 'esx-change-cd','esx-get-vm-uuid','sat-system-group-audit', 'esx-get-vm-name', 'esx-get-datastores','esx-get-resource-pools','esx-get-registered-vms','esx-get-hosts','sat-list-systems','sat-list-all-groups','jump','which','sat-system-version','sat-get-version','sat-get-api-call','sat-list-users','help','?','exit','clear','quit','version'])

#For X number of arguements
ONE = ['dock-events','dock-containers','list-images','list-domains', 'linode-list-ip', 'linode-list', 'avail-datacenters', 'avail-distributions', 'avail-plans', 'avail-stackscripts', 'nodebal-list', 'esx-list-datastores',  'sat-system-group-audit', 'esx-get-datastores','esx-get-resource-pools','esx-get-registered-vms','esx-get-hosts','sat-list-all-groups','sat-system-version','sat-list-users','sat-get-api-call','sat-get-version']
TWO = ['esx-destroy-vm','esx-create-from-ova','linode-list-ip', 'nodebal-node-list', 'nodebal-config-list', 'nodebal-create', 'linode-shutdown','domain-resource-list','esx-change-cd','esx-vm-device-info', 'esx-check-tools','esx-get-vm-uuid','broad-ad-search','esx-get-vm-name','sat-list-systems','jump','which','domain-resource-list']
THREE = ['esx-create-from-ovf','linode-create','domain-resource-list', 'esx-change-cd']
FOUR = ['domain-resource-create']
FIVE = ['domain-resource-create']
SIX = ['linode-disk-dist']
#For what class
RHSAT= ['sat-system-group-audit', 'sat-list-systems','sat-list-all-groups','sat-system-version','sat-list-users','sat-get-api-call','sat-get-version']
ADNET= ['search-for-name']
HELPER = ['hidden','?','help', 'quit', 'exit','clear','ls', 'version', 'qotd']
UCOMMANDS = ['search-for-id','which','jump']
VMUTILS = ['esx-destroy-vm','esx-create-from-ova','esx-create-from-ovf','esx-vm-device-info', 'esx-perf-query', 'esx-list-datastores',  'esx-check-tools', 'esx-change-cd','esx-get-vm-uuid','esx-get-vm-name','esx-get-datastores','esx-get-resource-pools','esx-get-registered-vms','esx-get-hosts']
DOMAIN= ['domain-resource-create','list-domains','domain-resource-list']
SA = ['list-images','linode-list','linode-list-ip','linode-create', 'linode-shutdown','linode-disk-dist']
LU = ['avail-datacenters', 'avail-distributions', 'avail-plans', 'avail-stackscripts']
NB = ['nodebal-list', 'nodebal-node-list', 'nodebal-config-list', 'nodebal-create']
CONTAINERS = ['dock-events','dock-containers']
for arg in sys.argv:
    arg_count += 1

#warnings are ignored because of unverified ssl warnings which could ruin output for scripting
import warnings
warnings.filterwarnings("ignore")



#These are lists of things that are persistent throughout the session
username=''
details = {}
def complete(text, state):
        for cmd in COMMANDS:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1


#os expand must be used for 
config_file = os.path.expanduser('~/.trash.sh')
hist_file = os.path.expanduser('~/.trash_history')
buff = {}
hfile = open(hist_file, "a")
if os.path.isfile(config_file):
    config=open(config_file, 'r')
    config=json.load(config)
else:
    username = raw_input("Username:")
    password = getpass.getpass("Password:")
    vcenter = raw_input("VCenter Server (ex: company.local):")
    ssh_pub = raw_input("ssh-pub:")
    sat_url =raw_input("Satellite Server Url (ex: https://redhat/rhn/rpc/api):")
    jump =raw_input("Jump Server(IP or DNS):")
    docker_ip =raw_input("Docker Remote API IP:")
    linode_api_key = getpass.getpass("Linode-API-Key:")
    api_key = linode_api_key 

    config= {"default":[{"username":username,"password":password,'vcenter':vcenter,"sat_url":sat_url,"jump":jump,"Linode-API-Key":api_key, "docker-ip":docker_ip, "ssh-pub":ssh_pub}]}
    
    config_file_new = open(config_file, "w")
    config_f = str(config)
    config_f = re.sub("'",'"',config_f)
    config_file_new.write(config_f)
    config_file_new.close 

#Ending when intercepting a Keyboard, Interrupt
def Exit_gracefully(signal, frame):
    #hfile.write(buff)
    sys.exit(0)



#DUH
def get_sat_key(config):
    signal.signal(signal.SIGINT, Exit_gracefully)
    #global username
    username = config["default"][0]["username"]
    password = config["default"][0]["password"]
    sat_url = config["default"][0]["sat_url"]
    docker_ip = config["default"][0]["docker-ip"]
    vcenter = config["default"][0]["vcenter"]
    ssh_pub = config["default"][0]["ssh-pub"]
    lkey = config["default"][0]["Linode-API-Key"]
    api_key = config["default"][0]["Linode-API-Key"]
    key={}
    key['username']=username
    key['password']=password
    key['ssh-pub']=ssh_pub
    #key['platform']=ucommands.os_platform()
    key['vcenter']=vcenter
    key['si']=None
    key['Linode-API-Key']=lkey
    key['docker-ip']=docker_ip
    if sat_url:

        if platform.python_version() == '2.6.6':
            key['client'] = xmlrpclib.Server(sat_url, verbose=0)
        else:
            key['client'] = xmlrpclib.Server(sat_url, verbose=0,context=ssl._create_unverified_context())
        

        key['key']=key["client"].auth.login(username, password)
    else:
        key['client'] = ''
    key['jump'] = config["default"][0]["jump"]
    try:
        return(key)
    except KeyError:
        print("Bad Credentials!")
        os.unlink(config_file)
        bye()
    return(key)

def esxi_connect(key):

    key['si'] = None
    username = key["username"]
    password = key["password"]
    vcenter = key["vcenter"]
    
    if platform.python_version() != '2.6.6':
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE

    try:
         
        if platform.python_version() == '2.6.6':
            key['si'] = SmartConnect(host=key['vcenter'], user=key['username'], pwd=key['password'], port=443)
        else:
            key['si'] = SmartConnect(host=key['vcenter'], user=key['username'], pwd=key['password'], port=443, sslContext=context)
    except IOError, e:
        print(e)
        pass
    
    return key['si']
    

trash_p = 'trash'

#main command line stuff
def cli():
    while True:
        valid = 0

        signal.signal(signal.SIGINT, Exit_gracefully)
        try:
            if 'libedit' in readline.__doc__:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")

            readline.set_completer(complete)
            readline.set_completer_delims(' ')
            cli = str(raw_input(PROMPT))
        except EOFError:
            bye()
        if hist_toggle == 1:
            hfile.write(cli + '\n')
        if 'key' in locals():
            pass
        else:
            key = get_sat_key(config)    

#This is not just a horrible way to take the commands and arguements, it's also shitty way to sanatize the input for one specific scenario

#I miss perl :(


        cli = re.sub('  ',' ', cli.rstrip())
            



##########################################################################################
# This starts the single trash commands
#######################################################################################
        buff = str({calendar.timegm(time.gmtime()) : cli})
        api_key = get_sat_key(config)
        #Write try statement here for error catching
        command = cli.split(' ', 1)[0]

        if command in ADNET:
            l_class = 'adnet'
        elif command in RHSAT:
            if key['client'] == '':
                print("You do not have a Redhat Satellite server in your ~/.trash.sh")
                command = ""
                cli = ""
            else:
                l_class = 'rhsat'
        elif command in DOMAIN:
            l_class = 'domain'
        elif command in CONTAINERS:
            l_class = 'dock_containers'
        elif command in SA:
            l_class = 'servers_action'
        elif command in LU:
            l_class = 'lin_utility'
        elif command in NB:
            l_class = 'node_balance'
        elif command in UCOMMANDS:
            l_class = 'ucommands'
        elif command in VMUTILS:
            if key['si'] == None:
                si = esxi_connect(key)
                    
                atexit.register(Disconnect, si)
            
            key['si'] = si 
            l_class = 'vmutils'
        else:
            l_class = ''
        
        
        if len(cli.split(' ')) > 0:
            if len(cli.split(' ')) ==6:
                command,arg_one,arg_two,arg_three,arg_four,arg_five = cli.split()
                if command in SIX:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four,arg_five)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==5:
                command,arg_one,arg_two,arg_three,arg_four = cli.split()
                if command in FIVE:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==4:
                command,arg_one,arg_two,arg_three = cli.split()
                if command in FOUR:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three)
                    print(result)
                    valid = 1

            if len(shlex.split(cli)) ==3:
                command,arg_one,arg_two = shlex.split(cli)
                if command in THREE:
                    command = command.replace("-", "_")
                    if l_class == 'vmutils':
                        api_key['vmarg'] = arg_one
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, si, arg_one, arg_two)
                    else:
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, arg_one, arg_two)
 
                    print(result)
                    valid = 1

            elif len(shlex.split(cli)) ==2:
                command,arguement = shlex.split(cli)
                if command in TWO:
                    command = command.replace("-", "_")
                    if l_class == 'vmutils':
                        api_key['vmarg'] = arguement
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, si)
                    else:
                        l_class = eval(l_class)
                        result = getattr(l_class, command)(api_key, arguement)
                    
                    print(result)
                    valid = 1
                
                else:
                    print("Invalid Arguements")

            else:
               if cli in ONE:
                    cli = cli.replace("-", "_")
                    
                    if l_class == 'vmutils':
                        l_class = eval(l_class)
                        result = getattr(l_class, cli)(api_key, si)
                        pprint(result)
                        valid = 1
                    else:    
                        l_class = eval(l_class)
                        result = getattr(l_class, cli)(api_key)
                        pprint(result)
                        valid = 1
               elif cli in HELPER:
                    if cli == "quit" or cli == "exit":
                        #hfile.write(buff)
                        hfile.close()
                        bye()
                    if cli == "version":
                        print(version())
                        valid = 1
                    if cli == "hidden":
                        print(hidden_menu())
                        valid = 1
                    if cli == "ls":
                        print(ls_menu())
                        valid = 1
                    if cli == "qotd":
                        print(qotd_menu())
                        valid = 1
                    if (cli == "help") or (cli == "?"):
                        print(help_menu())
                        valid = 1
                    if cli == "clear":
                        if ucommands.os_platform() == 'windows':
                            print(os.system('cls'))
                            valid = 1
                        if ucommands.os_platform() == 'nix':
                            #pprint(
                            os.system('clear')
                            valid = 1
               else:
                    print("Invalid Command")

    

        if valid == 0:
            print("Unrecoginized Command")


def help_menu():
####Why did I space the help like this, cause something something, then lazy
    help_var = """
(required) <optional>

If an arguement has spaces, use single quotes.


jump (destination) <variation on username> : go to another server, via the jump server
which (potential executable): find executables on the machine trash is running on

help,? : show commands and usage
quit, exit : leave the shell
clear : clear screen

ESX-API Commands
esx-get-hosts: get esx hosts
esx-get-registered-vms: get esx vms
esx-get-resource-pools: get esx resource pools
esx-get-datastores: get esx datastores
esx-get-vm-name (hostname): get vm object
esx-vm-device-info (vm-name): get info on vm
esx-check-tools (vm-name): check vm ware tools on vm
esx-get-vm-uuid (ip-of-vm): get uuid of vm
esx-list-datastores: List all datastores
esx-change-cd (vm-name) <iso>: change the iso of the vm, blank for blank
esx-create-from-ova (ova path): Create a VM from an OVA
esx-create-from-ovf (ovf path) (vmdk path): Create a VM from an OVF
esx-destroy-vm (bios-uuid): Destroy powered on VM


REDHAT SATELLITE API Commands
sat-list-users : lists satellite users
sat-get-api-call : get api calls for satellite
sat-get-version : satellite server version
sat-system-version : satellite system version
sat-list-all-groups: list all available groups
sat-list-systems (group) : list systems in a group
sat-system-group-audit: list all systems, and their assigned groups


LINODE Commands
linode-list : lists your linode servers
linode-create (DatacenterID) (PlanID) <PaymentTerm>: create Linode
linode-list-ip <linode_id> <IPaddress> : return JSON information about ip address and server 
avail-datacenters : lists available centers
avail-distributions : lists available distribution centers
nodebal-list : get list of lode balancers    
nodebal-config-list (id): get lode balancer specifics using id from list
nodebal-node-list (config id): get node list of a balancer
nodebal-create (DatacenterID): create node balancer

"""
    return(help_var)


def hidden_menu():
    hidden_var = """
(required) <optional>

Commands that have not quite reached maturity. Or otherwise don't make the cut.

ls: random insult return
qotd: random quote of the day
"""
    return(hidden_var)





def ls_menu():
    ls_messages=[]
    ls_messages.append("You know this isn't bash")
    ls_messages.append("You're just wasting time")
    ls_messages.append("Free Play")
    rando = random.randrange(0,3)
    return ls_messages[rando]


def qotd_menu():
    qotd_messages=[]
    qotd_messages.append("Don't let the Best, be the enemy of the Good.")
    qotd_messages.append("To understand recursion, you must first understand recursion.")
    qotd_messages.append("Always read JWZ's Blog, Always")
    qotd_messages.append("Use Vim. Do not stray the course")
    qotd_messages.append("Eliminate Tabs")
    rando = random.randrange(0,5)
    return qotd_messages[rando]


def version():
    version = pkg_resources.require("trash-shell")[0].version
    return version

def bye():
    exit()

if arg_count == 2:
    command = sys.argv[1]
#noauth is essentially for testing
    if command == "noauth":
        no_auth = 1
#history is to toggle writing a history file, there is currently no clean up so it is off by default
    if command == "history":
        hist_toggle = 1
    if command == "roulette":
        rando = random.randint(1, 3)
    if command == "extra":
        trash_p = config["default"][0]["prompt"]

                 

    if command == "sat-system-group-audit":
        api_key = get_sat_key(config)
        pprint(rhsat.sat_system_group_audit(api_key))
        valid = 1
        bye()
    if command == "sat-list-users":
        api_key = get_sat_key(config)
        pprint(rhsat.sat_list_users(api_key))
        valid = 1
        bye()
    if command == "sat-list-all-groups":
        api_key = get_sat_key(config)
        pprint(rhsat.sat_list_all_groups(api_key))
        valid = 1
        bye()
    if command == "sat-system-version":
        api_key = get_sat_key(config)
        pprint(rhsat.sat_system_version(api_key))
        valid = 1
        bye()
    if command == "sat-get-api-call":
        api_key = get_sat_key(config)
        pprint(rhsat.sat_get_api_call(api_key))
        valid = 1
        bye()
    if command == "esx-get-registered-vms":
        api_key = get_sat_key(config)
        key = api_key
        if key['si'] == None:
            si = esxi_connect(key)
            atexit.register(Disconnect, si)
            key['si'] = si 
        pprint(vmutils.esx_get_registered_vms(api_key, si))
        valid = 1
        bye()


PROMPT = trash_p + '> '

if no_auth == 1:
    api_key =0
else:
    api_key = get_sat_key(config)

####Again, shit way to do this, Here's hoping it's better in beta :)
    ##You know what, fuck you, it's fine
if arg_count == 3:
    command = sys.argv[1]
    arguement = sys.argv[2]
    if command == "which":
        print(ucommands.which(api_key, arguement))
        valid = 1
        bye()
    if command == "jump":
        print(ucommands.jump(api_key, arguement))
        valid = 1
        bye()
    if command == "esx-check-tools":
        api_key = get_sat_key(config)
        key = api_key
        if key['si'] == None:
            si = esxi_connect(key)
            atexit.register(Disconnect, si)
            key['si'] = si 
        api_key['vmarg'] = arguement
        print(vmutils.esx_check_tools(api_key, si))
        valid = 1
        bye()
    if command == "esx-vm-device-info":
        api_key = get_sat_key(config)
        key = api_key
        if key['si'] == None:
            si = esxi_connect(key)
            atexit.register(Disconnect, si)
            key['si'] = si 
        api_key['vmarg'] = arguement
        print(vmutils.esx_vm_device_info(api_key, si))
        valid = 1
        bye()



#if arg_count == 4:
#    command = sys.argv[1]
#    arg_one = sys.argv[2]
#    arg_two = sys.argv[3]
#
#
#    if command == "sat-list-systems-hosts-audit":
#        api_key = get_sat_key(config)
#        print(rhsat.sat_list_systems_hosts_audit(api_key, arg_one, arg_two))
#        valid = 1
#        bye()
#

 

if arg_count == 5:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5]

if arg_count == 6:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5] 






#######################################################################################
#
#######################################################################################
#
#######################################################################################
#
#######################################################################################
#
#######################################################################################    
#
#######################################################################################
