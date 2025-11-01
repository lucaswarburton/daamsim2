from tkinter import *
from tkinter import ttk
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Config import Configuration

from NSController import new_sim_controller

class new_sim_UI(Frame):
    def __init__(self, controller, master, bg = "salmon"):
        Frame.__init__(self, master, bg=bg)
        self.controller = controller
        config = Configuration.get_instance()

        self.labels = dict()
        self.entries = dict()
        
        
        self.labels["Title"] = Label(self, text = "Run New Simulation", bg="salmon", font=("Ariel",20, "bold"))
        self.labels["Title"].grid(column = 0, row=0, columnspan=3, padx=5, pady=5, sticky = W)
        
        self.enterbutton = Button(self, text = "Run Simulation", command = controller.run_new_sim)
        self.enterbutton.grid(column=1, row=1, padx=5, pady=5, sticky=W)
        
        self.labels["max_bank"] = Label(self, text = "ROV Max Bank (Deg):", bg="salmon")
        self.labels["max_bank"].grid(column = 1, row=2, padx=2, pady=2, sticky=W)
        self.entries["max_bank"] = Entry(self)
        self.entries["max_bank"].grid(column=2, row=2, padx=2, pady=2, sticky=W)
        self.entries["max_bank"].insert(0, config.daa_spec.max_bank)
        
        
        self.labels["range"] = Label(self, text = "ROV Sight Range (m):", bg="salmon")
        self.labels["range"].grid(column = 1, row=3, padx=2, pady=2, sticky=W)
        self.entries["range"] = Entry(self)
        self.entries["range"].grid(column=2, row=3, padx=2, pady=2, sticky=W)
        self.entries["range"].insert(0, config.daa_spec.range)
        
        self.labels["FOV"] = Label(self, text = "ROV FOV (Deg):", bg="salmon")
        self.labels["FOV"].grid(column = 1, row=4, padx=2, pady=2, sticky=W)
        self.entries["FOV"] = Entry(self)
        self.entries["FOV"].grid(column=2, row=4, padx=2, pady=2, sticky=W)
        self.entries["FOV"].insert(0, config.daa_spec.FOV)
        

        self.labels["ownsize"] = Label(self, text = "ROV Size (m):", bg="salmon")
        self.labels["ownsize"].grid(column = 1, row=5, padx=2, pady=2, sticky=W)
        self.entries["ownsize"] = Entry(self)
        self.entries["ownsize"].grid(column=2, row=5, padx=2, pady=2, sticky=W)
        self.entries["ownsize"].insert(0, config.daa_spec.ownsize)
        
        self.labels["ownspeed"] = Label(self, text = "ROV Size (kts):", bg="salmon")
        self.labels["ownspeed"].grid(column = 1, row=6, padx=2, pady=2, sticky=W)
        self.entries["ownspeed"] = Entry(self)
        self.entries["ownspeed"].grid(column=2, row=6, padx=2, pady=2, sticky=W)
        self.entries["ownspeed"].insert(0, config.daa_spec.ownsize)
        
        # self.labels["max_roll_rate"] = Label(self, text = "ROV Roll Rate:")
        # self.labels["max_roll_rate"].grid(column = 1, row=7)
        
        # self.labels["cust_button"] = Label(self, text = "Use Custom Speed Array:")
        # self.labels["cust_button"].grid(column = 1, row=8)
        
        # self.labels["min_speed"] = Label(self, text = "ROV Min Speed (Inclusive):")
        # self.labels["min_speed"].grid(column = 1, row=9)
        
        # self.labels["max_speed"] = Label(self, text = "ROV Max Speed (Inclusive):")
        # self.labels["max_speed"].grid(column = 1, row=10)
        
        # self.labels["speed_interval"] = Label(self, text = "ROV Speed Array Interval:")
        # self.labels["speed_interval"].grid(column = 1, row=11)

        self.pack_propagate(0)
        self.grid_propagate(0)
        
    def get_params(self):
        self
    
    def enable_custom_intruder_speed_array(self):
        self
   
    def disable_custom_intruder_speed_array(self):
        self
        
    def enable_custom_intruder_azimuth_array(self):
        self
   
    def disable_custom_intruder_azimuth_array(self):
        self
        
if __name__ == "__main__":
    w = Tk()
    w.geometry("500x500+50+50")
    controller = new_sim_controller()
    frame = new_sim_UI(master=w, controller=controller)
    controller.setView(frame)
    frame.pack(side = LEFT, fill = "both", expand=True)
    w.mainloop()
    
        
    