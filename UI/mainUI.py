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
        text_var = tkinter.StringVar(value="Please Plug In Your Contact Tracing Device")
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
        self.button = customtkinter.CTkButton(master=self, corner_radius=30, command=self.update_str, fg_color=("gray75", "blue"))
        self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.conn = Connection()

    def update_str(self):
        text_var = tkinter.StringVar(value="updated str")
        label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.update()

    def wait_for_connection(self):
        while self.conn.findConnectedDevices() == 0:
            pass
        self.update_str()

    def runMainWindow(self):
        self.mainloop()

if __name__ == '__main__':
    ui = MainWindow()
    # ui.wait_for_connection()
    ui.runMainWindow()
    