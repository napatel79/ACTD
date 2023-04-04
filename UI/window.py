from tkinter import *
import customtkinter

class Window(customtkinter.CTk):

    def __init__(self):
        super().__init__() 
        self.width = 1920
        self.height = 1080
        # customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")
        # self.style.configure("ACTD.labels", font=('helvetica', 25))#can be used to change all labels to this style
        self.title('ACTD')
        self.geometry(str(self.width) + 'x' + str(self.height))

    