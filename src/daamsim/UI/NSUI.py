from tkinter import *
from tkinter import ttk
from daamsim.Config import Configuration
from data_classes.current_data import CurrentData
from data_classes.CurrentSettings import CurrentSettings
from data_classes.daa_spec import DaaSpec
from calculations import math_util
from daamsim.UI.ScrollFrame import Scroll_Frame
from daamsim.UI.NSController import new_sim_controller

class new_sim_UI(Scroll_Frame):
    def __init__(self, controller, master, bg = "salmon"):
        super().__init__(controller=controller, master = master, SCROLLFRAMETYPE=new_sim_UI_inner_frame,  bg=bg)
        self.bg = bg

class new_sim_UI_inner_frame(Frame):
    def __init__(self, controller, master, bg = "salmon"):
        super().__init__(master, bg=bg)
        self.bg = bg
        self.controller = controller

        self.labels = dict()
        self.entries = dict()
 
        
        self.cur_settings = CurrentSettings()
        self.config = Configuration.get_instance()
        
        self.regenerate()
        
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    
    def regenerate(self):
        self.clear()
        self.daa_spec = CurrentData().specs
        i = 0

        self.labels["Title"] = Label(self, text = "DAA Simulations (ARC-b)", bg=self.bg, font=("Ariel",20, "bold"))
        self.labels["Title"].grid(column = 0, row=i, columnspan=3, padx=2, pady=2, sticky = W)
        i += 1
        
        self.enterbutton = Button(self, text = "Run Simulation", command = self.controller.run_new_sim)
        self.enterbutton.grid(column=1, row=i, padx=5, pady=5, sticky=W)
        i += 1

        i = self.setup_rpas(i)

        i = self.setup_intruder_chars(i)

        i = self.setup_daa_chars(i)

        i = self.setup_simulation_vars(i)
        
    #Sets up characteristics inputs for RPAS
    def setup_rpas(self, i):
        self.labels["rpas_Chars"] = Label(self, text = "RPAS Characteristics:", bg=self.bg, font=("Ariel",15, "bold"))
        self.labels["rpas_Chars"].grid(column = 0, row=i, columnspan=3, padx=2, pady=2, sticky = W)
        i += 1

        self.labels["rpas_max_bank_deg"] = Label(self, text = "RPAS Max Bank (Deg):", bg=self.bg)
        self.labels["rpas_max_bank_deg"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["rpas_max_bank_deg"] = Entry(self)
        self.entries["rpas_max_bank_deg"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["rpas_max_bank_deg"].insert(0, self.daa_spec.rpas_max_bank_deg)
        i +=1

        self.labels["rpas_wingspan"] = Label(self, text = "RPAS Wingspan (m):", bg=self.bg)
        self.labels["rpas_wingspan"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["rpas_wingspan"] = Entry(self)
        self.entries["rpas_wingspan"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["rpas_wingspan"].insert(0, self.daa_spec.rpas_wingspan)
        i += 1

        self.labels["rpas_max_roll_rate"] = Label(self, text = "RPAS Max Roll Rate (deg/s):", bg=self.bg)
        self.labels["rpas_max_roll_rate"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["rpas_max_roll_rate"] = Entry(self)
        self.entries["rpas_max_roll_rate"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["rpas_max_roll_rate"].insert(0, self.daa_spec.rpas_max_roll_rate)
        i += 1

        self.use_cust_rpas_speed = BooleanVar()
        self.use_cust_rpas_speed.set(self.cur_settings.custom_rpas_speed_enabled)
        
        self.entries["Cust_RPAS_Checkbox"] = Checkbutton(self, text="Use Custom RPAS Speed Array", font=("Ariel", 10, "bold"),variable=self.use_cust_rpas_speed, onvalue=True, offvalue=False, command=self.switch_cust_rpas_speed, bg=self.bg)
        self.entries["Cust_RPAS_Checkbox"].grid(column=1, row=i, padx=2, pady=2, sticky=W)
        i += 1

        self.labels["min_rpas_speed"] = Label(self, text = "Minimum RPAS Speed (Inclusive) (kts):", bg=self.bg)
        self.entries["min_rpas_speed"] = Entry(self)
        self.entries["min_rpas_speed"].insert(0, self.cur_settings.min_rpas_speed)
        self.min_rpas_speed_row = i
        i += 1
        
        self.labels["max_rpas_speed"] = Label(self, text = "Maximum RPAS Speed (Inclusive) (kts):", bg=self.bg)
        self.entries["max_rpas_speed"] = Entry(self)
        self.entries["max_rpas_speed"].insert(0, self.cur_settings.max_rpas_speed)
        self.max_rpas_speed_row = i
        i += 1

        self.labels["rpas_speed_interval"] = Label(self, text = "RPAS Speed Array Interval (kts):", bg=self.bg)
        self.entries["rpas_speed_interval"] = Entry(self)
        self.entries["rpas_speed_interval"].insert(0, self.cur_settings.rpas_speed_interval)
        self.rpas_speed_interval_row = i
        i += 1

        self.labels["custom_rpas_speed_array"] = Label(self, text = "RPAS Speed Custom Array (kts):", bg=self.bg)
        self.entries["custom_rpas_speed_array"] = Entry(self)
        self.entries["custom_rpas_speed_array"].insert(0, self.cur_settings.custom_rpas_speed_array)

        self.labels["custom_rpas_speed_instructions"] = Label(self, text = "Use commas to separate speeds", bg=self.bg)
        
        self.labels["custom_rpas_speed_example"] = Label(self, text = "Ex: 10, 15, 20", bg=self.bg)
        
        self.switch_cust_rpas_speed()
        
        return i

    #Sets up intruder Characteristics inputs
    def setup_intruder_chars(self, i):
        self.labels["Intruder_Chars"] = Label(self, text = "Intruder Characteristics:", bg=self.bg, font=("Ariel",15, "bold"))
        self.labels["Intruder_Chars"].grid(column = 0, row=i, columnspan=3, padx=2, pady=2, sticky = W)
        i += 1

        self.use_cust_intruder_speed = BooleanVar()
        self.use_cust_intruder_speed.set(self.cur_settings.custom_intruder_speed_enabled)
        
        self.entries["Cust_Intruder_Checkbox"] = Checkbutton(self, text="Use Custom Intruder Speed Array", font=("Ariel", 10, "bold"), variable=self.use_cust_intruder_speed, onvalue=True, offvalue=False, command=self.switch_cust_intruder_speed, bg=self.bg)
        self.entries["Cust_Intruder_Checkbox"].grid(column=1, row=i, padx=2, pady=2, sticky=W)
        i += 1

        self.labels["min_intruder_speed"] = Label(self, text = "Minimum Intruder Speed (Inclusive) (kts):", bg=self.bg)
        self.entries["min_intruder_speed"] = Entry(self)
        self.entries["min_intruder_speed"].insert(0, self.cur_settings.min_intruder_speed)
        self.min_intruder_speed_row = i
        i += 1
        
        self.labels["max_intruder_speed"] = Label(self, text = "Maximum Intruder Speed (Inclusive) (kts):", bg=self.bg)
        self.entries["max_intruder_speed"] = Entry(self)
        self.entries["max_intruder_speed"].insert(0, self.cur_settings.max_intruder_speed)
        self.max_intruder_speed_row = i
        i += 1
        
        self.labels["intruder_speed_interval"] = Label(self, text = "Intruder Speed Array Interval (kts):", bg=self.bg)
        self.entries["intruder_speed_interval"] = Entry(self)
        self.entries["intruder_speed_interval"].insert(0, self.cur_settings.intruder_speed_interval)
        self.intruder_speed_interval_row = i
        i += 1
        
        self.labels["custom_intruder_speed_array"] = Label(self, text = "Intruder Speed Custom Array (kts):", bg=self.bg)
        self.entries["custom_intruder_speed_array"] = Entry(self)
        self.entries["custom_intruder_speed_array"].insert(0, self.cur_settings.custom_intruder_speed_array)
        
        self.labels["custom_intruder_speed_instructions"] = Label(self, text = "Use commas to separate speeds", bg=self.bg)
        
        self.labels["custom_intruder_speed_example"] = Label(self, text = "Ex: 10, 15, 20", bg=self.bg)
        
        self.switch_cust_intruder_speed()
        return i

    #Setup daa Characteristics
    def setup_daa_chars(self, i):
        self.labels["DAA_Chars"] = Label(self, text = "DAA Characteristics:", bg=self.bg, font=("Ariel",15, "bold"))
        self.labels["DAA_Chars"].grid(column = 0, row=i, columnspan=3, padx=5, pady=5, sticky = W)
        i += 1

        self.labels["daa_declaration_range"] = Label(self, text = "DAA Sensor Declaration Range (m):", bg=self.bg)
        self.labels["daa_declaration_range"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["daa_declaration_range"] = Entry(self)
        self.entries["daa_declaration_range"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["daa_declaration_range"].insert(0, self.daa_spec.daa_declaration_range)
        i += 1
        
        self.labels["daa_fov_deg"] = Label(self, text = "DAA Horizontal FOV (Deg):", bg=self.bg)
        self.labels["daa_fov_deg"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["daa_fov_deg"] = Entry(self)
        self.entries["daa_fov_deg"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["daa_fov_deg"].insert(0, self.daa_spec.daa_fov_deg)
        i += 1

        self.labels["rate_of_revisit"] = Label(self, text = "Rate of Revisit (s):", bg=self.bg)
        self.labels["rate_of_revisit"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["rate_of_revisit"] = Entry(self)
        self.entries["rate_of_revisit"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["rate_of_revisit"].insert(0, self.daa_spec.rate_of_revisit)
        i += 1

        self.labels["scans_track"] = Label(self, text = "Scans to establish track:", bg=self.bg)
        self.labels["scans_track"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["scans_track"] = Entry(self)
        self.entries["scans_track"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["scans_track"].insert(0, self.daa_spec.scans_track)
        i += 1

        return i
        
    
    def setup_simulation_vars(self, i):    
        #Simulation Variables
        self.labels["Simulation_Vars"] = Label(self, text = "Simulation Variables:", bg=self.bg, font=("Ariel",15, "bold"))
        self.labels["Simulation_Vars"].grid(column = 0, row=i, columnspan=3, padx=5, pady=5, sticky = W)
        i += 1

        #Remove this later
        self.labels["NDecimals"] = Label(self, text = "Rounding Alpha:", bg=self.bg)
        self.labels["NDecimals"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["NDecimals"] = Entry(self)
        self.entries["NDecimals"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["NDecimals"].insert(0, self.daa_spec.NDecimals)
        i += 1
        
        self.labels["time_resol"] = Label(self, text = "Time Resolution (s):", bg=self.bg)
        self.labels["time_resol"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["time_resol"] = Entry(self)
        self.entries["time_resol"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["time_resol"].insert(0, self.daa_spec.time_resol)
        i += 1

        self.labels["conflict_volume"] = Label(self, text = "Horizontal Conflict Volume (m):", bg=self.bg)
        self.labels["conflict_volume"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["conflict_volume"] = Entry(self)
        self.entries["conflict_volume"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["conflict_volume"].insert(0, self.daa_spec.conflict_volume)
        i += 1

        self.labels["t_sim"] = Label(self, text = "Simulation Duration (s):", bg=self.bg)
        self.labels["t_sim"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["t_sim"] = Entry(self)
        self.entries["t_sim"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["t_sim"].insert(0, self.daa_spec.t_sim)
        i += 1

        self.labels["post_col"] = Label(self, text = "Post collision time (s):", bg=self.bg)
        self.labels["post_col"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["post_col"] = Entry(self)
        self.entries["post_col"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["post_col"].insert(0, self.daa_spec.post_col)
        i += 1

        self.labels["wind_speed"] = Label(self, text = "Wind speed (m/s):", bg=self.bg)
        self.labels["wind_speed"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["wind_speed"] = Entry(self)
        self.entries["wind_speed"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["wind_speed"].insert(0, self.daa_spec.wind_speed)
        i += 1
        
        self.labels["wind_dir"] = Label(self, text = "Wind direction (deg):", bg=self.bg)
        self.labels["wind_dir"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["wind_dir"] = Entry(self)
        self.entries["wind_dir"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["wind_dir"].insert(0, self.daa_spec.wind_dir)
        i += 1

        self.labels["human_factor_delay"] = Label(self, text = "Delay (s):", bg=self.bg)
        self.labels["human_factor_delay"].grid(column = 1, row=i, padx=2, pady=2, sticky=W)
        self.entries["human_factor_delay"] = Entry(self)
        self.entries["human_factor_delay"].grid(column=2, row=i, padx=2, pady=2, sticky=W)
        self.entries["human_factor_delay"].insert(0, self.daa_spec.human_factor_delay)
        i += 1
        
        #Azimuth Array
        self.use_cust_azimuth_array = BooleanVar()
        self.use_cust_azimuth_array.set(self.cur_settings.custom_encounter_azimuth_array_enabled)
        
        self.entries["Cust_Azimuth_Checkbox"] = Checkbutton(self, text="Use Custom Encounter Azimuth Array", font=("Ariel", 10, "bold"), variable=self.use_cust_azimuth_array, onvalue=True, offvalue=False, command=self.switch_cust_azimuth_array, bg=self.bg)
        self.entries["Cust_Azimuth_Checkbox"].grid(column=1, row=i, padx=2, pady=2, sticky=W)
        i += 1
        
        self.labels["encounter_azimuth_array_start"] = Label(self, text = "Encounter Azimuth Array Start (deg) (> -180):", bg=self.bg)
        self.entries["encounter_azimuth_array_start"] = Entry(self)
        self.entries["encounter_azimuth_array_start"].insert(0, self.cur_settings.encounter_azimuth_array_start)
        self.azimuth_start_row = i
        i += 1
        
        self.labels["encounter_azimuth_array_end"] = Label(self, text = "Encounter Azimuth Array End (deg) (< 180):", bg=self.bg)
        self.entries["encounter_azimuth_array_end"] = Entry(self)
        self.entries["encounter_azimuth_array_end"].insert(0, self.cur_settings.encounter_azimuth_array_end)
        self.azimuth_end_row = i
        i += 1

        self.labels["encounter_azimuth_array_interval"] = Label(self, text = "Encounter Azimuth Array Interval (deg):", bg=self.bg)
        self.entries["encounter_azimuth_array_interval"] = Entry(self)
        self.entries["encounter_azimuth_array_interval"].insert(0, self.cur_settings.encounter_azimuth_array_interval)
        self.azimuth_interval_row = i
        i += 1

        self.labels["custom_encounter_azimuth_array"] = Label(self, text = "Custom Encounter Azimuth Array (deg):", bg=self.bg)
        self.entries["custom_encounter_azimuth_array"] = Entry(self)
        self.entries["custom_encounter_azimuth_array"].insert(0, self.cur_settings.custom_encounter_azimuth_array)
        
        self.labels["custom_azimuth_array_instructions"] = Label(self, text = "Use commas to separate entries", bg=self.bg)
        
        self.labels["custom_azimuth_array_example"] = Label(self, text = "Ex: -90, 80, 90", bg=self.bg)
        
        self.switch_cust_azimuth_array()

        return i
        

        
    
    #Switches which set of inputs are visible for the custom intruder speed array.
    def switch_cust_rpas_speed(self):
        if (self.use_cust_rpas_speed.get()):
            self.enable_custom_rpas_speed_array()
        else:
            self.disable_custom_rpas_speed_array()
    
    
    def enable_custom_rpas_speed_array(self):  
        self.labels["min_rpas_speed"].grid_forget()
        self.entries["min_rpas_speed"].grid_forget()
        
        self.labels["max_rpas_speed"].grid_forget()
        self.entries["max_rpas_speed"].grid_forget()
        
        self.labels["rpas_speed_interval"].grid_forget()
        self.entries["rpas_speed_interval"].grid_forget()
        
        self.labels["custom_rpas_speed_array"].grid(column = 1, row=self.min_rpas_speed_row, padx=2, pady=2, sticky=W)
        self.entries["custom_rpas_speed_array"].grid(column=2, row=self.min_rpas_speed_row, padx=2, pady=2, sticky=W)
        
        self.labels["custom_rpas_speed_instructions"].grid(column = 1, row=self.max_rpas_speed_row, columnspan=2, padx=2, pady=2, sticky=W)
        
        self.labels["custom_rpas_speed_example"].grid(column = 1, row=self.rpas_speed_interval_row, columnspan=2, padx=2, pady=2, sticky=W)
        
   
    def disable_custom_rpas_speed_array(self):
        self.labels["custom_rpas_speed_array"].grid_forget()
        self.entries["custom_rpas_speed_array"].grid_forget()
        
        self.labels["custom_rpas_speed_instructions"].grid_forget()
        
        self.labels["custom_rpas_speed_example"].grid_forget()
        
        self.labels["min_rpas_speed"].grid(column = 1, row=self.min_rpas_speed_row, padx=2, pady=2, sticky=W)
        self.entries["min_rpas_speed"].grid(column=2, row=self.min_rpas_speed_row, padx=2, pady=2, sticky=W)
        
        self.labels["max_rpas_speed"].grid(column = 1, row=self.max_rpas_speed_row, padx=2, pady=2, sticky=W)
        self.entries["max_rpas_speed"].grid(column=2, row=self.max_rpas_speed_row, padx=2, pady=2, sticky=W)
        
        self.labels["rpas_speed_interval"].grid(column = 1, row=self.rpas_speed_interval_row, padx=2, pady=2, sticky=W)
        self.entries["rpas_speed_interval"].grid(column=2, row=self.rpas_speed_interval_row, padx=2, pady=2, sticky=W)
        


    
    #Switches which set of inputs are visible for the custom intruder speed array.
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
        
        self.labels["custom_intruder_speed_array"].grid(column = 1, row=self.min_intruder_speed_row, padx=2, pady=2, sticky=W)
        self.entries["custom_intruder_speed_array"].grid(column=2, row=self.min_intruder_speed_row, padx=2, pady=2, sticky=W)
        
        self.labels["custom_intruder_speed_instructions"].grid(column = 1, row=self.max_intruder_speed_row, columnspan=2, padx=2, pady=2, sticky=W)
        
        self.labels["custom_intruder_speed_example"].grid(column = 1, row=self.intruder_speed_interval_row, columnspan=2, padx=2, pady=2, sticky=W)
        
   
    def disable_custom_intruder_speed_array(self):
        self.labels["custom_intruder_speed_array"].grid_forget()
        self.entries["custom_intruder_speed_array"].grid_forget()
        
        self.labels["custom_intruder_speed_instructions"].grid_forget()
        
        self.labels["custom_intruder_speed_example"].grid_forget()
        
        self.labels["min_intruder_speed"].grid(column = 1, row=self.min_intruder_speed_row, padx=2, pady=2, sticky=W)
        self.entries["min_intruder_speed"].grid(column=2, row=self.min_intruder_speed_row, padx=2, pady=2, sticky=W)
        
        self.labels["max_intruder_speed"].grid(column = 1, row=self.max_intruder_speed_row, padx=2, pady=2, sticky=W)
        self.entries["max_intruder_speed"].grid(column=2, row=self.max_intruder_speed_row, padx=2, pady=2, sticky=W)
        
        self.labels["intruder_speed_interval"].grid(column = 1, row=self.intruder_speed_interval_row, padx=2, pady=2, sticky=W)
        self.entries["intruder_speed_interval"].grid(column=2, row=self.intruder_speed_interval_row, padx=2, pady=2, sticky=W)
        
        
    #Switches which set of inputs are visible for the custom intruder speed array.
    def switch_cust_azimuth_array(self):
        if (self.use_cust_azimuth_array.get()):
            self.enable_custom_encounter_azimuth_array()
        else:
            self.disable_custom_encounter_azimuth_array()    
        
    def enable_custom_encounter_azimuth_array(self):
        self.labels["encounter_azimuth_array_start"].grid_forget()
        self.entries["encounter_azimuth_array_start"].grid_forget()
        
        self.labels["encounter_azimuth_array_end"].grid_forget()
        self.entries["encounter_azimuth_array_end"].grid_forget()
        
        self.labels["encounter_azimuth_array_interval"].grid_forget()
        self.entries["encounter_azimuth_array_interval"].grid_forget()
        
        self.labels["custom_encounter_azimuth_array"].grid(column = 1, row=self.azimuth_start_row, padx=2, pady=2, sticky=W)
        self.entries["custom_encounter_azimuth_array"].grid(column=2, row=self.azimuth_start_row, padx=2, pady=2, sticky=W)
        
        self.labels["custom_azimuth_array_instructions"].grid(column = 1, row=self.azimuth_end_row, columnspan=2, padx=2, pady=2, sticky=W)
        
        self.labels["custom_azimuth_array_example"].grid(column = 1, row=self.azimuth_interval_row, columnspan=2, padx=2, pady=2, sticky=W)
        
   
    def disable_custom_encounter_azimuth_array(self):
        self.labels["custom_encounter_azimuth_array"].grid_forget()
        self.entries["custom_encounter_azimuth_array"].grid_forget()
        
        self.labels["custom_azimuth_array_instructions"].grid_forget()
        
        self.labels["custom_azimuth_array_example"].grid_forget()
        
        self.labels["encounter_azimuth_array_start"].grid(column = 1, row=self.azimuth_start_row, padx=2, pady=2, sticky=W)
        self.entries["encounter_azimuth_array_start"].grid(column=2, row=self.azimuth_start_row, padx=2, pady=2, sticky=W)
        
        self.labels["encounter_azimuth_array_end"].grid(column = 1, row=self.azimuth_end_row, padx=2, pady=2, sticky=W)
        self.entries["encounter_azimuth_array_end"].grid(column=2, row=self.azimuth_end_row, padx=2, pady=2, sticky=W)
        
        self.labels["encounter_azimuth_array_interval"].grid(column = 1, row=self.azimuth_interval_row, padx=2, pady=2, sticky=W)
        self.entries["encounter_azimuth_array_interval"].grid(column=2, row=self.azimuth_interval_row, padx=2, pady=2, sticky=W)
    
    def get_params(self):
        #Read RPAS Characteristics
        rpas_max_bank_deg = float(self.entries["rpas_max_bank_deg"].get())
        rpas_wingspan = float(self.entries["rpas_wingspan"].get())
        rpas_max_roll_rate = float(self.entries["rpas_max_roll_rate"].get())

        if(self.use_cust_rpas_speed.get()):
            rpas_speed_array = math_util.createCustArray(self.entries["custom_rpas_speed_array"].get())
        else:
            min_speed = float(self.entries["min_rpas_speed"].get())
            max_speed = float(self.entries["max_rpas_speed"].get())
            speed_interval = float(self.entries["rpas_speed_interval"].get())
            rpas_speed_array = math_util.make_array(min_speed, max_speed, speed_interval)

        #Read Intruder Chars
        if(self.use_cust_intruder_speed.get()):
            intruder_speed_array = math_util.createCustArray(self.entries["custom_intruder_speed_array"].get())
        else:
            min_speed = float(self.entries["min_intruder_speed"].get())
            max_speed = float(self.entries["max_intruder_speed"].get())
            speed_interval = float(self.entries["intruder_speed_interval"].get())
            intruder_speed_array = math_util.make_array(min_speed, max_speed, speed_interval)
             
        #Read DAA Chars
        daa_declaration_range = float(self.entries["daa_declaration_range"].get())
        daa_fov_deg = float(self.entries["daa_fov_deg"].get())
        rate_of_revisit = int(self.entries["rate_of_revisit"].get())
        scans_track = int(self.entries["scans_track"].get())
 
        #Read Simulation Variables
        time_resol = float(self.entries["time_resol"].get())
        conflict_volume = float(self.entries["conflict_volume"].get())
        t_sim = float(self.entries["t_sim"].get())
        post_col = float(self.entries["post_col"].get())
        wind_speed = float(self.entries["wind_speed"].get())
        wind_dir = float(self.entries["wind_dir"].get())
        NDecimals = int(self.entries["NDecimals"].get())
        human_factor_delay = int(self.entries["human_factor_delay"].get())

        if(self.use_cust_azimuth_array.get()):
            encounter_azimuth_array = math_util.createCustArray(self.entries["custom_encounter_azimuth_array"].get())
        else:
            min_azimuth = float(self.entries["encounter_azimuth_array_start"].get())
            max_azimuth = float(self.entries["encounter_azimuth_array_end"].get())
            azimuth_interval = float(self.entries["encounter_azimuth_array_interval"].get())
            encounter_azimuth_array = math_util.make_array(min_azimuth, max_azimuth, azimuth_interval)     
        
        
        params = DaaSpec(\
            rpas_max_bank_deg = rpas_max_bank_deg, \
            rpas_wingspan = rpas_wingspan, \
            rpas_max_roll_rate = rpas_max_roll_rate, \
            rpas_speed_array = rpas_speed_array, \
            intruder_speed_array = intruder_speed_array, \
            daa_declaration_range = daa_declaration_range, \
            daa_fov_deg = daa_fov_deg, \
            rate_of_revisit = rate_of_revisit, \
            scans_track = scans_track, \
            NDecimals = NDecimals, \
            time_resol = time_resol, \
            conflict_volume = conflict_volume, \
            t_sim = t_sim, \
            post_col = post_col, \
            wind_speed = wind_speed, \
            wind_dir = wind_dir, \
            human_factor_delay = human_factor_delay, \
            encounter_azimuth_array = encounter_azimuth_array
            )
        
        return params
    
    def save_current_settings(self):  
        self.cur_settings.custom_rpas_speed_enabled = self.use_cust_rpas_speed.get()
        self.cur_settings.min_rpas_speed =  self.entries["min_rpas_speed"].get()
        self.cur_settings.max_rpas_speed = self.entries["max_rpas_speed"].get()
        self.cur_settings.rpas_speed_interval = self.entries["rpas_speed_interval"].get()
        self.cur_settings.custom_rpas_speed_array = self.entries["custom_rpas_speed_array"].get()
        
        self.cur_settings.custom_intruder_speed_enabled = self.use_cust_intruder_speed.get()
        self.cur_settings.custom_intruder_speed_array = self.entries["custom_intruder_speed_array"].get()
        self.cur_settings.min_intruder_speed =  self.entries["min_intruder_speed"].get()
        self.cur_settings.max_intruder_speed = self.entries["max_intruder_speed"].get()
        self.cur_settings.intruder_speed_interval = self.entries["intruder_speed_interval"].get()
        
        self.cur_settings.custom_encounter_azimuth_array_enabled = self.use_cust_azimuth_array.get()
        self.cur_settings.custom_encounter_azimuth_array = self.entries["custom_encounter_azimuth_array"].get()
        self.cur_settings.encounter_azimuth_array_start =  self.entries["encounter_azimuth_array_start"].get()
        self.cur_settings.encounter_azimuth_array_end = self.entries["encounter_azimuth_array_end"].get()
        self.cur_settings.encounter_azimuth_array_interval = self.entries["encounter_azimuth_array_interval"].get()

        
        
        
if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    controller = new_sim_controller(None)

    scr_fr = new_sim_UI(controller=controller, master=root)
    scr_fr.pack(fill=BOTH, expand=1)
    


    root.mainloop()
    
        
    