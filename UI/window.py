from tkinter import *
import customtkinter

class Window(customtkinter.CTk):

    def __init__(self):
        super().__init__() 
        self.width = 600
        self.height = 600
        customtkinter.set_appearance_mode("Dark")
        self.title('ACTD')
        self.geometry(str(self.width) + 'x' + str(self.height))

    