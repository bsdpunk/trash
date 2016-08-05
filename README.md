# Trash
Trash is a shell I made that does esxi, and redhat stuff.
It's garbage.


## Description
You can use trash to manipulate the API's for ESXi and RedHat Satelite Server.


## Usage

beastietools with no arguements drops you into the shell allowing you to use tab completion:
```bash
beastietools> 
arp    extip  ls     quit   
beastietools> extip 
Successfully discovered 1 services:
  Device: Netgear CG3000DCR
    External IP address: 68.52.132.49
beastietools> quit
```

You may also use arguements if you already know what you want to do or if you want to script:
```bash
dusty@xor:~$ beastietools extip
Successfully discovered 1 services:
  Device: Netgear CG3000DCR
    External IP address: 68.52.132.49
```

## Installation

You can do a local install by downloading this repo then running the install:

```bash
git clone https://github.com/bsdpunk/trash
cd trash
sudo python setup.py install
```

Or you can do a non root / local install:

```bash
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user
pip install pyVmomi --user
python setup.py --user install
```

## Some things you can do with Trash
```bash
trash> help

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

REDHAT SATELLITE API Commands
sat-list-users : lists satellite users
sat-get-api-call : get api calls for satellite
sat-get-version : satellite server version
sat-system-version : satellite system version
sat-list-all-groups: list all available groups
sat-list-systems (group) : list systems in a group
sat-list-systems-hosts (group) : list hosts and roles of system in a group
sat-list-systems-hosts-audit (group) (role) : list all sytems in a group, not in role X(1-7)
sat-system-group-audit: list all systems, and their assigned groups
```
