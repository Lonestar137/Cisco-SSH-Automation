from netmiko import ConnectHandler
import getpass
import time
from rich.console import Console

from concurrent.futures import ThreadPoolExecutor
from time import sleep



class Site:
    
    def __init__(self, username, password, secret):
        #Initialize connection
        self.username = username
        self.password = password
        self.secret = secret
        self.ip=''
        self.console = Console()

    def Connect(self, ip=None):
        #Connect to a device.
        if self.ip == '' and ip == None:
            self.ip = input('Enter an IP to connect: ')
        
        if ip != None:
            # For multithreading
            Device = {
                    "ip": ip,
                    "username": self.username,
                    "password": self.password,
                    "secret": self.secret,
                    "device_type": "cisco_ios"
                    }
            return ConnectHandler(**Device)

        else:
            self.Device = {
                    "ip": self.ip,
                    "username": self.username,
                    "password": self.password,
                    "secret": self.secret,
                    "device_type": "cisco_ios"
                    }
            return ConnectHandler(**self.Device)
        

    def Enter_cli(self, ip=None):
        if ip != None:
            self.ip == ip

        if self.ip == '':
            self.ip = input('Enter an ip to connect:')
        
        ssh = self.Connect()
        ssh.enable()
        while True:
            self.cmd = input(ssh.find_prompt())
            if self.cmd == 'exit':
                ssh.disconnect()
                print('Session ended')
                break
            elif self.cmd == '':
                pass
            elif self.cmd.find('sh') != -1 and ssh.check_enable_mode() == True:
                print('send_cmd')
                print(ssh.send_command(self.cmd))
            else:
                print('write_channel')
                ssh.write_channel(self.cmd)

    def Mass_push(self, devices: list, cmds: str, network_ip=None):
        self.devices = devices
        self.cmds = cmds

        #List of device IP's is passed
        counter=0
        if network_ip == None:
            network_ip = input('Enter the network IP for the site: ')

        total_output=''
        #Actually pushes the CMDs.
        for i in self.devices:
            self.ip = network_ip+'.'+str(i)
            self.console.print('Connecting to ' + self.ip, style='green')
            try:
                ssh = self.Connect()
            except:
                #If fail to connect, then skip
                self.console.print(self.ip+' failed to connect.', style='red')
                continue

            ssh.enable()
            for line in self.cmds.split('\n'):
                if line.find('sh') != -1 and ssh.check_enable_mode() == True:
                    #TODO: Split the line with the sh command to prevent errors, i.e. enter conf mode before the show command it won't show.
                    self.response=str(ssh.send_command(line))
                    print(self.response)#Necessary for unit test
                    total_output+='\ncurrent: '+self.ip+'\n'+self.response
                else: 
                    ssh.write_channel(line)


            ssh.disconnect()
        return total_output

    def setDevices(self, devices: list, cmds: str, network_ip: str):
        self.devices=[]
        for i in devices:
            self.devices.append(network_ip+'.'+str(i))

        return self.devices

    def push(self, ip: str, cmds: str):
        total_output=''
        #Actually pushes the CMDs.
        self.console.print('Connecting to ' + ip, style='green')
        try:
            ssh = self.Connect(ip)
        except:
            #If fail to connect, then skip
            self.console.print(self.ip+' failed to connect.', style='red')
            return 0

        ssh.enable()
        for line in cmds.split('\n'):
            if line.find('sh') != -1 and ssh.check_enable_mode() == True:
                #TODO: Split the line with the sh command to prevent errors, i.e. enter conf mode before the show command it won't show.
                self.response=str(ssh.send_command(line))
                self.console.print(ip+' response: ', style='green')
                print(self.response)#Necessary for unit test
                total_output+='\ncurrent: '+ip+'\n'+self.response
            else: 
                ssh.write_channel(line)


        ssh.disconnect()
        return total_output


    def pool(self, devices, cmds, network_ip):

        self.setDevices(devices, cmds, network_ip)
        #self.push()
        #Concurrency thread pool initialization
        executor = ThreadPoolExecutor(5) # 5 threads in pool
        for ip in self.devices:
            future = executor.submit(self.push, ip, cmds)

        #future.done() #returns False if still working on tasks
        return future.result() #prints out the result of the .submit function (total_output)


if __name__ == '__main__':
    from decouple import config
    def main():
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

    main()

