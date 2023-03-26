import ttkbootstrap as tkb
from ttkbootstrap import *
from ttkbootstrap.constants import *

from Models.Note import *
from Helpers.Icon import *
from slugify import slugify
import string
import random
import json

class Notebook:
    def __init__(self, main):
        notes = Note.all()
        self.id = {}
        self.main = main
        main.title('Notewave')
        self.fontSizePx = -20
        self.user = json.loads(open('assets/user.json').read())
        
        # Logo
        ico = Image.open('D:\laragon\www\\app.notewave\\assets\logo.png')
        photo = ImageTk.PhotoImage(ico)
        main.iconphoto(False, photo)

        # Font
        self.fontspecs = font.Font(family="consolas", size=self.fontSizePx)

        # Notebook
        self.notebook = tkb.Notebook(main, bootstyle="primary")
        self.notebook.pack(pady=10, expand=True)

        if(notes):
            for index, note in enumerate(Note.all()):
                self.id[index] = note.id
                self.add_tab(note)
        else:
            self.add_tab()
      
        tkb.Button(main, text= "➕ New", bootstyle="success", command=self.add_tab).grid(row=1, column=0, sticky="nsew")
        tkb.Button(main, text= "➖ Delete", bootstyle="danger", command=self.remove_tab).grid(row=1, column=1, sticky="nsew")
        
        main.grid_rowconfigure(0, weight=1) # this needed to be added
        main.grid_columnconfigure(0, weight=1) 

    def new_font_size(self, event):
        if event.delta > 0:
            self.fontSizePx = self.fontSizePx - 2
        else:
            self.fontSizePx = self.fontSizePx + 2

        self.fontspecs.config(size=self.fontSizePx)
    
    def add_tab(self, note: dict = {}):    
        if not (note):
            letters = string.ascii_lowercase
            title = 'new-' + ''.join(random.choice(letters) for i in range(7))
            content = title + '\n'
        else:
            title = note.title
            content = note.title + '\n' + note.content
            
        # Tab
        self.tab_frame = tkb.Frame(self.notebook)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.notebook.add(self.tab_frame, text=title)
        
        # Text Area
        self.textarea = tkb.Text(self.tab_frame, font=self.fontspecs)
        self.textarea.insert(tkb.END, content)
        self.textarea.pack(fill="both", expand=True)
        self.textarea.bind('<KeyRelease>', self.save_tab)
        self.tab_frame.grid_propagate(False)
        
    def remove_tab(self):
        index = self.notebook.index(self.notebook.select())
    
        if index in self.id:
            id = self.id[index]
        else:
            id = 0
            
        self.notebook.forget(self.notebook.select())
        self.id[index] = 0
        Note.delete(id)        
        
    def save_tab(self, event):
        index = self.notebook.index(self.notebook.select())
        body = event.widget.get("1.0",'end-1c').split('\n', 2)
        title = body[0]
        slug = slugify(title)
        
        if len(body) > 1:
            content = body[1] 
        else:
            content = ''
        
        self.notebook.tab(self.notebook.select(), text=title)
        
        if index in self.id:
            id = self.id[index]
        else:
            id = 0
            
        data = {
            "id": id,
            "user_id": self.user['id'],
            "slug": slug, 
            "title": title,
            "content": content
        }
        
        id = Note.save(data)
        self.id[index] = id

