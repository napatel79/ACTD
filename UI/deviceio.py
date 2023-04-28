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


# Check if a specific device is connected
device_name = "Silicon Labs CP210x USB to UART Bridge"
serial_port ='COM1'
guid = "bebdac3f-3c33-44b4-b5bb-c90e76363475"
guid = "00000000-0000-0000-0000-000000000000"
olddata = "temp.txt"
data = "temp.txt"
# Connect to the device and print any received data
# Change the following values to match your serial port settings
# serial_port ='COM5'
baud_rate = 115200

file  = open("temp.txt", "a")
while True:
    try:
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Serial port {serial_port} opened successfully.")
        while True:
            try:
                if ser.in_waiting:
                    olddata = data
                    data = ser.readline().decode('utf-8').rstrip()
                    if ("deviceid" in olddata):
                        guid = data[:-2]
                    if("flush" in data):
                        file.close()
                        file  = open("temp.txt", "a")
                    if(len(data) < 32 and len(data) > 0):
                        file.close()
                        if not os.path.exists(relpath(guid)):
                            makedirs(relpath(guid))
                        file  = open(relpath(guid + "/" + data + ".txt"), "w")
                        print("logging to " + file.name)
                    else:
                        file.write(data + "\n")
                        print(f"Received data: {data} logged to {file.name}")
            except serial.serialutil.SerialException:
                time.sleep(1)
                break

    except serial.serialutil.SerialException:
        print(f"Serial port {serial_port} not available. Waiting for device...")
        time.sleep(1)
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            print("Found", port.device, "on", port.description)
            if device_name in port.description:
                serial_port = port.device
                print("Found", device_name, "on", serial_port)
                break
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
    
    