class DMController:
    def __init__(self):
        self.view = None
        self.model = None
        
    def setView(self, view):
        self.view = view
    
    def setmodel(self, model):
        self.model =  model

    def run_new_sim(self):
        self.view.setActiveFrame("NSUI")

    def run_cumulative_calc(self):
        self.model

    def run_sensitivity_calc(self):
        self.model

    def open_graph_manager(self):
        self.view.setActiveFrame("GMUI")

    def save_model(self):
        self

    def load_model(self):
        self
        
    def update_window(self):
        self.view.update()