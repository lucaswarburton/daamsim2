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
        self
        
    def update_window(self):
        self.window.update()
        
    def lock_buttons(self):
        self.view.lock_buttons()
        
    def calculation_mode(self):
        self.lock_buttons()
        self.window.setActiveFrame("ProgressFrameUI")