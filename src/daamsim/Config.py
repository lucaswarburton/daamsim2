import configparser
from pathlib import Path
from decimal import Decimal
from data_classes.daa_spec import daa_spec

class Configuration:
    _instance = None
    _config_file_path = Path.cwd() / "config.ini"

    def __init__(self):
        self.daa_spec = daa_spec()
        self.parseConfig()

    def get_instance():
        if Configuration._instance == None:
            Configuration._instance =  Configuration()
        return Configuration._instance

    def parseConfig(self):
        parser = configparser.ConfigParser()
        parser.read(Configuration._config_file_path)

        disable_ui = parser['Settings']['ui_disabled']
        disable_ui = disable_ui.lower()

        self.disable_ui = disable_ui == 'true' or   disable_ui == 't' or disable_ui == 'y' or disable_ui == 'yes'
        self.default_file_path = parser['Settings']['default_file_path']
        
        custom_intruder_speed_enabled = parser['Settings']['custom_intruder_speed_enabled']
        custom_intruder_speed_enabled = custom_intruder_speed_enabled.lower()
        
        #Get default intruder speed array
        if custom_intruder_speed_enabled == 'true' or custom_intruder_speed_enabled == 't' or custom_intruder_speed_enabled == 'y' or custom_intruder_speed_enabled == 'yes':
            self.daa_spec.intruder_speed_array = daa_spec.createCustArray(parser['DEFAULTS']['custom_intruder_speed_array'])
        else:
            #Set default intruder speed array
            min_speed =  Decimal(parser['DEFAULTS']['min_intruder_speed'])
            max_speed = Decimal(parser['DEFAULTS']['max_intruder_speed'])
            speed_interval = Decimal(parser['DEFAULTS']['intruder_speed_interval'])
            self.daa_spec.intruder_speed_array = daa_spec.createIntervalArray(min_speed, max_speed, speed_interval)
            
        custom_vector_array_enabled = parser['Settings']['custom_vector_array_enabled']
        custom_vector_array_enabled = custom_intruder_speed_enabled.lower()
        
        #Get default intruder speed array
        if custom_vector_array_enabled == 'true' or custom_vector_array_enabled == 't' or custom_vector_array_enabled == 'y' or custom_vector_array_enabled == 'yes':
            self.daa_spec.azimuth_vector_array = daa_spec.createCustArray(parser['DEFAULTS']['custom_vector_array'])
        else:
            #Set default intruder speed array
            min_speed =  Decimal(parser['DEFAULTS']['azimuth_vector_start'])
            max_speed = Decimal(parser['DEFAULTS']['azimuth_vector_end'])
            speed_interval = Decimal(parser['DEFAULTS']['azimuth_vector_array_interval'])
            self.daa_spec.azimuth_vector_array = daa_spec.createIntervalArray(min_speed, max_speed, speed_interval)
            
        self.daa_spec.max_bank = Decimal(parser['DEFAULTS']['max_bank_deg'])
        self.daa_spec.range = Decimal(parser['DEFAULTS']['range'])
        self.daa_spec.FOV = Decimal(parser['DEFAULTS']['FOV_deg'])
        self.daa_spec.ownsize = Decimal(parser['DEFAULTS']['rov_size'])
        self.daa_spec.ownspeed = Decimal(parser['DEFAULTS']['rov_speed'])
        self.daa_spec.max_roll_rate = Decimal(parser['DEFAULTS']['rov_max_roll_rate'])
        self.daa_spec.sigma_al = Decimal(parser['DEFAULTS']['sigma_al'])
        self.daa_spec.signma_cross = Decimal(parser['DEFAULTS']['signma_cross'])
        self.daa_spec.DMOD = Decimal(parser['DEFAULTS']['DMOD'])
        self.daa_spec.t_sim = Decimal(parser['DEFAULTS']['t_sim'])
        self.daa_spec.post_col = Decimal(parser['DEFAULTS']['post_col'])
        self.daa_spec.wind_speed = Decimal(parser['DEFAULTS']['wind_speed'])
        self.daa_spec.wind_dir = Decimal(parser['DEFAULTS']['wind_dir'])
        self.daa_spec.NDecimals = int(parser['DEFAULTS']['NDecimals'])
        self.daa_spec.sensor_rate = int(parser['DEFAULTS']['sensor_rate'])
        self.daa_spec.scans_track = int(parser['DEFAULTS']['scans_track'])
        self.daa_spec.t_warn = int(parser['DEFAULTS']['t_warn'])
        

Configuration().get_instance()
        
        
        

