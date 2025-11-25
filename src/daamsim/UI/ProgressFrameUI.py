from tkinter import *
from tkinter import ttk
import threading

class Progress_Frame(Frame):
    _instance = None
    def __init__(self, master, bg = "grey"):
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

        self.lock = threading.Lock()

        self.grid_propagate(0)

        Progress_Frame._instance = self
    
    def getinstance():
        if Progress_Frame._instance is not None:
            return Progress_Frame._instance
        else:
            raise Exception("Progress_Frame not initialized")
    
    #total = total number of actions to complete
    #message = relevant activity if any
    def setMain(self, total:int, message:str):
        with self.lock:
            self.main_complete = 0
            self.main_total = total
            self.main_endmessage = "/" + str(total) + " " + message
            self.main_label.configure(text=str(self.main_complete) + self.main_endmessage)
            self.main_progress_bar['value'] = 0
            self.update()
            self.update_idletasks()
    
    def increment_main(self, message = None):
        with self.lock:
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

    