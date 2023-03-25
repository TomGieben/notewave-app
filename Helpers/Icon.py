import tkinter as tk
from tkinter import PhotoImage

class Icon:
    @staticmethod
    def get(icon: str):
        return PhotoImage(file = r"D:\laragon\www\app.notewave\assets\icons\\"+ icon +".png")
    
    