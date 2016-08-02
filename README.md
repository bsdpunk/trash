-----
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user
pip install pyVmomi --user
python setup.py --user install


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

