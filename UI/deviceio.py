# -*- coding: utf-8 -*-


import serial.tools.list_ports
import serial
import time
import os
from os.path import exists
from os.path import relpath
from os import makedirs
import asyncio


# Get a list of available COM ports
ports = list(serial.tools.list_ports.comports())

# Check if a specific device is connected
device_name = "Silicon Labs CP210x USB to UART Bridge"
serial_port ='COM5'
for port in ports:
    print("Found", port.device, "on", port.description)
    if device_name in port.description:
        serial_port = port.device
        print("Found", device_name, "on", serial_port)
        break


# Connect to the device and print any received data
# Change the following values to match your serial port settings
# serial_port ='COM5'
baud_rate = 115200
if os.path.exists("deviceid.txt"):
  os.remove("deviceid.txt")
file  = open("temp.txt", "a")
while True:
    try:
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Serial port {serial_port} opened successfully.")
        while True:
            try:
                if ser.in_waiting:
                    data = ser.readline().decode('utf-8').rstrip()
                    if(len(data) < 32 and len(data) > 0):
                        file.close()
                        if(data != "deviceid" and exists("deviceid.txt")):
                            deviceidfile = open("deviceid.txt", "r")
                            guid = deviceidfile.read()[:-2]
                            #if not os.path.exists(relpath(guid)):
                            #    makedirs(relpath(guid))
                            file  = open(relpath( data + ".txt"), "w")#guid + "/" +
                        else:
                            file  = open(data + ".txt", "w")
                        print("logging to " + data)
                    else:
                        file.write(data + "\n")
                        print(f"Received data: {data}")
            except serial.serialutil.SerialException:
                time.sleep(1)
                break
    except serial.serialutil.SerialException:
        print(f"Serial port {serial_port} not available. Waiting for device...")
        time.sleep(1)




    

#arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
#def write_read(x):
#    arduino.write(bytes(x, 'utf-8'))
#    time.sleep(0.05)
#    data = arduino.readline()
#    return data
#while True:
#    num = input(">") # Taking input from user
#    value = write_read(num)
#    print(port + " " + str(value).replace("newline", '\n')[2:-1]) # printing the value
    
    