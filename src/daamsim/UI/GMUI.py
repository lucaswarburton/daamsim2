from tkinter import *
from tkinter import ttk

class GMUIFrame(Frame):
    def __init__(self, controller, master, bg = "green"):
        Frame.__init__(self, master, bg=bg)
        self.controller = controller

        self.pack_propagate(0)
        self.grid_propagate(0)

