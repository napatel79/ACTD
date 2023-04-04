import tkinter
from tkinter import *
import customtkinter

app = customtkinter.CTk()                 
app.geometry('720x480')
widget = Label(app, text='Spam', fg='white', bg='black')
widget.pack()

for widgets in app.winfo_children():
      widgets.destroy()
app.mainloop()

self.destroy()
        text_var = tkinter.StringVar(value="Check")
        label = customtkinter.CTkLabel(master=self, textvariable=text_var, fg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label.grid(row=0, column=0)
        button1 = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, fg_color=("gray75", "blue"))
        button1.grid(row=1,column=0)

        text_var2 = tkinter.StringVar(value="Update")
        label2 = customtkinter.CTkLabel(master=self, textvariable=text_var2, fg_color=("black", "gray75"),bg_color=("black", "gray75"),text_color='black',corner_radius=8)
        label2.grid(row=0, column=1)
        button2 = customtkinter.CTkButton(master=self, text='Enter',corner_radius=30, fg_color=("gray75", "blue"))
        button2.grid(row=1,column=1)
        self.update()