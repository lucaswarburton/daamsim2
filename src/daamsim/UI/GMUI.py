from tkinter import *
from tkinter import ttk

from data_classes.CurrentData import CurrentData
from daamsim.Config import Configuration

class GMUIFrame(Frame):
    def __init__(self, controller, master, bg = "lime green"):
        Frame.__init__(self, master, bg=bg)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frames = dict()
        
        self.frames["main_subframe"] = MainSubFrame(controller=controller, master=self, bg=bg)
        self.frames["main_subframe"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["per_speed_sub_frame"] = PerSpeedSubFrame(controller=controller, master=self, bg=bg)
        self.frames["per_speed_sub_frame"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["multi_speed_sub_frame"] = MultiSpeedPlotFrame(controller=controller, master = self, bg=bg)
        self.frames["multi_speed_sub_frame"].grid(row=0, column=0, sticky="nsew")
        
        self.bind("<Map>", self.on_raise)
        
    def setActiveFrame(self, frame_name):
        self.frames[frame_name].regenerate()
        self.frames[frame_name].tkraise()
        
    def lock_per_speed_button(self):
        self.frames["main_subframe"].lock_per_speed_button()
    
    def unlock_per_speed_button(self):
        self.frames["main_subframe"].unlock_per_speed_button()
    
    def on_raise(self, event):
        self.setActiveFrame("main_subframe")
    
    
    
    
class MainSubFrame(Frame):
    def __init__(self, controller, master, bg = "lime green"):
        Frame.__init__(self, master, bg=bg)
        self.controller = controller
        self.bg = bg
        
        self.title = Label(self, text = "Select a graph type:", font=("Ariel",20, "bold"), padx=5, pady=5, bg=bg)
        self.title.grid(column=0, row=1, padx=5, pady=5, sticky= W)
        
        self.per_speed_graphs_button = Button(self, text="Per Speed Graphs", padx= 5, pady= 5, command= lambda: self.controller.setActiveFrame("per_speed_sub_frame"))
        self.per_speed_graphs_button.grid(column=0, row = 2, padx=5, pady=5, sticky= W)
        
        self.multi_speed_graphs_button = Button(self, text="Multi Speed 3D Plots", padx= 5, pady= 5, command= lambda: self.controller.setActiveFrame("multi_speed_sub_frame"))
        self.multi_speed_graphs_button.grid(column=0, row = 3, padx=5, pady=5, sticky= W)
        
        
        self.per_speed_graphs_label = Label(self, text = "(If grayed out, run DAA Simulations (ARC-b) or load data)", padx=5, pady = 5, bg=bg)
        self.per_speed_graphs_label.grid(column=0, row=4, padx=5, pady=5, sticky= W)
        
        
    def lock_per_speed_button(self):
        self.per_speed_graphs_button.config(state=DISABLED)
    
    def unlock_per_speed_button(self):
        self.per_speed_graphs_button.config(state=NORMAL)
        
    def lock_multi_speed_buttion(self):
        self.multi_speed_graphs_button.config(state=DISABLED)
        
    def unlock_multi_speed_buttion(self):
        self.multi_speed_graphs_button.config(state=NORMAL)
        
    def regenerate(self):
        data = CurrentData()
        match data._sim_state:
            case 0:
                self.lock_per_speed_button()
                self.lock_multi_speed_buttion()
            case 1:
                self.unlock_per_speed_button()
                self.unlock_multi_speed_buttion()
        
    
class PerSpeedSubFrame(Frame):
    def __init__(self, controller, master, bg = "lime green"):
        Frame.__init__(self, master, bg=bg)
        self.bg = bg
        self.controller = controller
        
        self.back_button = Button(self,  text = "Back", command= lambda: controller.setActiveFrame("main_subframe"), font=("Ariel",12, "bold"))
        self.back_button.grid(column=0, row=0, padx=2, pady=2, sticky= W)
        
        self.title = Label(self, text = "Choose RPAS and Intruder Speed for subplot:", bg = bg, font=("Ariel",15, "bold"))
        self.title.grid(column=0, row=1,columnspan=3, padx=2, pady=2, sticky= W)
        
        self.regenerate()
        
        self.pack_propagate(0)
        self.grid_propagate(0)
        
    def regenerate(self):
        data = CurrentData()
        
        if data._sim_state != 0:
            self.rpas_speed = DoubleVar()
            speeds = data.specs.rpas_speed_array.tolist()
            self.rpas_speed.set(speeds[0])
            self.rpas_label = Label(self, text = "Select RPAS Speed (kts):", bg=self.bg)
            self.rpas_label.grid(column=0, row=2, padx=2, pady=2, sticky=W)
            self.rpas_box = ttk.Combobox(self, text = "Select RPAS speed value", textvariable=self.rpas_speed)
            self.rpas_box["values"] = speeds
            self.rpas_box.grid(column=1, row=2, padx=2, pady=2, sticky=W)
            
            self.intruder_speed = DoubleVar()
            speeds = data.specs.intruder_speed_array.tolist()
            self.intruder_speed.set(speeds[0])
            self.intruder_label = Label(self, text = "Select Intruder Speed (kts):", bg=self.bg)
            self.intruder_label.grid(column=0, row=3, padx=2, pady=2, sticky=W)
            self.intruder_box = ttk.Combobox(self, text = "Select Intruder speed value", textvariable=self.intruder_speed)
            self.intruder_box["values"] = speeds
            self.intruder_box.grid(column=1, row=3, padx=2, pady=2, sticky= W)
            
            self.display_plot_button = Button(self, text="Create Graph", command=lambda: self.controller.displayPerSpeedGraph(self.rpas_speed.get(), self.intruder_speed.get()))
            self.display_plot_button.grid(column=0, row=4, padx=2, pady=2, sticky= W)
        
            self.display_all_button = Button(self, text="Create All Graphs", command=self.controller.displayAllPerSpeedGraphs)
            self.display_all_button.grid(column=0, row=5, padx=2, pady=2, sticky= W)
            
class MultiSpeedPlotFrame(Frame):
    def __init__(self, controller, master, bg = "lime green"):
        Frame.__init__(self, master, bg=bg)
        self.bg = bg
        self.controller = controller
        
        self.back_button = Button(self,  text = "Back", command= lambda: controller.setActiveFrame("main_subframe"), font=("Ariel",12, "bold"))
        self.back_button.grid(column=0, row=0, padx=2, pady=2, sticky= W)
        
        self.title = Label(self, text = "3D Multispeed Plots", bg = bg, font=("Ariel",20, "bold"))
        self.title.grid(column=0, row=1,columnspan=3, padx=2, pady=2, sticky= W)
        
        self.regenerate()
        
        self.pack_propagate(0)
        self.grid_propagate(0)
        
    def update_speed_select(self):
        if self.speed_selection.get() == 0:
            speeds = self.data.specs.rpas_speed_array.tolist()
        elif self.speed_selection.get() == 1:
            speeds = self.data.specs.intruder_speed_array.tolist()
        self.speed_box["values"] = speeds
        self.speed.set(speeds[0])
        
            
    def create_graph(self):
        #RPAS Surface Graph
        if self.speed_selection.get() == 0 and self.graph_type_selection.get() == 0:
            self.controller.displayRPASSurfaceGraph(self.speed.get(), self.down_sample_factor.get())
        elif self.speed_selection.get() == 0 and self.graph_type_selection.get() == 1:
            self.controller.displayRPASLineGraph(self.speed.get(), self.down_sample_factor.get())
        elif self.speed_selection.get() == 1 and self.graph_type_selection.get() == 0:
            self.controller.displayIntruderSurfaceGraph(self.speed.get(), self.down_sample_factor.get())
        elif self.speed_selection.get() == 1 and self.graph_type_selection.get() == 1:
            self.controller.displayIntruderLineGraph(self.speed.get(), self.down_sample_factor.get())
    
    # def create_all_graphs(self):
        
            
        
        
    def regenerate(self):
        self.data = CurrentData()
        
        if self.data._sim_state != 0:
            self.rpas_speed = DoubleVar()
            
            self.select_speed_plot_label = Label(self, text="Observe 3D plot for a single given:", bg=self.bg, font=("Ariel",12, "bold"))
            self.select_speed_plot_label.grid(column=0, row= 2, columnspan=3,  sticky = W)
            
            self.speed_selection = IntVar(self, 0)
            
            self.rpas_radio_button = Radiobutton(self, text="RPAS Speed", variable=self.speed_selection, value = 0, command=self.update_speed_select, bg=self.bg)
            self.rpas_radio_button.grid(column=0, row = 3, sticky=W)
            
            self.intruder_radio_button = Radiobutton(self, text="Intruder Speed", variable=self.speed_selection, value = 1, command=self.update_speed_select, bg=self.bg)
            self.intruder_radio_button.grid(column=1, row=3, sticky=W)
            
            self.speed = DoubleVar()
            self.speed_label = Label(self, text = "Select Given Speed (kts):", bg=self.bg, font=("Ariel",12, "bold"))
            self.speed_label.grid(column=0, row=4, padx=2, pady=2, sticky=W, columnspan=2)
            self.speed_box = ttk.Combobox(self, text = "Select RPAS speed value", textvariable=self.speed)
            self.speed_box.grid(column=2, row=4, padx=2, pady=2, sticky=W)
            self.update_speed_select()
            
            self.select_speed_plot_label = Label(self, text="3D Graph Type:", bg=self.bg, font=("Ariel",12, "bold"))
            self.select_speed_plot_label.grid(column=0, row= 5, columnspan=2,  sticky = W)
            
            self.graph_type_selection = IntVar(self, 0)
            
            self.surface_radio_button = Radiobutton(self, text="Surface", variable=self.graph_type_selection, value = 0, bg=self.bg)
            self.surface_radio_button.grid(column=0, row = 6, sticky=W)
            
            self.lines_radio_button = Radiobutton(self, text="Line (Pass Fail)", variable=self.graph_type_selection, value = 1, bg=self.bg)
            self.lines_radio_button.grid(column=1, row=6, sticky=W)
            
            self.down_sample_factor = IntVar()
            self.down_sample_factor.set(Configuration().down_sample_factor)
            
            self.down_sample_factor_label = Label(self, text="Target Down Sample Factor:", bg=self.bg, font=("Ariel",10, "bold"))
            self.down_sample_factor_label.grid(column=0, row=7, columnspan=2, padx=2, pady=2, sticky=W)
            
            self.down_sample_factor_entry = Scale(self, from_=1, to=100, orient=HORIZONTAL, variable=self.down_sample_factor, bg=self.bg, bd=0, highlightthickness=0, length=400)
            self.down_sample_factor_entry.grid(column=2, row=7, columnspan=5, padx=2, pady=2, sticky=W)
            
            self.display_plot_button = Button(self, text="Create Graph", command=self.create_graph)
            self.display_plot_button.grid(column=0, row=8, padx=2, pady=10, sticky= W)
        
            # self.display_all_button = Button(self, text="Create All Graphs", command=self.controller.displayAllPerSpeedGraphs)
            # self.display_all_button.grid(column=0, row=5, padx=2, pady=2, sticky= W)

