from tkinter import filedialog
from tkinter import messagebox

from daamsim.Config import Configuration
from . import SaveLoadController
from . import DMUI


class DMController:
    def __init__(self):
        self.window = None
        self.view = None
        
    def set_window(self, window) -> None:
        self.window = window
        
    def set_view(self, view) -> None:
        self.view: DMUI.DMUIFrame = view

    def run_new_sim(self) -> None:
        self.window.set_active_frame("NSUI")

    def run_cumulative_calc(self) -> None:
        self
        #to be implemented
        

    def run_sensitivity_calc(self) -> None:
        self
        #to be implemented

    def open_graph_manager(self) -> None:
        self.window.set_active_frame("GMUI")

    def save_view(self) -> None:
        self.window.set_active_frame("SAVE")
        #to be implemented

    def load(self) -> None:
        filepath = filedialog.askopenfilename(initialdir=Configuration.get_instance().default_load_file_path)
        if filepath == "":
            return
        try:
            success = SaveLoadController.LoadController.load_state(filepath)
        
            if success:
                self.window.frames["NSUI"].scrolling_frame.regenerate()
                self.lock_buttons()
                self.unlock_buttons()
                self.run_new_sim()
                self.update_window()
                messagebox.showinfo("Successfully Loaded!", "The data was successfully loaded!")
            else:
                messagebox.showerror("Failed","Failed to load!\nUnrecognized file type or format\nDid you load the wrong file or a depreciated file?")
        except:
            messagebox.showerror("Error", "Unexpected Error Encountered Trying to Load Data")
        
    def update_window(self) -> None:
        self.window.update()
        
    def lock_buttons(self) -> None:
        self.view.lock_buttons()
    
    def unlock_buttons(self) -> None:
        self.view.unlock_buttons()
        
    def calculation_mode(self) -> None:
        self.lock_buttons()
        self.window.set_active_frame("ProgressFrameUI")