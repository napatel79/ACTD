import tkinter
from tkinter import *
import customtkinter
import window
from window import *
import time
import checkConnection
from checkConnection import Connection
import readKey
from readKey import KeyReader
import requests
import uuid
import json
from datetime import datetime, timezone

class MainWindow(Window):

    def __init__(self):
        super().__init__()
        self.conn = Connection()
        self.keyObj = KeyReader()
        self.place_string('ACTD')
        self.button = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, command=self.wait_for_connection, fg_color=("gray75", "blue"), bg_color='gray75')
        self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        
    def clear_screen(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.configure(fg_color='gray75')
        
        
    def place_string(self, text, buttonExists=False, buttonText='', buttonCmd=None):
        text_var = tkinter.StringVar(value=text)
        self.label = customtkinter.CTkLabel(master=self,
                               textvariable=text_var,
                               width=self.width,
                               height=self.height,
                               fg_color=("black", "gray75"),
                               bg_color=("black", "gray75"),
                               text_color='black',
                               corner_radius=8)
        self.label.configure(font=('Helvatical bold',50))
        self.label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.update()

            
        
        
    def wait_for_connection(self):
        strVal = 'Please Plug in your Tracing Device. Once Connected Press the Button Below'
        self.place_string(strVal)
        
        button = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, command=self.checkDeviceConnection, fg_color=("gray75", "blue"), bg_color='gray75')
        button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)


    def checkDeviceConnection(self):
        strVal = 'Checking Connection. Please Wait'
        self.place_string(strVal) 
        self.after(1000, self.didConnect)#TODO:change this to 6 sec so 6000
        
        

    def didConnect(self):
        if self.conn.findConnectedDevices(): #so it was connected
            #get the stored UID first
            self.storedUID = self.getStoredUID()
            self.checkUpdateScreen()
        else: #go to check device connection
            text_var = 'No Tracing Device Was Connected Please Reconnect the Tracing Device'
            self.place_string(text_var)
            self.after(3000, self.checkDeviceConnection)


    def getStoredUID(self):
        
        return self.keyObj.readUID()
        

    def checkUpdateScreen(self):
        self.clear_screen()
        
        frame = customtkinter.CTkFrame(master=self,width=self.width, height=self.height,corner_radius=10, bg_color='gray75', fg_color='gray75')
        # frame.pack(fill=BOTH, expand=YES, anchor='center')
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER,)
        text_var = tkinter.StringVar(value="Check")
        label = customtkinter.CTkLabel(master=frame, textvariable=text_var, fg_color="gray75",text_color='black',corner_radius=8)
        label.configure(font=('Helvatical bold',60))
        label.grid(row=0, column=0, padx=(0, 10))
        button1 = customtkinter.CTkButton(master=frame, text='Enter',corner_radius=30, fg_color=("gray75", "blue"), command=self.checkInfectionStatus)
        button1.grid(row=1,column=0)
        
        text_var2 = tkinter.StringVar(value="Update")
        label2 = customtkinter.CTkLabel(master=frame, textvariable=text_var2, fg_color="gray75",text_color='black',corner_radius=8)
        label2.configure(font=('Helvatical bold',60))
        label2.grid(row=0, column=2)
        button2 = customtkinter.CTkButton(master=frame, text='Enter',corner_radius=30, fg_color=("gray75", "blue"), command=self.updateInfectionStatus)
        button2.grid(row=1,column=2)
        
        self.update()

    
    def checkInfectionStatus(self):
        uuid1 = '3d6913d1-4887-4384-a3a9-a1e906b25541'
        uuid2 = '248d08d9-df6c-4e89-9462-5e5df4573422'
        uuid3 = '6fbdae85-93f9-4ac8-a245-2978edc05db3'
        uuid4 = 'dd6131f9-82b2-4f83-8d32-d3ccd290f694'
        uuid5 = '0928bf94-b7be-4127-b9dd-62fbb5adaaa5'
        uuid6 = 'd7de87a7-cc71-4464-bdda-3d47fc0b22e6'
        uuid7 = '082c155b-3e1e-4745-8d96-c11b43541ed7'
        uuid8 = '8196b759-a38a-468d-9889-340451bbd888'
        

        #TODO: send self.storedUID to the db
        PATH = 'http://34.29.55.201:9090'
        
        

        try :
            self.clear_screen()
            r = requests.get(PATH + '/check', json={
                "UUID": str(uuid4),
            })
            if r.status_code == 200: #TODO: check the status of the infection and if true say quarantine and if false say you are healthy
                self.place_string(str(r.json()))
            else:   
                self.place_string('There was an error in the server. Please Try Again.')         
        except:
            self.place_string('There was an error in the server. Please Try Again.')
            # print(f"Status Code: {r.status_code, r.content}")
        finally:
            button = customtkinter.CTkButton(master=self, text='Home',corner_radius=30, command=self.checkUpdateScreen, fg_color=("gray75", "blue"), bg_color='gray75')
            button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)


    def updateInfectionStatus(self):
        uuid1 = '3d6913d1-4887-4384-a3a9-a1e906b25541'
        uuid2 = '248d08d9-df6c-4e89-9462-5e5df4573422'
        uuid3 = '6fbdae85-93f9-4ac8-a245-2978edc05db3'
        uuid4 = 'dd6131f9-82b2-4f83-8d32-d3ccd290f694'
        uuid5 = '0928bf94-b7be-4127-b9dd-62fbb5adaaa5'
        uuid6 = 'd7de87a7-cc71-4464-bdda-3d47fc0b22e6'
        uuid7 = '082c155b-3e1e-4745-8d96-c11b43541ed7'
        uuid8 = '8196b759-a38a-468d-9889-340451bbd888'
        PATH = 'http://34.29.55.201:9090'  



            
        try:
            r = requests.post(PATH + '/insert', json={
                "UUID": str(self.storedUID), #TODO:replace this with self.uuid or the stored rom key
                "UUID2": str(uuid4),
                "Infected": True,
                "ContactDate": str(datetime.utcnow())
            })
            if r.status_code == 200:
                self.place_string('Your status has been updated successfully. If infected, please notify your local health center and quarantine properly.')
            else:   
                self.place_string('There was an error in the server. Please Try Again.') 
            # print(f"Status Code: {r.status_code}, Response: {r.json()}")
        except:
            self.place_string('There was an error in the server. Please Try Again.') 
            # print(f"Status Code: {r.status_code, r.content}")
        finally:
            button = customtkinter.CTkButton(master=self, text='Home',corner_radius=30, command=self.checkUpdateScreen, fg_color=("gray75", "blue"), bg_color='gray75')
            button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        


    def runMainWindow(self):
        self.mainloop()



if __name__ == '__main__':
    ui = MainWindow()
    # ui.wait_for_connection()
    ui.runMainWindow()
    
    #TODO: make code that runs in the background that does an insert statment each of the uuids it
    #stores in the filesystem






