import ttkbootstrap as tkb
from ttkbootstrap import *
from ttkbootstrap.constants import *

from Models.User import *
from Helpers.Notebook import *

import os
import sys

class Login:
    def __init__(self, main):
        main.title('Notewave')
        
        # Logo
        ico = Image.open('D:\laragon\www\\app.notewave\\assets\logo.png')
        photo = ImageTk.PhotoImage(ico)
        main.iconphoto(False, photo)

        #email label and text entry box
        emailLabel = tkb.Label(main, text="Email")
        emailLabel.grid(row=0, column=0)
        emailEntry = tkb.Entry(main)
        emailEntry.grid(row=0, column=1)  

        #password label and password entry box
        passwordLabel = tkb.Label(main,text="Password")
        passwordLabel.grid(row=1, column=0)
        passwordEntry = tkb.Entry(main, show='*')
        passwordEntry.grid(row=1, column=1)

        #login button
        loginButton = tkb.Button(main, text="Login", command=lambda: self.validate(emailEntry, passwordEntry)).grid(row=4, column=0)  
        
        self.main = main
    def validate(self, email, password):
        if(User.exists(email.get(), password.get())):
            user = User.get(email.get())
            file = open("assets/user.json", "w")
            file.write(str(User.serialize(user)).replace("'", '"'))
            file.close()
            
            os.execl(sys.executable, sys.executable, *sys.argv)


    
    