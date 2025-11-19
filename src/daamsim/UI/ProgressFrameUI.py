from tkinter import *
from tkinter import ttk
import threading

class Progress_Frame(Frame):
    _instance = None
    def __init__(self, master, bg = "grey"):
        super().__init__(master, bg=bg)
        self.bg = bg

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
    
    def increment_main(self, message = None):
        with self.lock:
            if not message is None:
                self.main_endmessage = "/" + str(self.main_total) + " " + message
        
            self.main_complete += 1
            self.main_label.configure(text=str(self.main_complete) + self.main_endmessage)
            self.main_progress_bar["value"] = (float(self.main_complete) / float(self.main_total)) *100.0

    #total = total number of actions to complete
    #message = relevant activity if any
    def setSecondary(self, total:int, message:str):
        with self.lock:
            self.secondary_complete = 0
            self.secondary_total = total
            self.secondary_endmessage = "/" + str(total) + " " + message
            self.secondary_label.configure(text=str(self.secondary_complete) + self.secondary_endmessage)
            self.secondary_progress_bar['value'] = 0
    
    def increment_secondary(self, message = None):
        with self.lock:
            if not message is None:
                self.secondary_endmessage = "/" + str(self.main_total) + " " + message
        
            self.secondary_complete += 1
            self.secondary_label.configure(text=str(self.secondary_complete) + self.secondary_endmessage)
            self.secondary_progress_bar["value"] = (float(self.secondary_complete) / float(self.main_total)) * 100.0


    def reset(self):
        self.main_progress_bar = ttk.Progressbar(self, length = 200)
        self.main_progress_bar.grid(column=0, row=1, padx=10, pady=2)
        self.main_label = Label(self, bg=self.bg)
        self.main_label.grid(column=0, row=2, padx=10, pady=2)
        self.secondary_progress_bar = ttk.Progressbar(self, length = 200)
        self.secondary_progress_bar.grid(column=0, row = 3, padx=10, pady=2)
        self.secondary_label = Label(self, bg=self.bg)
        self.secondary_label.grid(column=0, row = 4, padx=10, pady=2)


if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    frame = Progress_Frame(root)
    frame.pack(fill=BOTH, expand=1)
    num_suites = 10
    num_cases = 10
    frame.setMain(num_suites, "Test Suites")
    frame.setSecondary(num_cases, "Test Cases")

    def buttonPress():
        frame.increment_secondary()
        if frame.secondary_complete >= 10:
            frame.setSecondary(num_cases, "Test Cases")
            frame.increment_main()
        
    
    button = Button(frame, command=buttonPress, text="Run Test")
    button.grid(column=0, row = 5)

    root.mainloop()

    