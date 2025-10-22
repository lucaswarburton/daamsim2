from tkinter import *
from tkinter import ttk

class GMUIFrame(Frame):
    def __init__(self, controller, master = None, cnf = {}, background = "white", bd = 2, bg = "green", border = 0, borderwidth = 0, class_ = "Frame", colormap = "", container = False, cursor = "", height = 0, highlightbackground = "grey", highlightcolor = "white", highlightthickness = 0, name = "graphs", padx = 0, pady = 0, relief = "flat", takefocus = 0, visual = "", width = 0):
        super().__init__(master, cnf, background=background, bd=bd, bg=bg, border=border, borderwidth=borderwidth, class_=class_, colormap=colormap, container=container, cursor=cursor, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, visual=visual, width=width)
        self.controller = controller

        self.pack_propagate(0)
        self.grid_propagate(0)

