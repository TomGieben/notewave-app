import ttkbootstrap as tkb
from ttkbootstrap import *
from ttkbootstrap.constants import *

from Models.Note import *
from slugify import slugify
import string
import random

class Notebook:
    def __init__(self, main):
        notes = Note.all()
        self.main = main
        main.title('Notewave')
        self.fontSizePx = -20
        
        # Logo
        ico = Image.open('assets/logo.png')
        photo = ImageTk.PhotoImage(ico)
        main.iconphoto(False, photo)

        # Font
        self.fontspecs = font.Font(family="consolas", size=self.fontSizePx)

        # Notebook
        self.notebook = tkb.Notebook(main, bootstyle="info")
        self.notebook.pack(pady=10, expand=True)

        if(notes):
            for note in Note.all():
                self.add_tab(note)
        else:
            self.add_tab()
      
        tkb.Button(main, text= "New", bootstyle="success", command=self.add_tab).grid(row=1, column=0, sticky="nsew")
        tkb.Button(main, text= "Delete", bootstyle="danger", command=self.remove_tab).grid(row=1, column=1, sticky="nsew")

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
            content = ''
        else:
            title = note.title
            content = note.content
            
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
        title = self.notebook.tab(self.notebook.select(), "text")
        slug = slugify(title)
        
        self.notebook.forget(self.notebook.select())
        Note.delete(slug)
        
        if not (Note.all()):
            self.add_tab()
            
        
    def save_tab(self, event):
        title = self.notebook.tab(self.notebook.select(), "text")
        content = event.widget.get("1.0",'end-1c')
        slug = slugify(title)
        data = {
            "slug": slug, 
            "title": title,
            "content": content
        }
        
        Note.save(data)

