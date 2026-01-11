from dataclasses import dataclass
import numpy as np
import json

@dataclass
class DaaSpec:
    #Read RPAS Characteristics
    rpas_max_bank_deg: float
    rpas_wingspan: float
    rpas_max_roll_rate: float

    rpas_speed_array: np.array

    #Intruder Characteristics
    intruder_speed_array: np.array

    #DAA Characteristics
    daa_declaration_range: float
    daa_fov_deg: float
    rate_of_revisit: float
    scans_track: int

    #Simulation Variables
    NDecimals: int
    time_resol: float
    conflict_volume: float
    t_sim: float
    post_col: float
    wind_speed: float
    wind_dir: float
    human_factor_delay: float
    encounter_azimuth_array: np.array
    
    # def toJSON(self):
    #     dictionary = dict()
    #     for attr in dir(self):
    #         if not callable(getattr(self, attr)) and not attr.startswith("__"):
    #             if isinstance(getattr(self, attr), np.ndarray):
    #                 dictionary[attr] = getattr(self, attr).tolist()
    #             else:
    #                 dictionary[attr] = getattr(self, attr)
        
    #     return json.dumps(dictionary, indent=4)
        
    # def fromJSON(self, json_string):
    #     dictionary: dict = json.loads(json_string)
    #     for name in dictionary.keys():
    #         curratt = dictionary[name]
    #         if isinstance(curratt, list):
    #             setattr(self, name, np.array(curratt))
    #         elif isinstance(curratt, dict) or isinstance(curratt, DaaSpec):
    #             setattr(self, name, curratt)
    #         else:
    #             raise ValueError
            
            
        
    #     return json.dumps(dictionary, indent=4)
        
        
        

