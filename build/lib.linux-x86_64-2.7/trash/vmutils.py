from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl
from pyVmomi import vim
import time
import atexit
import argparse
import datetime
import json
def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
            print out
        else:
            out = '%s completed successfully.' % actionName
            print out
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        raise task.info.error
        print out

    return task.info.result



def _get_obj(content, vimtype, name):
    """
    Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def _get_all_objs(content, vimtype):
    """
    Get all the vsphere objects associated with a given type
    """
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        obj.update({c: c.name})
    return obj


def login_in_guest(username, password):
    return vim.vm.guest.NamePasswordAuthentication(username=username,password=password)

def start_process(si, vm, auth, program_path, args=None, env=None, cwd=None):
    cmdspec = vim.vm.guest.ProcessManager.ProgramSpec(arguments=args, programPath=program_path, envVariables=env, workingDirectory=cwd)
    cmdpid = si.content.guestOperationsManager.processManager.StartProgramInGuest(vm=vm, auth=auth, spec=cmdspec)
    return cmdpid

def is_ready(vm):

    while True:
        system_ready = vm.guest.guestOperationsReady
        system_state = vm.guest.guestState
        system_uptime = vm.summary.quickStats.uptimeSeconds
        if system_ready and system_state == 'running' and system_uptime > 90:
            break
        time.sleep(10)

def esx_get_hosts(key, si):
    content = si.RetrieveContent()
    return _get_all_objs(content, [vim.HostSystem])

def print_vmwareware_tools_status(vm):
    print _columns_four.format(vm.name,
                               vm.guest.toolsRunningStatus,
                               vm.guest.toolsVersion,
                               vm.guest.toolsVersionStatus2)



_columns_four = "{0:<20} {1:<30} {2:<30} {3:<20}"

def esx_get_vm_name(key, si):
    """
    Find a virtual machine by it's name and return it
    """
    return _get_obj(si.RetrieveContent(), [vim.VirtualMachine], key['vmarg'])

def esx_check_tools(key, si):
    vm_obj = esx_get_vm_name(key, si)
    if vm_obj:
        print _columns_four.format('Name', 'Status',
                                       'Version', 'Version Status')
        print_vmwareware_tools_status(vm_obj)
    else:
        print "VM not found"



#def esx_vm_devices(key, si):
    
 #   for dev in vm_obj.config.hardware.device:
#        if isinstance(dev, vim.vm.device.VirtualCdrom) \
#                and dev.deviceInfo.label == cdrom_label:
 #           virtual_cdrom_device = dev


def esx_change_cd(key, si, full_path_to_iso=None, cdrom_number=1):
    """ Updates Virtual Machine CD/DVD backend device
    :param vm_obj: virtual machine object vim.VirtualMachine
    :param cdrom_number: CD/DVD drive unit number
    :param si: Service Instance
    :param full_path_to_iso: Full path to iso
    :return: True or false in case of success or error
    """
    vm_obj = esx_get_vm_name(key, si)
    cdrom_prefix_label = 'CD/DVD drive '
    cdrom_label = cdrom_prefix_label + str(cdrom_number)
    virtual_cdrom_device = None
    for dev in vm_obj.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualCdrom) \
                and dev.deviceInfo.label == cdrom_label:
            virtual_cdrom_device = dev

    if not virtual_cdrom_device:
        raise RuntimeError('Virtual {} could not '
                           'be found.'.format(cdrom_label))

    virtual_cd_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_cd_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_cd_spec.device = vim.vm.device.VirtualCdrom()
    #print(virtual_cd_spec.device.backing) 
    virtual_cd_spec.device.controllerKey = virtual_cdrom_device.controllerKey
    virtual_cd_spec.device.key = virtual_cdrom_device.key
    virtual_cd_spec.device.connectable = \
        vim.vm.device.VirtualDevice.ConnectInfo()
    # if full_path_to_iso is provided it will mount the iso
    if full_path_to_iso:
        virtual_cd_spec.device.backing = \
            vim.vm.device.VirtualCdrom.IsoBackingInfo()
        virtual_cd_spec.device.backing.fileName = full_path_to_iso
        virtual_cd_spec.device.connectable.connected = True
        virtual_cd_spec.device.connectable.startConnected = True
    else:
        virtual_cd_spec.device.backing = \
            vim.vm.device.VirtualCdrom.RemotePassthroughBackingInfo()
    # Allowing guest control
    virtual_cd_spec.device.connectable.allowGuestControl = True

    dev_changes = []
    dev_changes.append(virtual_cd_spec)
    spec = vim.vm.ConfigSpec()
    #print(dev_changes)
    spec.deviceChange = dev_changes
    task = vm_obj.ReconfigVM_Task(spec=spec)
    wait_for_task(task, si)
    return True


def esx_get_vm_uuid(key, si):
    """
    Find a virtual machine by it's name and return it
    """
    search_index = si.content.searchIndex
    print(search_index)
    vm = search_index.FindByIp(None, key['vmarg'], True)

    return vm.summary.config.uuid





def get_host_by_name(si, name):
    """
    Find a virtual machine by it's name and return it
    """
    return _get_obj(si.RetrieveContent(), [vim.HostSystem], name)

def get_resource_pool(si, name):
    """
    Find a virtual machine by it's name and return it
    """
    return _get_obj(si.RetrieveContent(), [vim.ResourcePool], name)

def esx_get_resource_pools(key, si):
    """
    Returns all resource pools
    """
    return _get_all_objs(si.RetrieveContent(), [vim.ResourcePool])

def esx_get_datastores(key, si):
    """
    Returns all datastores
    """
    return _get_all_objs(si.RetrieveContent(), [vim.Datastore])

#def esx_get_hosts(key, si):
    """
    Returns all hosts
    """
    #return _get_all_objs(key['content'], [vim.VirtualMachine])

def get_datacenters(si):
    """
    Returns all datacenters
    """
    return _get_all_objs(si.RetrieveContent(), [vim.Datacenter])

def esx_get_registered_vms(key, si):
    """
    Returns all vms
    """
    return _get_all_objs(si.RetrieveContent(), [vim.VirtualMachine])


def ps_exec(key, si, subp):

    vm = esx_get_vm_name()

    creds = vim.vm.guest.NamePasswordAuthentication(
        username=subp['user'], password=subp['pwd']
    )

    try:
        pm = content.guestOperationsManager.processManager

        ps = vim.vm.guest.ProcessManager.ProgramSpec(
            programPath=subp['exec'],
            arguments=subp['args']
        )
        res = pm.StartProgramInGuest(vm, creds, ps)



    except IOError, e:
        print e

    return 0




def esx_list_datastores(key, si):
    #atexit.register(connect.Disconnect, si)
    content = si.RetrieveContent()
    # Search for all ESXi hosts
    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.HostSystem],
                                                        True)
    args =get_args(key)
    print(args) 
    esxi_hosts = objview.view
    objview.Destroy()

    datastores = {}
    for esxi_host in esxi_hosts:
        if not args.json:
            print("{}\t{}\t\n".format("ESXi Host:    ", esxi_host.name))

            # All Filesystems on ESXi host
        storage_system = esxi_host.configManager.storageSystem
        host_file_sys_vol_mount_info = \
                storage_system.fileSystemVolumeInfo.mountInfo

        datastore_dict = {}
            # Map all filesystems
        for host_mount_info in host_file_sys_vol_mount_info:
                # Extract only VMFS volumes
            if host_mount_info.volume.type == "VMFS":

                extents = host_mount_info.volume.extent
                if not args.json:
                    print_fs(host_mount_info)
                else:
                    datastore_details = {
                        'uuid': host_mount_info.volume.uuid,
                        'capacity': host_mount_info.volume.capacity,
                        'vmfs_version': host_mount_info.volume.version,
                        'local': host_mount_info.volume.local,
                        'ssd': host_mount_info.volume.ssd
                    }

                extent_arr = []
                extent_count = 0
                for extent in extents:
                    if not args.json:
                        print("{}\t{}\t".format(
                            "Extent[" + str(extent_count) + "]:",
                            extent.diskName))
                        extent_count += 1
                    else:
                            # create an array of the devices backing the given
                            # datastore
                        extent_arr.append(extent.diskName)
                            # add the extent array to the datastore info
                        datastore_details['extents'] = extent_arr
                            # associate datastore details with datastore name
                        datastore_dict[host_mount_info.volume.name] = \
                            datastore_details
                if not args.json:
                    print

            # associate ESXi host with the datastore it sees
        datastores[esxi_host.name] = datastore_dict

    if args.json:
        print(json.dumps(datastores))

    return 0


def get_args(key):
    """
   Supports the command-line arguments listed below.
   """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=False, action='store',
                        help='Remote host to connect to', default="key['vcenter']")
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=False, action='store',
                        help='User name to use when connecting to host', default="key['username']")
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use when connecting to host', default="key['password']")
    parser.add_argument('-j', '--json', default=False, action='store_true',
                        help='Output to JSON')
    parser.add_argument('-S', '--disable_ssl_verification',
                        required=False,
                        action='store_true',
                        help='Disable ssl host certificate verification')
    args = parser.parse_args()
    return args


def print_fs(host_fs):
    """
    Prints the host file system volume info
    :param host_fs:
    :return:
    """
    print("{}\t{}\t".format("Datastore:     ", host_fs.volume.name))
    print("{}\t{}\t".format("UUID:          ", host_fs.volume.uuid))
    print("{}\t{}\t".format("Capacity:      ", sizeof_fmt(
        host_fs.volume.capacity)))
    print("{}\t{}\t".format("VMFS Version:  ", host_fs.volume.version))
    print("{}\t{}\t".format("Is Local VMFS: ", host_fs.volume.local))
    print("{}\t{}\t".format("SSD:           ", host_fs.volume.ssd))


def sizeof_fmt(num):
    """
    Returns the human readable version of a file size
    :param num:
    :return:
    """
    for item in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')



def esx_perf_query(key, si):



    content = si.RetrieveContent()
    search_index = si.content.searchIndex
    #print(search_index)
    host = vim.HostSystem('host-27615')

    perfManager = content.perfManager
    metricId = vim.PerformanceManager.MetricId(counterId=6, instance="*")
    startTime = datetime.datetime.now() - datetime.timedelta(hours=1)
    endTime = datetime.datetime.now()

    query = vim.PerformanceManager.QuerySpec(maxSample=1,
                                                 entity=host,
                                                 metricId=[metricId],
                                                 startTime=startTime,
                                                 endTime=endTime)

    print(perfManager.QueryPerf(querySpec=[query]))

    return 




def esx_vm_device_info(key, si):


    search_index = si.content.searchIndex

    # without exception find managed objects using durable identifiers that the
    # search index can find easily. This is much better than caching information
    # that is non-durable and potentially buggy.

    vm = esx_get_vm_name(key, si)
    print("Found Virtual Machine")
    print("=====================")
    details = {'name': vm.summary.config.name,
               'instance UUID': vm.summary.config.instanceUuid,
               'bios UUID': vm.summary.config.uuid,
               'path to VM': vm.summary.config.vmPathName,
               'guest OS id': vm.summary.config.guestId,
               'guest OS name': vm.summary.config.guestFullName,
               'host name': vm.runtime.host.name,
               'last booted timestamp': vm.runtime.bootTime}
    
    for name, value in details.items():
        print("  {0:{width}{base}}: {1}".format(name, value, width=25, base='s'))

    print("  Devices:")
    print("  --------")
    for device in vm.config.hardware.device:
        # diving into each device, we pull out a few interesting bits
        dev_details = {'key': device.key,
                       'summary': device.deviceInfo.summary,
                       'device type': type(device).__name__,
                       'backing type': type(device.backing).__name__}

        print("  label: {0}".format(device.deviceInfo.label))
        print("  ------------------")
        for name, value in dev_details.items():
            print("    {0:{width}{base}}: {1}".format(name, value,
                                                      width=15, base='s'))

        if device.backing is None:
            continue

        # the following is a bit of a hack, but it lets us build a summary
        # without making many assumptions about the backing type, if the
        # backing type has a file name we *know* it's sitting on a datastore
        # and will have to have all of the following attributes.
        if hasattr(device.backing, 'fileName'):
                datastore = device.backing.datastore
                if datastore:
                    print("    datastore")
                    print("        name: {0}".format(datastore.name))
                    # there may be multiple hosts, the host property
                    # is a host mount info type not a host system type
                    # but we can navigate to the host system from there
                    for host_mount in datastore.host:
                        host_system = host_mount.key
                        print("        host: {0}".format(host_system.name))
                    print("        summary")
                    summary = {'capacity': datastore.summary.capacity,
                               'freeSpace': datastore.summary.freeSpace,
                               'file system': datastore.summary.type,
                               'url': datastore.summary.url}
                    for key, val in summary.items():
                        print("            {0}: {1}".format(key, val))
                print("    fileName: {0}".format(device.backing.fileName))
                print("    device ID: {0}".format(device.backing.backingObjectId))

        print("  ------------------")

    print("=====================")

def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj



def create_from_iso(key, si):
#Untested


        content = si.RetrieveContent()

        vm_name = key['vmarg']
        vm = get_obj(content, [vim.VirtualMachine], vm_name)

        print "Attaching iso to CD drive of ", vm_name
        cdspec = None
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualCdrom):
                cdspec = vim.vm.device.VirtualDeviceSpec()
                cdspec.device = device
                cdspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit

                cdspec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
                for datastore in vm.datastore:
                    cdspec.device.backing.datastore = datastore
                    break
                cdspec.device.backing.fileName = key['iso_path']
                cdspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
                cdspec.device.connectable.startConnected = True
                cdspec.device.connectable.allowGuestControl = True

        vmconf = vim.vm.ConfigSpec()
        vmconf.deviceChange = [cdspec]
        print "Giving first priority for CDrom Device in boot order"
        vmconf.bootOptions = vim.vm.BootOptions(bootOrder=[vim.vm.BootOptions.BootableCdromDevice()])
        task = vm.ReconfigVM_Task(vmconf)

        wait_for_task(task, si)

        print "Successfully changed boot order priority and attached iso to the CD drive of VM ", vm_name

        print "Power On the VM to boot from iso"
        vm.PowerOnVM_Task() 




def virtual_interface(key, si):

    
        content = si.RetrieveContent()
        vm = esx_get_vm_name(key['vmarg'])
        # This code is for changing only one Interface. For multiple Interface
        # Iterate through a loop of network names.
        device_change = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                nicspec = vim.vm.device.VirtualDeviceSpec()
                nicspec.operation = \
                    vim.vm.device.VirtualDeviceSpec.Operation.edit
                nicspec.device = device
                nicspec.device.wakeOnLanEnabled = True

                if not args.is_VDS:
                    nicspec.device.backing = \
                        vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                    nicspec.device.backing.network = \
                        get_obj(content, [vim.Network], args.network_name)
                    nicspec.device.backing.deviceName = args.network_name
                else:
                    network = get_obj(content,
                                      [vim.dvs.DistributedVirtualPortgroup],
                                      args.network_name)
                    dvs_port_connection = vim.dvs.PortConnection()
                    dvs_port_connection.portgroupKey = network.key
                    dvs_port_connection.switchUuid = \
                        network.config.distributedVirtualSwitch.uuid
                    nicspec.device.backing = \
                        vim.vm.device.VirtualEthernetCard. \
                        DistributedVirtualPortBackingInfo()
                    nicspec.device.backing.port = dvs_port_connection

                nicspec.device.connectable = \
                    vim.vm.device.VirtualDevice.ConnectInfo()
                nicspec.device.connectable.startConnected = True
                nicspec.device.connectable.allowGuestControl = True
                device_change.append(nicspec)
                break

        config_spec = vim.vm.ConfigSpec(deviceChange=device_change)
        task = vm.ReconfigVM_Task(config_spec)
        tasks.wait_for_tasks(task, si)
        print "Successfully changed network"
