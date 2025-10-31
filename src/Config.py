import configparser
from pathlib import Path
from decimal import Decimal
from data_classes.daa_spec import daa_spec

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

        disable_ui = parser['Settings']['ui_disabled']
        disable_ui = disable_ui.lower()

        self.disable_ui = disable_ui == 'true' or   disable_ui == 't' or disable_ui == 'y' or disable_ui == 'yes'
        self.default_file_path = parser['Settings']['default_file_path']
        
        custom_intruder_speed_enabled = parser['Settings']['custom_intruder_speed_enabled']
        custom_intruder_speed_enabled = custom_intruder_speed_enabled.lower()
        
        #Get default intruder speed array
        if custom_intruder_speed_enabled == 'true' or custom_intruder_speed_enabled == 't' or custom_intruder_speed_enabled == 'y' or custom_intruder_speed_enabled == 'yes':
            intruder_speed_array = daa_spec.createCustArray(parser['DEFAULTS']['custom_intruder_speed_array'])
        else:
            #Set default intruder speed array
            min_speed =  Decimal(parser['DEFAULTS']['min_intruder_speed'])
            max_speed = Decimal(parser['DEFAULTS']['max_intruder_speed'])
            speed_interval = Decimal(parser['DEFAULTS']['intruder_speed_interval'])
            intruder_speed_array = daa_spec.createIntervalArray(min_speed, max_speed, speed_interval)
            
        custom_vector_array_enabled = parser['Settings']['custom_vector_array_enabled']
        custom_vector_array_enabled = custom_intruder_speed_enabled.lower()
        
        #Get default intruder speed array
        if custom_vector_array_enabled == 'true' or custom_vector_array_enabled == 't' or custom_vector_array_enabled == 'y' or custom_vector_array_enabled == 'yes':
            azimuth_vector_array = daa_spec.createCustArray(parser['DEFAULTS']['custom_vector_array'])
        else:
            #Set default intruder speed array
            min_speed =  Decimal(parser['DEFAULTS']['azimuth_vector_start'])
            max_speed = Decimal(parser['DEFAULTS']['azimuth_vector_end'])
            speed_interval = Decimal(parser['DEFAULTS']['azimuth_vector_array_interval'])
            azimuth_vector_array = daa_spec.createIntervalArray(min_speed, max_speed, speed_interval)
            
        max_bank = Decimal(parser['DEFAULTS']['max_bank_deg'])
        range = Decimal(parser['DEFAULTS']['range'])
        FOV = Decimal(parser['DEFAULTS']['FOV_deg'])
        ownsize = Decimal(parser['DEFAULTS']['rov_size'])
        ownspeed = Decimal(parser['DEFAULTS']['rov_speed'])
        max_roll_rate = Decimal(parser['DEFAULTS']['rov_max_roll_rate'])
        sigma_al = Decimal(parser['DEFAULTS']['sigma_al'])
        signma_cross = Decimal(parser['DEFAULTS']['signma_cross'])
        DMOD = Decimal(parser['DEFAULTS']['DMOD'])
        t_sim = Decimal(parser['DEFAULTS']['t_sim'])
        post_col = Decimal(parser['DEFAULTS']['post_col'])
        wind_speed = Decimal(parser['DEFAULTS']['wind_speed'])
        wind_dir = Decimal(parser['DEFAULTS']['wind_dir'])
        NDecimals = int(parser['DEFAULTS']['NDecimals'])
        sensor_rate = int(parser['DEFAULTS']['sensor_rate'])
        scans_track = int(parser['DEFAULTS']['scans_track'])
        t_warn = int(parser['DEFAULTS']['t_warn'])
        
        self.daa_spec = daa_spec(\
            max_bank=max_bank, \
            range=range,\
            FOV=FOV,\
            ownsize=ownsize,\
            ownspeed=ownspeed,\
            max_roll_rate=max_roll_rate, \
            azimuth_vector_array=azimuth_vector_array, \
            intruder_speed_array=intruder_speed_array, \
            sigma_al=sigma_al, \
            signma_cross= signma_cross, \
            DMOD=DMOD, \
            t_sim=t_sim, \
            post_col=post_col, \
            wind_speed=wind_speed, \
            wind_dir=wind_dir, \
            NDecimals=NDecimals, \
            sensor_rate=sensor_rate, \
            scans_track=scans_track, \
            t_warn=t_warn)
    
        

Configuration.get_instance()
        
        
        

