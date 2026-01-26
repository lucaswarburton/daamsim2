from calculations.batch_rr_calcs import batch_calcs
from . import NSUI
from . import DMController

class NewSimController:
    def __init__(self, master_controller) -> None:
        self.view = None
        self.master_controller: DMController.DMController = master_controller
    
    def set_view(self, view) -> None:
        self.view:  NSUI.NewSimUIInnerFrame = view
    
    def update_window(self) -> None:
        self.master_controller.update_window()
         
    def run_new_sim(self) -> None:
        daa_spec = self.view.get_params()
        self.master_controller.calculation_mode()
        batch_calcs(daa_spec)
        self.master_controller.unlock_buttons()
        
    
    