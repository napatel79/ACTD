import tkinter
from tkinter import *
import customtkinter
import window
from window import *
import time
import checkConnection
from checkConnection import Connection

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
        self.button = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, command=self.wait_for_connection, fg_color=("gray75", "blue"))
        self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.conn = Connection()

        

    def wait_for_connection(self):
        text_var = tkinter.StringVar(value="Please Plug in your Tracing Device. Once Connected Press the Button Below")
        label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label.configure(font=('Helvatical bold',30))
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.update()
        button = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, command=self.checkDeviceConnection, fg_color=("gray75", "blue"))
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
            self.checkUpdateScreen()
        else: #go to check device connection
            text_var = tkinter.StringVar(value="No Tracing Device Was Connected Please Reconnect the Tracing Device.")
            label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
            label.configure(font=('Helvatical bold',30))
            label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.update()
            self.after(3000, self.checkDeviceConnection)



    def checkUpdateScreen(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side='bottom', fill='x')
        button_frame.grid_columnconfigure(0, weight=1)
        #make two buttons for update and check
        button = customtkinter.CTkButton(master=button_frame, text='Update',corner_radius=30, command=self.checkDeviceConnection, fg_color=("gray75", "blue"))
        self.update()

    
    def runMainWindow(self):
        self.mainloop()



if __name__ == '__main__':
    ui = MainWindow()
    # ui.wait_for_connection()
    ui.runMainWindow()
    