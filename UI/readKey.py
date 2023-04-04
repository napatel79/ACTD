
import serial.tools.list_ports
import serial
import serial
import time

# Get a list of available COM ports
ports = list(serial.tools.list_ports.comports())

# Check if a specific device is connected
device_name = "Arduino"
port_name = None
for port in ports:
    if device_name in port.description:
        port_name = port.device
        print("Found", device_name, "on", port_name)
        break


# Connect to the device and print any received data
# Change the following values to match your serial port settings
serial_port ='COM3'
baud_rate = 9600
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




    
# port = 'COM3'
# #arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
# #def write_read(x):
# #    arduino.write(bytes(x, 'utf-8'))
# #    time.sleep(0.05)
# #    data = arduino.readline()
# #    return data
# #while True:
# #    num = input(">") # Taking input from user
# #    value = write_read(num)
# #    print(port + " " + str(value).replace("newline", '\n')[2:-1]) # printing the value
    
    