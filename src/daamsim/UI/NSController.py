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
        
        
    
    