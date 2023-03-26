from Helpers.Notebook import *
from Helpers.Login import *
from Models.User import *

main = tkb.Window()

if User.isAuthenticated():
    Notebook(main)
else:
    Login(main)
    
main.mainloop()