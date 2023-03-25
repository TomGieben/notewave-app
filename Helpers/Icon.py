import tkinter as tk
from tkinter import PhotoImage

class Icon:
    @staticmethod
    def get(icon: str):
        return PhotoImage(file = r"D:\laragon\www\notewave\assets\icons\\"+ icon +".png")
    
    