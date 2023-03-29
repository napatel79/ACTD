import tkinter
from tkinter import *
import customtkinter
import window
from window import *
import time

class MainWindow(Window):

    def __init__(self):
        super().__init__()
        text_var = tkinter.StringVar(value="Please Plug In Your Contact Tracing Device")
        label = customtkinter.CTkLabel(master=self,
                               textvariable=text_var,
                               width=self.width,
                               height=self.height,
                               fg_color=("black", "gray75"),
                               bg_color=("black", "gray75"),
                               text_color='black',
                               corner_radius=8)
        label.configure(font=('Helvatical bold',50))
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def update_str(self):
        text_var = tkinter.StringVar(value="updated str")
        label = customtkinter.CTkLabel(master=self, textvariable=text_var, width=self.width, height=self.height, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label.configure(font=('Helvatical bold',50))
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def wait_for_connection(self):
        self.after(1000, self.update_str)

    def runMainWindow(self):
        self.mainloop()

if __name__ == '__main__':
    ui = MainWindow()
    ui.wait_for_connection()
    ui.runMainWindow()
    