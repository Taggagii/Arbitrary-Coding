from psutil import process_iter, wait_procs
from time import sleep

def find_proper_name(similar_name): # for debugging purposes
    '''
        returns a list of all processes whose names contain [similar_name]
    '''
    ls = set()
    for i in process_iter(['name']):
        if similar_name.lower() in i.info['name'].lower():
            ls.add(i.info["name"])
    return ls


def find_procs_by_name(names):
    '''
        returns a list of all processes whose names are contained within [names]
    '''
    ls = []
    for i in process_iter(['name']):
        if i.info['name'] in names:
            ls.append(i)
    return ls

def on_terminate(proc):
    print(f"Process {proc.name} terminated with exit code {proc.returncode}");


forbidden_processes = ["chrome.exe", "Discord.exe"]

while True:
    procs = find_procs_by_name(forbidden_processes)
    
    for p in procs:
        p.terminate()

    gone, alive = wait_procs(procs, timeout = 3, callback = on_terminate) # todo : make sure timeout is a good value for this application

    for p in alive:
        p.kill()

    sleep(5)
