from tkinter import *
from tkinter import ttk

from DMController import DMController

class DMUIFrame(Frame):
    def __init__(self, controller, master = None, cnf = {}, background = "white", bd = 2, bg = "blue", border = 0, borderwidth = 0, class_ = "Frame", colormap = "", container = False, cursor = "", height = 0, highlightbackground = "grey", highlightcolor = "white", highlightthickness = 0, name = "data_manager", padx = 0, pady = 0, relief = "flat", takefocus = 0, visual = "", width = 0):
        super().__init__(master, cnf, background=background, bd=bd, bg=bg, border=border, borderwidth=borderwidth, class_=class_, colormap=colormap, container=container, cursor=cursor, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, visual=visual, width=width)
        self.controller = controller

        self.new_sim_button = Button(self, text = "Run New Simulation", command=controller.run_new_sim)
        self.calculate_cumulative_data_button = Button(self,text = "Calculate Sample Cumulative Risk Ratio", command=controller.run_cumulative_calc)
        self.calculate_daa_sensitivity_button = Button(self, text = "Calculate Sample Sensitivity", command = controller.run_sensitivity_calc)
        self.view_graphs_button = Button(self, text = "View Graphs", command = controller.open_graph_manager)
        self.save_data_button = Button(self, text = "Save Data", command = controller.save_model)
        self.load_data_button = Button(self, text = "Load Data", command = controller.load_model)

        self.new_sim_button.grid(column = 1, row = 1, padx=5, pady=5, sticky = NSEW)
        self.calculate_cumulative_data_button.grid(column = 1, row = 2, padx=5, pady=5, sticky = NSEW)
        self.calculate_daa_sensitivity_button.grid(column = 1, row = 3, padx=5, pady=5, sticky = NSEW)
        self.view_graphs_button.grid(column = 1, row = 4, padx=5, pady=5, sticky = NSEW)
        self.save_data_button.grid(column = 1, row = 5, padx=5, pady=5, sticky = NSEW)
        self.load_data_button.grid(column = 1, row =61, padx=5, pady=5, sticky = NSEW)

        self.pack_propagate(0)
        self.grid_propagate(0)
    


