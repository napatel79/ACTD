import platform
import os

class Connection():
    def __init__(self):
        self.osType = platform.platform()
    
    def findConnectedDevices(self):
        if self.osType.contains('windows'):
            os.system('Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }')