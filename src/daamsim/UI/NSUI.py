from tkinter import *
from tkinter import ttk
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "data_classes"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "calculations"))
from Config import Configuration
from daa_spec import DaaSpec
from decimal import Decimal
import math_util

from NSController import new_sim_controller

class new_sim_UI(Frame):
    def __init__(self, controller, master, bg = "salmon"):
        Frame.__init__(self, master, bg=bg)
        self.controller = controller
        config = Configuration.get_instance()

        self.labels = dict()
        self.entries = dict()
        
        self.labels["Title"] = Label(self, text = "Run New Simulation", bg="salmon", font=("Ariel",20, "bold"))
        self.labels["Title"].grid(column = 0, row=0, columnspan=3, padx=2, pady=2, sticky = W)
        
        self.enterbutton = Button(self, text = "Run Simulation", command = controller.run_new_sim)
        self.enterbutton.grid(column=1, row=1, padx=5, pady=5, sticky=W)
        
        #ROV Variables
        
        self.labels["ROV_Vars"] = Label(self, text = "ROV Variables:", bg="salmon", font=("Ariel",15, "bold"))
        self.labels["ROV_Vars"].grid(column = 0, row=2, columnspan=3, padx=2, pady=2, sticky = W)
        
        self.labels["max_bank"] = Label(self, text = "ROV Max Bank (Deg):", bg="salmon")
        self.labels["max_bank"].grid(column = 1, row=3, padx=2, pady=2, sticky=W)
        self.entries["max_bank"] = Entry(self)
        self.entries["max_bank"].grid(column=2, row=3, padx=2, pady=2, sticky=W)
        self.entries["max_bank"].insert(0, config.daa_spec.max_bank)
        
        
        self.labels["range"] = Label(self, text = "ROV Sight Range (m):", bg="salmon")
        self.labels["range"].grid(column = 3, row=3, padx=2, pady=2, sticky=W)
        self.entries["range"] = Entry(self)
        self.entries["range"].grid(column=4, row=3, padx=2, pady=2, sticky=W)
        self.entries["range"].insert(0, config.daa_spec.range)
        
        self.labels["FOV"] = Label(self, text = "ROV FOV (Deg):", bg="salmon")
        self.labels["FOV"].grid(column = 1, row=5, padx=2, pady=2, sticky=W)
        self.entries["FOV"] = Entry(self)
        self.entries["FOV"].grid(column=2, row=5, padx=2, pady=2, sticky=W)
        self.entries["FOV"].insert(0, config.daa_spec.FOV)
        

        self.labels["ownsize"] = Label(self, text = "ROV Size (m):", bg="salmon")
        self.labels["ownsize"].grid(column = 3, row=5, padx=2, pady=2, sticky=W)
        self.entries["ownsize"] = Entry(self)
        self.entries["ownsize"].grid(column=4, row=5, padx=2, pady=2, sticky=W)
        self.entries["ownsize"].insert(0, config.daa_spec.ownsize)
        
        self.labels["ownspeed"] = Label(self, text = "ROV Size (kts):", bg="salmon")
        self.labels["ownspeed"].grid(column = 1, row=7, padx=2, pady=2, sticky=W)
        self.entries["ownspeed"] = Entry(self)
        self.entries["ownspeed"].grid(column=2, row=7, padx=2, pady=2, sticky=W)
        self.entries["ownspeed"].insert(0, config.daa_spec.ownsize)
        
        self.labels["ROV_Roll_Rate"] = Label(self, text = "ROV Roll Rate (deg/s):", bg="salmon")
        self.labels["ROV_Roll_Rate"].grid(column = 3, row=7, padx=2, pady=2, sticky=W)
        self.entries["ROV_Roll_Rate"] = Entry(self)
        self.entries["ROV_Roll_Rate"].grid(column=4, row=7, padx=2, pady=2, sticky=W)
        self.entries["ROV_Roll_Rate"].insert(0, config.daa_spec.max_roll_rate)
        
        self.labels["Intruder_Vars"] = Label(self, text = "Intruder Variables:", bg="salmon", font=("Ariel",15, "bold"))
        self.labels["Intruder_Vars"].grid(column = 0, row=9, columnspan=3, padx=2, pady=2, sticky = W)
        
        #Intruder Variables
        
        #Speed Array
        self.use_cust_intruder_speed = BooleanVar()
        self.use_cust_intruder_speed.set(config.custom_intruder_speed_enabled)
        
        self.entries["Cust_Intruder_Checkbox"] = Checkbutton(self, text="Use Custom Intruder Speed Array",variable=self.use_cust_intruder_speed, onvalue=True, offvalue=False, command=self.switch_cust_intruder_speed, bg="salmon")
        self.entries["Cust_Intruder_Checkbox"].grid(column=1, row=10, padx=2, pady=2, sticky=W)
        
        self.labels["min_intruder_speed"] = Label(self, text = "Minimum Intruder Speed (Inclusive):", bg="salmon")
        self.entries["min_intruder_speed"] = Entry(self)
        self.entries["min_intruder_speed"].insert(0, config.min_speed)
        
        self.labels["max_intruder_speed"] = Label(self, text = "Maximum Intruder Speed (Inclusive):", bg="salmon")
        self.entries["max_intruder_speed"] = Entry(self)
        self.entries["max_intruder_speed"].insert(0, config.max_speed)
        
        self.labels["intruder_speed_interval"] = Label(self, text = "Intruder Speed Array Interval:", bg="salmon")
        self.entries["intruder_speed_interval"] = Entry(self)
        self.entries["intruder_speed_interval"].insert(0, config.speed_interval)
        
        self.labels["custom_intruder_speed"] = Label(self, text = "Intruder Speed Custom Array:", bg="salmon")
        self.entries["custom_intruder_speed"] = Entry(self)
        self.entries["custom_intruder_speed"].insert(0, config.custom_intruder_speed_array)
        
        self.labels["custom_intruder_speed_instructions"] = Label(self, text = "Use commas to separate speeds", bg="salmon")
        
        self.labels["custom_intruder_speed_example"] = Label(self, text = "Ex: 10, 15, 20", bg="salmon")
        
        self.switch_cust_intruder_speed()
        
        
        #Azimuth Array
        self.use_cust_azimuth_array = BooleanVar()
        self.use_cust_azimuth_array.set(config.custom_vector_array_enabled)
        
        self.entries["Cust_Azimuth_Checkbox"] = Checkbutton(self, text="Use Custom Azimuth Array",variable=self.use_cust_azimuth_array, onvalue=True, offvalue=False, command=self.switch_cust_azimuth_array, bg="salmon")
        self.entries["Cust_Azimuth_Checkbox"].grid(column=1, row=14, padx=2, pady=2, sticky=W)
        
        self.labels["azimuth_vector_start"] = Label(self, text = "Azimuth Array Start (deg) (> -180):", bg="salmon")
        self.entries["azimuth_vector_start"] = Entry(self)
        self.entries["azimuth_vector_start"].insert(0, config.min_azimuth)
        
        self.labels["azimuth_vector_end"] = Label(self, text = "Azimuth Array End (deg) (< 180):", bg="salmon")
        self.entries["azimuth_vector_end"] = Entry(self)
        self.entries["azimuth_vector_end"].insert(0, config.max_azimuth)
        
        self.labels["azimuth_array_interval"] = Label(self, text = "Azimuth Array Interval:", bg="salmon")
        self.entries["azimuth_array_interval"] = Entry(self)
        self.entries["azimuth_array_interval"].insert(0, config.azimuth_interval)
        
        self.labels["custom_azimuth_array"] = Label(self, text = "Custom Azimuth Array:", bg="salmon")
        self.entries["custom_azimuth_array"] = Entry(self)
        self.entries["custom_azimuth_array"].insert(0, config.custom_azimuth_vector_array)
        
        self.labels["custom_azimuth_array_instructions"] = Label(self, text = "Use commas to separate entries", bg="salmon")
        
        self.labels["custom_azimuth_array_example"] = Label(self, text = "Ex: -90, 80, 90", bg="salmon")
        
        self.switch_cust_azimuth_array()
        
        #Simulation Variables
        self.labels["Simulation_Vars"] = Label(self, text = "Simulation Variables:", bg="salmon", font=("Ariel",15, "bold"))
        self.labels["Simulation_Vars"].grid(column = 0, row=18, columnspan=3, padx=5, pady=5, sticky = W)
        
        self.labels["time_resol"] = Label(self, text = "Time Resolution for approximation:", bg="salmon")
        self.labels["time_resol"].grid(column = 1, row=19, padx=2, pady=2, sticky=W)
        self.entries["time_resol"] = Entry(self)
        self.entries["time_resol"].grid(column=2, row=19, padx=2, pady=2, sticky=W)
        self.entries["time_resol"].insert(0, config.daa_spec.time_resol)
        
        self.labels["sigma_al"] = Label(self, text = "Sigma al:", bg="salmon")
        self.labels["sigma_al"].grid(column = 1, row=20, padx=2, pady=2, sticky=W)
        self.entries["sigma_al"] = Entry(self)
        self.entries["sigma_al"].grid(column=2, row=20, padx=2, pady=2, sticky=W)
        self.entries["sigma_al"].insert(0, config.daa_spec.sigma_al)
        
        self.labels["sigma_cross"] = Label(self, text = "Sigma cross:", bg="salmon")
        self.labels["sigma_cross"].grid(column = 1, row=21, padx=2, pady=2, sticky=W)
        self.entries["sigma_cross"] = Entry(self)
        self.entries["sigma_cross"].grid(column=2, row=21, padx=2, pady=2, sticky=W)
        self.entries["sigma_cross"].insert(0, config.daa_spec.sigma_cross)
        
        self.labels["DMOD"] = Label(self, text = "DMOD:", bg="salmon")
        self.labels["DMOD"].grid(column = 1, row=22, padx=2, pady=2, sticky=W)
        self.entries["DMOD"] = Entry(self)
        self.entries["DMOD"].grid(column=2, row=22, padx=2, pady=2, sticky=W)
        self.entries["DMOD"].insert(0, config.daa_spec.DMOD)
        
        self.labels["t_sim"] = Label(self, text = "t sim:", bg="salmon")
        self.labels["t_sim"].grid(column = 1, row=23, padx=2, pady=2, sticky=W)
        self.entries["t_sim"] = Entry(self)
        self.entries["t_sim"].grid(column=2, row=23, padx=2, pady=2, sticky=W)
        self.entries["t_sim"].insert(0, config.daa_spec.t_sim)
        
        self.labels["post_col"] = Label(self, text = "Post collision time (s):", bg="salmon")
        self.labels["post_col"].grid(column = 1, row=23, padx=2, pady=2, sticky=W)
        self.entries["post_col"] = Entry(self)
        self.entries["post_col"].grid(column=2, row=23, padx=2, pady=2, sticky=W)
        self.entries["post_col"].insert(0, config.daa_spec.post_col)
        
        self.labels["wind_speed"] = Label(self, text = "Wind speed (m/s):", bg="salmon")
        self.labels["wind_speed"].grid(column = 1, row=24, padx=2, pady=2, sticky=W)
        self.entries["wind_speed"] = Entry(self)
        self.entries["wind_speed"].grid(column=2, row=24, padx=2, pady=2, sticky=W)
        self.entries["wind_speed"].insert(0, config.daa_spec.wind_speed)
        
        self.labels["wind_dir"] = Label(self, text = "Wind direction:", bg="salmon")
        self.labels["wind_dir"].grid(column = 1, row=25, padx=2, pady=2, sticky=W)
        self.entries["wind_dir"] = Entry(self)
        self.entries["wind_dir"].grid(column=2, row=25, padx=2, pady=2, sticky=W)
        self.entries["wind_dir"].insert(0, config.daa_spec.wind_dir)
        
        self.labels["NDecimals"] = Label(self, text = "Rounding Alpha:", bg="salmon")
        self.labels["NDecimals"].grid(column = 1, row=26, padx=2, pady=2, sticky=W)
        self.entries["NDecimals"] = Entry(self)
        self.entries["NDecimals"].grid(column=2, row=26, padx=2, pady=2, sticky=W)
        self.entries["NDecimals"].insert(0, config.daa_spec.NDecimals)
        
        self.labels["sensor_rate"] = Label(self, text = "Rate of Revisit:", bg="salmon")
        self.labels["sensor_rate"].grid(column = 1, row=27, padx=2, pady=2, sticky=W)
        self.entries["sensor_rate"] = Entry(self)
        self.entries["sensor_rate"].grid(column=2, row=27, padx=2, pady=2, sticky=W)
        self.entries["sensor_rate"].insert(0, config.daa_spec.sensor_rate)
        
        self.labels["scans_track"] = Label(self, text = "# of scans needed to establish track:", bg="salmon")
        self.labels["scans_track"].grid(column = 1, row=28, padx=2, pady=2, sticky=W)
        self.entries["scans_track"] = Entry(self)
        self.entries["scans_track"].grid(column=2, row=28, padx=2, pady=2, sticky=W)
        self.entries["scans_track"].insert(0, config.daa_spec.scans_track)
        
        self.labels["t_warn"] = Label(self, text = "Time to give pilot to execute CA maneuver (s):", bg="salmon")
        self.labels["t_warn"].grid(column = 1, row=29, padx=2, pady=2, sticky=W)
        self.entries["t_warn"] = Entry(self)
        self.entries["t_warn"].grid(column=2, row=29, padx=2, pady=2, sticky=W)
        self.entries["t_warn"].insert(0, config.daa_spec.t_warn)

        self.pack_propagate(0)
        self.grid_propagate(0)
    
    """
    Switches which set of inputs are visible for the custom intruder speed array.
    """
    def switch_cust_intruder_speed(self):
        if (self.use_cust_intruder_speed.get()):
            self.enable_custom_intruder_speed_array()
        else:
            self.disable_custom_intruder_speed_array()
    
    
    def enable_custom_intruder_speed_array(self):  
        self.labels["min_intruder_speed"].grid_forget()
        self.entries["min_intruder_speed"].grid_forget()
        
        self.labels["max_intruder_speed"].grid_forget()
        self.entries["max_intruder_speed"].grid_forget()
        
        self.labels["intruder_speed_interval"].grid_forget()
        self.entries["intruder_speed_interval"].grid_forget()
        
        self.labels["custom_intruder_speed"].grid(column = 1, row=11, padx=2, pady=2, sticky=W)
        self.entries["custom_intruder_speed"].grid(column=2, row=11, padx=2, pady=2, sticky=W)
        
        self.labels["custom_intruder_speed_instructions"].grid(column = 1, row=12, columnspan=2, padx=2, pady=2, sticky=W)
        
        self.labels["custom_intruder_speed_example"].grid(column = 1, row=13, columnspan=2, padx=2, pady=2, sticky=W)
        
   
    def disable_custom_intruder_speed_array(self):
        self.labels["custom_intruder_speed"].grid_forget()
        self.entries["custom_intruder_speed"].grid_forget()
        
        self.labels["custom_intruder_speed_instructions"].grid_forget()
        
        self.labels["custom_intruder_speed_example"].grid_forget()
        
        self.labels["min_intruder_speed"].grid(column = 1, row=11, padx=2, pady=2, sticky=W)
        self.entries["min_intruder_speed"].grid(column=2, row=11, padx=2, pady=2, sticky=W)
        
        self.labels["max_intruder_speed"].grid(column = 1, row=12, padx=2, pady=2, sticky=W)
        self.entries["max_intruder_speed"].grid(column=2, row=12, padx=2, pady=2, sticky=W)
        
        self.labels["intruder_speed_interval"].grid(column = 1, row=13, padx=2, pady=2, sticky=W)
        self.entries["intruder_speed_interval"].grid(column=2, row=13, padx=2, pady=2, sticky=W)
        
        
    """
    Switches which set of inputs are visible for the custom intruder speed array.
    """
    def switch_cust_azimuth_array(self):
        if (self.use_cust_azimuth_array.get()):
            self.enable_custom_intruder_azimuth_array()
        else:
            self.disable_custom_intruder_azimuth_array()    
        
    def enable_custom_intruder_azimuth_array(self):
        self.labels["azimuth_vector_start"].grid_forget()
        self.entries["azimuth_vector_start"].grid_forget()
        
        self.labels["azimuth_vector_end"].grid_forget()
        self.entries["azimuth_vector_end"].grid_forget()
        
        self.labels["azimuth_array_interval"].grid_forget()
        self.entries["azimuth_array_interval"].grid_forget()
        
        self.labels["custom_azimuth_array"].grid(column = 1, row=15, padx=2, pady=2, sticky=W)
        self.entries["custom_azimuth_array"].grid(column=2, row=15, padx=2, pady=2, sticky=W)
        
        self.labels["custom_azimuth_array_instructions"].grid(column = 1, row=16, columnspan=2, padx=2, pady=2, sticky=W)
        
        self.labels["custom_azimuth_array_example"].grid(column = 1, row=17, columnspan=2, padx=2, pady=2, sticky=W)
        
   
    def disable_custom_intruder_azimuth_array(self):
        self.labels["custom_azimuth_array"].grid_forget()
        self.entries["custom_azimuth_array"].grid_forget()
        
        self.labels["custom_azimuth_array_instructions"].grid_forget()
        
        self.labels["custom_azimuth_array_example"].grid_forget()
        
        self.labels["azimuth_vector_start"].grid(column = 1, row=15, padx=2, pady=2, sticky=W)
        self.entries["azimuth_vector_start"].grid(column=2, row=15, padx=2, pady=2, sticky=W)
        
        self.labels["azimuth_vector_end"].grid(column = 1, row=16, padx=2, pady=2, sticky=W)
        self.entries["azimuth_vector_end"].grid(column=2, row=16, padx=2, pady=2, sticky=W)
        
        self.labels["azimuth_array_interval"].grid(column = 1, row=17, padx=2, pady=2, sticky=W)
        self.entries["azimuth_array_interval"].grid(column=2, row=17, padx=2, pady=2, sticky=W)
    
    def get_params(self):
        max_bank = Decimal(self.entries["max_bank"].get())
        range = Decimal(self.entries["range"].get())
        FOV = Decimal(self.entries["FOV"].get())
        ownsize = Decimal(self.entries["ownsize"].get())
        ownspeed = Decimal(self.entries["ownspeed"].get())
        max_roll_rate = Decimal(self.entries["ROV_Roll_Rate"].get())
        
        if(self.use_cust_intruder_speed.get()):
            intruder_speed_array = math_util.create_Cust_array(self.entries["custom_intruder_speed"].get())
        else:
            min_speed = Decimal(self.entries["min_intruder_speed"].get())
            max_speed = Decimal(self.entries["max_intruder_speed"].get())
            speed_interval = Decimal(self.entries["intruder_speed_interval"].get())
            intruder_speed_array = math_util.make_array(min_speed, max_speed, speed_interval)
            
        if(self.use_cust_azimuth_array.get()):
            azimuth_vector_array = math_util.create_Cust_array(self.entries["custom_azimuth_array"].get())
        else:
            min_azimuth = Decimal(self.entries["azimuth_vector_start"].get())
            max_azimuth = Decimal(self.entries["azimuth_vector_end"].get())
            azimuth_interval = Decimal(self.entries["azimuth_array_interval"].get())
            azimuth_vector_array = math_util.make_array(min_azimuth, max_azimuth, azimuth_interval)     
        
        time_resol = Decimal(self.entries["time_resol"].get())
        sigma_al = Decimal(self.entries["sigma_al"].get())
        sigma_cross = Decimal(self.entries["sigma_cross"].get())
        DMOD = Decimal(self.entries["DMOD"].get())
        t_sim = Decimal(self.entries["t_sim"].get())
        post_col = Decimal(self.entries["post_col"].get())
        wind_speed = Decimal(self.entries["wind_speed"].get())
        wind_dir = Decimal(self.entries["wind_dir"].get())
        NDecimals = int(self.entries["NDecimals"].get())
        sensor_rate = int(self.entries["sensor_rate"].get())
        scans_track = int(self.entries["scans_track"].get())
        t_warn = int(self.entries["t_warn"].get())
        
        params = DaaSpec(\
            max_bank=max_bank, \
            range=range,\
            FOV=FOV,\
            ownsize=ownsize,\
            ownspeed=ownspeed,\
            max_roll_rate=max_roll_rate, \
            azimuths=azimuth_vector_array, \
            intruder_speeds=intruder_speed_array, \
            time_resol = time_resol, \
            sigma_al=sigma_al, \
            sigma_cross= sigma_cross, \
            DMOD=DMOD, \
            t_sim=t_sim, \
            post_col=post_col, \
            wind_speed=wind_speed, \
            wind_dir=wind_dir, \
            NDecimals=NDecimals, \
            sensor_rate=sensor_rate, \
            scans_track=scans_track, \
            t_warn=t_warn)
        
        return params
        
        
        

    
        
    