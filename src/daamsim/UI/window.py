from tkinter import *
from tkinter import ttk

from DMUI import DMUIFrame 
from GMUI import GMUIFrame
from DMController import DMController

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.frames = dict()

        screen_width = super().winfo_screenwidth()
        screen_height = super().winfo_screenheight()
        super().title("DAAMSIM")
        super().geometry(str(int(screen_width*3/4)) + 'x' + str(int(screen_height * 3/4)) + '+' + str(int(screen_width/8)) + '+' + str(int(screen_height/8)))

        main_controller = DMController()
        main_controller.setView(self)

        self.pack_propagate(0)

             
        
    def setDMUIFrame(self, frame):
        
        self.DMUIFrame = frame
        self.DMUIFrame.pack(side = LEFT, fill = "both", expand=True)

    def setActiveFrame(self, frame):
        if isinstance(frame, str):
            self.ActiveFrame = self.frames[frame]
        else:
            self.ActiveFrame = frame
        self.ActiveFrame.pack(side = RIGHT, fill="both", expand=True)

    # def setActiveFrame(self, frameName):
    #     self.setActiveFrame(self.frames[frameName])

    def addFrame(self, frameName, frame):
        self.frames[frameName] = frame
        

        




    
        



 