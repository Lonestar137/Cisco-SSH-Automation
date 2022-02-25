from Mass_push import Site
from decouple import config
import threading
from rich.console import Console

#concurrency
from concurrent.futures import ThreadPoolExecutor
from time import sleep


def singlemode():
    # Logs into devices one at a time, slowly, easier to read.
    USER=config('SSH_USER')
    PASSWORD=config('SSH_PASS')
    SECRET=config('ENABLE_SECRET')

    device = Site(USER, PASSWORD, SECRET)

    site1 = config('SITE1')
    site1_devices = config('SITE1_DEVICES', cast=lambda v: [s.strip() for s in v.split(' ')])

    #Open designated file and read line to string
    cmd_file = config('FILE')
    with open('commands/'+cmd_file, 'r') as file:
        cmd = file.read()

    print(cmd)
    console = Console()
    console.print('Run the above commands on each device? (y/n)', style='bold green')
    if input() == 'y':
        console.print('Running commands on devices...', style='bold yellow')
    else:
        console.print('Aborting...', style='bold red') 
        exit()
    
    device.Mass_push(site1_devices, cmd, site1)

def multimode():

    # Runs the jobs concurrently.  Meaning really fast multitasking.
    USER=config('SSH_USER')
    PASSWORD=config('SSH_PASS')
    SECRET=config('ENABLE_SECRET')

    device = Site(USER, PASSWORD, SECRET)

    site1 = config('SITE1')
    site1_devices = config('SITE1_DEVICES', cast=lambda v: [s.strip() for s in v.split(' ')])

    #Open designated file and read line to string
    cmd_file = config('FILE')
    with open('commands/'+cmd_file, 'r') as file:
        cmd = file.read()

    print(cmd)
    console = Console()
    console.print('Run the above commands on each device? (y/n)', style='bold green')
    if input() == 'y':
        console.print('Running commands on devices...', style='bold yellow')
    else:
        console.print('Aborting...', style='bold red') 
        exit()
    
    device.pool(site1_devices, cmd, site1)

if config('TYPE') == 'singlemode':
    singlemode()
elif config('TYPE') == 'multimode':
    multimode()
