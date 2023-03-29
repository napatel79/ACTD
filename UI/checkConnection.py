import platform
import os

class Connection():
    def __init__(self):
        self.osType = platform.system().lower()
    
    def findConnectedDevices(self):
        if 'windows' in self.osType:
            devices = os.popen('powershell \"Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match \'^USB\' }\"').read()#basically os.system but saves output to a var

        else:
            devices = os.popen
conn = Connection()
conn.findConnectedDevices()