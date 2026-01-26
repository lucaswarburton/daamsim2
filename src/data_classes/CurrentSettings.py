from daamsim.Config import Configuration
import json

class CurrentSettings:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            config = Configuration()

            self.custom_rpas_speed_enabled = config.custom_rpas_speed_enabled
            self.min_rpas_speed =  config.min_rpas_speed
            self.max_rpas_speed = config.max_rpas_speed
            self.rpas_speed_interval = config.rpas_speed_interval
            self.custom_rpas_speed_array = config.custom_rpas_speed_array
        
            self.custom_intruder_speed_enabled = config.custom_intruder_speed_enabled
            self.custom_intruder_speed_array = config.custom_intruder_speed_array
            self.min_intruder_speed =  config.min_intruder_speed
            self.max_intruder_speed = config.max_intruder_speed
            self.intruder_speed_interval = config.intruder_speed_interval
        
            self.custom_encounter_azimuth_array_enabled = config.custom_encounter_azimuth_array_enabled
            self.custom_encounter_azimuth_array = config.custom_encounter_azimuth_array
            self.encounter_azimuth_array_start =  config.encounter_azimuth_array_start
            self.encounter_azimuth_array_end = config.encounter_azimuth_array_end
            self.encounter_azimuth_array_interval = config.encounter_azimuth_array_interval
            
    def toJSON(self):
        return json.dumps(self.__dict__, indent= 4)
    

    def fromJSON(self, json_string) -> bool: 
        dictionary: dict = json.loads(json_string)
           
        for name in dictionary.keys():
            setattr(self, name, dictionary[name])
   
        return True
    