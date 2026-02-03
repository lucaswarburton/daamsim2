from tkinter import *
from tkinter import ttk

from data_classes.current_data import CurrentData

class GMUIFrame(Frame):
    def __init__(self, controller, master, bg = "green"):
        Frame.__init__(self, master, bg=bg)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frames = dict()
        
        self.frames["main_subframe"] = MainSubFrame(controller=controller, master=self, bg=bg)
        self.frames["main_subframe"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["per_speed_sub_frame"] = PerSpeedSubFrame(controller=controller, master=self, bg=bg)
        self.frames["per_speed_sub_frame"].grid(row=0, column=0, sticky="nsew")
        
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
    def __init__(self, controller, master, bg = "green"):
        Frame.__init__(self, master, bg=bg)
        self.controller = controller
        self.bg = bg
        
        self.title = Label(self, text = "Select a graph type:", font=("Ariel",20, "bold"), padx=5, pady=5, bg=bg)
        self.title.grid(column=0, row=1, padx=5, pady=5, sticky= W)
        
        self.per_speed_graphs_button = Button(self, text="Per Speed Graphs", padx= 5, pady= 5, command= lambda: self.controller.setActiveFrame("per_speed_sub_frame"))
        self.per_speed_graphs_button.grid(column=0, row = 2, padx=5, pady=5, sticky= W)
        self.per_speed_graphs_label = Label(self, text = "(If grayed out, run new sim or load data)", padx=5, pady = 5, bg=bg)
        self.per_speed_graphs_label.grid(column=0, row=3, padx=5, pady=5, sticky= W)

    
    def lock_per_speed_button(self):
        self.per_speed_graphs_button.config(state=DISABLED)
    
    def unlock_per_speed_button(self):
        self.per_speed_graphs_button.config(state=NORMAL)
        
    def regenerate(self):
        data = CurrentData()
        match data._sim_state:
            case 0:
                self.lock_per_speed_button()
            case 1:
                self.unlock_per_speed_button()
        
    
class PerSpeedSubFrame(Frame):
    def __init__(self, controller, master, bg = "green"):
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

