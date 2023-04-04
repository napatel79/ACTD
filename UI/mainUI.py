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

class MainWindow(Window):

    def __init__(self):
        super().__init__()
        text_var = tkinter.StringVar(value="ACTD")
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
        self.button = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, command=self.wait_for_connection, fg_color=("gray75", "blue"), bg_color='gray75')
        self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.conn = Connection()
        self.keyObj = KeyReader()

        

    def wait_for_connection(self):
        text_var = tkinter.StringVar(value="Please Plug in your Tracing Device. Once Connected Press the Button Below")
        label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label.configure(font=('Helvatical bold',30))
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.update()
        button = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, command=self.checkDeviceConnection, fg_color=("gray75", "blue"), bg_color='gray75')
        button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)


    def checkDeviceConnection(self):
        text_var = tkinter.StringVar(value="Checking Connection. Please Wait")
        label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label.configure(font=('Helvatical bold',30))
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.update()
        self.after(1000, self.didConnect)#TODO:change this to 6 sec so 6000
        
        

    def didConnect(self):
        if self.conn.findConnectedDevices(): #so it was connected
            #get the stored UID first
            self.storedUID = self.getStoredUID()
            self.checkUpdateScreen()
        else: #go to check device connection
            text_var = tkinter.StringVar(value="No Tracing Device Was Connected Please Reconnect the Tracing Device.")
            label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
            label.configure(font=('Helvatical bold',30))
            label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.update()
            self.after(3000, self.checkDeviceConnection)


    def getStoredUID(self):
        return self.keyObj.readKey()
        

    def checkUpdateScreen(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.configure(fg_color='gray75')
        
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
        button2 = customtkinter.CTkButton(master=frame, text='Enter',corner_radius=30, fg_color=("gray75", "blue"))
        button2.grid(row=1,column=2)
        
        self.update()

    
    def checkInfectionStatus(self):
        #TODO: send self.storedUID to the db

    def updateInfectionStatus(self):
        #TODO: update infection of hte storeduid in the db
    def runMainWindow(self):
        self.mainloop()



if __name__ == '__main__':
    ui = MainWindow()
    # ui.wait_for_connection()
    ui.runMainWindow()
    