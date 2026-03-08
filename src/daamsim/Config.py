import configparser
from pathlib import Path
import numpy as np

from data_classes.DaaSpec import DaaSpec
from calculations import math_util



class Configuration:
    _instance = None
    _config_file_path = Path.cwd() / "config.ini"
    
    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.parseConfig()

    def parseConfig(self) -> None:
        parser = configparser.ConfigParser()
        parser.read(Configuration._config_file_path)
        
        self.valid_true_values = ["true", "t", "y", "yes"] #The valid inputs for true in the config file

        disable_ui = parser['Settings']['ui_disabled']
        disable_ui = disable_ui.lower()
        self.disable_ui = disable_ui in self.valid_true_values
        
        self.default_load_file_path = parser['Settings']['default_load_file_path']
        self.default_save_file_path = parser['Settings']['default_save_file_path']
        self.default_prob_dist_file = parser['Settings']['default_prob_dist_file_path']
            
        
        #Read RPAS Characteristics
        rpas_max_bank_deg = float(parser['DAA Defaults']['rpas_max_bank_deg'])
        rpas_wingspan = float(parser['DAA Defaults']['rpas_wingspan'])
        rpas_max_roll_rate = float(parser['DAA Defaults']['rpas_max_roll_rate'])
        rpas_speed_array = self.get_rpas_speed_array(parser)

        #Intruder Characteristics
        intruder_detection_thresh_arc_min = float(parser['DAA Defaults']['intruder_detection_thresh_arc_min'])
        intruder_maneuver_delay = float(parser['DAA Defaults']['intruder_maneuver_delay'])
        intruder_speed_array = self.get_intruder_speed_array(parser)

        #DAA Characteristics
        daa_declaration_range = float(parser['DAA Defaults']['daa_declaration_range'])
        daa_fov_deg = float(parser['DAA Defaults']['daa_fov_deg'])
        rate_of_revisit = int(parser['DAA Defaults']['rate_of_revisit'])
        scans_track = int(parser['DAA Defaults']['scans_track'])

        #Simulation Variables
        NDecimals = int(parser['DAA Defaults']['NDecimals'])
        time_resol = float(parser['DAA Defaults']['time_resol'])
        conflict_volume = float(parser['DAA Defaults']['conflict_volume'])
        t_sim = float(parser['DAA Defaults']['t_sim'])
        post_col = float(parser['DAA Defaults']['post_col'])
        wind_speed = float(parser['DAA Defaults']['wind_speed'])
        wind_dir = float(parser['DAA Defaults']['wind_dir'])
        human_factor_delay = int(parser['DAA Defaults']['human_factor_delay'])
        encounter_azimuth_array = self.get_encounter_azimuth_array(parser)
        
        #Other Defaults
        self.down_sample_factor = int(parser['Other Defaults']['down_sample_factor'])
        
        self.daa_spec = DaaSpec(\
            rpas_max_bank_deg = rpas_max_bank_deg, \
            rpas_wingspan = rpas_wingspan, \
            rpas_max_roll_rate = rpas_max_roll_rate, \
            rpas_speed_array = rpas_speed_array, \
            intruder_detection_thresh_arc_min = intruder_detection_thresh_arc_min, \
            intruder_maneuver_delay = intruder_maneuver_delay, \
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
        
    def get_rpas_speed_array(self, parser:configparser.ConfigParser)-> np.ndarray:
        custom_rpas_speed_enabled = parser['Settings']['custom_rpas_speed_enabled']
        custom_rpas_speed_enabled = custom_rpas_speed_enabled.lower().strip()
        self.custom_rpas_speed_enabled = custom_rpas_speed_enabled in self.valid_true_values

        self.min_rpas_speed =  float(parser['DAA Defaults']['min_rpas_speed'])
        self.max_rpas_speed = float(parser['DAA Defaults']['max_rpas_speed'])
        self.rpas_speed_interval = float(parser['DAA Defaults']['rpas_speed_interval'])

        self.custom_rpas_speed_array = parser['DAA Defaults']['custom_rpas_speed_array']

        if self.custom_rpas_speed_enabled:
            rpas_speed_array = math_util.createCustArray(self.custom_rpas_speed_array)
        if self.custom_rpas_speed_enabled:
            rpas_speed_array = math_util.createCustArray(self.custom_rpas_speed_array)
        else:
            rpas_speed_array = math_util.make_array(self.min_rpas_speed, self.max_rpas_speed, self.rpas_speed_interval)
            rpas_speed_array = math_util.make_array(self.min_rpas_speed, self.max_rpas_speed, self.rpas_speed_interval)
            
        return rpas_speed_array
        
    def get_intruder_speed_array(self, parser:configparser.ConfigParser)-> np.ndarray:
        custom_intruder_speed_enabled = parser['Settings']['custom_intruder_speed_enabled']
        custom_intruder_speed_enabled = custom_intruder_speed_enabled.lower().strip()
        self.custom_intruder_speed_enabled = custom_intruder_speed_enabled in self.valid_true_values

        self.custom_intruder_speed_array = parser['DAA Defaults']['custom_intruder_speed_array']
        self.min_intruder_speed =  float(parser['DAA Defaults']['min_intruder_speed'])
        self.max_intruder_speed = float(parser['DAA Defaults']['max_intruder_speed'])
        self.intruder_speed_interval = float(parser['DAA Defaults']['intruder_speed_interval'])
        
        if self.custom_intruder_speed_enabled:
            intruder_speed_array = math_util.createCustArray(self.custom_intruder_speed_array)
        else: 
            intruder_speed_array = math_util.make_array(self.min_intruder_speed, self.max_intruder_speed, self.intruder_speed_interval)

        return intruder_speed_array
        
    def get_encounter_azimuth_array(self, parser:configparser.ConfigParser)-> np.ndarray:
        custom_encounter_azimuth_array_enabled = parser['Settings']['custom_encounter_azimuth_array_enabled']
        custom_encounter_azimuth_array_enabled = custom_encounter_azimuth_array_enabled.lower().strip()
        self.custom_encounter_azimuth_array_enabled = custom_encounter_azimuth_array_enabled in self.valid_true_values

        self.custom_encounter_azimuth_array = parser['DAA Defaults']['custom_encounter_azimuth_array']
        self.encounter_azimuth_array_start =  float(parser['DAA Defaults']['encounter_azimuth_array_start'])
        self.encounter_azimuth_array_end = float(parser['DAA Defaults']['encounter_azimuth_array_end'])
        self.encounter_azimuth_array_interval = float(parser['DAA Defaults']['encounter_azimuth_array_interval'])
        
        if self.custom_encounter_azimuth_array_enabled:
            encounter_azimuth_array = math_util.createCustArray(self.custom_encounter_azimuth_array)
        else: 
            encounter_azimuth_array = math_util.make_array(self.encounter_azimuth_array_start, self.encounter_azimuth_array_end, self.encounter_azimuth_array_interval)

        return encounter_azimuth_array
        

        

        


 
        

        
        
        

