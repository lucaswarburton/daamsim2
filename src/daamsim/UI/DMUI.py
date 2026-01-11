from tkinter import *
from tkinter import ttk

class DMUIFrame(Frame):
    def __init__(self, controller, master, bg = "blue"):
        Frame.__init__(self, master, bg=bg, width=250)
        self.controller = controller

        self.new_sim_button = Button(self, text = "DAA Simulations (ARC-b)", command=controller.run_new_sim)
        self.calculate_cumulative_data_button = Button(self,text = "Calculate Sample Cumulative Risk Ratio", command=controller.run_cumulative_calc)
        self.calculate_daa_sensitivity_button = Button(self, text = "Calculate Sample Sensitivity", command = controller.run_sensitivity_calc)
        self.view_graphs_button = Button(self, text = "View Graphs", command = controller.open_graph_manager)
        self.save_data_button = Button(self, text = "Save Data", command = controller.save_view)
        self.load_data_button = Button(self, text = "Load Data", command = controller.load)

        self.new_sim_button.grid(column = 1, row = 1, padx=15, pady=10, sticky = NSEW)
        self.calculate_cumulative_data_button.grid(column = 1, row = 2, padx=15, pady=10, sticky = NSEW)
        self.calculate_daa_sensitivity_button.grid(column = 1, row = 3, padx=15, pady=10, sticky = NSEW)
        self.view_graphs_button.grid(column = 1, row = 4, padx=15, pady=10, sticky = NSEW)
        self.save_data_button.grid(column = 1, row = 5, padx=15, pady=10, sticky = NSEW)
        self.load_data_button.grid(column = 1, row =61, padx=15, pady=10, sticky = NSEW)

        self.pack_propagate(0)
        self.grid_propagate(0)
    
    def lock_buttons(self):
        self.new_sim_button.config(state=DISABLED)
        self.calculate_cumulative_data_button.config(state=DISABLED)
        self.calculate_daa_sensitivity_button.config(state=DISABLED)
        self.view_graphs_button.config(state=DISABLED)
        self.save_data_button.config(state=DISABLED)
        self.load_data_button.config(state=DISABLED)
    
    def unlock_buttons(self):
        self.new_sim_button.config(state=NORMAL)
        self.calculate_cumulative_data_button.config(state=NORMAL)
        self.calculate_daa_sensitivity_button.config(state=NORMAL)
        self.view_graphs_button.config(state=NORMAL)
        self.save_data_button.config(state=NORMAL)
        self.load_data_button.config(state=NORMAL)


