import configparser
from pathlib import Path
import sys
import os
from data_classes.daa_spec import DaaSpec
from calculations import math_util



class Configuration:
    _instance = None
    _config_file_path = Path.cwd() / "config.ini"

    def __init__(self):
        self.parseConfig()

    def get_instance():
        if Configuration._instance == None:
            Configuration._instance =  Configuration()
        return Configuration._instance

    def parseConfig(self):
        parser = configparser.ConfigParser()
        parser.read(Configuration._config_file_path)
        
        self.valid_true_values = ["true", "t", "y", "yes"] #The valid inputs for true in the config file

        disable_ui = parser['Settings']['ui_disabled']
        disable_ui = disable_ui.lower()
        self.disable_ui = disable_ui in self.valid_true_values
        
        self.default_load_file_path = parser['Settings']['default_load_file_path']
        self.default_save_file_path = parser['Settings']['default_save_file_path']
            
        
        #Read RPAS Characteristics
        rpas_max_bank_deg = float(parser['DEFAULTS']['rpas_max_bank_deg'])
        rpas_wingspan = float(parser['DEFAULTS']['rpas_wingspan'])
        rpas_max_roll_rate = float(parser['DEFAULTS']['rpas_max_roll_rate'])
        rpas_speed_array = self.get_rpas_speed_array(parser)

        #Intruder Characteristics
        intruder_speed_array = self.get_intruder_speed_array(parser)

        #DAA Characteristics
        daa_declaration_range = float(parser['DEFAULTS']['daa_declaration_range'])
        daa_fov_deg = float(parser['DEFAULTS']['daa_fov_deg'])
        rate_of_revisit = int(parser['DEFAULTS']['rate_of_revisit'])
        scans_track = int(parser['DEFAULTS']['scans_track'])

        #Simulation Variables
        NDecimals = int(parser['DEFAULTS']['NDecimals'])
        time_resol = float(parser['DEFAULTS']['time_resol'])
        conflict_volume = float(parser['DEFAULTS']['conflict_volume'])
        t_sim = float(parser['DEFAULTS']['t_sim'])
        post_col = float(parser['DEFAULTS']['post_col'])
        wind_speed = float(parser['DEFAULTS']['wind_speed'])
        wind_dir = float(parser['DEFAULTS']['wind_dir'])
        human_factor_delay = int(parser['DEFAULTS']['human_factor_delay'])
        encounter_azimuth_array = self.get_encounter_azimuth_array(parser)
        
        self.daa_spec = DaaSpec(\
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
        
    def get_rpas_speed_array(self, parser):
        custom_rpas_speed_enabled = parser['Settings']['custom_rpas_speed_enabled']
        custom_rpas_speed_enabled = custom_rpas_speed_enabled.lower().strip()
        self.custom_rpas_speed_enabled = custom_rpas_speed_enabled in self.valid_true_values

        self.min_rpas_speed =  float(parser['DEFAULTS']['min_rpas_speed'])
        self.max_rpas_speed = float(parser['DEFAULTS']['max_rpas_speed'])
        self.rpas_speed_interval = float(parser['DEFAULTS']['rpas_speed_interval'])

        self.custom_rpas_speed_array = parser['DEFAULTS']['custom_rpas_speed_array']

        if self.custom_rpas_speed_enabled:
            rpas_speed_array = math_util.createCustArray(self.custom_rpas_speed_array)
        else:
            rpas_speed_array = math_util.make_array(self.min_rpas_speed, self.max_rpas_speed, self.rpas_speed_interval)
            
        return rpas_speed_array
        
    def get_intruder_speed_array(self, parser):
        custom_intruder_speed_enabled = parser['Settings']['custom_intruder_speed_enabled']
        custom_intruder_speed_enabled = custom_intruder_speed_enabled.lower().strip()
        self.custom_intruder_speed_enabled = custom_intruder_speed_enabled in self.valid_true_values

        self.custom_intruder_speed_array = parser['DEFAULTS']['custom_intruder_speed_array']
        self.min_intruder_speed =  float(parser['DEFAULTS']['min_intruder_speed'])
        self.max_intruder_speed = float(parser['DEFAULTS']['max_intruder_speed'])
        self.intruder_speed_interval = float(parser['DEFAULTS']['intruder_speed_interval'])
        
        if self.custom_intruder_speed_enabled:
            intruder_speed_array = math_util.createCustArray(self.custom_intruder_speed_array)
        else: 
            intruder_speed_array = math_util.make_array(self.min_intruder_speed, self.max_intruder_speed, self.intruder_speed_interval)

        return intruder_speed_array
        
    def get_encounter_azimuth_array(self, parser):
        custom_encounter_azimuth_array_enabled = parser['Settings']['custom_encounter_azimuth_array_enabled']
        custom_encounter_azimuth_array_enabled = custom_encounter_azimuth_array_enabled.lower().strip()
        self.custom_encounter_azimuth_array_enabled = custom_encounter_azimuth_array_enabled in self.valid_true_values

        self.custom_encounter_azimuth_array = parser['DEFAULTS']['custom_encounter_azimuth_array']
        self.encounter_azimuth_array_start =  float(parser['DEFAULTS']['encounter_azimuth_array_start'])
        self.encounter_azimuth_array_end = float(parser['DEFAULTS']['encounter_azimuth_array_end'])
        self.encounter_azimuth_array_interval = float(parser['DEFAULTS']['encounter_azimuth_array_interval'])
        
        if self.custom_encounter_azimuth_array_enabled:
            encounter_azimuth_array = math_util.createCustArray(self.custom_encounter_azimuth_array)
        else: 
            encounter_azimuth_array = math_util.make_array(self.encounter_azimuth_array_start, self.encounter_azimuth_array_end, self.encounter_azimuth_array_interval)

        return encounter_azimuth_array
        

        

        


 
        

        
        
        

