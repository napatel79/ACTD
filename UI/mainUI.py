import tkinter
from tkinter import *
import customtkinter
import window
from window import *

class MainWindow(Window):

    def __init__(self):
        super().__init__()
        text_var = tkinter.StringVar(value="Please Plug In Your Contact Tracing Device")
        label = customtkinter.CTkLabel(master=self,
                               textvariable=text_var,
                               width=self.width,
                               height=self.height,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        # self.initText = customtkinter.CTkTextbox(master=self, width=self.width)
        # self.initText.grid(row=0, column=0)
        # self.initText.insert(self.width/2, 'Please Plug In Your Contract Tracing Device\n')

    def runMainWindow(self):
        self.mainloop()

if __name__ == '__main__':
    ui = MainWindow()
    ui.runMainWindow()
    