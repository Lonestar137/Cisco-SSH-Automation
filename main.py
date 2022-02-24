from Mass_push import Site
from decouple import config
import getpass
import time
import threading
from rich.console import Console



USER=config('SSH_USER')
PASSWORD=config('SSH_PASS')
SECRET=config('ENABLE_SECRET')
site2=config('SITE2_ENABLED', cast=bool)

device = Site(USER, PASSWORD, SECRET)
#device.Mass_push([48], 'sh run | i hostname', '10.251.11')

site1 = config('SITE1')
site1_devices = config('SITE1_DEVICES', cast=lambda v: [s.strip() for s in v.split(' ')])

if site2: 
    site2 = config('SITE2')
    site2_devices = config('SITE2_DEVICES', cast=lambda v: [s.strip() for s in v.split(' ')])


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


thread1 = threading.Thread(target=device.Mass_push, args=(site1_devices, cmd, site1))
thread1.start()

if site2:
    thread2 = threading.Thread(target=device.Mass_push, args=(site2_devices, cmd, site2))
    thread2.start()
