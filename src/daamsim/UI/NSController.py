import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "calculations"))
from batch_rr_calcs import batch_calcs

class new_sim_controller:
    def __init__(self, master_controller):
        self.view = None
        self.model = None
        self.master_controller = master_controller
    
    def setView(self, view):
        self.view = view
    
    def setmodel(self, model):
        self.model =  model
    
    def update_window(self):
        self.master_controller.update_window()
         
    def run_new_sim(self):
        daa_spec = self.view.get_params()
        self.master_controller.calculation_mode()
        batch_calcs(daa_spec)
        self.master_controller.unlock_buttons()
        
    
    