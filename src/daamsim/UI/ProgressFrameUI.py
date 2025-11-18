from tkinter import *
from tkinter import ttk

class Progress_Frame(Frame):
    def __init__(self, master, bg = "grey"):
        Frame.__init__(self, master, bg=bg)

        self.pack_propagate(0)
        self.grid_propagate(0)