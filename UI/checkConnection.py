import platform
import os
import time

class Connection():
    def __init__(self):
        self.osType = platform.system().lower()
    
    def findConnectedDevices(self):
        if 'windows' in self.osType:
            devices = os.popen('powershell \"Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match \'^USB\' }\"').read()#basically os.system but saves output to a var
            # if 'nameOfMicroController' in devices: #then the device is plugged in
            if 1:
                time.sleep(2)
                return 1
            else:
                return 0
        else:
            pass
            #check mac and windows
