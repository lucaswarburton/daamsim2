from tkinter import filedialog
from tkinter import messagebox
from daamsim.Config import Configuration
from .SaveLoadController import LoadController


class DMController:
    def __init__(self):
        self.window = None
        self.view = None
        
    def setWindow(self, window):
        self.window = window
        
    def setView(self, view):
        self.view = view

    def run_new_sim(self):
        self.window.setActiveFrame("NSUI")

    def run_cumulative_calc(self):
        self
        #to be implemented
        

    def run_sensitivity_calc(self):
        self
        #to be implemented

    def open_graph_manager(self):
        self.window.setActiveFrame("GMUI")

    def save_view(self):
        self.window.setActiveFrame("SAVE")
        #to be implemented

    def load(self):
        filepath = filedialog.askopenfilename(initialdir=Configuration.get_instance().default_load_file_path)
        if filepath == "":
            return
        success = LoadController.load_state(filepath)
        if success:
            messagebox.showinfo("Successfully Loaded!", "The data was successfully loaded!")
            self.lock_buttons()
            self.unlock_buttons()
            self.run_new_sim()
            self.update_window()
        else:
            messagebox.showerror("Failed","Failed to load!\nUnrecognized file type or format\nDid you load a valid file?")
        #Load file in
        #to be implemented
        
    def update_window(self):
        self.window.update()
        
    def lock_buttons(self):
        self.view.lock_buttons()
    
    def unlock_buttons(self):
        self.view.unlock_buttons()
        
    def calculation_mode(self):
        self.lock_buttons()
        self.window.setActiveFrame("ProgressFrameUI")