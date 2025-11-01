class new_sim_controller:
    def __init__(self):
        self.view = None
        self.model = None
    
    def setView(self, view):
        self.view = view
    
    def setmodel(self, model):
        self.model =  model
        
    def run_new_sim(self):
        daa_spec = self.view.get_params()
        
    
    