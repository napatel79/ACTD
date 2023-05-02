
import serial.tools.list_ports
import serial
import serial
import time

class KeyReader():
    def __init__(self): 
        self.fileName = 'deviceid.txt'
        self.recievedFilename = 'received.txt'
        self.storedUID = 'temp-uid'
        self.receivedUID = []

    def readUID(self):
        try:
            f = open(self.fileName)
            key = f.read()
            key = key.strip()
            self.storedUID = key
        except:
            print('stored file was not found. please try again')
    
    def readReceived(self):
        try:
            f = open(self.recievedFilename)
            self.receivedUID.append(f.readline().strip())
        except:
            print('received file was not found. please try again')

    
    
       



     
    
    