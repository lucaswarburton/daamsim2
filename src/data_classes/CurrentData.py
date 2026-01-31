import threading
import json
import numpy as np
import pickle


from .DaaSpec import DaaSpec
from .CurrentSettings import CurrentSettings
from daamsim.Config import Configuration

class CurrentData:
    _instance = None
    _lock = threading.Lock()
    _ENCODING = "latin-1"
    _JSONv = "DAAMSIMJSONv1.0"

    _dict_field_names = [
        "rr_val",
        "azimuth_vect",
        "r_min_m",
        "r_min_over",
        "ground_int_speed",
        "alpha_oncoming_vect",
        "alpha_overtake_vect",
        "clos_vel",
        "clos_vel_over",
    ]
    #0 for start up state
    #1 for rr_calcs ran
    _sim_state = 0

    def __new__(cls) -> None:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            for name in self._dict_field_names:
                setattr(self, name, np.array([]))
            self._initialized = True
            self._sim_state = 0
            self.specs = Configuration().daa_spec

    def clear(self) -> None:
        for name in self._dict_field_names:
            getattr(self, name).clear()
        self._sim_state = 0
        self.specs = None
    
    def to_json(self) -> str:
        dictionary = dict()
        dictionary['JSONIdentifier'] = CurrentData._JSONv
        dictionary['_initialized'] = self._initialized
        dictionary['_sim_state'] = self._sim_state
        dictionary['specs'] = self.specs.toJSON()
        dictionary['settings'] = CurrentSettings().toJSON()
        for name in self._dict_field_names:
            dictionary[name] = pickle.dumps(getattr(self, name)).decode(CurrentData._ENCODING)

        return json.dumps(dictionary, indent= 4)
    

    
    def from_json(self, json_string: str) -> bool: 
        dictionary: dict = json.loads(json_string)
        if not 'JSONIdentifier' in dictionary:
            return False
        elif dictionary['JSONIdentifier'] != CurrentData._JSONv:
            return False
        
        self._initialized = dictionary["_initialized"]
        self._sim_state = dictionary["_sim_state"]
        self.specs.fromJSON(dictionary["specs"])
        CurrentSettings().fromJSON(dictionary['settings'])
        
        dictionary.pop('JSONIdentifier')
        dictionary.pop("_initialized")
        dictionary.pop("_sim_state")
        dictionary.pop("specs")
        dictionary.pop("settings")
        
        for name in dictionary.keys():
            setattr(self, name, pickle.loads(dictionary[name].encode(CurrentData._ENCODING)))
   
        return True
        
