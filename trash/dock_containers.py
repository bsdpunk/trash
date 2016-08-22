from docker import Client

def dock_containers(api):
    cli = Client(base_url='tcp://'+api['docker-ip'] +':2375')
    return cli.containers()

def dock_commit(api):
    return 0

def dock_events(api):
    cli = Client(base_url='tcp://'+api['docker-ip'] +':2375')
    return cli.events()
    
