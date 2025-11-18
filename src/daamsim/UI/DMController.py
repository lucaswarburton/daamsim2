from tkinter import filedialog
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Config import Configuration



class DMController:
    def __init__(self):
        self.window = None
        self.model = None
        self.view = None
        
    def setWindow(self, window):
        self.window = window
    
    def setmodel(self, model):
        self.model =  model
        
    def setView(self, view):
        self.view = view

    def run_new_sim(self):
        self.window.setActiveFrame("NSUI")

    def run_cumulative_calc(self):
        self.model

    def run_sensitivity_calc(self):
        self.model

    def open_graph_manager(self):
        self.window.setActiveFrame("GMUI")

    def save_model(self):
        self

    def load_model(self):
        filepath = filedialog.askopenfilename(initialdir=Configuration.get_instance().default_load_file_path)
        #Load file in
        
    def update_window(self):
        self.window.update()
        
    def lock_buttons(self):
        self.view.lock_buttons()
    
    def unlock_buttons(self):
        self.view.unlock_buttons()
        
    def calculation_mode(self):
        self.lock_buttons()
        self.window.setActiveFrame("ProgressFrameUI")