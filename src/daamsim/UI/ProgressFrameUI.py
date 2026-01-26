from tkinter import *
from tkinter import ttk

class ProgressFrame(Frame):
    _instance = None
    
    def __new__(cls,  *args, **kwargs) -> None:
        if cls._instance is None:
            cls._instance = super(ProgressFrame, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, master=None, bg = "grey") -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            super().__init__(master, bg=bg)
            self.bg = bg
        
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=1)
        
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=0)
            self.rowconfigure(2, weight=0)
            self.rowconfigure(3, weight=1)

            self.reset()

            self.grid_propagate(0)
    
    #total = total number of actions to complete
    #message = relevant activity if any
    def set_main(self, total:int, message:str)-> None:
        self.main_complete = 0
        self.main_total = total
        self.main_endmessage = "/" + str(total) + " " + message
        self.main_label.configure(text=str(self.main_complete) + self.main_endmessage)
        self.main_progress_bar['value'] = 0
        self.update()
        self.update_idletasks()
    
    def increment_main(self, message:str = None):
        if not message is None:
            self.main_endmessage = "/" + str(self.main_total) + " " + message
        
        self.main_complete += 1
        self.main_label.configure(text=str(self.main_complete) + self.main_endmessage)
        self.main_progress_bar["value"] = (float(self.main_complete) / float(self.main_total)) *100.0
        self.update()
        self.update_idletasks()

    def reset(self):
        self.main_progress_bar = ttk.Progressbar(self, length = 200, )
        self.main_progress_bar.grid(column=1, row=1, padx=10, pady=2)
        self.main_label = Label(self, bg=self.bg, font=("Ariel",15))
        self.main_label.grid(column=1, row=2, padx=10, pady=2)

    