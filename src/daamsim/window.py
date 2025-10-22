from tkinter import *
from tkinter import ttk

from DMUI import DMUIFrame 
from GraphUI import GMUIFrame

class Window(Tk):
    def __init__(self):
        super().__init__(None, "DAAMSIM",'Tk', 1)
        screen_width = super().winfo_screenwidth()
        screen_height = super().winfo_screenheight()
        super().title("DAAMSIM")
        super().geometry(str(int(screen_width/2)) + 'x' + str(int(screen_height/2)) + '+' + str(int(screen_width/4)) + '+' + str(int(screen_height/4)))
        
        frame1 = DMUIFrame(self)
        frame2 = GMUIFrame(self)

        frame1.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        frame2.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        



w = Window()
w.mainloop()   