from tkinter import *
from tkinter import ttk

from .DMUI import DMUIFrame 
from .DMController import DMController

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.frames = dict()
        self.container = Frame(self, width=300)

        self.container.pack(side = RIGHT, fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        
        screen_width = super().winfo_screenwidth()
        screen_height = super().winfo_screenheight()
        super().title("DAAMSIM")
        super().geometry(str(int(screen_width*3/4)) + 'x' + str(int(screen_height * 3/4)) + '+' + str(int(screen_width/8)) + '+' + str(int(screen_height/8)))

        main_controller = DMController()
        main_controller.set_window(self)

        self.pack_propagate(0)

             
        
    def set_DMUI_frame(self, frame: DMUIFrame):
        self.DMUIFrame = frame
        self.DMUIFrame.pack(side = LEFT, fill = "both", expand=False)
  

    def set_active_frame(self, frame):
        if isinstance(frame, str):
            self.ActiveFrame = self.frames[frame]
        else:
            self.ActiveFrame = frame
        self.ActiveFrame.event_generate("<Map>")
        self.ActiveFrame.tkraise()
        self.update()
        self.update_idletasks()

    def add_frame(self, frameName:str, frame: str):
        self.frames[frameName] = frame
    
    
        
        

        




    
        



 