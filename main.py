from Mass_push import Site
from dotenv import dotenv_values
import getpass
import time
import threading



credentials = dotenv_values('creds.env')
USER=credentials['USER']
PASSWORD=credentials['PASSWORD']
SECRET=credentials['SECRET']

device = Site(USER, PASSWORD, SECRET)
#device.Mass_push([48], 'sh run | i hostname', '10.251.11')

thread1 = threading.Thread(target=device.Mass_push, args=([48], 'sh run | i hostname', '10.251.11'))
thread1.start()