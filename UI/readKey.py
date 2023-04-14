
import serial.tools.list_ports
import serial
import serial
import time

class KeyReader():
    def __init__(self): 
        self.fileName = 'devicedata.txt'
        

    def readUID(self):
        try:
            f = open(self.fileName)
            key = f.read()
            return key
        except:
            print('file was not found. please try again')
       



     
    
    
